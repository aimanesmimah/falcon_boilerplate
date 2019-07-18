import falcon, json
from urllib import request
from abc import ABCMeta, abstractmethod


# cors middleware
class CrossDomain(object):
    def __init__(self):
        self.cors_base= "Access-Control-Allow-"
        self.cors= [
                    ('Origin','*'), 
                    ('Methods','GET, PUT, POST, DELETE'),
                    ('Credentials','true'),
                    ('Headers','Origin, Authorization, Content-Type, X-Requested-With')
                ]

    def process_response(self,request,response,resource,arg=''):
        for key,val in self.cors:
            response.set_header(f'{self.cors_base}{key}',val)


class RequireJSON:

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')


class JSON_translator:
    def process_request(self, req, resp):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['payload'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource,arg=''):
        if not hasattr(resp.context, 'result'):
            return

        resp.body = json.dumps(resp.context.result)


middlewares= [ CrossDomain, RequireJSON, JSON_translator ]

