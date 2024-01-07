from flask import Flask
from flask_cors import CORS

from geocode.config import config, hooks

from .base import CorsMiddleware

config.load()
application = Flask(__name__)
middlewares = [CorsMiddleware()]
hooks.register_http_middleware(middlewares)
CORS(application)
hooks.register_http_endpoint(application)

# def simple(args):
#     app.run(host="0.0.0.0", port=7878)

def simple(args):
    from wsgiref.simple_server import make_server

    httpd = make_server(args.host, int(args.port), application)
    print("Serving HTTP on {}:{}…".format(args.host, args.port))
    try:
        httpd.serve_forever()
    except (KeyboardInterrupt, EOFError):
        print("Bye!")