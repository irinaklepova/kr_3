import pytest
from kr_3.src.utils.functions import load_data, data_to_format, hidden_card_or_account_number, output_operations


# Фикстура для загрузки операций из JSON-файла
@pytest.fixture
def operations_data():
    return load_data()


def test_data_to_format():
    """Тест форматирования даты"""
    date_str = '2018-03-23T10:45:06.972075'
    assert (data_to_format(date_str)) == '23.03.2018'


# парамертизация для теста на отображение номера карты или счета
@pytest.mark.parametrize("value, expected", [
    ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
    ("Visa Platinum 1246377376343588", "Visa Platinum 1246 37** **** 3588"),
    ("МИР 8201420097886664", "МИР 8201 42** **** 6664"),
    ("Счет 64686473678894779589", "Счет **9589"),
    (None, "")
])
def test_hidden_card_or_account_number(value, expected):
    """Тест отображения номера карты или счета"""
    assert hidden_card_or_account_number(value) == expected


def test_output_operations(operations_data, capsys):
    """Тест вывода операций"""
    output_operations(operations_data)
    captured = capsys.readouterr()
    # Проверяем, что вывод содержит ожидаемые строки
    assert "19.11.2019" in captured.out
    assert "Maestro 7810 84** **** 5568" in captured.out
    assert "Счет **2869" in captured.out
    assert "30153.72 руб." in captured.out
