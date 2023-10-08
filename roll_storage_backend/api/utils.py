from datetime import datetime as dt
import decimal
from django.db.models import Avg, Q, Max, Min, Sum

from storage.models import Coil


def str_to_datetime_converter(string):
    """Функция для конвертирования строкового
    представления даты в модель объекта datetime."""

    return dt.strptime(string, "%Y-%m-%d").date()


def get_id_filter(request):
    """Функция для извлечения диапазона
    идентификаторов рулонов из GET запроса."""

    begin_id_range = request.query_params.get('begin_id_range')
    end_id_range = request.query_params.get('end_id_range')

    if begin_id_range and end_id_range:
        return begin_id_range, end_id_range
    return None


def get_length_filter(request):
    """Функция для извлечения диапазона
    длин рулонов из GET запроса."""

    begin_length_range = request.query_params.get('begin_length_range')
    end_length_range = request.query_params.get('end_length_range')

    if begin_length_range and end_length_range:
        return begin_length_range, end_length_range
    return None


def get_weight_filter(request):
    """Функция для извлечения диапазона
    весов рулонов из GET запроса."""

    begin_weight_range = request.query_params.get('begin_weight_range')
    end_weight_range = request.query_params.get('end_weight_range')

    if begin_weight_range and end_weight_range:
        return begin_weight_range, end_weight_range
    return None


def get_add_date_filter(request):
    """Функция для извлечения диапазона
    дат добавления рулона из GET запроса."""

    begin_add_date_range = request.query_params.get('begin_add_date_range')
    end_add_date_range = request.query_params.get('end_add_date_range')

    if begin_add_date_range and end_add_date_range:
        return begin_add_date_range, end_add_date_range
    return None


def get_deletion_date_filter(request):
    """Функция для извлечения диапазона
    дат удаления рулона из GET запроса."""

    begin_deletion_date_range = request.query_params.get(
        'begin_deletion_date_range'
    )
    end_deletion_date_range = request.query_params.get(
        'end_deletion_date_range'
    )

    if begin_deletion_date_range and end_deletion_date_range:
        return begin_deletion_date_range, end_deletion_date_range
    return None


def get_query_filter_queryset(request):
    """Функция для фильтрации queryset'a по параметрам GET запроса.
    Собирает все указанные значения фильров и использует их комбинацию."""

    filters = {}

    if get_id_filter(request):
        """Метод фильрации по id."""

        begin_id_range, end_id_range = get_id_filter(request)
        filters['id__range'] = [begin_id_range, end_id_range]

    if get_length_filter(request):
        """Метод фильрации по длине рулона."""

        begin_length_range, end_length_range = get_length_filter(request)
        filters['length__range'] = [begin_length_range, end_length_range]

    if get_weight_filter(request):
        """Метод фильрации по весу рулона."""

        begin_weight_range, end_weight_range = get_weight_filter(
            request
        )
        filters['weight__range'] = [begin_weight_range,
                                    end_weight_range]

    if get_add_date_filter(request):
        """Метод фильрации по дате добавления рулона."""
        begin_add_date_range, end_add_date_range = get_add_date_filter(
            request
        )
        filters['add_date__range'] = [begin_add_date_range,
                                      end_add_date_range]

    if get_deletion_date_filter(request):
        """Метод фильрации по дату удаления рулона со склада."""

        begin_deletion_range, end_deletion_range = get_deletion_date_filter(
            request
        )
        filters['deletion_date__range'] = [
            begin_deletion_range,
            end_deletion_range
        ]
    return Coil.objects.filter(
        Q(**filters)
    ) if filters else Coil.objects.all()


