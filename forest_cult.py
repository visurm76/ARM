import datetime
import modules

now_year = datetime.datetime.now()
path_files = 'gubaha.sqlite'


class Culture(object):
    kz_culture = ((31, 10), (8, 9))

    def __init__(self, dictKey=['Квартал', 'Выдел', 'Кат.земель', 'Гл.порода', \
                                'Возраст1', 'Год посадки', 'Возраст2', 'Возраст3', 'Возраст4', \
                                'Год посадки', 'Происх.1', 'Происх.2', 'Происх.3']):
        self.dictKey = dictKey

    def filter_bd(self):
        """
        Функция выбирает лесные культуры и сравнивает год посадки и возраст
        :return: Печатает на экран таблицу с ошибочными выделами
        """

        array = []

        # Выборка из БД выделов с кат. земель - лесные культуры, насаждения с примесью л/к

        for i in modules.connect_sqlite(self.dictKey):
            if i[2] in Culture.kz_culture[0] and i[4] < 24:
                age = 2000
            else:
                age = 1900

            if i[2] in Culture.kz_culture[0]:
                array.append([int(i[0]), i[1], i[2], i[3], i[4], int(i[5]) + age])
            else:
                if i[6] == 3:
                    array.append([int(i[0]), i[1], i[2], i[6], int(i[5]) + age])
                elif i[7] == 3:
                    array.append([int(i[0]), i[1], i[2], i[7], int(i[5]) + age])
                elif i[8] == 3:
                    array.append([int(i[0]), i[1], i[2], i[8], int(i[5]) + age])

            # Проверяем вычисленный возраст по году посадки

            error_num = []

            for num in array:
                age_culture = now_year.year - num[5]
                if age_culture == num[4]:
                    continue
                else:
                    error_num.append([num[0], num[1], num[4], num[5]])
        # print(array)
        print(error_num)
        for i in error_num:
            print('|{:<5}|{:<5}|{:<5}|{:<5}|'.format(int(i[0]), i[1])
            # Выводим в красивом виде
            # print('Несоответствие: возраст и год посадки л/к')
            # print('---------------------------')
            # print('|{:<5}|{:<5}|{:<5}|{:<5}|'.format('№кв.', '№выд.', 'Возраст', 'Год посадки'))
            # print('---------------------------')
            # for i in error_num:
            # print('|{:<5}|{:<5}|{:<5}|{:<5}|'.format(int(i[0]), i[1], num[2], num[3]))
            # print('---------------------------')

d = Culture()

print(d.filter_bd())

