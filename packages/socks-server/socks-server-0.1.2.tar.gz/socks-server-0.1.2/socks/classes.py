# Standart python modules
import os
import sys
import json
import socket
import fnmatch
import threading
import traceback

# Import stuff from the module
from .utils import *
from .constants import *
from .exeptions import *
from .generate_colored import *

# Import version from __init__.py
from . import __version__


class Request:
    def __init__(self, req, origin, ignore_body=False) -> None:
        self.req = req
        self.params = {}
        self.headers = {}
        self.body = ""
        self.origin = origin
        self.isBody = False

        # Parse HTTP request
        for i, l in enumerate(req.split("\r\n")):
            if i == 0:
                self.method, self.path, self.protocol = l.split(" ")
                self.path = self.path.split("?")[0]
                self.params = {}
                if len(l.split("?")) > 1:
                    self.params = parseKeyValue(l.split("?")[1].split(" ")[0])
            else:
                if l == "":
                    self.isBody = True
                else:
                    if not self.isBody:
                        self.headers[l.split(": ")[0]] = l.split(": ")[1]
                    else:
                        self.body += l + "\n"
        del self.isBody

        # Parse Body
        if "Content-Type" in self.headers and not ignore_body:
            try:
                if self.headers["Content-Type"] == "application/x-www-form-urlencoded":
                    self.form = parseKeyValue(self.body)
                elif self.headers["Content-Type"] == "application/json":
                    self.json = json.loads(self.body)
            except Exception as e:
                raise MalformedBodyException(
                    "Malformed body in request: " + str(e) + "\n\n" + self.body
                )

    # Throw exception if key is requested but not found
    def __getattribute__(self, __name: str):
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            raise NoSuchContentInRequestException(
                "Key not found in request: "
                + __name
                + "\nEither you requested a key that is not in this request (e.g. "
                + (
                    "form"
                    if self.headers["Content-Type"]
                    == "application/x-www-form-urlencoded"
                    else "json"
                )
                + ") or the key is not defined in general."
            )

    def __str__(self) -> str:
        return self.req

    def __repr__(self) -> str:
        return self.req


class Route:
    # A class for simple internal route handling
    def __init__(self, func, path: str = None, methods: list = ["GET"]):
        self.func = func
        self.path = path
        self.methods = methods

    def __str__(self) -> str:
        return f"<Route path={self.path} methods={self.methods} function={self.func.__name__}>"

    def __repr__(self) -> str:
        return self.__str__()


