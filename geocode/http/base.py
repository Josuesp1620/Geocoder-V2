import logging
import logging.handlers
from pathlib import Path
import time

from flask import request, Response, jsonify
from werkzeug.exceptions import InternalServerError

from geocode.config import config
from geocode.core.core import reverse, search
from geocode.core.db import DB
from geocode.helpers.text import EntityTooLarge

notfound_logger = None
query_logger = None
slow_query_logger = None


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    filename = Path(config.LOG_DIR).joinpath("{}.log".format(name))
    try:
        handler = logging.handlers.TimedRotatingFileHandler(
            str(filename), when="midnight"
        )
    except FileNotFoundError:
        print("Unable to write to {}".format(filename))
    else:
        logger.addHandler(handler)
    return logger


@config.on_load
def on_load():
    if config.LOG_NOT_FOUND:
        global notfound_logger
        notfound_logger = get_logger("notfound")

    if config.LOG_QUERIES:
        global query_logger
        query_logger = get_logger("queries")

    if config.SLOW_QUERIES:
        global slow_query_logger
        slow_query_logger = get_logger("slow_queries")


def log_notfound(query):
    if config.LOG_NOT_FOUND:
        notfound_logger.debug(query)


def log_query(query, results):
    if config.LOG_QUERIES:
        if results:
            result = str(results[0])
            score = str(round(results[0].score, 2))
        else:
            result = "-"
            score = "-"
        query_logger.debug("\t".join([query, result, score]))


def log_slow_query(query, results, timer):
    if config.SLOW_QUERIES:
        if results:
            result = str(results[0])
            score = str(round(results[0].score, 2))
            id_ = results[0].id
        else:
            result = "-"
            score = "-"
            id_ = "-"
        slow_query_logger.debug("\t".join([str(timer), query, id_, result, score]))


class CorsMiddleware:
    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Headers", "X-Requested-With")


class View:

    config = config

    def match_filters(self, req):
        filters = {}
        if 'filters' in req.json:
            for name in config.FILTERS:
                if name in req.json['filters']:
                    filters[name] = str(req.json['filters'][name])
        return filters

    def render(
        self, req, resp, results, query=None, filters=None, center=None, limit=None
    ):
        results = {
            "type": "FeatureCollection",
            "version": "draft",
            "features": [r.format() for r in results],
            "attribution": config.ATTRIBUTION
        }
        if query:
            results["query"] = query
        if filters:
            results["filters"] = filters
        if center:
            results["center"] = center
        if limit:
            results["limit"] = limit
        return self.json(results)

    to_geojson = render  # retrocompat.

    def json(self, content):
        return jsonify(content), 200

    def parse_float(sel, req, *keys):
        try:
            for key in keys:
                val = req.json[key]
                if val is not None:
                    return float(val)
        except (ValueError, TypeError) as e:
            raise InternalServerError(f"invalid value: {key}") from e
        return None

    def parse_lon_lat(self, req):
        lat = self.parse_float(req, "lat", "latitude")
        lon = self.parse_float(req, "lon", "lng", "long", "longitude")

        if lon and (lon > 180 or lon < -180):
            raise InternalServerError("out of range lon")
        
        elif lat and (lat > 90 or lat < -90):
            raise InternalServerError("out of range lat")
        return lon, lat
    
class Search(View):
    def on_post(self, req, resp):

        body_params = req.json.keys()
        query = req.json['query']
        limit = req.json['limit'] if 'limit' in body_params else 5
        autocomplete = req.json['autocomplete'] if 'autocomplete' in body_params else False
        lon = None
        lat = None
        if "lat" in body_params and "lon" in body_params:
            lon, lat = self.parse_lon_lat(req)

        center = None
        if lon and lat:
            center = (lon, lat)
        filters = self.match_filters(req)
        timer = time.perf_counter()
        try:
            results = search(
                query,
                limit=limit,
                autocomplete=autocomplete,
                lat=lat,
                lon=lon,
                **filters
            )
        except EntityTooLarge as e:
            raise InternalServerError(e)
        timer = int((time.perf_counter() - timer) * 1000)
        if not results:
            log_notfound(query)
        log_query(query, results)
        if config.SLOW_QUERIES and timer > config.SLOW_QUERIES:
            log_slow_query(query, results, timer)
        return self.render(
            req, resp, results, query=query, filters=filters, center=center, limit=limit
        )


class Reverse(View):
    def on_post(self, req, resp, **kwargs):
        body_params = req.json.keys()
        lon, lat = self.parse_lon_lat(req)
        if lon is None:
             raise InternalServerError("lon")
        if lat is None:
             raise InternalServerError("lat")
        limit = req.json['limit'] if 'limit' in body_params else 1
        filters = self.match_filters(req)
        results = reverse(lat=lat, lon=lon, limit=limit, **filters)
        return self.render(req, resp, results, filters=filters, limit=limit)


class Health(View):
    def on_get(self, req, resp):
        return self.json(
            req,
            resp,
            {"status": "HEALTHY", "redis_version": DB.info().get("redis_version")},
        )

def register_http_endpoint(api):
    @api.route('/')
    def index():
        return 'Hello, World!'
    @api.route('/search', methods=["POST"])
    def search():
        return Search().on_post(request, Response)
    @api.route('/reverse', methods=["POST"])
    def reverse():
        return Reverse().on_post(request, Response)


def register_command(subparsers):
    parser = subparsers.add_parser("serve", help="Run debug server")
    parser.set_defaults(func=run)
    parser.add_argument(
        "--host", default="127.0.0.1", help="Host to expose the demo serve on"
    )
    parser.add_argument(
        "--port", default="7878", help="Port to expose the demo server on"
    )


def run(args):
    # Do not import at load time for preventing config import loop.
    from .wsgi import simple

    simple(args)
