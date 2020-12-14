import os

def print_empty_lines(count_lines):
    for i in range(count_lines):
        print()


def print_like_dir_list(dirlist, path_print):
    # выводит на консоль в стиле команды dir списка файлов 
    print_empty_lines(4)
    for file_name in dirlist:
        print(file_name)
    print('------------>')
    print('In current directory:', path_print)


def show_directory(path):
    # выводит на консоль содержание указанной директории (папки) и возвращает удачность выполнения операции
    if os.path.exists(path) and os.path.isdir(path):
        files = os.listdir(path)
        print_like_dir_list(files, path)


def show_current_directory():
    # выводит на консоль содержание текущей директории (папки)
    show_directory(os.getcwd())
    

def get_directory_up(path_now):
    # шагает на ступень выше из текущей папки (директории)    
    result_path = ''
    path_list = []
    if os.path.exists(path_now) and os.path.isdir(path_now):
        simbol = '\\'
        if  simbol in path_now:
            path_list = path_now.split(simbol)        
        elif '/' in path_now:
            simbol = '/'
            path_list = path_now.split(simbol)
        if len(path_list) > 0:
            result_path = path_list[0]
            if len(path_list) > 1:        
                for i in range(1, len(path_list)-1):
                    result_path += simbol + path_list[i]
    return result_path


def set_directory():
    # устанавливает директорию (папку)
    command_list = ('exit', '..', 'cd', 'set')
    param_string = ''
    result = False
    while param_string != 'exit':
        print_empty_lines(2)
        show_current_directory()
        print()
        print('Введите команду:', command_list, end = ' ')
        param_string = input().strip()
        if param_string == 'cd':
            print('Введите имя ппки:', end = ' ')
            dir_string = input().strip()
            new_path = os.getcwd() + '\\' + dir_string
            if os.path.isdir(new_path):
                os.chdir(new_path)
        elif param_string == '..':
            up_dir = get_directory_up(os.getcwd())
            if up_dir != '':                
                os.chdir(up_dir)
        elif param_string == 'set':
            print_empty_lines(3)
            print('----------------------------------')
            print('Выбрана директория: ', os.getcwd())
            result = True
            break
    return [result, os.getcwd()]


def get_directory(common = '', start_path = ''):
    # возвращает не устанавливая выбранную директорию (папку)
    command_list = ('exit', '..', 'cd', 'set')
    param_string = ''
    result = False
    if start_path == '':
        accept_dir = os.getcwd()
    else:
        accept_dir = start_path
    while param_string != 'exit':        
        print_empty_lines(2)        
        show_directory(accept_dir)
        print()
        print(common)
        print('Введите команду:', command_list, end = ' ')
        param_string = input().strip()
        if param_string == 'cd':
            print('Введите имя ппки:', end = ' ')
            new_path = input().strip()
            new_path = os.path.join(accept_dir, new_path)
            if os.path.isdir(new_path):
                accept_dir = new_path
        elif param_string == '..':
            new_path = get_directory_up(accept_dir)
            if new_path != '':                
                accept_dir = new_path
        elif param_string == 'set':
            print_empty_lines(3)
            print('----------------------------------')
            print('Выбрана директория: ', accept_dir)
            result = True
            break
    return [result, accept_dir]

