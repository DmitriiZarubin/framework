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

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        request = {}

        for front in self.fronts:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
