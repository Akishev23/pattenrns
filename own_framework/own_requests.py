"""
Module for different type of request with params handling
"""


class AnyTypeRequest:
    @staticmethod
    def parse_input_data(data: str) -> dict:
        if data:
            res = dict()
            for item in data.split('&'):
                key, val = item.split('=')
                res.update({key: val})
            return res


class GetRequest(AnyTypeRequest):

    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = GetRequest.parse_input_data(query_string)
        return request_params


class PostRequest(AnyTypeRequest):
    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        content_length_data = env.get('CONTENT_LENGTH')
        if content_length_data:
            content_length = int(content_length_data)
            data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
            return data
        return b''

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data
