import quopri
from own_framework.own_requests import GetRequest, PostRequest


class PageNotFound404:
    def __call__(self):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    """Base class for whole project framework."""

    def __init__(self, routes_obj):
        self.routes_lst = routes_obj

    def __call__(self, environ: dict, start_response) -> list:
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = dict()
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_request_params(environ)
            request['data'] = data
            print(f'got POST: {Framework.decode_value(data)}')
        elif method == 'GET':
            request_params = GetRequest().get_request_params(environ)
            request['request_params'] = request_params
            print(f'got GET: {request_params}')

        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        code, body = view()
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('cp1251')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
