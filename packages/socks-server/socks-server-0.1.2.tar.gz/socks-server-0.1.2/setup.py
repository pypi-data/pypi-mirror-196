# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['socks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'socks-server',
    'version': '0.1.2',
    'description': 'Socks is a simple server framework, built only using the standard python library.',
    'long_description': '# socks\n\nSocks (**sock**et **s**erver) is a simple server framework, built only using the standard python library. Its syntax is strongly inspired by the microframework [flask](https://palletsprojects.com/p/flask/).\n\n## Basic usage\n\n```py\nfrom socks import Socks, Response\n\napp = Socks()\n\n@app.route(path:str, methods:list[str]=["GET"])\ndef function(req):\n    return Response(f"<h1>{req.method}</h1>", contentType="text/html")\n```\n\nFor other things, look at the testserver.py file.',
    'author': 'PaddeCraft',
    'author_email': '70023807+PaddeCraft@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PaddeCraft/socks',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
