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
EXPORT_DATA = "Экспорт данных"
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
    "4" : EXPORT_DATA, 
    "5" : SEARCH, 
    "6" : DELETE, 
    "7" : UPDATE,
    'q' : EXIT
}

def print_color(color_before, text, color_after = ''):
    print(color_before)
    print(text)
    if color_after != '':
        print(color_after)

def print_red(text, color_after = ''):
    print_color("\033[31m", text, color_after)

# Сохраняем данные (сериализации JSON Python)
def save_data(phonebook, path = DATA_JSON) :
    with open(path, "w", encoding='utf-8') as write_file:
        json.dump(phonebook, write_file, ensure_ascii=False, indent=4)
    
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

def import_chois(data = load_data()):
    msg = "Выберете файлы для импорта в формате json"
    title = "Импорт данных"
    paht_json = fileopenbox(msg=msg, title = title, default='*', filetypes=[["*.json", "JSON file"]], multiple=False)
    if paht_json is None:
        print("Cancel")
        return        
    
    data_json = load_data_json(paht_json) 
    data.update(data_json) 
    save_data(data)

def export_chois(data = load_data()):
    msg = "Назовите файл для экспорта в формате json"
    title = "Экспорт данных"
    paht_json = filesavebox(msg=msg, title = title, default='phone_data.json', filetypes=[["*.json", "JSON file"]])
    if paht_json is None:
        print("Cancel")
        return        
    save_data(data, paht_json)

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
        choice = choicebox("Выберите действие", "Главная форма", com)
        print(f"choice={choice}")
        if choice == COMMAND.get("q") or choice == 'x' or choice == None:
            print(choice)       
            return
        elif choice == COMMAND.get("1"): # отображение всего списка
            print(choice)             
            data = view_all()  
            msgbox(convert_to_str(data), choice)
        elif choice == COMMAND.get("2"): # сохранение
            print(choice)
            save_chois()
            continue
        elif choice == COMMAND.get("3"): # импорт
            print(choice)     
            import_chois()
        elif choice == COMMAND.get("4"): # экспорт
            print(choice)            
            export_chois()
        elif choice == COMMAND.get("5"): # поиск
            print(choice) 
            find_chois()        
        elif choice == COMMAND.get("6"): # удаление  
            print(choice)          
            del_chois()     
        elif choice == COMMAND.get("7"): # изменение данных  
            print(choice)          
            update_chois()
    
view_cycle()
