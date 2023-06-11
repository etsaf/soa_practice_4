## Практика 4. Разработка REST веб-сервиса

Сафонова Елизавета, БПМИ-206

-------

### Задача 1

Собрать и запустить образ:

```
docker build --tag python-docker .
docker run -d -p 5001:5000 python-docker
```

При этом запускается один Flask сервер, который позволяет добавлять, просматривать, редактировать и удалять информацию по профилю игрока. В профиле может храниться информация об имени, аватаре, поле и e-mail пользователя. Взаимодействовать с сервером можно с помощью curl, зная id, присвоенные игрокам (его можно получить при добавлении пользователя).

```
Информация обо всех пользователях:
curl --location --request GET 'http://localhost:5001/profiles/api/v1.0/users'

Информация о пользователе с заданным id (в этом примере id=1):
curl --location --request GET 'http://localhost:5001//profiles/api/v1.0/users/1'

Добавление игрока с заданным профилем (в этом примере с именем "To test POST" и аватаром "test.jpg"):
curl --location --request POST 'http://localhost:5001/profiles/api/v1.0/users' --header 'Content-Type: application/json' --data-raw '{ "name": "To test POST","picture": "test.jpg"}'

Изменение профиля игрока (в этом примере меняется имя):
curl --location --request PUT 'http://localhost:5001/profiles/api/v1.0/users/3' --header 'Content-Type: application/json' --data-raw '{ "name": "To test PUT"}'

Удаление профиля игрока (в примере id=3):
curl --location --request DELETE 'http://localhost:5001//profiles/api/v1.0/users/3'
```

### Задача 2

Flask сервер из предыдущего задания также умеет создавать pdf-файлы с информацией о пользователях.

```
Создать pdf-файл по данному пользователю (при id=1):
curl --location --request POST 'http://localhost:5001//profiles/api/v1.0/users/make_pdf/1'

Ответ на этот запрос возвращает URL, где можно получить pdf. Пример ответа со ссылкой:
{"pdf":"http://localhost:5001/profiles/api/v1.0/users/pdf/1"}
Файл скачается при открытии браузере ссылки http://localhost:5001/profiles/api/v1.0/users/pdf/1. Пример файла - example.pdf.
```

### Комментарий

- Для удобства ручной проверки картинка в выводе командной строки, вместо нее выводится строка "picture hidden". В файле картинка есть.

- Написанный сервер основан на источниках, упомянутых в методических указаниях: <https://github.com/domage/soa-curriculum/tree/main/examples/flask-rest-tutorial> и <https://github.com/geonaut/flask-todo-rest-api>
