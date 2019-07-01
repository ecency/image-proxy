import io

import requests
from flask import Flask, send_file
from flask_caching import Cache
from werkzeug.middleware.proxy_fix import ProxyFix
import tempfile
import os

app = None
cache = None

tempdir = os.path.join(tempfile.gettempdir(), 'image-proxy')


def __flask_setup():
    global app, cache

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DEFAULT_TIMEOUT': 3600, 'CACHE_DIR': tempdir})

    @app.route('/favicon.ico')
    def favicon():
        return 'favicon'

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        if cache.get(path) is None:
            resp = requests.get('https://steemitimages.com/{}'.format(path))
            content = resp.content
            content_type = resp.headers['content-type']

            cache.set(path, {'content': content, 'content_type': content_type})
        else:
            c = cache.get(path)

            content = c['content']
            content_type = c['content_type']

        if content_type.startswith('image'):
            return send_file(
                io.BytesIO(content),
                mimetype=content_type)

        return content


def __run_dev_server():
    global app

    app.config['DEVELOPMENT'] = True
    app.config['DEBUG'] = True

    app.run(host='127.0.0.1', port=8088)


__flask_setup()

if __name__ == '__main__':
    __run_dev_server()