class Socks:
    def __init__(self, name: str = "generic", prefix: str = "/") -> None:
        """Initialize the socks server

        Args:
            name (str, optional):   A project name. Unused now, may be
                                    used in a later version.
                                    Defaults to "generic".
            prefix (str, optional): The url prefix. Defaults to "/".
        """
        self.name = name
        self.subapps = []
        self.routes = []
        self.calculatedRoutes = []
        self.errorHandlers = {}
        self.prefix = prefix

        self.appPath = getAppRunDir()

        self.register_subapp = self.registerSubapp
        self.calculate_routes = self.calculateRoutes
        self.error_handler = self.errorHandler
        self.get_error_page = self.getErrorPage

    def __str__(self) -> str:
        return f"<Socks version={__version__} name={self.name}>"

    def calculateRoutes(self):
        """Calculate the routes of the server"""
        for s in self.subapps:
            s.calculateRoutes()
            for r in s.calculatedRoutes:
                self.calculatedRoutes.append(
                    Route(r.func, self.prefix + r.path, r.methods)
                )

        for r in self.routes:
            self.calculatedRoutes.append(Route(r.func, self.prefix + r.path, r.methods))

        # Only forwards slash
        self.calculatedRoutes = [
            Route(r.func, r.path.replace("\\", "/"), r.methods)
            for r in self.calculatedRoutes
        ]

        # Clean up double slashes
        self.calculatedRoutes = [
            Route(r.func, r.path.replace("//", "/"), r.methods)
            for r in self.calculatedRoutes
        ]

    def run(
        self,
        port: int = 8080,
        host: str = "127.0.0.1",
        debug: bool = False,
        reload: bool = False,
        allowCustomHeaders: bool = False,
    ):
        """Run the server

        Args:
            port (int, optional):       The server port. Defaults to 8080.
            host (str, optional):       The server hostname/ip address. Defaults
                                        to "127.0.0.1".
            debug (bool, optional):     If enabled, you'll see an error report
                                        when accessing a route that produces an
                                        excenption. Defaults to False.
            reload (bool, optional):    If enabled, server will restart when
                                        files are changed. Defaults to False.
            allowCustomHeaders (bool, optional): If enabled, you can set custom
                                        headers in the request. Defaults to False.
        """
        self.calculateRoutes()
        self.allowCustomHeaders = allowCustomHeaders

        s = Server(self.calculatedRoutes, host, port, debug, reload, self)
        s.run()

    def route(self, path: str = None, methods: list = ["GET"]):
        """Add a route to the server

        Args:
            path (str, optional):       The path to be accessed. Defaults to None.
            methods (list, optional):   The methods to be accessed. Defaults to
                                        ["GET"].
        """

        def wrapper(func):
            self.routes.append(Route(func, path, methods))
            return func

        return wrapper

    def registerSubapp(self, subapp: "Socks"):
        """Register a subapp to the server

        Args:
            subapp (Socks): The subapp to be registered.
        """
        self.subapps.append(subapp)

    def errorHandler(self, code: int):
        """Set an error handler for a specific error code

        Args:
            code (int): The error code.
        """

        def wrapper(func):
            self.errorHandlers[code] = {
                "func": func,
                "code": code,
                "message": ERROR_CODES[str(code)],
                "description": ERROR_CODE_DESCRIPTIONS[str(code)],
            }
            return func

        return wrapper

    def getErrorPage(self, code: int):
        """Get the error page for a specific error code

        Args:
            code (int): The error code.
        """
        if code in self.errorHandlers:
            page = self.errorHandlers[code]["func"](
                {
                    "code": code,
                    "message": self.errorHandlers[str(code)]["message"],
                    "description": self.errorHandlers[str(code)]["description"],
                }
            )
        else:
            msg = str(code) + " " + ERROR_CODES[str(code)]
            page = (
                "<h1>"
                + msg
                + "</h1>"
                + "<p>"
                + ERROR_CODE_DESCRIPTIONS[str(code)]
                + "</p><title>"
                + msg
                + "</title>"
            )
        return Response(page, status=code, contentType="text/html")


