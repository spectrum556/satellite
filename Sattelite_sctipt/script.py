from data_reader import DataReader as Dr



class Constructor:
    values_dict = {}

    def __init__(self):
        self.description = Dr.get_description()
        self.names = Dr.get_names()
        self.make_zeros_values_dict()

    def make_zeros_values_dict(self):
        for name in self.names:
            self.values_dict[name] = 0


total = Constructor()
print(total.values_dict)


# top_dict['NX'] = 1  # кількість пікселів по координаті X (довгота)
# top_dict['NY'] = 1  # кількість пікселів по координаті Y (широта)
# top_dict['NT'] = 1  # кількість різних спостережень для тієї ж ділянки на поверхні
# top_dict['NPIXELS'] = 1  # число одночасно спостережних пікселів в групі пікселів (2 на 2 = 4)
# top_dict['TIMESTAMP'] = '2010-08-14T11:33:04Z'  # час у форматі iso8601
# top_dict['HOBS'] = 670000.00  # висота в метрах, на якій знаходиться прилад над рівнем моря
# top_dict['NSURF'] = 1  # буде включено в наступних версіях GRASP, зараз не використовується
# top_dict['IFGAS'] = 1  # = 1 - якщо присутнє поглинання газами, 0  - якщо відсутнє поглинання газами
# top_dict['end'] = 'NPIXELS  TIMESTAMP  HEIGHT_OBS(m)  NSURF  IFGAS'  # TODO: уточнити необіхність цієї штуки
#
# top_dict['IX'] = 1  # вказує на розташування пікселя вздовж координати X в обраній групі пікселів для відтворення.