class Statistics:
    """Модель данных статистики."""

    def __init__(self,
                 queryset,
                 begin_period_date,
                 end_period_date):
        self.queryset = queryset
        self.begin_period_date = begin_period_date
        self.end_period_date = end_period_date
        self.filtered_queryset = self.get_coils_filtered_on_period()

    def __str__(self):
        """Строковое представление класса."""

        return 'Статистика по рулонам на складе за период'

    def get_period(self):
        """Метод получения периода поучения информации."""
        period = f'{self.begin_period_date} - {self.end_period_date}'
        print(f'В классе: {period}')
        return period

    def decimal_rounding(self, value):
        """Функция округления чисел с
        плавающей точкой до 3 знаков после запятой.
        Принимает на вход значение decimal ли float."""

        if value and isinstance(value,
                                decimal.Decimal
                                ) or type(value) is float:
            rounded_digit = decimal.Decimal(value)
            return rounded_digit.quantize(decimal.Decimal('0.000'))
        raise Exception('Не удалось округлить значение.')

    def get_coils_filtered_on_period(self):
        """Метод фильтрации QuerySet'a по периоду, указанному
        в запросе статистики. Проверяет рулоны с датой
        удаления и без."""

        return self.queryset.filter(
            Q(add_date__lte=self.end_period_date,
              deletion_date__gte=self.begin_period_date) |
            Q(add_date__range=[
                self.begin_period_date,
                self.end_period_date
                ],
                deletion_date=None)
        )

    def get_added_coil_count_on_period(self):
        """Метод извлечения количества
        добавленных рулонов за период."""

        return self.queryset.filter(add_date__range=[
                    self.begin_period_date,
                    self.end_period_date
                ]
        ).count()

    def get_deleted_coil_count_on_period(self):
        """Метод извлечения количества
        удаленных рулонов за период."""
        return self.queryset.filter(
            deletion_date__range=[
                self.begin_period_date,
                self.end_period_date]
                ).count()

    def get_average_coil_length(self):
        """Метод извлечения средней
        длины рулонов за период."""

        return self.decimal_rounding(
            self.filtered_queryset.aggregate(
                Avg('length')
            )['length__avg']
        )

    def get_average_coil_weight(self):
        """Метод извлечения среднего
        веса рулонов за период."""

        return self.decimal_rounding(
            self.filtered_queryset.aggregate(
                Avg('weight')
            )['weight__avg']
        )

    def get_max_coil_length(self):
        """Метод извлечения максимальной
        длины рулона на складе за период."""

        return self.decimal_rounding(
            self.filtered_queryset.aggregate(
                Max('length')
            )['length__max']
        )

    def get_min_coil_length(self):
        """Метод извлечения минимальной
        длины рулона на складе за период."""

        return self.decimal_rounding(
            self.filtered_queryset.aggregate(
                Min('length')
            )['length__min']
        )

    def get_max_coil_weight(self):
        """Метод извлечения максимального
        веса рулона на складе за период."""

        return self.decimal_rounding(
            self.filtered_queryset.aggregate(
                Max('weight')
            )['weight__max']
        )

    def get_min_coil_weight(self):
        """Метод извлечения минимального
        веса рулона на складе за период."""

        return self.decimal_rounding(
            self.filtered_queryset.aggregate(
                Min('weight')
            )['weight__min']
        )

    def get_sum_coils_weight(self):
        """Метод извлечения суммарного
        веса рулонов на складе за период."""

        return self.decimal_rounding(
            self.filtered_queryset.aggregate(
                Sum('weight')
            )['weight__sum']
        )

    def get_max_timedelta(self):
        """Функция извлечения максимальной
        продолжительности нахождения рулона на складе.
        Работает только с периодом, который задан для фильрации.
        При выходе параметров рулона за пределы диапазона фильтра,
        искуственно ограничивает его до укзанных дат."""

        max_timedelta = None
        coil_timedelta = None

        for coil in self.filtered_queryset:
            added_date = coil.add_date
            deleted_date = coil.deletion_date
            if deleted_date is None:
                deleted_date = self.end_period_date
            if added_date < self.begin_period_date <= deleted_date:
                added_date = self.begin_period_date
            if added_date <= deleted_date > self.end_period_date:
                deleted_date = self.end_period_date
            coil_timedelta = (deleted_date - added_date).days + 1
            if max_timedelta is None or max_timedelta < coil_timedelta:
                max_timedelta = coil_timedelta
                coil_number = coil.pk

        return max_timedelta, coil_number

    def get_min_timedelta(self):
        """Функция извлечения максимальной
        продолжительности нахождения рулона на складе.
        Работает только с периодом, который задан для фильрации.
        При выходе параметров рулона за пределы диапазона фильтра,
        искуственно ограничивает его до укзанных дат."""

        min_timedelta = None
        coil_timedelta = None

        for coil in self.filtered_queryset:
            added_date = coil.add_date
            deleted_date = coil.deletion_date
            if deleted_date is None:
                deleted_date = self.end_period_date
            if added_date < self.begin_period_date <= deleted_date:
                added_date = self.begin_period_date
            if added_date <= deleted_date > self.end_period_date:
                deleted_date = self.end_period_date
            coil_timedelta = (deleted_date - added_date).days + 1
            if min_timedelta is None or min_timedelta > coil_timedelta:
                min_timedelta = coil_timedelta
                coil_number = coil.pk
        return min_timedelta, coil_number

    def get_statistic_data(self):
        """Метод получения данных статистики, собранных вместе.
        Задействует встроенные методы для получения информации."""

        data = {}
        max_timedelta, max_timedelta_coil_number = self.get_max_timedelta()
        min_timedelta, min_timedelta_coil_number = self.get_min_timedelta()

        data['Количество добавленных, шт.'
             ] = self.get_added_coil_count_on_period()
        data['Количество удаленных рулонов, шт.'
             ] = self.get_deleted_coil_count_on_period()
        data['Средняя длина рулона за период, м.'
             ] = self.get_average_coil_length()
        data['Средний вес рулонов за период, кг.'
             ] = self.get_average_coil_weight()
        data['Максимальная длина рулона за период, м.'
             ] = self.get_max_coil_length()
        data['Минимальная длина рулона за период, м.'
             ] = self.get_min_coil_length()
        data['Максимальный вес рулона за период, кг.'
             ] = self.get_max_coil_weight()
        data['Минимальный вес рулона за период, кг.'
             ] = self.get_min_coil_weight()
        data['Суммарный вес рулонов за период, кг.'
             ] = self.get_sum_coils_weight()
        data['Максимальный промежуток между добавлением и удалением.'
             ] = {'Дней на складе': {max_timedelta},
                  'Рулон номер': {max_timedelta_coil_number}}
        data['Минимальный промежуток между добавлением и удалением.'
             ] = {'Дней на складе': {min_timedelta},
                  'Рулон номер': {min_timedelta_coil_number}}
        return data
