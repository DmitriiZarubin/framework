from datetime import date
from views import Index, About, Contact


def date_front(request):
    request['data'] = date.today()


fronts = [date_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
}
