import sqlite3 as sl
import json
import os
from easygui import * 

# Константа с название файла с данными
DATA_JSON = "data_telphones.json"

DATA_DB = "phones.db"

# # создаем подключение к БД
conn = sl.connect(DATA_DB)

# # создаем курсор - объект для выполнения SQL
cur = conn.cursor()

DATA_DEFAULT_KEY_NAME = "name"
DATA_PHONES_KEY = "phones"
DATA_BIRTHDAY_KEY = "birthday"
DATA_EMAIL_KEY = "email"
DEFAULT_COLOR = "\033[0m"

VIEW = "Просмотр записей"
SAVE = "Сохранение записи"
IMPORT_DATA = "Импорт данных"
EXPORT_DATA = "Экспорт данных"
SEARCH = "Поиск записи"
DELETE = "Удаление записи"
UPDATE = "Изменение записи"
EXIT = "Выход"

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

# создали SQL запрос и выполнили
cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts
            (          
            name TEXT PRIMARY KEY,
            birthday TEXT,
            email TEXT
            );
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS phones
            (
            id INTEGER PRIMARY KEY,          
            name TEXT,
            phone TEXT,
            FOREIGN KEY (name)
            REFERENCES contacts (name)
            );
            """)

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

def set_data(data = {}, contact = ()):
    name = contact[0]      
    print(f"name = contact[0]={name}, contact={contact}")      
    cur.execute("SELECT * FROM phones WHERE name = ?", (name,))
    sql_phones = cur.fetchall()
    print(f"sql_phones={sql_phones}")
    phones = []
    for phone in sql_phones:
        phones.append(phone[1])      
    data.update(get_date(name, phones, contact[1], contact[2])) 
    return

def del_sql_contact(name):
    cur.execute('DELETE FROM phones WHERE name = ?', (name,))
    cur.execute('DELETE FROM contacts WHERE name = ?', (name,))
    conn.commit()    

def upt_contact(data = {}, phones_old = []): 
    for k, v in data.items():  
        phones = v.get(DATA_PHONES_KEY);  
        for i, phone in enumerate(phones_old):    
            set_phone = phones[i]
            print(f"set_phone={set_phone}, name={k}, phone={phone}")
            cur.execute("UPDATE phones SET phone = ? WHERE name = ? and phone = ?", (set_phone, k, phone))    
        cur.execute("UPDATE contacts SET birthday = ?, email = ?  WHERE name = ?", (v.get(DATA_BIRTHDAY_KEY), v.get(DATA_EMAIL_KEY), k))
    conn.commit()    
    return

def select_contacts(name = ""): 
    data = {}
    contacts = []
    if name == "":
        cur.execute("SELECT * FROM contacts;")
        contacts += cur.fetchall()
    else:         
        cur.execute("SELECT name, birthday, email FROM contacts WHERE name = ?", (name,))      
        contacts = cur.fetchall()
  
    phones = []  

    print(f"contacts={contacts}")  
  
    if len(contacts) == 0:
        return {}
    else:        
        for contact in contacts:
            set_data(data, contact)             
    return data

def add_contact(contact = {}):
    print(f"data_save={contact}") 
    for k, v in contact.items():   
        cur.execute(f"INSERT INTO contacts VALUES ('{k}','{v.get(DATA_BIRTHDAY_KEY)}','{v.get(DATA_EMAIL_KEY)}');")
        phones = v.get(DATA_PHONES_KEY);
        for phone in phones:
            cur.execute(f"INSERT INTO phones VALUES ('{k}','{phone}');")
        conn.commit()  
       
# Вщзвращаем значения для контакта name
def select_by_name(name):
    data_name = {}
    cur.execute(f"SELECT * FROM contacts WHERE name = '{name}';")
    data_name = cur.fetchall()[0]
    cur.execute(f"SELECT * FROM phones WHERE name = '{name}';")
    sql_phones = cur.fetchall()
    conn.commit()
    print(f"data_name={data_name}")
    phones = []
    for phone in sql_phones:
        phones.append(phone[1])  
    return {
            DATA_PHONES_KEY : phones, 
            DATA_BIRTHDAY_KEY : data_name[1], 
            DATA_EMAIL_KEY :  data_name[2]
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
    
# Преобразование словаря в строки с переносом и табуляцией
def convert_to_str(data):
    str = ''
    print(f"data={data}")
    for k, v in data.items():
        str_atr =''
        for atr, val in dict(v).items():              
            str_atr += f"\n \t {atr}: {convert_val_to_str(val)}"
            # str_atr += f"\n \t {atr}: {str_val}"
        str += f"{DATA_DEFAULT_KEY_NAME}: {k}{str_atr}\n" 
    return str

# Проверка на валидность полей (не пустые поля) 
# valid_checks - для каждого поля свои проверки на валидность
def check_and_get_values(msg, title, field_names, field_values, valid_checks = {}):
    while 1:  
        errmsg = msg  
        # if len(field_names) == len(field_values) and valid_checks.get(DATA_DEFAULT_KEY_NAME) is not None and field_values[0] in valid_checks.get(DATA_DEFAULT_KEY_NAME):
        #     errmsg += "Введите другое имя контакта!\n"
        # else:
        for i, field_name in enumerate(field_names): 
            if valid_checks.get(field_name) is not None and field_values[i] in valid_checks.get(field_name):
                errmsg += "Введите другое имя контакта!\n"    
            if field_values[i].strip() == "":
                errmsg += "Поле '{}' не должно быть пустым!\n".format(field_name)            
        if errmsg == msg:
            print("errmsg == msg + ")
            return field_values # no problems found
        field_values = multenterbox(errmsg, title, field_names, field_values)
        if field_values is None:           
            print("Cancel")
            return []         

def get_date(name, phones, birthday, email): 
    print(f"name = {name}, phones = {phones}, birthday = {birthday}, email = {email}")    
    return {name : {
            DATA_PHONES_KEY : phones, 
            DATA_BIRTHDAY_KEY : birthday, 
            DATA_EMAIL_KEY :  email
            }
        }

def save_sql_chois():
    msg = "Введите информацию для нового контакта: \n (если требуется несколько телефонов - ввод через запятую)\n"
    title = "Сохранение записи"
    field_names = [DATA_DEFAULT_KEY_NAME, DATA_PHONES_KEY, DATA_BIRTHDAY_KEY, DATA_EMAIL_KEY]   
    field_values = multenterbox(msg, title, field_names)
    if field_values is None:
        print("Cancel")
        return
    # Проверка на пустые поля
    data_contacts = select_contacts()      
    field_values = check_and_get_values(msg, title, field_names, field_values, {DATA_DEFAULT_KEY_NAME : data_contacts})
    
    if len(field_values) == 0:           
        print("Cancel")
        return
    phones = []
    # убираем пробелы в номерах телефона если есть
    for phone in field_values[1].split(','):
        phones.append(phone.strip())    
    data = get_date(field_values[0], phones, field_values[2], field_values[3])        
    add_contact(data)

def import_sql_chois():
    msg = "Выберете файлы для импорта в формате json"
    title = "Импорт данных"
    paht_json = fileopenbox(msg=msg, title = title, default='*', filetypes=[["*.json", "JSON file"]], multiple=False)
    if paht_json is None:
        print("Cancel")
        return    
    
    data_json = load_data_json(paht_json) 
    all_data = select_contacts().keys()
    print(f"data_json={data_json}, all_data={all_data}")
    for k,v in data_json.items():
        if k in all_data:
            continue
        add_contact({k:v})

def export_sql_chois():
    data = select_contacts()
    msg = "Назовите файл для экспорта в формате json"
    title = "Экспорт данных"
    paht_json = filesavebox(msg=msg, title = title, default='phone_data.json', filetypes=[["*.json", "JSON file"]])
    if paht_json is None:
        print("Cancel")
        return        
    save_data(data, paht_json)

def find_sql_chois():
    msg = "Введите название контакта:\n "
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
        print(f"field_values[0]={field_values[0]}")
        data = select_contacts(field_values[0])   
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
        msg = f"Контакт для {com} \n{warn}"
    
    for name in names:
        msg += name + "\n"   
    return multenterbox(msg, title, field_names)

def del_sql_chois(): 
    non_stop = True
    warn = ""      
    while non_stop:      
        title = "Удаление контакта"
        field_names = [DATA_DEFAULT_KEY_NAME]
        data = select_contacts()
        names = list(data.keys())             
        field_values = get_field_values(warn, title, field_names, names, "удаления:")
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
        del_sql_contact(name)

def update_sql_chois(): 
    non_stop=True
    warn = ""
    while non_stop:
        title = "Изменение контакта"
        field_names = [DATA_DEFAULT_KEY_NAME]
        data = select_contacts()
        names = list(data.keys())
        field_values = get_field_values(warn, title, field_names, names, "изменения:")

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
        
        data_name = select_by_name(name)
        print(f"type={type(data_name)}")
        print(f"data_name={data_name}")
        msg = "Введите информацию которую хотите изменить \n (если требуется несколько телефонов - ввод через запятую)\n"
        title = "Изменение записи"
        field_names = [DATA_DEFAULT_KEY_NAME]  
        field_values = [name] 
        phones_old = []
        for k,v in data_name.items():
            if isinstance(v, list):
                for phone in v:
                    phones_old.append(phone)
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
        
        phones = []
        for phone in field_values[1].split(','):
            phones.append(phone.strip()) 

        data = get_date(field_values[0], phones, field_values[2], field_values[3])
        print(f"phones_old={phones_old}")
        upt_contact(data, phones_old)
    
def view_cycle():
    non_stop = True
    while non_stop:    
        com = list(COMMAND.values())
        choice = choicebox("Выберите действие:", "Главная форма", com)
        print(f"choice={choice}")
        if choice == COMMAND.get("q") or choice == 'x' or choice == None:
            print(choice)       
            return
        elif choice == COMMAND.get("1"): # отображение всего списка
            print(choice)             
            # data = view_all()  
            data = select_contacts()    
            msgbox(convert_to_str(data), choice)
        elif choice == COMMAND.get("2"): # сохранение
            print(choice)
            save_sql_chois()          
        elif choice == COMMAND.get("3"): # импорт
            print(choice)     
            import_sql_chois()
        elif choice == COMMAND.get("4"): # экспорт
            print(choice)            
            export_sql_chois()
        elif choice == COMMAND.get("5"): # поиск
            print(choice) 
            find_sql_chois()     
        elif choice == COMMAND.get("6"): # удаление  
            print(choice)          
            del_sql_chois()    
        elif choice == COMMAND.get("7"): # изменение данных  
            print(choice)          
            update_sql_chois()
    
view_cycle()
conn.close()
