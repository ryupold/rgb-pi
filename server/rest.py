import log
import thread
import rgb
import server
import sys

from datetime import timedelta
from flask import Flask, render_template, request, current_app, make_response
from flask.ext.jsonpify import jsonify
from functools import update_wrapper

app = Flask(__name__)


def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/request')
@crossdomain(origin='*', methods=['GET', 'PUT', 'POST', 'OPTIONS'])
def rgbpi_request():
    print "request args= ", request.args
    client_request = request.args.get('request')
    return jsonify(answer=server.applyCommand(client_request)), 200


def startWebservice(threadName, param):
    # Bind to PORT if defined, otherwise default to 5000.
    log.l('starting asyncronous server thread', log.LEVEL_UI)
    thread.start_new_thread(rgb.startServer, (threadName, param, ))
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if len(sys.argv)>1 and sys.argv[1] == "webserver":
    startWebservice('rest thread', 1)


