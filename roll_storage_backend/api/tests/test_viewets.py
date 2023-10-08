from datetime import datetime as dt, timedelta as td
import json
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.test import Client
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED)
from rest_framework.test import APITestCase

from api.tests.fixtures import (get_test_coil_data,
                                TEST_COIL_STATS_JSON,
                                TEST_COIL_URL_HEADERS)
from storage.models import Coil


TEST_COIL_DATA = get_test_coil_data()


class CoilTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for coil_number in range(1, len(TEST_COIL_DATA) + 1):
            coil = TEST_COIL_DATA[coil_number]
            Coil.objects.create(
                length=coil['length'],
                weight=coil['weight']
            )

    def setUp(self):
        self.guest_client = Client()

    def test_coil_view_create_data(self):
        coil_count = Coil.objects.all().count()
        request_url = reverse('api:coil-list')

        data = {
            'length': 10,
            'weight': 2
        }
        response = self.guest_client.post(
            request_url, data, format='json'
        )
        self.assertEqual(
            Coil.objects.all().count(),
            coil_count + 1,
            ('Убедитесь, что объект рулона '
             'создается в базе данных')
        )
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED,
            'Убедитесь, что POST запрос на эндпоинт. '
            f'{request_url} возвращает статус HTTP_201_CREATED')
        self.assertEqual(
            get_object_or_404(
                Coil,
                pk=response.data['id']
            ).weight,
            data['weight'],
            ('Вес рулона в базе данных не соответствует '
             'переданной в POST запросе.')
        )
        self.assertEqual(
            get_object_or_404(Coil,
                              pk=response.data['id']
                              ).add_date,
            dt.now().date(),
            ('Дата добавления рулона на склад должна '
             'содержать текущую дату, добавленную автоматически.')
        )

    def test_coil_soft_delete_data(self):
        coil_pk = 5
        request_url = reverse('api:coil-detail',
                              kwargs={'pk': coil_pk})
        response = self.guest_client.delete(request_url)
        self.assertTrue(
            Coil.objects.filter(pk=coil_pk).exists(),
            'Убедитесь, что метод DELETE не удаляет '
            'объект рулона из базы данных, а присваевает дату '
            'удаления со склада существующему объекту.'
        )
        deleted_coil = get_object_or_404(Coil, pk=coil_pk)
        self.assertEqual(
            response.status_code,
            HTTP_202_ACCEPTED,
            ('Убедитесь, что метод мягкого удаления '
             'возвращает статус HTTP_202_ACCEPTED')
        )
        self.assertEqual(
            deleted_coil.deletion_date,
            dt.now().date(),
            'Убедитесь, что при удалении для объекта автоматически '
            'устанавливается сегодняшняя дата удаления.'
        )

    def test_coil_viewset_json_response(self):
        """Проверяем конт"""
        request_url = reverse('api:coil-list')
        response = self.guest_client.get(
            request_url, format='json'
        )
        self.assertEqual(
            len(json.loads(response.content)),
            len(TEST_COIL_DATA),
            f'Убедитесь, что все рулоны отображаются '
            f'при GET запросе на эндпоинт {request_url}.')
        for headers, expected_objects_count in TEST_COIL_URL_HEADERS.items():
            with self.subTest(headers=headers):
                request_url_with_filters = f'{request_url}{headers}'
                response = self.guest_client.get(
                    request_url_with_filters, format='json'
                )
                self.assertEqual(
                    len(response.data),
                    expected_objects_count,
                    'Убедитесь, что при GET запросами с параметрами: '
                    ', количество выдаваемых объектов изменяется.'
                    f'url с ошибкой: {request_url_with_filters}'
                )

    def test_coil_stats_json_response_without_dates(self):
        request_url = reverse('api:coil-stats')
        response = self.guest_client.get(
            request_url, format='json'
        )
        test_json_data = TEST_COIL_STATS_JSON['Данные']
        curren_json_data = response.data['Данные']
        for field, value in test_json_data.items():
            with self.subTest(field=field, value=value):
                self.assertEqual(
                    test_json_data[field],
                    curren_json_data[field],
                    'Убедитесь, что в поле '
                    f'{test_json_data[field]} возвращается '
                    f'значение {value}, а не {curren_json_data[field]}'
                )

    def test_coil_stats_dates_json(self):
        request_url = reverse('api:coil-stats')
        begin_date_range = dt.now().date()
        end_date_rage = dt.now().date() + td(days=1)
        request_url_with_filters = (f'{request_url}?begin_date_range='
                                    f'{begin_date_range}&'
                                    f'end_date_range={end_date_rage}')
        response = self.guest_client.get(
            request_url_with_filters, format='json'
        )
        self.assertEqual(
            response.data['Начало периода'],
            begin_date_range,
            'Убедитесь, что при добавлении даты начала периода в запрос, '
            'она успешно обрабатывается системой.'
        )
        self.assertEqual(
            response.data['Окончание периода'],
            end_date_rage,
            'Убедитесь, что при добавлении даты окончания периода в запрос, '
            'она успешно обрабатывается системой'
        )
