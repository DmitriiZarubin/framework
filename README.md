lesson_1

ubuntu на windows 10 установить не удалось, поэтому примеры запускал на virtualbox

для запуска через wsgi используется команда:
uwsgi --http :8000 --wsgi-file fwsgi.py

через wsgiref запустить получилось


lesson_2

Запуск сервера... http://127.0.0.1:8080
Нам пришли GET-параметры: {}
/
127.0.0.1 - - [26/Apr/2021 22:06:32] "GET / HTTP/1.1" 200 4629
Нам пришёл post-запрос: {'name': 'поле_для_имени', 'email': 'поле_для_почты@mail.ru', 'location': 'msk', 'member': 'yes'}
/
127.0.0.1 - - [26/Apr/2021 22:09:38] "POST / HTTP/1.1" 200 4629