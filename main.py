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
YELLOW_COLOR = "\033[33m"
DEFAULT_COLOR = "\033[0m"

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
    print_color(YELLOW_COLOR, text, color_after)

def print_blue(text, color_after = ''):
    print_color("\033[34m", text, color_after)

def setAtributes(name_atr, atributes):
    return

# Сохраняем данные (сериализации JSON Python)
def save_data(phonebook) :
    with open(DATA_JSON, "w", encoding='utf-8') as write_file:
        json.dump(phonebook, write_file, ensure_ascii=False, indent=4)

def import_data(phonebook):
    choise = input("Выбирите откуда импортировать данные (1 - из файла json, 2 - из строки: ")
    data = {}
    print(f"choise={choise}")
    if choise == "1":
        file = input("Укажите путь для импорта: ")
        print(f"file={file}")
        data = load_data_json(file)
    elif choise == "2":
        data = input("Введите контакты строчкой: ")
    phonebook.update(data)
    save_data(phonebook)

# Изменить атрибут
def update_data(name):
    phonebook = load_data()
    print(f"phonebook={phonebook}")
    if name in phonebook:
        data_get = phonebook.pop(name) # получаем список атрибутов контакта name
    else:
        print_red(f"Контакт '{name}' не найден!")
        return
    if data_get == None or len(data_get) == 0:            
        print_red("Контакт не найден!")
        return
    print(f"data_get={data_get}")     
    d = [name]
    d.extend(data_get.keys()) 
    print(YELLOW_COLOR) # изменяем в жёлтый
    com = input(f"Выбирите что хотите изменить '{', '.join(d)}' :").strip()
    if com == '':
        print_red("Вводимое значение должно быть не пустым!")
        return
    if com == str(name):
        name_new = input(f"Введите новое название для контакта: ").strip()
        if name_new == '':
            print_red("Контакт не может быть пуст!")
            return
        name = name_new
    elif com in d:
        d = data_get.get(com) # получаем значения атрибута com по ключу
        com_new = []
        print(*d)
        if isinstance(d, list):
            non_stop = True
            while non_stop: 
                an = input(f"Хотите добавить запись - введите 'w', хотите изменить - введите 'u', закончить изменение - 'q': ").strip()  
                if an == "u": # изменение записи           
                    atr = input(f"Выбирите какое значение изменять '{', '.join(d)}': ").strip()
                    if atr in d:
                        d.pop(d.index(atr))       
                        atr_new = input(f"Введите новое значение для {com} вместо {atr}: ").strip()
                        d.append(atr_new) 
                    else:
                        print_red(f"Значение '{atr}' отсутствует", YELLOW_COLOR) # сначала красный потом жёлтый
                    # answ = input(f"Закончить изменения значений '{', '.join(d)}' -'q' иначе Enter: ").strip()
                    # if answ == 'q':
                    #     non_stop = False
                elif an == 'w': # добавить значение
                    atr_new = input(f"Введите новое значение для {com}: ").strip()
                    d.append(atr_new) 
                elif an == 'q': # завершить изменение
                    non_stop = False
                else:
                    print_red(f"Повторите выбор для '{com}'!")
                print(*d)
            com_new = d
        else:
            com_new = input(f"Введите новое значение для {com}: ").strip()
        data_get[com] = com_new   
        setAtributes(com, data_get)     
        print(f"phonebook = {phonebook}")
    else:
        print_red(f"Вводимое значение '{com}' не найдено в контакте!")
        return
    phonebook[name] = data_get
    save_data(phonebook)
    
def load_data_json(file = DATA_JSON):
    with open(file, "r", encoding='utf-8') as read_file:
        file_content = read_file.read()
        # Проверяем, пустой ли файл
        if not file_content.strip():
            return {}      
    return json.loads(file_content)

# Загружаем данные (десериализации JSON Python)
# на вход подаём массив из 
# key_name - имя контакта, 
# key_list - название типа данных из контакта которое хотим получить, 
# index from list - индекс из списка с данными 
def load_data(data_keys=[]) :
    ph = load_data_json()  
    if len(data_keys) == 0: # возвращаем весь список
        return ph
    if (len(data_keys) == 1): # возвращаем если что нашли по name      
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

non_stop = True
while non_stop:
    print_green(f"Комманды для работы: {COMMAND}", YELLOW_COLOR) # текст зелёный, потом жёлтый 
    com = input("Введите комманду для работы: ")
    if not com in COMMAND.keys(): 
        print_red("Введена не верная команда! Повторите ввод")            
        continue
    if (com == 'q'): # выход
        non_stop = False
        print_red("Выполнен выход из программы!", DEFAULT_COLOR)      
        continue
    data = load_data() 
    if (com == "1"): # просмотр
        print_blue("Просмотр записей")             
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
        import_data(data)
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
        print(f"Контакты: {str(', '.join(data.keys()))}")
        name = input(f"Введите имя контакта который хотите поменять: ")     
        update_data(name) 
 

