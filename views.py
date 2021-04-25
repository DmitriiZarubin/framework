from framework.templator import render


class Index:
    """
    класс для шаблона index
    """

    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))


class About:
    """
    класс для шаблона about
    """

    def __call__(self, request):
        return '200 OK', render('about.html')
