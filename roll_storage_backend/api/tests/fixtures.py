from datetime import datetime as dt
from decimal import Decimal

TEST_COIL_COUNT = 10

TEST_COIL_URL_HEADERS = {
    '?begin_id_range=1&end_id_range=5': 5,
    '?begin_length_range=1&end_length_range=5': 5,
    '?begin_weight_range=1&end_weight_range=5': 5,
    f'?begin_add_date_range={dt.now().date()}&'
    f'end_add_date_range={dt.now().date()}': 10,
    f'?begin_deletion_date_range={dt.now().date()}&'
    f'end_deletion_date_range={dt.now().date()}': 0
}


TEST_COIL_STATS_JSON = {
    'Начало периода': dt.now().date(),
    'Окончание': {dt.now().date()},
    'Данные': {
        'Количество добавленных, шт.': 10,
        'Количество удаленных рулонов, шт.': 0,
        'Средняя длина рулона за период, м.': Decimal('5.500'),
        'Средний вес рулонов за период, кг.': Decimal('5.500'),
        'Максимальная длина рулона за период, м.': Decimal('10.000'),
        'Минимальная длина рулона за период, м.': Decimal('1.000'),
        'Максимальный вес рулона за период, кг.': Decimal('10.000'),
        'Минимальный вес рулона за период, кг.': Decimal('1.000'),
        'Суммарный вес рулонов за период, кг.': Decimal('55.000'),
        'Максимальный промежуток между добавлением и удалением.': {
            'Дней на складе': {1},
            'Рулон номер': {1}
        },
        'Минимальный промежуток между добавлением и удалением.': {
            'Дней на складе': {1},
            'Рулон номер': {1}
        }
    }
}


def get_test_coil_data():
    coil_list = {}
    for index in range(1, TEST_COIL_COUNT + 1):
        test_coil = {}
        test_coil['length'] = index
        test_coil['weight'] = index
        coil_list[index] = test_coil
    return coil_list
