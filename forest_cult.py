import sqlite3
from sys import argv
import datetime

now_year = datetime.datetime.now()
path_files = 'gubaha.sqlite'


# select = "SELECT kv,sknr,zk FROM gubaha_kizel"
class Data(object):
    def connect_sqlite(self, select):
        """
        Функция считывания данных из базы данных
        return: список списков (квартал, выдел)
        """
        conn = sqlite3.connect(path_files)
        cur = conn.cursor()
        # Делаем запрос к базе данных и выбираем нужные столбцы из таблицы"SELECT kv,sknr,zk FROM gubaha_vydel"
        cur.execute(select)  # "SELECT kv,sknr,zk FROM gubaha_kizel"
        # Результат запроса в виде списка кортежей
        results = cur.fetchall()
        conn.close()
        return results


class Culture(object):
    def __init__(self):
        self.other = Data()

    def filter_bd(self):
        """
        Функция выбирает лесные культуры и сравнивает год посадки и возраст
        :return:
        """
        kz_culture = ((31, 10), (8, 9))
        array = []

        """ Выборка из БД выделов с кат. земель - лесные культуры, насаждения с примесью л/к """

        for i in self.other.connect_sqlite("SELECT kv,sknr,zk,amz1,amz2,amz3,amz4,\
                                                   kil1,kil2,kil3,kil4,dm11 FROM gubaha_kizel"):
            if i[2] == 31 or i[2] == 10 and i[3] < 25:
                age = 2000
            else:
                age = 1900

            if i[2] in kz_culture[0]:
                array.append([int(i[0]), i[1], i[2], i[3], int(i[11]) + age])
            else:
                if i[2] in kz_culture[1]:
                    if i[8] == 3:
                        array.append([int(i[0]), i[1], i[2], i[4], int(i[11]) + age])
                    elif i[9] == 3:
                        array.append([int(i[0]), i[1], i[2], i[5], int(i[11]) + age])
                    elif i[10] == 3:
                        array.append([int(i[0]), i[1], i[2], i[6], int(i[11]) + age])

            """ Проверяем вычисленный возраст по году посадки"""
            error_num = []
            for num in array:
                age_culture = now_year.year - num[4]
                if age_culture == num[3]:
                    continue
                else:
                    error_num.append([num[0], num[1]])
        return error_num


class Breeds(object):
    def __init__(self):
        self.other = Data()

    def filter_bd(self):
        array = []
        for i in self.other.connect_sqlite("SELECT kv,sknr,zk,amz1,dm11 FROM gubaha_kizel"):
            if i[2] == 31 or i[2] == 10 or i[2] == 8:
                array.append([int(i[0]), int(i[1]), int(i[2]), int(i[3]), int(i[4])])
        return array


class Age(Culture):
    pass


class Tax(Culture):
    pass


s = Data()
d = Culture()
# print(s.connect_sqlite())
print(d.filter_bd())
