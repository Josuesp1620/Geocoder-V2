from flask import Flask
from flask_cors import CORS

from geocode.config import config, hooks

from .base import CorsMiddleware

config.load()
app = Flask(__name__)
middlewares = [CorsMiddleware()]
hooks.register_http_middleware(middlewares)
CORS(app)
hooks.register_http_endpoint(app)

def simple(args):
    app.run(host="0.0.0.0", port=7878)
