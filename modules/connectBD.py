import sqlite3
import modules

name_files = 'gubaha.sqlite'


def selectAll(lst):
    """
    Функция генерации запроса в БД на основе словаря dictData
    :param info: список ключей словаря dictData
    :return: запрос в формате SQL
    """
    arr = []
    for i in lst:
        arr.append(modules.dictData[i])
        sel = "SELECT " + ','.join(arr) + " FROM gubaha_kizel"
    return sel


def connect_sqlite(select):
    """
    Функция считывания данных из базы данных
    return: список списков (квартал, выдел)
    """
    conn = sqlite3.connect(name_files)
    cur = conn.cursor()
    # Делаем запрос к базе данных и выбираем нужные столбцы из таблицы"SELECT kv,sknr,zk FROM gubaha_vydel"
    cur.execute(selectAll(select))  # "SELECT kv,sknr,zk FROM gubaha_kizel"
    # Результат запроса в виде списка кортежей
    results = cur.fetchall()
    # Сохраняем изменения
    conn.commit()
    #Закрываем соединение
    conn.close()
    return results
