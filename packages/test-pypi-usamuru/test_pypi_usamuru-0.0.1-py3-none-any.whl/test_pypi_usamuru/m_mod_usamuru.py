import numpy


def name(first, last):
    full = first + '' + last
    return full.title()


def get_numpy_arr(list):
    return numpy.array(list)


if __name__ == '__main__':
    print('Maciej', 'Grodzki')
    print(get_numpy_arr([1, 2, 3, 4, 5, ]))
