import sqlite3 as sl
import json
import os
from easygui import *

# Константа с название файла с данными
DATA_JSON = "data_telphones.json"

DATA_DEFAULT_KEY = "name"
DATA_PHONES_KEY = "phones"
DATA_BIRTHDAY_KEY = "birthday"
DATA_EMAILS_KEY = "emails"

COMMAND = {
    "1" : "просмотр", 
    "2" : "сохранение", 
    "3" : "импорт", 
    "4" : "поиск", 
    "5" : "удаление", 
    "6" : "изменение данных",
    'q' : "выход"
}

def print_color(color_before, text, color_after = ''):
    print(color_before)
    print(text)
    if color_after != '':
        print(color_after)

def print_green(text, color_after = ''):
    print_color("\033[32m", text, color_after)

def print_red(text, color_after = ''):
    print_color("\033[31m", text, color_after)

def print_yellow(text, color_after = ''):
    print_color("\033[33m", text, color_after)

def print_blue(text, color_after = ''):
    print_color("\033[34m", text, color_after)

# Сохраняем данные (сериализации JSON Python)
def save_data(phonebook) :
    with open(DATA_JSON, "w", encoding='utf-8') as write_file:
        json.dump(phonebook, write_file, ensure_ascii=False, indent=4)

# Загружаем данные (десериализации JSON Python)
# на вход подаём массив из 
# key_name - имя контакта, 
# key_list - название типа данных из контакта которое хотим получить, 
# index from list - индекс из списка с данными 
def load_data(data_keys=[]) :
    print(f"len={len(data_keys)}")
    with open(DATA_JSON, "r", encoding='utf-8') as read_file:
        file_content = read_file.read()
        # Проверяем, пустой ли файл
        if not file_content.strip():
            return {}      
        ph = json.loads(file_content)
    print(f"ph={ph}")
    if len(data_keys) == 0: # возвращаем весь список
        return ph
    if (len(data_keys) == 1): # возвращаем если что нашли по name 
        # return ph[data_keys[0].lower()]        
        name = str(data_keys[0]).strip()
        print(f"выборка по контакту={name}")
        if len(name) == 0:
            print_red("Имя контакта не может быть пустым!")
            return
        if ph.get(name) == None:            
            return {}      
        return {name : ph[name]}
    elif (len(data_keys) == 2): # возвращаем выбранный атрибут name
        return {data_keys[1]: ph[data_keys[0]][data_keys[1]]}
    elif (len(data_keys) == 2):
        return {data_keys[1]: ph[data_keys[0]][data_keys[1]][data_keys[2]]}

# Словарь по дефолту
phonebook = {
    "name": {   "phones": [], 
                "birthday": "", 
                "emails": [] } 
             }

# Если файла нет то создаём и сохраняем
if not os.path.exists(DATA_JSON):
    save_data(phonebook)

# Загружаем данные из файла
# data = load_data()

def isDefaultData(data):
    # print(f"data={data}")
    if (len(data) == 0):
        return True
    elif (len(data) == 1):     
        for d in data.values():
            if (isinstance(d, list) or isinstance(d, str)) and len(d) > 0:
                return data[DATA_DEFAULT_KEY] == DATA_DEFAULT_KEY and False
            if isinstance(d, int) and d != None:
                return data[DATA_DEFAULT_KEY] == DATA_DEFAULT_KEY and False
    return True

non_stop = True
while non_stop:
    print_green(f"Комманды для работы: {COMMAND}", "\033[33m") # текст зелёный, потом жёлтый 
    com = input("Введите комманду для работы: ")
    if not com in COMMAND.keys(): 
        print_red("Введена не верная команда! Повторите ввод")            
        continue
    if (com == 'q'): # выход
        non_stop = False
        print_red("Выполнен выход из программы!", "\033[0m")      
        continue
    data = load_data()
    print(f"data={data}")
    if (com == "1"): # просмотр
        print_blue("Просмотр записей")
        # if (isDefaultData(data)):           
        if (len(data) == 0):           
            print_red("Список контактов пуст!") 
            continue
        print(data)
    elif (com == "2"): # сохранение
        print_blue("Сохранение записи")
        name = input("Введите имя контакта: ")
        phones = input("Введите номер(а) телефона(ов) через пробел если их несколько: ")
        birthday = input("Введите дату рождения: ")
        emails = input("Введите адрес(а) электронной почты через пробел если их несколько: ")              
        data[name] = {
            DATA_PHONES_KEY : phones.split(), 
            DATA_BIRTHDAY_KEY : birthday, 
            DATA_EMAILS_KEY : emails.split()
            }
        print(f"data_save={data}")
        save_data(data)
    elif (com == "3"): # импорт
        print_blue("Импорт данных")
    elif (com == "4"): # поиск
        print_blue("Поиск записи")
        name = input("Введите имя контакта для поиска: ")
        data = load_data([name])
        if len(data) == 0:            
            print_red("Контакта не найден!")
        else:    
            print(data)
    elif (com == "5"): # удаление
        print_blue("Удаление записи")
        name = input("Введите имя контакта для удаления: ")       
        data.pop(name)
        save_data(data)
    elif (com == "6"): # изменение данных  
        print_blue("Изменение записи")
        name = input("Введите имя контакта: ")
        data = load_data([name])
        if len(data) == 0:            
            print_red("Контакта не найден!")
            continue                
        print_green(f"Выбирите что хотите изменить: {data.values()}")
