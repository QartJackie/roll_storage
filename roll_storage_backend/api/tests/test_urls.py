from django.urls import reverse
from django.test import Client
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_201_CREATED,
                                   HTTP_405_METHOD_NOT_ALLOWED,
                                   HTTP_202_ACCEPTED,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.test import APITestCase

from storage.models import Coil


class CoilUrlsStatusTest(APITestCase):
    """Тест urls проекта."""

    @classmethod
    def setUpClass(cls):
        """Общая настройка."""
        super().setUpClass()
        cls.coil = Coil.objects.create(
            length=10,
            weight=2
        )
        cls.coil_count = 1
        cls.coil_list_url = 'api:coil-list'
        cls.coil_detail_url = 'api:coil-detail'
        cls.coil_stats_url = '/coil/stats/'
        cls.detail_kwargs = {'pk': cls.coil}
        cls.unexisting_page = '/unexisting_page/'

    def setUp(self):
        """Вспомогательная настройка."""
        self.guest_client = Client()

    def test_coil_list_endpoint_status(self):
        """Проверяем статусы /api/v1/coil/."""

        request_url = reverse('api:coil-list')
        response = self.guest_client.get(request_url)

        self.assertEqual(
            response.status_code,
            HTTP_200_OK,
            ('Убедитесь, что GET запрос на эндпоинт. '
             f'{request_url} возвращает статус HTTP_200_OK')
        )

        request_methods = {
            self.guest_client.get: HTTP_200_OK,
            self.guest_client.post: HTTP_400_BAD_REQUEST,
            self.guest_client.put: HTTP_405_METHOD_NOT_ALLOWED,
            self.guest_client.patch: HTTP_405_METHOD_NOT_ALLOWED,
            self.guest_client.delete: HTTP_405_METHOD_NOT_ALLOWED
        }

        for client_with_method, expected_status in request_methods.items():
            msg_add = ''
            with self.subTest(client_with_method=client_with_method):
                response = client_with_method(request_url)
                if expected_status == HTTP_400_BAD_REQUEST:
                    msg_add = 'без данных'
                self.assertEqual(
                    response.status_code,
                    expected_status,
                    (f'Убедитесь, что метод {client_with_method.__name__} '
                     f'{msg_add} возвращает статус {expected_status}')

                )

    def test_coil_create_with_data_status(self):
        """Проверяем статус создания
        обекта рулона с данными."""

        request_url = reverse('api:coil-list')
        data = {'length': 15,
                'weight': 3}
        response = self.guest_client.post(request_url, data, format='json')
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED,
            (f'Убедитесь, что POST запрос на эндпоиинт {request_url} '
             f'возвращает статус {HTTP_201_CREATED}')
        )

    def test_coil_detail_endpoint_status(self):
        """Проверяем статусы методов на странице detail."""

        request_url = reverse('api:coil-detail', kwargs={'pk': self.coil.pk})
        request_methods = {
            self.guest_client.get: HTTP_200_OK,
            self.guest_client.post: HTTP_405_METHOD_NOT_ALLOWED,
            self.guest_client.put: HTTP_405_METHOD_NOT_ALLOWED,
            self.guest_client.patch: HTTP_405_METHOD_NOT_ALLOWED,
            self.guest_client.delete: HTTP_202_ACCEPTED
        }

        for client_with_method, expected_status in request_methods.items():
            with self.subTest(client_with_method=client_with_method):
                response = client_with_method(request_url)
                self.assertEqual(
                    response.status_code,
                    expected_status,
                    (f'Убедитесь, что метод {client_with_method.__name__} '
                     f'возвращает статус {expected_status}')
                )

    def test_coil_stats_endpont_status(self):
        """Проверяем статусы методов страницы статистики"""

        request_url = reverse('api:coil-stats')
        request_methods = {
            self.guest_client.get: HTTP_200_OK,
            self.guest_client.post: HTTP_405_METHOD_NOT_ALLOWED,
            self.guest_client.put: HTTP_405_METHOD_NOT_ALLOWED,
            self.guest_client.patch: HTTP_405_METHOD_NOT_ALLOWED,
            self.guest_client.delete: HTTP_405_METHOD_NOT_ALLOWED
        }

        for client_with_method, expected_status in request_methods.items():
            with self.subTest(client_with_method=client_with_method):
                response = client_with_method(request_url)
                self.assertEqual(
                    response.status_code,
                    expected_status,
                    (f'Убедитесь, что метод {client_with_method.__name__} '
                     f'возвращает статус {expected_status}')
                )
