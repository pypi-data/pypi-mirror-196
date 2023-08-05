import asyncio
import logging
import secrets
import falcon

from time import time
from falcon import media

try:
    from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
except ImportError:
    from wsproto.utilities import ProtocolError

    ConnectionClosedError = ConnectionClosedOK = ProtocolError

import falcon.asgi

from .rate_limiter import get_rate_limiter
from . import __version__
from .config import Config
from .util import timeout, json_dumps, json_loads, event_as_json, JSONDecodeError
from .errors import AuthenticationError, StorageError


class Client:
    __slots__ = (
        "ws",
        "remote_addr",
        "log",
        "id",
        "subscription_queue",
        "send_task",
        "rate_limiter",
        "timeout",
        "auth_token",
        "sent",
        "start_time",
    )

    def __init__(self, ws, req, rate_limiter=None, log=None, timeout=1800):
        self.ws = ws
        self.remote_addr = req.remote_addr if req else "%s:%s" % ws.remote_address
        origin = req.get_header("origin") if req else ws.origin
        self.id = f"{self.remote_addr}-{secrets.token_hex(2)}"
        self.log = log
        self.log.info(f"Accepted {self.id} from Origin: {origin}")
        self.subscription_queue = asyncio.Queue()
        self.send_task = None
        self.sent = 0
        self.rate_limiter = rate_limiter
        self.timeout = timeout
        self.auth_token = {}
        self.start_time = time()

    def validate_message(self, message):
        if not isinstance(message, list):
            return False
        if len(message) < 2:
            return False
        if message[0] not in ("EVENT", "REQ", "CLOSE", "AUTH"):
            return False
        return True

    async def send_subscriptions(self, ws_send):
        get_from_storage = self.subscription_queue.get
        self.log.debug("%s waiting for subs", self.id)
        while True:
            try:
                sub_id, event = await get_from_storage()
                if event is not None:
                    # message = json_dumps(["EVENT", sub_id, event.to_json_object()])
                    message = event_as_json(sub_id, event)
                else:
                    # done with stored events
                    message = f'["EOSE","{sub_id}"]'

                await ws_send(message)
                # self.log.debug("SENT: %s", message)
                self.sent += len(message)
            except (
                falcon.WebSocketDisconnected,
                ConnectionClosedError,
                ConnectionClosedOK,
                asyncio.CancelledError,
            ):
                break
            except Exception:
                self.log.exception("subs")

    async def start(self, storage, ws_send, ws_recv):
        ws = self.ws
        client_id = self.id
        remote_addr = self.remote_addr

        if storage.authenticator.is_enabled:
            challenge = storage.authenticator.get_challenge(remote_addr)
            self.log.debug("Sent challenge %s to %s", challenge, client_id)
            await ws_send(json_dumps(["AUTH", challenge]))
            throttle = await storage.authenticator.should_throttle(self.auth_token)
        else:
            throttle = 0

        while True:
            try:
                async with timeout(self.timeout):
                    message = json_loads(await ws_recv())

                if not self.validate_message(message):
                    if throttle:
                        await asyncio.sleep(throttle)
                    continue

                self.log.debug("RECEIVED: %s", message)
                command = message[0]

                if self.rate_limiter and self.rate_limiter.is_limited(
                    remote_addr, message
                ):
                    if command == "EVENT":
                        response = [
                            "OK",
                            message[1]["id"],
                            False,
                            "rate-limited: slow down",
                        ]
                    else:
                        response = ["NOTICE", "rate-limited"]
                    await ws_send(json_dumps(response))
                    continue

                if command == "REQ":
                    sub_id = str(message[1])
                    await storage.subscribe(
                        client_id,
                        sub_id,
                        message[2:],
                        self.subscription_queue,
                        auth_token=self.auth_token,
                    )
                    if throttle:
                        await asyncio.sleep(throttle)
                    if self.send_task is None:
                        self.send_task = asyncio.create_task(
                            self.send_subscriptions(ws_send)
                        )
                elif command == "CLOSE":
                    sub_id = str(message[1])
                    await storage.unsubscribe(client_id, sub_id)
                elif command == "EVENT":
                    try:
                        event, result = await storage.add_event(
                            message[1], auth_token=self.auth_token
                        )
                    except (StorageError, AuthenticationError) as e:
                        throttle = max(throttle, 1) * 2
                        self.log.error("Auth error %s. Throttling %s", str(e), throttle)
                        result = False
                        reason = str(e)
                        eventid = ""
                    except Exception as e:
                        self.log.error(str(e))
                        result = False
                        reason = str(e)
                        eventid = ""
                    else:
                        eventid = event.id
                        reason = "" if result else "duplicate: exists"
                        self.log.info(
                            "%s added %s from %s", client_id, event.id, event.pubkey
                        )
                    finally:
                        if throttle:
                            await asyncio.sleep(throttle)
                        await ws_send(json_dumps(["OK", eventid, result, reason]))
                elif command == "AUTH" and storage.authenticator.is_enabled:
                    self.auth_token = await storage.authenticator.authenticate(
                        message[1], challenge=challenge
                    )
                    throttle = await storage.authenticator.should_throttle(
                        self.auth_token
                    )

            except StorageError as e:
                self.log.warning("storage error: %s for %s", e, client_id)
                await ws_send(json_dumps(["NOTICE", str(e)]))
            except AuthenticationError as e:
                self.log.warning("Auth error. %s token:%s", str(e), self.auth_token)
                await ws_send(json_dumps(["NOTICE", str(e)]))
            except (
                falcon.WebSocketDisconnected,
                ConnectionClosedError,
                ConnectionClosedOK,
            ):
                break
            except JSONDecodeError:
                self.log.debug("json decoding")
                continue
            except asyncio.TimeoutError:
                self.log.info("%s timed out", client_id)
                await ws.close(code=1013)
                break
            except Exception:
                self.log.exception("client loop")
                await ws.close(code=1013)
                break
        await storage.unsubscribe(self.id)

    async def stop(self):
        if self.send_task:
            self.send_task.cancel()
            try:
                await self.send_task
            except asyncio.CancelledError:
                pass
        self.rate_limiter.cleanup()
        duration = time() - self.start_time
        self.log.info(
            "Done %s. Sent: %d Bytes. Duration: %d Seconds",
            self,
            self.sent,
            duration,
        )

    def __str__(self):
        return f"{self.auth_token.get('pubkey', 'anon')}@{self.id}"


