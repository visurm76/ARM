import datetime
import modules

culture_year = 2023
path_files = 'gubaha.sqlite'


class Culture(object):
    def __init__(self):
        """
        Функция отпраляет запрос с перечнем столбцов, для формирования SQL запроса в базу данных
        """
        self.tpl_cult = modules.connect_sqlite(['Квартал', 'Выдел', 'Кат.земель', \
                                                'ПМ1', 'ПМ%', 'РТК1', 'ПМ2', 'РТК2', \
                                                'ПМ3', 'РТК3', 'Цел.порода', 'Гл.порода', \
                                                'Порода', 'Возраст1', 'Происх.1', 'Год посадки'])

    # Выбираем выдела  с лесными культурами

    def filterCulture(self):
        """
        Функция выбирает выдела по категории земель, которые отностся к л/к
        :return: список кортежей # [('97', 7, 10, None, None, None, None, None, None, None, 'С', 'С', 'С', 53, 3, '70')]
        """
        lst_cult = []
        for num in self.tpl_cult:
            if num[2] == 10 or num[2] == 31:
                lst_cult.append(num)
        return lst_cult

    def controleOrigin(self):
        """
        Функция контроля происхождения
        :return:
        """
        error_origin = [[int(num[0]), num[1], num[14]] for num in Culture.filterCulture(self) if num[14] !=3]

        print('Несоответствие: происхождение л/к')
        print('-' * 21)
        print('|{:<5}|{:<5}|{:<5}|'.format('№кв.', '№выд.', 'Происх.'))
        print('-' * 21)
        for i in error_origin:
            if i[2] == None:
                i[2] = 'None'
                print(f"|{i[0]:^5}|{i[1]:<5}|{i[2]:<7}|")
            else:
                print(f"|{i[0]:^5}|{i[1]:<5}|{i[2]:<7}|")
        print('-' * 21)


    def controleAge(self):
        """
        Функция контроля возраста и года посадки л/к
        :return: Список (квартал, выдел, возраст и год посадки)
        """
        error_age = []
        for row in Culture.filterCulture(self):
                if row[13] < 24:
                    age = 2000
                else:
                    age = 1900
                if row[13] == (culture_year - (int(row[15]) + age)):
                    continue
                else:
                    error_age.append([int(row[0]), int(row[1]), row[13], int(row[15]) + age, row[14]])
        print()
        print('Несоответствие: возраст и год посадки л/к')
        print('-' * 41)
        print('|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|'.format('№кв.', '№выд.', 'Возраст', \
                                                       'Год посадки', 'Происх.'))
        print('-' * 41)
        for i in error_age:
            print('|{:^5}|{:<5}|{:<7}|{:^11}|{:^7}|'.format(int(i[0]), i[1], i[2], i[3], i[4]))
        print('-' * 41)





p = Culture()
print(p.controleAge())
#p.controleOrigin()
