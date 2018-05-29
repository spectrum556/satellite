from math import sin, cos, atan


class Calibration:
    eps = {1: 3, 2: 3}
    e = {1: 8, 2: 8}
    q_inst = 0.2
    u_inst = 0.1
    q_cal = 2**0.5 / 2
    u_cal = 2**0.5 / 2
    beta_nadir = 0

    def __init__(self):
        self.R = {}
        self.D = {}

        self.params_dict = {'q': 0,
                            'u': 0,
                            'DoLP': 0,
                            'AoLP': 0}
        self.RD = {}
        self.c = {}
        self.s = {}
        self.delta_I = {}
        self.K = {}
        self.a = {}

        self.is_first = True

    def make_calibration(self, R, D_list):
        self.R = R
        self.calculate_mean_dark(D_list)
        self.calc_radiometric_A()  # TODO make this coef
        self.calculate_parameters()
        self.update_parameters()

        self.calculate_stokes_parameters()

        self.params_dict['DoLP'] = (self.params_dict['q']**2 + self.params_dict['u']**2)**0.5

        # TODO: check atan: degree or radiands
        self.params_dict['AoLP'] = atan(self.params_dict['u'] / self.params_dict['q']) / 2 - 90 + self.beta_nadir

        print(self.params_dict)

    def calculate_mean_dark(self, D_list):
        for key in D_list:
            self.D[key] = sum(D_list[key]) / (len(D_list[key]))

    def calc_radiometric_A(self):
        pass

    def calculate_parameters(self):
        self.calc_RD()
        self.calc_c_and_s()

        if self.is_first:
            self.calc_K()
            self.calc_a()
            self.is_first = False


        self.calc_delta_I()

    def update_parameters(self):
        self.update_K()
        self.update_a()

    def calc_a(self):
        self.a['q'] = (1 + self.e[1]) / (1 - self.e[1])
        self.a['u'] = (1 + self.e[2]) / (1 - self.e[2])

    def update_a(self):
        q_cal_ = - self.q_cal * cos(2 * self.eps[1]) - self.u_cal * sin(2 * self.eps[1])
        u_cal_ = self.q_cal * sin(2 * self.eps[2]) - self.u_cal * cos(2 * self.eps[2])
        q_inst_ = self.q_inst * cos(2 * self.eps[1]) + self.u_inst * sin(2 * self.eps[1])
        u_inst_ = - self.q_inst * sin(2 * self.eps[2]) + self.u_inst * cos(2 * self.eps[2])

        common_part = (1 + self.q_cal * self.q_inst + self.u_cal * self.u_inst)
        q_numerator = (q_cal_ + q_inst_)
        u_numerator = (u_cal_ + u_inst_)
        q_ratio = (self.RD['0'] - self.K[1] * self.RD['90']) / (self.RD['0'] + self.K[1] * self.RD['90'])
        u_ratio = (self.RD['45'] - self.K[2] * self.RD['135']) / (self.RD['45'] + self.K[2] * self.RD['135'])

        self.a['q'] = q_numerator / q_ratio / common_part
        self.a['u'] = u_numerator / u_ratio / common_part

    def update_K(self):
        q_inst_ = self.q_inst * cos(2 * self.eps[1]) + self.u_inst * sin(2 * self.eps[1])
        u_inst_ = - self.q_inst * sin(2 * self.eps[2]) + self.u_inst * cos(2 * self.eps[2])

        self.K[1] = (1 - self.a['q'] * q_inst_) / (1 + self.a['q'] * q_inst_) * self.RD['0'] / self.RD['90']
        self.K[2] = (1 - self.a['u'] * u_inst_) / (1 + self.a['u'] * u_inst_) * self.RD['45'] / self.RD['135']

    def calc_RD(self):
        for key in self.R:
            self.RD[key] = self.R[key] - self.D[key]

    def calc_c_and_s(self):
        # TODO: check sin, cos: degree or radiands

        self.s[1] = sin(self.eps[1])
        self.s[2] = sin(self.eps[2])
        self.c[1] = cos(self.eps[1])
        self.c[2] = cos(self.eps[2])

    def calc_K(self):
        self.K[1] = self.RD['0'] / self.RD['90']
        self.K[2] = self.RD['45'] / self.RD['135']

    def calc_delta_I(self):
        self.delta_I['0,90'] = (self.RD['0'] - self.K[1] * self.RD['90']) / (self.RD['0'] + self.K[1] * self.RD['90']) * self.a['q']
        self.delta_I['45,135'] = (self.RD['45'] - self.K[2] * self.RD['135']) / (self.RD['45'] + self.K[2] * self.RD['135']) * self.a['u']


    def get_main_numerator_q(self):
        part_1 = self.q_inst * self.s[2] * (self.s[1] + self.u_inst * self.delta_I['0,90'])
        part_2 = - (1 + self.u_inst ** 2) * (self.c[2] * self.delta_I['0,90'] - self.s[1] * self.delta_I['45,135'])
        part_3 = self.c[1] * self.q_inst * (self.c[2] + self.u_inst * self.delta_I['45,135'])
        return part_1 + part_2 + part_3

    def get_main_numerator_u(self):
        part_1 = self.c[1] * self.c[2] * self.u_inst
        part_2 = - (self.s[2] + self.q_inst**2 * self.s[2] - self.c[2] * self.q_inst * self.u_inst) * self.delta_I['0,90']
        part_3 = - self.c[1] * (1 + self.q_inst**2) * self.delta_I['45,135']
        part_4 = self.s[1] * self.u_inst * (self.s[2] - self.q_inst * self.delta_I['45,135'])
        return part_1 + part_2 + part_3 + part_4

    def get_main_denominator(self):
        part_1 = self.s[1] * self.s[2]
        part_2 = self.c[2] * self.q_inst * self.delta_I['0,90']
        part_3 = self.s[2] * self.u_inst * self.delta_I['0,90']
        part_4 = - self.q_inst * self.s[1] * self.delta_I['45,135']
        part_5 = self.c[1] * (self.c[2] + self.u_inst * self.delta_I['45,135'])
        return part_1 + part_2 + part_3 + part_4 + part_5

    def calculate_stokes_parameters(self):
        self.params_dict['q'] = self.get_main_numerator_q() / self.get_main_denominator()
        self.params_dict['u'] = self.get_main_numerator_u() / self.get_main_denominator()

obj = Calibration()

R = {'0': 1000,
     '45': 5000,
     '90': 7300,
     '135': 1800}

D_list ={'0': [3,4,5],
    '45': [4,5,6],
    '90': [6,7,8],
    '135': [5,6,7]}


obj.make_calibration(R, D_list)
obj.make_calibration(R, D_list)
obj.make_calibration(R, D_list)

