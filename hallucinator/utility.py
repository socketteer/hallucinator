import math


#TODO combine normalize methods?
def normalize_3(vector):
    mag = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    normal_vec = (vector[0] / mag, vector[1] / mag, vector[2] / mag)
    return normal_vec


def normalize(vector):
    mag = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    normal_vec = (vector[0] / mag, vector[1] / mag)
    return normal_vec
