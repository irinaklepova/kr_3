import json
import os.path
from datetime import datetime


def load_data():
    """получает список словарей из json-файла, фильтрует пустые словари"""
    file_path = os.path.join(os.path.dirname(__file__), "../operations.json")
    with (open(file_path, 'r', encoding="utf-8") as file):
        data_json = json.load(file)  # преобразуем json в список словарей
        data = []  # исключаем случаи попадания пустых словарей в список
        for item in data_json:
            if len(item) != 0:
                data.append(item)
            else:
                continue
        return data


def last_operations(operations_list):
    """выбирает последние 5 словарей если операция EXECUTED, добавляет их в рабочий список"""
    last_5_operations = []
    for operation in operations_list:
        if operation["state"] == "EXECUTED":
            last_5_operations.append(operation)
    return last_5_operations[:5]


def data_to_format(date):
    """преобразует дату перевода в формат ДД.ММ.ГГГГ"""
    date_ob = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
    date_format = date_ob.strftime('%d.%m.%Y')
    date = date_format
    return date


def hidden_card_or_account_number(card_or_account_number):
    """Маскировать номер карты или счета"""
    # Проверяем, содержит ли номер слова "Visa","Mastercard", "Maestro" или "МИР"
    if card_or_account_number is not None:
        name = ''
        number = ''
        for symbol in card_or_account_number:
            if symbol.isalpha() or symbol == ' ':
                name += symbol
            elif symbol.isdigit():
                number += symbol
        if name.find("Visa") or name.find("Mastercard") or name.find("Maestro") or name.find("МИР"):
            card_or_account_number = name + number[:4] + ' ' + number[4:6] + '** **** ' + number[-4:]
        if "Счет" in name:
            card_or_account_number = name + '**' + number[-4:]
        return card_or_account_number
    else:
        return ''


def output_operations(data):
    """выводит информацию по операции в заданном формате"""
    data_sort = sorted(data, key=lambda d: d["date"], reverse=True)  # сортируем список по убыванию
    operations_list = last_operations(data_sort)
    for operation in operations_list:
        date = data_to_format(operation["date"])
        description = operation["description"]
        account_number = hidden_card_or_account_number(operation["to"])
        amount = operation["operationAmount"]["amount"]
        name = operation["operationAmount"]["currency"]["name"]
        try:
            card_number = hidden_card_or_account_number(operation["from"])
        except KeyError:
            card_number = ''

        print(f"{date} {description}")
        print(f"{card_number} -> {account_number}")
        print(f"{amount} {name}\n")
