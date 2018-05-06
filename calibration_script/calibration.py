from math import sin, cos


class Dark_maker:
    def __init__(self, D_list):
        self.D_list = D_list
        self.D = {}
    def get_D(self):
        for key in self.D_list:
            self.D[key] = sum(self.D_list[key]) / (len(self.D_list[key]))
        return self.D

R = {'0': 0, '45': 0, '90': 0, '135': 0}
D_list = {'0': [0, 1, 5], '45': [0, 1, 2], '90': [0, 1, 2], '135': [0, 1, 2]}
D = Dark_maker(D_list).get_D()


class Calibration:
    eps = {1: 0, 2: 0}
    e = {1: 0, 2: 0}
    q_inst = 0
    u_inst = 0
    q_cal = 2 ** 0.5 / 2
    u_cal = 2 ** 0.5 / 2

    def __init__(self, R, D):
        self.R = R
        self.D = D
        self.RD = {}
        self.c = {}
        self.s = {}
        self.K = {}
        self.a = {}
        self.delta_I = {}

        self.alfa = {}



        self.make_parameters()

    def make_parameters(self):
        self.make_a()
        self.make_RD()
        self.make_c_and_s()
        self.make_K()
        self.make_a()

    def make_orbit_cal(self):
        q_cal_ = - self.q_cal * cos(2 * self.eps[1]) - self.u_cal * sin(2 * self.eps[1])
        u_cal_ = self.q_cal * sin(2 * self.eps[2]) - self.u_cal * cos(2 * self.eps[2])

        q_inst_ = self.q_inst * cos(2 * self.eps[1]) + self.u_inst * sin(2 * self.eps[1])
        u_inst_ = - self.q_inst * sin(2 * self.eps[2]) + self.u_inst * cos(2 * self.eps[2])

        self.alfa['q'] = (q_cal_ + q_inst_) / (self.RD['0'] - K1)

    def make_a(self):
        self.a['q'] = (1 + self.e[1]) / (1 - self.e[1])
        self.a['u'] = (1 + self.e[2]) / (1 - self.e[2])

    def make_RD(self):
        for key in self.R:
            self.RD[key] = self.R[key] - self.D[key]

    def make_c_and_s(self):
        self.s[1] = sin(self.eps[1])
        self.s[2] = sin(self.eps[2])
        self.c[1] = cos(self.eps[1])
        self.c[2] = cos(self.eps[2])

    def make_K(self):
        self.K[1] = self.RD['0'] / self.RD['90']
        self.K[2] = self.RD['45'] / self.RD['135']

    def make_delta_I(self):
        self.delta_I['0,90'] = (self.RD['0'] - self.K[1] * self.RD['90']) / (self.RD['0'] + self.K[1] * self.RD['90']) * self.a['q']
        self.delta_I['45,135'] = (self.RD['45'] - self.K[2] * self.RD['135']) / (self.RD['45'] + self.K[2] * self.RD['135']) * self.a['u']

def get_numerator_q():
    part_1 = q_inst * s[2] * (s[1] + u_inst * delta_I['0,90'])
    part_2 = - (1 + u_inst ** 2) * (c[2] * delta_I['0.90'] - s[1] * delta_I['45,135'])
    part_3 = c[1] * q_inst * (c[2] + u_inst * delta_I['45,135'])
    return part_1 + part_2 + part_3

def get_numerator_u():
    part_1 = c[1] * c[2] * u_inst
    part_2 = - (s[2] + q_inst**2 * s[2] - c[2] * q_inst * u_inst) * delta_I['0,90']
    part_3 = - c[1] * (1 + q_inst**2) * delta_I['45,135']
    part_4 = s[1] * u_inst * (s[2] - q_inst * delta_I['45,135'])
    return part_1 + part_2 + part_3 + part_4

def get_denominator():
    part_1 = s[1] * s[2]
    part_2 = c[2] * q_inst * delta_I['0,90']
    part_3 = s[2] * u_inst * delta_I['0,90']
    part_4 = - q_inst * s[1] * delta_I['45,135']
    part_5 = c[1] * (c[2] + u_inst * delta_I['45,135'])
    return part_1 + part_2 + part_3 + part_4 + part_5

def get_param():
    q = get_numerator_q() / get_denominator()
    u = get_numerator_u() / get_denominator()
    return q, u