class BaseResource:
    def __init__(self, storage):
        self.storage = storage
        self.log = logging.getLogger(__name__)


class NostrAPI(BaseResource):
    """
    Handles nostr websocket interface
    """

    def __init__(self, storage, rate_limiter=None):
        super().__init__(storage)
        self.rate_limiter = rate_limiter

    async def on_get(self, req: falcon.Request, resp: falcon.Response):
        if req.accept == "application/nostr+json":
            supported_nips = [1, 2, 5, 9, 11, 12, 15, 20, 26, 33, 40]
            if Config.authentication.get("enabled"):
                supported_nips.append(42)
            if Config.fts_enabled:
                supported_nips.append(50)
            metadata = {
                "name": Config.relay_name,
                "description": Config.relay_description,
                "pubkey": Config.sysop_pubkey,
                "contact": Config.sysop_contact,
                "supported_nips": supported_nips,
                "software": "https://code.pobblelabs.org/fossil/nostr_relay",
                "version": __version__,
            }
            resp.media = metadata
        elif Config.redirect_homepage:
            raise falcon.HTTPFound(Config.redirect_homepage)
        else:
            resp.text = "try using a nostr client :-)"
        resp.append_header("Access-Control-Allow-Origin", "*")
        resp.append_header("Access-Control-Allow-Headers", "*")
        resp.append_header("Access-Control-Allow-Methods", "*")

    async def on_websocket(self, req: falcon.Request, ws: falcon.asgi.WebSocket):
        if Config.origin_blacklist:
            origin = str(req.get_header("origin")).lower()
            if origin in Config.origin_blacklist:
                self.log.warning("Blocked origin %s from connecting", origin)
                await ws.close(code=1008)
                return

        try:
            if self.rate_limiter and self.rate_limiter.is_limited(
                req.remote_addr, ["ACCEPT"]
            ):
                await ws.close(code=1013)
                self.log.warning("rate-limited ACCEPT %s", req.remote_addr)
                return
            await ws.accept()

        except falcon.WebSocketDisconnected:
            return

        client = Client(
            ws,
            req,
            rate_limiter=self.rate_limiter,
            log=self.log,
            timeout=Config.get("message_timeout", 1800),
        )

        try:
            # from .util import easy_profiler

            # with easy_profiler():
            await client.start(self.storage, ws.send_text, ws.receive_text)
        except (
            falcon.WebSocketDisconnected,
            ConnectionClosedError,
            ConnectionClosedOK,
        ):
            pass
        finally:
            await client.stop()


class NostrStats(BaseResource):
    async def on_get(self, req: falcon.Request, resp: falcon.Response):
        try:
            resp.media = await self.storage.get_stats()
        except:
            self.log.exception("stats")


class ViewEventResource(BaseResource):
    async def on_get(self, req: falcon.Request, resp: falcon.Response, event_id: str):
        try:
            event = await self.storage.get_event(event_id)
        except ValueError:
            raise falcon.HTTPNotFound
        except Exception:
            self.log.exception("get-event")
        if event:
            resp.media = event.to_json_object()
        else:
            raise falcon.HTTPNotFound


