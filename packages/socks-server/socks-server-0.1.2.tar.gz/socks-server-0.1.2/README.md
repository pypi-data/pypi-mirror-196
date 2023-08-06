# socks

Socks (**sock**et **s**erver) is a simple server framework, built only using the standard python library. Its syntax is strongly inspired by the microframework [flask](https://palletsprojects.com/p/flask/).

## Basic usage

```py
from socks import Socks, Response

app = Socks()

@app.route(path:str, methods:list[str]=["GET"])
def function(req):
    return Response(f"<h1>{req.method}</h1>", contentType="text/html")
```

For other things, look at the testserver.py file.