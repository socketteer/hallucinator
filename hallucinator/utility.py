import math


def vec_eq(v1, v2):
    for c1, c2 in zip(v1, v2):
        if not math.isclose(c1, c2, abs_tol=0.001):
            return False
    return True


def magnitude(vector, p=2):
    return sum(map(lambda x: x ** p, vector)) ** (1.0 / p)


def normalize(vector, p=2):
    mag = magnitude(vector, p)
    return tuple(map(lambda x: x/mag, vector))




def test_normalize():
    import random

    def old_normalize(vector):
        mag = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        normal_vec = (vector[0] / mag, vector[1] / mag)
        return normal_vec

    def old_normalize3(vector):
        mag = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
        normal_vec = (vector[0] / mag, vector[1] / mag, vector[2] / mag)
        return normal_vec

    rand = lambda: random.uniform(0, 5)
    for i in range(100):
        a, b, c = rand(), rand(), rand()

        assert vec_eq(normalize((a,b)), old_normalize((a,b)))
        assert vec_eq(normalize((a,b,c)), old_normalize3((a,b,c)))



if __name__ == "__main__":
    test_normalize()