class NostrIDP(BaseResource):
    """
    Serve /.well-known/nostr.json
    """

    async def on_get(self, req: falcon.Request, resp: falcon.Response):
        name = req.params.get("name", "")
        domain = req.host
        if name:
            identifier = f"{name}@{domain}"
        else:
            identifier = ""
        try:
            resp.media = await self.storage.get_identified_pubkey(
                identifier, domain=domain
            )
        except Exception:
            self.log.exception("idp")
        # needed for web clients
        resp.append_header("Access-Control-Allow-Origin", "*")
        resp.append_header("Access-Control-Allow-Headers", "*")
        resp.append_header("Access-Control-Allow-Methods", "*")


class SetupMiddleware:
    def __init__(self, storage):
        self.storage = storage

    async def process_request(self, req, resp):
        if req.root_path:
            req.path = req.path.replace(req.root_path, "/", 1)

    async def process_request_ws(self, req, resp):
        if req.root_path:
            req.path = req.path.replace(req.root_path, "/", 1)

    async def process_startup(self, scope, event):
        if Config.DEBUG:
            asyncio.get_running_loop().set_debug(True)
        if Config.should_run_notifier:
            from .notifier import NotifyServer

            self.notify_server = NotifyServer()
            self.notify_server.start()
        await self.storage.setup()
        from .util import Periodic

        await Periodic.start_pending()

    async def process_shutdown(self, scope, event):
        await self.storage.optimize()
        await self.storage.close()


def create_app(conf_file=None, storage=None):
    import os
    import os.path
    import logging, logging.config

    Config.load(conf_file)
    if Config.DEBUG:
        print(Config)

    if Config.logging:
        logging.config.dictConfig(Config.logging)
    else:
        logging.basicConfig(
            format="%(asctime)s %(name)s %(levelname)s %(message)s",
            level=logging.DEBUG if Config.DEBUG else logging.INFO,
        )

    from .storage import get_storage

    store = storage or get_storage()

    rate_limiter = get_rate_limiter(Config)

    json_handler = media.JSONHandlerWS(
        dumps=json_dumps,
        loads=json_loads,
    )

    logging.info("Starting version %s", __version__)
    api = NostrAPI(store, rate_limiter=rate_limiter)
    app = falcon.asgi.App(middleware=SetupMiddleware(store))
    app.add_route("/", api)
    app.add_route("/stats/", NostrStats(store))
    app.add_route("/e/{event_id}", ViewEventResource(store))
    app.add_route("/.well-known/nostr.json", NostrIDP(store))
    app.ws_options.media_handlers[falcon.WebSocketPayloadType.TEXT] = json_handler

    return app


def run_with_gunicorn(conf_file=None):
    """
    Run the app using gunicorn's ASGIApplication
    """
    app = create_app(conf_file)
    from gunicorn.app.base import Application

    class ASGIApplication(Application):
        def load_config(self):
            import sys

            if sys.implementation.name == "pypy":
                from uvicorn.workers import UvicornH11Worker

                # UvicornH11Worker.CONFIG_KWARGS["ws"] = "wsproto"
                worker_class = "uvicorn.workers.UvicornH11Worker"
            else:
                worker_class = "uvicorn.workers.UvicornWorker"
            self.cfg.set("worker_class", worker_class)
            for k, v in Config.gunicorn.items():
                self.cfg.set(k.lower(), v)

        def load(self):
            # this should fix a memory leak in websocket compression
            from nostr_relay import monkeypatch

            monkeypatch.monkey()
            # this ensures that the unnecessary MessageLoggerMiddleware isn't added
            from uvicorn.config import logger

            logger.setLevel(logging.WARNING)
            return app

    ASGIApplication().run()


def run_with_uvicorn(conf_file=None, in_thread=False):
    """
    Run the app using uvicorn.
    Optionally, start the server in a daemon thread
    """
    import sys

    from nostr_relay import monkeypatch

    monkeypatch.monkey()
    from uvicorn.config import logger

    logger.setLevel(logging.WARNING)

    import uvicorn

    app = create_app(conf_file)

    options = dict(Config.gunicorn)
    if "bind" in options:
        bind = options.pop("bind")
        options["port"] = int(bind.rsplit(":", 1)[1])
    if "loglevel" in options:
        options["log_level"] = options.pop("loglevel")

    if sys.implementation.name == "pypy":
        options.update({"loop": "asyncio", "http": "h11"})

    uv_config = uvicorn.Config(app, **options)
    server = uvicorn.Server(uv_config)

    if in_thread:
        import threading

        thr = threading.Thread(target=server.run, daemon=True)
        thr.start()
    else:
        server.run()
