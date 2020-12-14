# ver 1.0.1

import os
import os.path
import move_cur_dir
import sys
import configparser
import psycopg2 
import json
from datetime import datetime
from psycopg2 import sql
from os.path import abspath
import nyktools as nyk


def list_to_str_join(s, ls):
    return str(s).join(str(e) for e in ls)


def show_menu(): # Меню действий
    command_list = {0:'Выход', 1:'Сохранить данные БД в json', 2:'Проверка наличия обновлений структуры БД', 3:'Апдейт структуры БД', 4:'Полная очистка и обновление БД', 5:'Восстановление данных из json в БД'}
    move_cur_dir.print_empty_lines(2)
    print('Введите номер дальнейших действий. Выберите команду:')
    for i in command_list.keys():
        print(i, '<---', command_list[i])


def get_base_version(config):
    result = '0.0.0'
    with psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (config.get("DB", "dbname"), config.get("DB", "user"), config.get("DB", "host"), config.get("DB", "password"))) as db:
        with db.cursor() as curs:
            print('Работа с БД:', config.get("DB", "host"), '----->', config.get("DB", "dbname"))
            curs.execute("SELECT base_ver FROM versions")
            row = curs.fetchone()
            if len(row)==1 and row[0] != None:
                result = row[0]
    print('Версия базы данных:', result)
    return result


def get_list_files_from_dir(path, root_name = '', ext = ''):
    if path != '': 
        if os.path.exists(path) and os.path.isdir(path):
            files = os.listdir(path)
            if root_name != '':
                files = list(filter(lambda x: x.find(root_name) >= 0, files))
            if ext != '' and len(files)>0:
                files = list(filter(lambda x: x.find('.' + ext) >= 0, files))
    return files


def get_list_files_dir(caption, root_name = '', ext = '', pat = ''):    
    files = []
    path = move_cur_dir.get_directory(caption, pat)
    if path[0]: 
        files = get_list_files_from_dir(path[1], root_name, ext)
        if os.path.exists(path[1]) and os.path.isdir(path[1]):
            files.append(path[1])
    return files


def get_list_updates(pat = ''):
    result = None
    path = pat
    files = get_list_files_dir('Выберите директорию с файлами апдейтов базы данных:', root_name = 'PhotoCProDB_up_', pat = path)
    if len(files) > 0:
        path = files[-1] 
        del files[-1]
    if len(files) > 0:
        verses = set()
        print(files)
        for sst in files:
            ffl = sst.split('.')
            verses.add(tuple(map(lambda x: int(x), ffl[0].split('_')[2:5:1])))
        if len(verses) > 0:
            result = [verses, path]
    return result


def get_from_file(file_name):
    txt = ''
    with open(file_name, "r") as r_file:
        txt = r_file.read()
    return txt


def get_file_name_up_by_vers(vers, path):
    result = ''
    files = get_list_files_from_dir(path, root_name = 'PhotoCProDB_up_' + '_'.join(str(e) for e in vers))
    if len(files) >= 1:
        result = os.path.join(path, files[0])
    return result


def run_up_database_to_vers(config, vers, pat = ''):
    result = False
    ver_str = list_to_str_join('.', vers)
    path = pat
    if path == '':
        path = move_cur_dir.get_directory('Выберите директорию с файлами апдейтов базы данных:', pat)
        if path[0]:
            path = path[1]
        else:
            print('Отмена выполнения обновления v: ' + ver_str)
            return result
    with psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (config.get("DB", "dbname"), config.get("DB", "user"), config.get("DB", "host"), config.get("DB", "password"))) as db:
        with db.cursor() as curs:
            print('Работа с БД:', config.get("DB", "host"), '----->', config.get("DB", "dbname"))
            sql_script = get_from_file(get_file_name_up_by_vers(vers, path))
            if sql_script != '':
                print('Выполняем обновление структуры БД v: ' + ver_str)
                print(sql_script)
                try:
                    curs.execute(sql_script)
                    db.commit()
                    print('Коммит обновления' + ver_str + 'успешный!')
                    result = True
                except psycopg2.DatabaseError as e:
                    print(f'Error {e}')
                    db.rollback()
                    result = False
    return result


