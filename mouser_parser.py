# -*- coding: utf-8 -*-
"""
Mouser Parser

- Поиск по Part-Number через Mouser API
- Вывод основных полей: категория, наличие, срок поставки, цена, описание
- Работа в цикле: ввод Part-Number пока пользователь не введёт 'exit'
- Простая таблица вывода через prettytable

"""
import requests
import prettytable as pt

API_KEY = "da536944-b444-476c-876c-aaffc40aad64"

def get_part_info(part_number):
    url = "https://api.mouser.com/api/v1/search/partnumber"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    params = {"apiKey": API_KEY}
    payload = {
        "SearchByPartRequest": {
            "mouserPartNumber": part_number
        }
    }
    
    r = requests.post(url, headers=headers, params=params, json=payload)
    data = r.json()

    if data.get("Errors"):
        print("Ошибка API:", data["Errors"])
        return None

    try:
        part = data["SearchResults"]["Parts"][0]
        return {
            "Product Category": part.get("Category", "N/A"),
            "Stock": part.get("Availability", "N/A"),
            "Factory Lead Time": part.get("FactoryLeadTime", "N/A"),
            "Unit Price (1)": part.get("PriceBreaks", [{}])[0].get("Price", "N/A"),
            "Description": part.get("Description", "N/A")
        }
    except (IndexError, KeyError):
        print("Деталь не найдена")
        return None

def print_table(info):
    table = pt.PrettyTable()
    table.field_names = ["Параметр", "Значение"]
    for key, value in info.items():
        table.add_row([key, value])
    print(table)

if __name__ == "__main__":
    while True:
        part_number = input("Введите Part-Number (или 'exit' для выхода): ").strip()
        if part_number.lower() == "exit":
            print("Выход из программы.")
            break
        if not part_number:
            print("Вы ничего не ввели. Попробуйте снова.")
            continue
        
        info = get_part_info(part_number)
        if info:
            print_table(info)
