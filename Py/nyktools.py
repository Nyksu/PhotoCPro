'''
v 0.0.1
'''

import re
import time
from functools import wraps

rim_dict = {'I':(1,1),'V':(5,0),'X':(10,1),'L':(50,0),'C':(100,1),'D':(500,0),'M':(1000,1)}

def input_easy(cap, default):
    '''
    DOCSTRING:
    функция упрощает получение контролируемого ввода. 
    Преобразует по возможности строку в Int и float,
    Пробельные символы с краёв ввода - убирает.
    Если ввели пустую строку, то выводит то, что по умолчанию.
    INPUT: cap - caption, строка, приглашающая к вводу. default - значение по умолчанию.
    OUTPUT: возвращает либо int, либо float, если в них возможно конвертировать, иначе - str.
    При пустом вводе возвращает значение по умолчанию - люого типа.
    '''
    if default: 
        print("По умолчанию", default)
    res = input(cap).strip()
    if res:
        if res.isdigit():
            res = int(res) # доступно целое положительное число
        else:
            if res[0] == '-' and str(res[1:]).isdigit():
                res = int(res) # доступно целое отрицательное число
            else:
                pt = r"^[+-]?([0-9]*[.]{1})([0-9]+)?$"
                if re.search(pt, res):
                    res = float(res) # доступно число с плавающей точкой
    else:
        res = default
    return res

def messure_func_time(func):    
    '''
    DOCSTRING: декоратор измеряющий время исполнения функции
    Применение:  над описанием измеряемой функции добавляем строку @messure_func_time
    '''
    @wraps(func) # Декорируем декоратор (делаем достумным описания декарируемых функцй)
    def inner(*args, **kwargs):
        print(f'!!!! Тест времени исполнения функции {func.__name__}. Начало работы функции.')
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f'Время исполнения функции {func.__name__} составило: {end - start}')
        return res
    return inner

def is_str_roman_digits(rim):
    '''
    DOCSTRING:
    функция тестирует корректность римских цифр до 3999.
    INPUT: rim - строка с римскими цифрами.
    OUTPUT: Возвратит либо False (при любом не верном виде строки римскими цифрами),
    любо True, когда запись римскими цифрами - верна.
    '''
    res = False
    if not isinstance(rim, str):
        return res
    test_rim = str(rim).upper().strip()
    # Комплексная проверка (не римские цифры, некорректные повторы символов, не коректная последовательность символов)
    pt = r"[^IVXLCDM]|VV|LL|DD|M{4,}|I{4,}|X{4,}|C{4,}|I{2,}[VX]|I[CMLD]|I[VX]+I|V[CMLDX]|X[DM]|X[LC]+X|X{2,}[LC]|L[CDM]|C[DM]+C|C{2,}[DM]|DM"
    if not re.findall(pt, test_rim):
        res = True
    return res
    

def roman_to_digit(rim):
    '''
    DOCSTRING:
    функция переводит римские цифры до 3999 в число.
    Функция проверяет корректность входящей римской цифры с помощью функции is_str_roman_digits.
    INPUT: rim - строка с римскими цифрами.
    OUTPUT: Возвратит либо None (при любом не верном виде строки римскими цифрами), 
    либо 0, если входящее значение - пустая строка, любо число (положительное целое число), 
    соответствующее римской входящей цифре.
    '''
    res = 0
    if not is_str_roman_digits(rim):
        return None
    mir = str(rim[::-1]).upper().strip()    
    for c in range(len(rim)):
        r = rim_dict[mir[c]][0]
        if c > 0:
            if rim_dict[mir[c]][1] and rim_dict[mir[c-1]][0] > r:
                r = - r
        res += r
    return res