def need_update_base(config, vv = None, do_update = False, pat = ''):
    result = {'result':False}
    if do_update:
        result['no_up_do'] = True
    path = pat
    vers_base = tuple(map(lambda x: int(x), get_base_version(config).split('.')[0:3:1]))
    if vv == None:
        verses = get_list_updates(path)
        if verses != None:
            path = verses[1]
            verses = verses[0]
    else:
        verses = vv # заданные версии, без поиска файлов апдейта
    if verses != None and len(verses) > 0:
        result = {'result':False, 'path':path, 'allvers':verses, 'ver_b':vers_base}
        for sst in verses:
            if sst > vers_base:
                if do_update:
                    # вызов функции выполнения обновления.
                    result['no_up_do'] = False
                    result['result'] = run_up_database_to_vers(config, sst, pat = path)
                    if result['result']:
                        result['ver_b'] = sst
                    else:
                        result['no_up_do'] = True
                        break
                else:
                    result['result'] = True
                    result['first_up_ver'] = sst
                    break
    return result


def if_type_then_to_str(item, sample_type):    
    if type(item) == type(sample_type):
        result = str(item)
    else:
        result = item
    return result 


def change_type_to_str_in_list(dat, typ):    
    res = list(dat)
    for ii in range(len(dat)):
        res[ii] = if_type_then_to_str(dat[ii],typ)
    return res


def get_count_rows_table(config, table_name):
    result = -1
    with psycopg2.connect("dbname=%s user=%s host=%s password=%s" % 
        (config.get("DB", "dbname"), config.get("DB", "user"), 
        config.get("DB", "host"), config.get("DB", "password"))) as db:
        with db.cursor() as curs:
            sql = 'select count(*) as kvo from ' + table_name
            curs.execute(sql)
            row = curs.fetchone()
            if len(row)==1 and row[0] != None:
                result = row[0]
    return result


def run_sql_script(config, script, set_isolat = False):
    result = False
    with psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (config.get("DB", "dbname"), config.get("DB", "user"), config.get("DB", "host"), config.get("DB", "password"))) as db:
        with db.cursor() as curs:
            print('Работа с БД:', config.get("DB", "host"), '----->', config.get("DB", "dbname"))
            if set_isolat:
                db.set_isolation_level(0)
            try:
                curs.execute(script)
            except psycopg2.DatabaseError as e:
                print(f'Error {e}')
                db.rollback()
                result = False
                return result
            db.commit()
            result = True
            print('Скрипт выполнен!')
    return result


def drop_all_in_db(config):
    result = False
    with psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (config.get("DB", "dbname"), config.get("DB", "user"), config.get("DB", "host"), config.get("DB", "password"))) as db:
        with db.cursor() as curs:
            print('Работа с БД:', config.get("DB", "host"), '----->', config.get("DB", "dbname"))
            db.set_isolation_level(0)
            try:
                # удаляем вьювы
                count = int(config.get('VIEWS','count'))
                for ii in range(count):
                    curs.execute('DROP VIEW IF EXISTS ' + config.get('VIEWS', str(ii+1)) + ' CASCADE')
                print('Вьювы в БД удалены.')
                # удаляем служебные таблицы
                count = int(config.get('SYSTABLES','count'))
                for ii in range(count):
                    curs.execute('DROP TABLE IF EXISTS ' + config.get('SYSTABLES', str(ii+1)) + ' CASCADE')
                print('Служебные таблицы в БД удалены.')
                # удаляем основные таблицы
                count = int(config.get('TABLES','count_tables'))
                for ii in reversed(range(count)):
                    table_name = config.get('TABLES', str(ii+1)).split(',')[0]
                    curs.execute('DROP TABLE IF EXISTS ' + table_name + ' CASCADE')
                    print('Удалена таблица: ' + table_name)
                print('Основные таблицы в БД удалены.')
            except psycopg2.DatabaseError as e:
                print(f'Error {e}')
                db.rollback()
                result = False
                return result
            db.commit()
            result = True
            print('Очистка БД выполнена!')
    return result


def load_data_to_db_from_json(data, config):
    result = False
    with psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (config.get("DB", "dbname"), config.get("DB", "user"), config.get("DB", "host"), config.get("DB", "password"))) as db:
        with db.cursor() as curs:
            db.set_isolation_level(0)
            tables_count = data["tables_count"]
            try:
                for tabl_num in range(1, tables_count + 1):
                # for tabl_num in reversed(range(1, tables_count + 1)):
                    table_name = data["table_"+str(tabl_num)]
                    col_names = data["tab-fields_"+str(tabl_num)]
                    sql_insert = 'insert into ' + table_name + '(' + list_to_str_join(', ', col_names) + ') values (' + ('%s, ' * len(col_names))[0:-2:1] + ')'
                    rows_count = data["tab-rows-count_"+str(tabl_num)]
                    for row_num in range(1, rows_count + 1):
                        values = data["t"+str(tabl_num)+"_"+str(row_num)]
                        curs.execute(sql_insert, tuple(values))
                    if ('id' in col_names) and (rows_count > 0): # устанавливаем генератор ID
                        max_tbl_id = data["tab-max-id_"+str(tabl_num)]
                        sql_insert = "SELECT setval('" + table_name + "_id_seq', %s, true)"
                        curs.execute(sql_insert,(max_tbl_id,))
                    print('Залиты денные для таблицы: ' + table_name + ' --- ' + str(rows_count) + ' строк.')
            except psycopg2.DatabaseError as e:
                print(f'Error {e}')
                db.rollback()
                result = False
                return result
            db.commit()
            result = True
            print('Данные успешно залиты в таблицы!')
    return result


