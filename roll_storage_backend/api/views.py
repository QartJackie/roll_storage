import datetime as dt
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from api.serializers import CoilSerializer
from api.utils import (get_query_filter_queryset,
                       Statistics,
                       str_to_datetime_converter)
from storage.models import Coil


class CoilViewSet(viewsets.ModelViewSet):
    """Вьюсет рулонов."""

    queryset = Coil.objects.all()
    serializer_class = CoilSerializer
    permission_classes = (AllowAny, )
    http_method_names = ['get', 'post', 'delete']

    def get_object(self):
        """Метод получения объекта по идентификатору.
        По умолчанию PRIMARY KEY = id модели рулона."""

        coil_id = self.kwargs.get('pk')
        return get_object_or_404(Coil, id=coil_id)

    def get_queryset(self):
        """Метод получения QuerySet'a с фильтрами и без."""

        if self.request.method == 'GET':
            queryset = get_query_filter_queryset(self.request)
            return queryset

    def destroy(self, request, *args, **kwargs):
        """Метод мягконо удаления рулона со склада.
        Присваивает дату удаления, объект БД не удалется."""

        instance = self.get_object()

        if instance.deletion_date is None:

            instance.deletion_date = dt.datetime.now().date()
            instance.save()
            return Response(
                {'detail':
                 f'Рулон с номером {instance.id} удален со склада.'},
                status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response(
                {'denied': 'Рулон уже удален со склада.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

    @action(methods=['get'], detail=False,
            url_name='stats', url_path='stats')
    def get_stats(self, request):
        """Метод для просмотра статистики по рулонам склада."""

        response_data = {}
        queryset = self.get_queryset()
        begin_date_range = request.query_params.get('begin_date_range')
        end_date_range = request.query_params.get('end_date_range')

        if begin_date_range and end_date_range:
            begin_date_range = str_to_datetime_converter(begin_date_range)
            end_date_range = str_to_datetime_converter(end_date_range)
        else:
            begin_date_range = dt.datetime.now().date()
            end_date_range = dt.datetime.now().date()
        if begin_date_range > end_date_range:
            return Response(
                {'error': 'Дата начала периода не может '
                          'быть больше даты окончания.'},
                status=status.HTTP_403_FORBIDDEN
            )
        stats = Statistics(queryset,
                           begin_date_range,
                           end_date_range)
        if len(stats.get_coils_filtered_on_period()) == 0:
            response_data['message'] = (
                'Выборка данных пуста, невозможно предоставить '
                'статистику. Проверьте даты периода, по умолчанию '
                'период установлен на сегодня')
        else:
            stats = Statistics(queryset,
                               begin_date_range,
                               end_date_range)
            response_data['Начало периода'] = begin_date_range
            response_data['Окончание периода'] = end_date_range
            response_data['Данные'] = stats.get_statistic_data()

        return Response(response_data, status=status.HTTP_200_OK)
