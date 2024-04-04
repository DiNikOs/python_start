import sqlite3 as sl
import json
import os
from easygui import * 

# Константа с название файла с данными
DATA_JSON = "data_telphones.json"

DATA_DEFAULT_KEY_NAME = "name"
DATA_PHONES_KEY = "phones"
DATA_BIRTHDAY_KEY = "birthday"
DATA_EMAIL_KEY = "email"
YELLOW_COLOR = "\033[33m"
DEFAULT_COLOR = "\033[0m"

VIEW = "Просмотр записей"
SAVE = "Сохранение записи"
IMPORT_DATA = "Импорт данных"
SEARCH = "Поиск записи"
DELETE = "Удаление записи"
UPDATE = "Изменение записи"
EXIT = "Выход"

PHONE = "phone"

BUTTON_OK = "OK"
BUTTON_CANCEL = "CANCEL"
BUTTON_ADD_PHONE = "Add phone"
BUTTON_DEL_PHONE = "Del phone"

COMMAND = {
    "1" : VIEW, 
    "2" : SAVE, 
    "3" : IMPORT_DATA, 
    "4" : SEARCH, 
    "5" : DELETE, 
    "6" : UPDATE,
    'q' : EXIT
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
            print_red("Имя контакта не может быть пустым!", DEFAULT_COLOR)
            return
        if ph.get(name) == None:
            print_red("Контакт не найден!", DEFAULT_COLOR)
            return {}      
        return {name : ph[name]}
    elif (len(data_keys) == 2): # возвращаем выбранный атрибут name
        return {data_keys[1]: ph[data_keys[0]][data_keys[1]]}
    elif (len(data_keys) == 2):
        return {data_keys[1]: ph[data_keys[0]][data_keys[1]][data_keys[2]]}
    
# Изменить атрибут
def update_data(name, data = load_data()):   
    print(f"phonebook={data}")
    if name in data:
        data_get = data.pop(name) # получаем список атрибутов контакта name
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
        print(f"phonebook = {data}")
    else:
        print_red(f"Вводимое значение '{com}' не найдено в контакте!")
        return
    data[name] = data_get
    save_data(data)

# Показ всего списка
# По дефолту подгружаем из функии load_data()
def view_all(data = {}):
    if len(data) == 0:
        data = load_data() 
    if (len(data) == 0):           
        print_red("Список контактов пуст!") 
        return 0
    print(data)
    return data

# Сохранение записи
# По дефолту подгружаем из функии load_data()
def save_recording_data(data = load_data()):
    name = input("Введите имя контакта: ")
    if name in data.keys():
        print_red("Контакт с таким именем уже есть в списке! Выбирете другое название контакта.")
        return
    phones = input("Введите номер(а) телефона(ов) через пробел если их несколько: ")
    birthday = input("Введите дату рождения: ")
    email = input("Введите адрес электронной почты: ")              
    data[name] = {
        DATA_PHONES_KEY : phones.split(), 
        DATA_BIRTHDAY_KEY : birthday, 
        DATA_EMAIL_KEY : email
        }
    print(f"data_save={data}")    
    save_data(data)

# Удаление записи
# data - список из которого будем удалять по дефолту подгружаем из функии load_data()
# key_del - ключ по  которому будем удалять
def del_data(key_del, data = load_data()):
    data.pop(key_del)
    save_data(data)

def program_cycle():
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
        # data = load_data() 
        if (com == "1"): # просмотр
            print_blue("Просмотр записей")   
            if view_all() == 0:  
                continue            
        elif (com == "2"): # сохранение
            print_blue("Сохранение записи")
            save_recording_data()
        elif (com == "3"): # импорт
            print_blue("Импорт данных")     
            import_data()
        elif (com == "4"): # поиск
            print_blue("Поиск записи")
            name = input("Введите имя контакта для поиска: ")
            data = load_data([name])
            if len(data) == 1:  
                print(data)
        elif (com == "5"): # удаление
            print_blue("Удаление записи")
            name = input("Введите имя контакта для удаления: ")       
            del_data(name)
        elif (com == "6"): # изменение данных  
            print_blue("Изменение записи")      
            print(f"Контакты: {str(', '.join(data.keys()))}")
            name = input(f"Введите имя контакта который хотите поменять: ")     
            update_data(name) 
  
# Преобразование в строке через запятую если список
def convert_val_to_str(val):
    str_val = ''
    if isinstance(val, list):
        for i, l in enumerate(val):
            if i < len(val) - 1:
                str_val += l + ','
            else:
                str_val += l
    else:
        str_val = val 
    return str_val

# Преобразование словаря в строки с переносом и табуляцией
def convert_to_str(data = load_data()):
    str = ''
    for k, v in data.items():
        str_atr =''
        for atr, val in dict(v).items():              
            str_atr += f"\n \t {atr}: {convert_val_to_str(val)}"
            # str_atr += f"\n \t {atr}: {str_val}"
        str += f"{DATA_DEFAULT_KEY_NAME}: {k}{str_atr}\n" 
    return str

def get_field_names(phones, fieldNames):
    fn = [fieldNames[0]]
    non_stop = True
    count = 0
    while non_stop:   
        if phones == 1:
            fn.append(PHONE)
            non_stop = False
            continue
        else:
            if count == 0:
                fn.append(PHONE)
                count+=1
            else:
                fn.append(f"{PHONE}{count}")
            count+=1
    fn.extend(fieldNames[-2:])

# Проверка на валидность полей (не пустые поля) 
# valid_checks - для каждого поля свои проверки на валидность
def check_and_get_values(msg, title, field_names, field_values, valid_checks = []):
    while 1:
        errmsg = msg            
        for i, field_name in enumerate(field_names):
            if field_values[i].strip() == "":
                errmsg += "Поле '{}' не должно быть пустым!\n".format(field_name)
        if errmsg == msg:
            print("errmsg == msg + ")
            return field_values # no problems found
        field_values = multenterbox(errmsg, title, field_names, field_values)
        if field_values is None:           
            print("Cancel")
            return []  

def save_data_val(data, field_values):
    phones = []
    # убираем пробелы в номерах телефона если есть
    for phone in field_values[1].split(','):
        phones.append(phone.strip()) 

    data[field_values[0]] = {
        DATA_PHONES_KEY : phones, 
        DATA_BIRTHDAY_KEY : field_values[2], 
        DATA_EMAIL_KEY : field_values[3]
        }
    print(f"data_save={data}")    
    save_data(data)
  
def save_chois(data = load_data()):
    msg = "Введите информацию для нового контакта \n (если требуется несколько телефонов - ввод через запятую)\n"
    title = "Сохранение записи"
    field_names = [DATA_DEFAULT_KEY_NAME, DATA_PHONES_KEY, DATA_BIRTHDAY_KEY, DATA_EMAIL_KEY]   
    field_values = multenterbox(msg, title, field_names)
    if field_values is None:
        print("Cancel")
        return
    # Проверка на пустые поля
    field_values = check_and_get_values(msg, title, field_names, field_values)

    if len(field_values) == 0:           
        print("Cancel")
        return
    save_data_val(data, field_values)    

def find_chois():
    msg = "Введите название контакта\n "
    title = "Поиск записи"
    field_names = [DATA_DEFAULT_KEY_NAME]   
    field_values = multenterbox(msg, title, field_names)
    if field_values is None:
        print("Cancel")
        return

    while 1:  
        # Проверка на пустые поля
        field_values = check_and_get_values(msg, title, field_names, field_values)
        if len(field_values) == 0:           
            print("Cancel")
            return   
        data = load_data([field_values[0]])   
        print(f"find_cont={data}")
        errmsg = ""   
        # проверка наличия записи контакта       
        if len(data) == 0:
            errmsg += "Контакт '{}' не найден! Введите другое название\n".format(field_values[0])        
            field_values = multenterbox(errmsg, title, field_names, field_values)
        else:          
            field_values = multenterbox(convert_to_str(data), title, field_names, field_values) 
        if field_values is None:           
            print("Cancel")
            return  
        
def get_field_values(warn, title, field_names, names, com):
    if len(names) == 0:
        msg = f"Нет контактов для {com}! \n"
    else:
        msg = f"Выберите контакт для {com} \n{warn}"
    
    for name in names:
        msg += name + "\n"   
    return multenterbox(msg, title, field_names)

def del_chois(): 
    non_stop = True
    warn = ""      
    while non_stop:      
        title = "Удаление контакта"
        field_names = [DATA_DEFAULT_KEY_NAME]
        data = load_data()
        names = list(data.keys())
             
        field_values = get_field_values(warn, title, field_names, names, "удаления")
        if field_values is None:
            print("Cancel")
            return        
        # Проверка на пустые поля
        field_values = check_and_get_values(warn, title, field_names, field_values)   
        print(f"field_values={field_values}")     
        if field_values is None or len(field_values) == 0:
            print("Cancel")
            return   
        name = field_values[0]
        if name not in names:
            warn = f"Контакт '{name}' отсутствует!\n"
            continue
        else:
            warn = ""
        data.pop(name)
        save_data(data)    

def update_chois(data = load_data()): 
    non_stop=True
    warn = ""
    while non_stop:
        title = "Изменение контакта"
        field_names = [DATA_DEFAULT_KEY_NAME]
        data = load_data()
        names = list(data.keys())
        field_values = get_field_values(warn, title, field_names, names, "изменения")
        if field_values is None:
            print("Cancel")
            return        
        # Проверка на пустые поля
        field_values = check_and_get_values(warn, title, field_names, field_values)   
        print(f"field_values={field_values}")     
        if field_values is None or len(field_values) == 0:
            print("Cancel")
            return   
        name = field_values[0]
        if name not in names:
            warn = f"Контакт '{name}' отсутствует!\n"
            continue
        else:
            warn = ""
        
        data_name = data[name]
        print(f"type={type(data_name)}")
        print(f"data_name={data_name}")
        msg = "Введите информацию которую хотите изменить \n (если требуется несколько телефонов - ввод через запятую)\n"
        title = "Изменение записи"
        field_names = [DATA_DEFAULT_KEY_NAME]  
        field_values = [name] 
        for k,v in data_name.items():
            field_names.append(k)                     
            field_values.append(convert_val_to_str(v))
        field_values = multenterbox(msg, title, field_names, field_values)
        print(f"field_values={field_values}")
        if field_values is None:
            print("Cancel")
            return
        # Проверка на пустые поля
        field_values = check_and_get_values(msg, title, field_names, field_values)   
        print(f"field_values={field_values}")
        if len(field_values) == 0:           
            print("Cancel")
            return 
        data.pop(name)
        save_data_val(data, field_values)
    # return
    
def view_cycle():
    non_stop = True
    while non_stop:    
        com = list(COMMAND.values())
        choice = choicebox("Выберите запрос", "Главная форма", com)
        print(f"choice={choice}")
        if choice == COMMAND.get("q") or choice == 'x' or choice == None:
            print("Exit")       
            return
        elif choice == COMMAND.get("1"): # отображение всего списка
            print("Просмотр записей")             
            data = view_all()  
            msgbox(convert_to_str(data), "Просмотр записей")
        elif choice == COMMAND.get("2"): # сохранение
            print("Сохранение записи")
            save_chois()
            continue
        elif choice == COMMAND.get("3"): # импорт
            print("Импорт данных")     
            pass
        elif choice == COMMAND.get("4"): # поиск
            print("Поиск записи")            
            find_chois()
        elif choice == COMMAND.get("5"): # удаление
            print("Удаление записи") 
            del_chois()             
        elif choice == COMMAND.get("6"): # изменение данных  
            print("Изменение записи")          
            update_chois()
    
view_cycle()