def save_date_from_db_to_json(filename, config, base):
    dd = datetime.date(datetime.now())
    base['Base_Version'] = get_base_version(config)
    with psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (config.get("DB", "dbname"), config.get("DB", "user"), config.get("DB", "host"), config.get("DB", "password"))) as db:
        with db.cursor() as curs:
            print('Репликация данных из БД в json.')
            base["tables_count"] = int(config.get("TABLES", "count_tables"))
            for tabl_num in range(1,base["tables_count"]+1): # по циклу извлекаем таблицы из БД для сохранения и переноса данных
                tabl = config.get("TABLES", str(tabl_num)).split(',') # из ини-файла конфигурации читаем наименования таблиц и поле сортировки (обычно это id)
                base["table_"+str(tabl_num)] = tabl[0] # в структуру записваеем назавние таблицы и её синоним (в прямом порядке и обратном  след. строка) формируется имя вида: table_i
                base[tabl[0]] = "table_"+str(tabl_num)
                sql_select_tab = "SELECT * FROM " + tabl[0] + " order by " + tabl[1] # собираем строку запроса данных таблицы  
                curs.execute(sql_select_tab)         
                col_names = [cn[0] for cn in curs.description]  # получаем имена полей из запроса.
                base["tab-fields_"+str(tabl_num)] = col_names # записываем в структуру имена полей. формируется имя вида: tab-fields_i
                query_rows = curs.fetchall()
                base["tab-rows-count_"+str(tabl_num)] = len(query_rows) # записываем в структуру количество строк таблицы (селекта). формируется имя вида: tab-rows-count_i
                i_row = 0
                for i_row in range(len(query_rows)): # записи, построчно, записываем в структуру                    
                    base["t"+str(tabl_num)+"_"+str(i_row+1)]  = change_type_to_str_in_list(query_rows[i_row], dd)  #  формируется имя вида: ti_j
                if ('id' in col_names) and (len(query_rows) > 0):  #  если в таблице есть поле id, то сохраняем максиум значения id в структуру под именем tab-max-id_i
                    base["tab-max-id_"+str(tabl_num)] = query_rows[i_row][0]
    with open(filename, "w") as write_file:
        json.dump(base, write_file)
    print(os.path.join(path_to_save_dump, db_dump_data), 'записан в форате json') 


base_path = os.path.dirname(abspath(__file__))
ini_conf_name = 'save-db-data.ini'
db_dump_data = 'dump-db-data.json'
path_to_save_dump = base_path
path_updates = ''
carent_ver_base = tuple([0, 0, 0])
all_up_base_vers_present = None
first_up_base_vers_present = None
base = dict()
sql_all_tables = "SELECT table_name FROM information_schema.tables  where table_schema='public' ORDER BY table_name"

if not os.path.exists(os.path.join(base_path, ini_conf_name)):
    sys.exit('Не найден файл конфигурации: ' + ini_conf_name)

config = configparser.ConfigParser()
config.read(os.path.join(base_path, ini_conf_name))

host = nyk.input_easy('Введите адрес сервера: ', config.get("DB", "host"))
psw = str(nyk.input_easy('Введите пароль пользователя БД: ', ''))

config.set("DB", "host", host)
config.set("DB", "password", psw)