class Server:
    def __init__(self, routes, host, port, debug, reload, instance):
        self.routes = routes

        # Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Save settings
        self.instance = instance
        self.host = host
        self.port = port
        self.debug = debug
        self.reload = reload

        # Start server
        try:
            self.sock.bind((host, port))
        except OSError:
            print(red("Cannot bind address {}:{}!".format(host, port)))
            exit(1)
        self.sock.listen(1)
        self.enabled = True

    def fileWatcheThread(self):
        fileWatcherMsg = True
        for a in sys.argv:
            if a == "is-restarted":
                fileWatcherMsg = False

        if fileWatcherMsg:
            print(
                gray(
                    "Starting file watcher\nWatching directory {} \n".format(
                        self.instance.appPath
                    )
                )
            )
            sys.argv.append("is-restarted")

        oldState = []
        firstRun = True
        while True:
            newState = []
            # Add all files that end with .py to the list using os.walk,
            # and check if oldState is equal to newState
            for root, _, files in os.walk(self.instance.appPath):
                for f in files:
                    if f.endswith(".py") or f.endswith(".html"):
                        newState.append(
                            {
                                os.path.join(root, f): os.stat(
                                    os.path.join(root, f)
                                ).st_mtime
                            }
                        )
            if oldState != newState:
                oldState = newState
                if not firstRun:
                    print("Reloading server...")

                    # Shutdown and unbind server
                    self.enabled = False
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()

                    # Replace current process
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                firstRun = False

    def run(self):
        # Display done if restarted
        if "is-restarted" in sys.argv:
            print(green("Done.\n"))

        # Start reloading
        if self.reload:
            t = threading.Thread(target=self.fileWatcheThread)
            t.daemon = True
            t.start()

        # Display ip address
        if self.host in ["", "0.0.0.0"]:
            print(f"[*] Running on http://{getLocalIp()}:{self.port}")
        else:
            print(f"[*] Running on http://{self.host}:{self.port}")

        # Main Loop
        while True:
            if not self.enabled:
                break
            try:
                conn, addr = self.sock.accept()
            except KeyboardInterrupt:
                print("\n\nRecieved keyboard interrupt, exiting...")
                sys.exit()

            # data = conn.recv(1024)
            headers = ""
            while not headers.endswith("\r\n\r"):
                headers += conn.recv(1).decode("utf-8")

            r = Request(headers + "\n", "", ignore_body=True)
            length = r.headers.get("Content-Length")

            if not length:
                length = 1023
            else:
                length = int(length)

            data = headers.encode("utf-8") + conn.recv(length + 1)

            if self.debug:
                print("\n\n\n")
                print("Connection from ", addr)
                print(data.decode("utf-8"))
            res = None
            try:
                req = Request(data.decode("utf-8"), addr)
            except Exception as e:
                if self.debug:
                    print(e)
                res = ErrorResponse(500)
            try:
                found = False
                foundButWrongMethod = False
                for r in self.routes:
                    if r.path in [req.path, req.path + "/"]:
                        if req.method in r.methods:
                            found = True
                            if not res:
                                res = r.func(req)
                            if not type(res) == Response:
                                if type(res) == ErrorResponse:
                                    res = self.instance.getErrorPage(res.code)
                                else:
                                    res = Response(res)
                            conn.send(str(res).encode("utf-8"))
                            break
                        else:
                            foundButWrongMethod = True
                if foundButWrongMethod:
                    found = True
                    res = self.instance.getErrorPage(405)
                    conn.send(str(res).encode("utf-8"))
                if not found:
                    conn.send(str(self.instance.getErrorPage(404)).encode("utf-8"))
            except Exception as e:
                if self.debug:
                    # print and send traceback
                    print(traceback.format_exc())
                    # Send traceback to client
                    conn.send(
                        b"HTTP/1.1 500 Internal Server Error\n\n"
                        + b"<h1>500 Internal Server Error</h1><br>"
                        + traceback.format_exc()
                        .replace("    ", ">> ")
                        .replace("\n", "<br>")
                        .encode("utf-8")
                    )

                else:
                    conn.send(str(self.instance.getErrorPage(500)).encode("utf-8"))
            conn.close()


class ErrorResponse:
    def __init__(self, code) -> None:
        self.code = code


class Response:
    def __init__(
        self, body, contentType: str = "", status: int = 200, headers: dict = {}
    ) -> None:
        self.topLine = "HTTP/1.1 " + str(status) + " " + ERROR_CODES.get(str(status))
        self.headers = headers
        self.headers["Content-Type"] = contentType
        self.headers["Server"] = "Socks/" + __version__
        self.body = body
        self.usesOfficialHeaders = True

        # Check if the headers are valid
        for ct in contentType.replace(" ", "").split(","):
            if not ct in VALID_HEADERS:
                self.usesOfficialHeaders = False

        # If ContentType is "", and the body is a dict,
        # set the ContentType to application/json
        if contentType == "" and type(self.body) == dict:
            self.headers["Content-Type"] = "application/json"
            self.body = json.dumps(self.body)

        # Format dicts as correct body for some content types
        if contentType == "application/json":
            self.body = json.dumps(self.body)
        elif contentType == "application/xxx-www-form-urlencoded":
            tmp = []
            for key, val in self.body.items():
                tmp.append(urllib.parse.quote(key) + "=" + urllib.parse.quote(val))
            self.body = "&".join(tmp)

        # If ContentType is "", set it to text/plain
        if not self.headers["Content-Type"]:
            self.headers["Content-Type"] = "text/plain"

        # Make sure body is string
        self.body = str(self.body)

        self.headers["Content-Length"] = str(len(self.body))

    def __str__(self) -> str:
        return (
            self.topLine
            + "\n"
            + ("\n".join([k + ": " + v for k, v in self.headers.items()]))
            + "\n\n"
            + self.body
        )

    def __repr__(self) -> str:
        return self.__str__()
