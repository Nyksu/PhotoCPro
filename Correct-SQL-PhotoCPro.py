import os
aa = []
# Читаем из файла конфигураци путь до файла со скриптом SQL
with open("conf.txt", "r") as file_conf:
    ss = file_conf.readline().strip()
if ss.startswith('path = '):
    aa = ss.split(sep=' = ')
filenameSQL = str(aa[1])
print('Open', filenameSQL)
# берем весь текст из файла SQL
with open(filenameSQL, "r") as fSQL:
    txt = fSQL.read()
print('Взяли текст из', filenameSQL)
# Убираем лишние пробелы
i = 0
while txt.find('  ') > -1:
    txt = txt.replace('  ',' ')
    i += 1
print('Удалили', i, 'лишних пробелов')
# Убираем лишние возвраты коретки
i = 0
while txt.find('\n\n\n') > -1:
    txt = txt.replace('\n\n\n','\n\n')
    i += 1
print('Удалили', i, 'лишних строк')
# убираем лишние скобки
i = 0
while txt.find(')) ') > -1:
    txt = txt.replace(')) ',') ')
    i += 1
print('Удалили', i, 'лишних скобок')
# Убираем вторичное появление индексов с номером CREATE INDEX IFK_Rel - заменяем на знак комментария
i = 0
while txt.find('CREATE INDEX IFK_Rel') > -1:
    txt = txt.replace('CREATE INDEX IFK_Rel','-- ')
    i += 1
print('Закомментировали', i, 'лишних индексов')
# записываем в файд исправления
if os.path.exists(filenameSQL):
    os.remove(filenameSQL)
with open(filenameSQL, "w") as fSQL:
    fSQL.write(txt)
print('Файл', filenameSQL, 'исправлен и сохранён.')
    
