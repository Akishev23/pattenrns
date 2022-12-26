import quopri
from own_framework.own_requests import GetRequest, PostRequest
from own_framework.templator import render


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found', 'text/html'


class Framework:
    """Base class for whole project framework."""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ: dict, start_response) -> list:
        path = environ['PATH_INFO']
        if not path.endswith('/') and not '.' in path:
            path = f'{path}/'
        request = dict()
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_request_params(environ)
            request['data'] = Framework.decode_value(data)
            print(f'got POST: {Framework.decode_value(data)}')
        elif method == 'GET':
            request_params = GetRequest().get_request_params(environ)
            if request_params:
                request['request_params'] = Framework.decode_value(request_params)
                print(f'got GET: {path}: {Framework.decode_value(request_params)}')
            else:
                print(f'got GET: {path}')

        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        for front in self.fronts_lst:
            front(request)

        code, body, mime = view(request)
        start_response(code, [('Content-Type', mime)])
        return [body.encode('cp1251')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'CP1251')
            val_decode_str = quopri.decodestring(val).decode('CP1251')
            new_data[k] = val_decode_str
        return new_data
