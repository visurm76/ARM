import sqlite3
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

    kz_culture = ((31, 10), (8, 9))

    def __init__(self):
        self.other = Data()

    def filter_bd(self, selekt):
        """
        Функция выбирает лесные культуры и сравнивает год посадки и возраст
        :return: Печатает на экран таблицу с ошибочными выделами
        """

        array = []

        # Выборка из БД выделов с кат. земель - лесные культуры, насаждения с примесью л/к

        for i in self.other.connect_sqlite(selekt):
            if i[2] in Culture.kz_culture[0] and i[3] < 24:
                age = 2000
            else:
                age = 1900

            if i[2] in Culture.kz_culture[0]:
                array.append([int(i[0]), i[1], i[2], i[3], int(i[11]) + age])
            else:
                if i[2] in Culture.kz_culture[1]:
                    if i[8] == 3:
                        array.append([int(i[0]), i[1], i[2], i[4], int(i[11]) + age])
                    elif i[9] == 3:
                        array.append([int(i[0]), i[1], i[2], i[5], int(i[11]) + age])
                    elif i[10] == 3:
                        array.append([int(i[0]), i[1], i[2], i[6], int(i[11]) + age])

            # Проверяем вычисленный возраст по году посадки

            error_num = []
            #print(array)
            for num in array:
                age_culture = now_year.year - num[4]
                if age_culture == num[3]:
                    continue
                else:
                    error_num.append([num[0], num[1]])

        # Выводим в красивом виде
        print('Несоответствие: возраст и год посадки л/к')
        print('---------------------------')
        print('|{:<5}|{:<5}|'.format('№кв.', '№выд.'))
        print('---------------------------')
        for i in error_num:
            print('|{:<5}|{:<5}|'.format(int(i[0]), i[1]))
        print('---------------------------')


class BreedsOrigin(Data):

    def __init__(self):
        self.other = Culture()

    def filter_bd(self, selekt):
        """
        Проверяет соответствие категории земель (л/к) и происхождения
        :param selekt: SQL запрос к БД
        :return: Список списков (квартал, выдел, категория земель)
        """
        mass = []

        for i in self.connect_sqlite(selekt):
            if i[2] in Culture.kz_culture[0] and i[5] != 3:
                mass.append([int(i[0]), i[1], i[2], i[3], i[4], i[5]])
        print('Несоответствие: категория земель и происхождение')
        print('------------------------')
        print('|{:<5}|{:<5}|{:<5}|'.format('№кв.', '№выд.', 'Кат.земель'))
        print('------------------------')
        for i in mass:
            print('|{:<5}|{:<5}|{:<10}|'.format(i[0], i[1], i[2]))
        print('------------------------')


class Age(Culture):
    pass


class Tax(Culture):
    pass


s = Data()
d = Culture()
z = BreedsOrigin()
print(d.filter_bd("SELECT kv,sknr,zk,amz1,amz2,amz3,amz4,kil1,kil2,kil3,kil4,dm11 FROM gubaha_kizel"))
print(z.filter_bd("SELECT kv,sknr,zk,ard1,mr1,kil1 FROM gubaha_kizel"))
