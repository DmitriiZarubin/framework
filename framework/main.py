import quopri
from framework.requests import GetRequests, PostRequests


class PageNotFound404:
    """
    класс для ошибки 404
    """

    def __call__(self, request):
        return '404', '404 Page not found'


class Framework:
    """
    Основной класс фреймворка
    """

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = data
            print(f'Нам пришёл post-запрос: {Framework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = request_params
            print(f'Нам пришли GET-параметры: {request_params}')

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        for front in self.fronts:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        print(environ['PATH_INFO'])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data


class DebugApp(Framework):
    """
    WSGI-application - логирующий вид
    """

    def __init__(self, routes_obj, fronts_obj):
        self.app = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.app(env, start_response)


class FakeApp(Framework):
    """
    WSGI-application - фейковый вид
    """

    def __init__(self, routes_obj, fronts_obj):
        self.app = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
