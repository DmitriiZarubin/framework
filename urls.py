from datetime import date


def date_front(request):
    request['date'] = date.today()


fronts = [date_front]
