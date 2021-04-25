from datetime import date
from views import Index, About


def date_front(request):
    request['data'] = date.today()


fronts = [date_front]

routes = {
    '/': Index(),
    '/about/': About(),
}
