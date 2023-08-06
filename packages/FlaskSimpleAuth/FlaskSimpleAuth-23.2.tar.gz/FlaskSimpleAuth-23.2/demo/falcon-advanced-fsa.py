# FlaskSimpleAuth version of Falcon Advanced Quistart Example
#
# https://falcon.readthedocs.io/en/stable/user/quickstart.html
#

import json
import uuid
import logging
import requests

logging.basicConfig()
log = logging.getLogger(f"things.{__name__}")

# unclear…
class StorageEngine:
    def get_things(self, marker, limit):
        return [{'id': str(uuid.uuid4()), 'color': 'green'}]

    def add_thing(self, thing):
        thing['id'] = str(uuid.uuid4())
        return thing

# forward search and return the Response
SEARCH = {
    "d": "https://duckduckgo.com",
    "g": "https://www.google.com/search",
    "y": "https://search.yahoo.com/search",
}

def search(engine, query):
    res = requests.get(SEARCH[engine], params={"q": query})
    return fsa.Response(res.text, res.status_code, mimetype=res.headers["content-type"])

# new authentication scheme
@app.authentication("fernet")
def get_fernet_token_auth(app: Flask, req: Request) -> str|None:
    token = req.headers.get("Authorization", None)
    accid = req.headers.get("Account-ID", None)
    if not token or not accid:
        raise fsa.ErrorResponse("missing fernet authentication headers", 401, 
                                headers={"WWW-Authenticate", "Token type=\"Fernet\""})
    # FIXME should really check a token…
    return accid if token == f"Fernet-{accid}" else None

# check that the clients really accepts JSON and would send JSON
@app.before_request
def require_json(req: Request):
    if "application/json" not in req.headers.get("Accept", ""):
        raise fsa.ErrorResponse("client must accept JSON", 400)    
    if "application/json" not in req.headers.get("Content-Type", "application/json"):
        raise fsa.ErrorResponse("client must send JSON", 400)    

# FIXME JSONTranslator
# I do not understand what it seeks to do
# I understand that the point is to show whether a special type handler
# can be added…

# max_body for some path!
# @app.before_request
def max_body(req: Request):
    if req.content_length > 50:
        raise fsa.ErrorResponse("request body too large", 400)

def max_body(limit):
    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = (
                'The size of the request is too large. The body must not '
                'exceed ' + str(limit) + ' bytes in length.'
            )

            raise falcon.HTTPPayloadTooLarge(
                title='Request body is too large', description=msg
            )

    return hook


class ThingsResource:
    def __init__(self, db):
        self.db = db

    def on_get(self, req, resp, user_id):
        marker = req.get_param('marker') or ''
        limit = req.get_param_as_int('limit') or 50

        try:
            result = self.db.get_things(marker, limit)
        except Exception as ex:
            self.logger.error(ex)

            description = (
                'Aliens have attacked our base! We will '
                'be back as soon as we fight them off. '
                'We appreciate your patience.'
            )

            raise falcon.HTTPServiceUnavailable(
                title='Service Outage', description=description, retry_after=30
            )

        # NOTE: Normally you would use resp.media for this sort of thing;
        # this example serves only to demonstrate how the context can be
        # used to pass arbitrary values between middleware components,
        # hooks, and resources.
        resp.context.result = result

        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_200

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp, user_id):
        try:
            doc = req.context.doc
        except AttributeError:
            raise falcon.HTTPBadRequest(
                title='Missing thing',
                description='A thing must be submitted in the request body.',
            )

        proper_thing = self.db.add_thing(doc)

        resp.status = falcon.HTTP_201
        resp.location = '/%s/things/%s' % (user_id, proper_thing['id'])


# Configure your WSGI server to load "things.app" (app is a WSGI callable)
app = falcon.App(
    middleware=[
        AuthMiddleware(),
        RequireJSON(),
        JSONTranslator(),
    ]
)

db = StorageEngine()
things = ThingsResource(db)
app.add_route('/{user_id}/things', things)

# If a responder ever raises an instance of StorageError, pass control to
# the given handler.
app.add_error_handler(StorageError, StorageError.handle)

# Proxy some things to another service; this example shows how you might
# send parts of an API off to a legacy system that hasn't been upgraded
# yet, or perhaps is a single cluster that all data centers have to share.
sink = SinkAdapter()
app.add_sink(sink, r'/search/(?P<engine>ddg|y)\Z')

# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
