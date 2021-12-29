import logging
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort
from flask_caching import Cache
from cdisc import Cdiscount_requests

logging.basicConfig(level=logging.INFO)

config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}

response = Cdiscount_requests()
app = Flask(__name__)
app.config.from_mapping(config)

cache = Cache(app)
api = Api(app)


class Cdis_parse(Resource):
    def url_proxy(self):
        if request.get_json():
            logging.info(f" JSON {request.json}")
            url = request.json.get("url")
            proxy = request.json.get("proxy")
            if not url:
                abort(400, error="URL not found in JSON")
            return url, proxy
        args = request.args
        if args.get("url"):
            url = args.get("url")
        else:
            abort(400, error="URL not found in args")
        if args.get("proxy"):
            proxy = args.get("proxy")
        else:
            proxy = None
        return url, proxy

    def get(self):
        url, proxy = self.url_proxy()
        logging.info(f"Proxy {proxy} ")
        logging.info(f"URL = {url}")
        r = response.parse(url, proxy)
        if isinstance(r, dict):
            if r.get("error"):
                return jsonify(error=str(r.get("error")))
        return jsonify(jsons=r["jsons"], html=r["html"])  # jsonify(html=str(html))#

    def post(self):
        url, proxy = self.url_proxy()
        logging.info(f"Proxy {proxy} ")
        logging.info(f"URL = {url}")
        r = response.parse(url, proxy)
        if isinstance(r, dict):
            if r.get("error"):
                return jsonify(error=str(r.get("error")))
        return jsonify(jsons=r["jsons"], html=r["html"])  # jsonify(html=str(html))#


api.add_resource(Cdis_parse, "/parser/cdiscount/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
