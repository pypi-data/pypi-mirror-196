import numpy


def name(first, last):
    """Returns full data of parameters"""

    full = first + " " + last
    return full.title()


def get_numpy(listy):
    """Returns array of numpy package"""

    return numpy.array(listy)


if __name__ == "__main__":
    print("Michal", "Karakula")
    print(get_numpy([1, 2, 3, 4, 5]))