comand_num = None
while comand_num != 0:
    show_menu()
    comand_num = int(input().strip())
    if comand_num == 1:
        save_date_from_db_to_json(os.path.join(path_to_save_dump, db_dump_data), config, base)
    elif comand_num == 2 or comand_num == 3: # проверка - нужны ли апдеёты  или, собственно, попытка обновления структуры БД
        res = need_update_base(config, vv = None if comand_num == 2 else all_up_base_vers_present, do_update = (comand_num == 3), pat = path_updates)
        if len(res) > 1:
            path_updates = res.get('path', '')
            carent_ver_base = res.get('ver_b', tuple([0, 0, 0]))
            all_up_base_vers_present = res.get('allvers', None)
            ver_db_str = list_to_str_join('.', carent_ver_base)
        if res.get('result', False):
            if len(res) > 1:
                first_up_base_vers_present = res.get('first_up_ver', None)
            move_cur_dir.print_empty_lines(2)
            print('ПРОВЕРКА НА НЕОБХОДИМОСТЬ ОБНОВЛЕНИЯ СТРУКТУРЫ БД v: ' + ver_db_str)
            sstr = 'не определён'
            if first_up_base_vers_present != None and comand_num == 2:
                sstr =  list_to_str_join('.', first_up_base_vers_present)    
            if comand_num == 2:
                print('База данных нуждается в обновлении. Апдейты готовы к установке. Сдежующий: ' + sstr)
            else:
                print('Структура базы данных нуждалась в обновлении. Апдейты установлены успешно!')
        else:
            move_cur_dir.print_empty_lines(2)
            print('ПРОВЕРКА НА НЕОБХОДИМОСТЬ ОБНОВЛЕНИЯ СТРУКТУРЫ БД v: ' + ver_db_str)
            sstr = 'Для базы данных нет необходимых апдейтов. Или не правильно указан путь к файлам обновления.'
            if comand_num == 3 and res.get('no_up_do', False):
                sstr = 'Структура базы данных нуждается в обновлении. Возникла ошибка при установке обновления структуры БД.'
            print(sstr)
    elif comand_num == 4: # Удаление данных и структуры БД, создание структыры из начального скрипта.
        sstr = input('Вы действительно хотите удалить все данные и структуру БД? Операция не отменима! Рекомендуем сохранить данные. Если да, то напечатайте yes : ')
        if sstr == 'yes':
            res = drop_all_in_db(config)
            if res:
                print('База данных полностью очищена, все таблицы и данные удалены.')
                print('Выполним скрипт создания структуры БД.')
                input('Нажмите ENTER для продолжения.')
                sstr = 'Выберите директорию с файлом скрипта создания таблиц базы данных:'
                res = False
                files = get_list_files_dir(sstr, root_name = 'PhotoCProDB.sql', ext = '', pat = path_updates)
                if len(files) == 2:                    
                    path_updates = files[1]
                    file_name = os.path.join(path_updates, 'PhotoCProDB.sql')
                    script = get_from_file(file_name)
                    if script != '':
                        res = run_sql_script(config, script, True)
                if not res:
                    print('Структура БД не создана. Либо файл скрипта не найден, либо скрипт содержит ошибки.')
                else:
                    print('Структура БД создана! Проверьте необъодимость обновления структуры.')
    elif comand_num == 5: # Загрузка данных в пустую БД данных в формате json
        print('Внимание!!! Таблицы базы данных должны быть полностью очищены. Иначе возможны коллизии и ошибки в данных.')
        print('Начинаем проверку основных таблиц на присутствие данных:')
        count = int(config.get('TABLES','count_tables'))
        res = True
        for ii in reversed(range(count)):
            table_name = config.get('TABLES', str(ii+1)).split(',')[0]
            count = get_count_rows_table(config, table_name)
            if count < 0:
                print('Проблемы с таблицей: ' + table_name + ' Скорее всего таблица отсутствует в этой версии БД.')
                res = False
            if count > 0:
                print('Проблемы с таблицей: ' + table_name + ' Данные не очищены!')
                res = False
        if not res:
            print('Данные не могут быть загружены в БД.')
            input('Нажмите ENTER для продолжения.')
        else:
            # Заливаем данные
            j_file_name = os.path.join(path_to_save_dump, db_dump_data)
            if os.path.exists(j_file_name) and os.path.isfile(j_file_name) and os.path.getsize(j_file_name) > 100:
                with open(j_file_name, "r") as json_file_r:
                    base = json.load(json_file_r)
                if 'Base_Version' in base.keys():
                    jbd_vers_str = base['Base_Version']
                    bd_vers_str = get_base_version(config)
                    if jbd_vers_str != '' and bd_vers_str == jbd_vers_str:
                        carent_ver_base = tuple(map(lambda x: int(x), jbd_vers_str.split('.')))
                        # запускаем функцию заливки данных
                        load_data_to_db_from_json(base, config)
                    else:
                        print('Версия данных не совпадает с версией БД! Файл: ' + jbd_vers_str + ' и база данных: ' + bd_vers_str)
                        print('Файл с данными: ' + j_file_name)
                else:
                    print('Данные не те или не полные! Проверьте файл с данными!')
                    print('Файл с данными: ' + j_file_name)
            else:
                print('Файл с данными не найден или его размер слишком мал! Проверьте файл с данными!')
                print('Файл с данными: ' + j_file_name)
            input('Нажмите ENTER для продолжения.')
