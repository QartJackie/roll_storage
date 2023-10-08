# ROLL STAGE
##### Сервис учета информации о складских остатках.
###### На текущем этапе возможна работа с рулонами.

## Стек:

Python 3.9
Django DRF 3.2
Pytest
PostgreSQL
Docker
Nginx


#### Запуск проекта:
Клонируйте репозиторий и подготовьте сервер, при оркестрации контенеров, учтите уже имеющуюся настройку nginx, для маршрутизации запросов:
```
docker-compose.production.yml <username>@<host>:/home/<username>/roll_storage/
nginx.conf <username>@<host>:/home/<username>/roll_storage/
.env <username>@<host>:/home/<username>/roll_storage/
```

Установите docker и docker-compose:
```sudo apt install docker.io```
```sudo apt install docker-compose```

Создайте или скопируйте файл .env с данными для запуска приложения.
Соберите контейнеры и выполните миграции:

```sudo docker compose -f docker-compose.production.yml up -d```
```sudo docker compose -f docker-compose.production.yml exec <имя контейнера> python manage.py migrate```

Для работы достаточно начать делать запросы. Права на тест системы не утсанавливались, и создавать пользователя не придется. Но если Вы хотите установить права, то в проекте заготовлена модель User. Поэтому достаточно будет использовать стандартные пакеты Django для настройки аутентификации по токену,



## Доступные эндпоинты

```
[GET] http://localhost:8000/api/v1/coil/ - список всех рулонов, бывавших на складе
[GET] http://localhost:8000/api/v1/coil/<Номер рулона для просмотра информации>/
[POST] http://localhost:8000/api/v1/coil/ - добавление рулона на склад, длина и вес рулона обязательны.
[DELETE] http://localhost:8000/api/v1/coil/<Номер рулона для удаления со склада>/ - мягкое удаление рулона, с установкой даты удаления со склада
[GET] http://localhost:8000/api/v1/coil/stats/ - статистика по рулонам
```
## Реализована фильтрация списка рулонов и статистики по рулонам:
### Список рулонов:
```
[GET] http://localhost:8000/api/v1/coil/?<Начальное значение>&<конечное значение>/
```
##### Для фильтрации рулонов предусмотрены параметры. Для фильтрации нужно задать минимум 2 параметра - начальное и конечное значение, в одном поле фильтрации. Начальное значение всегда начинается с begin, а конечное с end. ###
_______________________________________________________________________________________________________
##### Возможна комбинация нескольких периодов.
_______________________________________________________________________________________________________
```begin_id_range - end_id_range``` (Фильтрация по значению id)
```Пример: [GET] http://localhost:8000/api/v1/coil/?begin_id_range=5&end_id_range=122/```

```begin_length_range - end_length_range``` (Фильтрация по значению длинны рулона)
```Пример: [GET] http://localhost:8000/api/v1/coil/?begin_length_range=15&end_length_range=1000/```

```begin_weight_range - end_weight_range``` (Фильтрация по значению веса рулона)
```Пример: [GET] http://localhost:8000/api/v1/coil/?begin_weight_range=3&end_weight_range=100/```

```begin_add_date_range - end_add_date_range``` (Фильтрация по дате добавления рулона на склад)
```Пример: [GET] http://localhost:8000/api/v1/coil/?begin_add_date_range="2023-08-01"&end_add_date_range="2023-10-08"/```

```begin_deletion_date_range - end_deletion_date_rang``` (Фильтрация по дате удаления рулона со склада)
```Пример: [GET] http://localhost:8000/api/v1/coil/?begin_deletion_date_range="2023-08-01"&end_deletion_date_range="2023-10-08"/```

##### Для эндпоинта со статистикой предусмотрены 2 параметра периода, в который входят две даты:

```По умолчанию система отдает отчет за текущий день, и если вы хотите выбрать период, передайте параметры как описано ниже```

```begin_date_tange``` - Начало периода выборки
```end_date_range``` - Окончание периода выборки
```Пример: [GET] http://localhost:8000/api/v1/coil/stats/?begin_date_range="2023-08-01"&end_date_range="2023-10-08"/```


#### Тесты

Проект частично покрыт тестами, чтобы запустить тесты достаточно запустить команду в корне проекта: 

```pytest -rA```

