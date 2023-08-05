import numpy

def name(first, last):
    full = first + " " + last
    return full.title()

def get_numpy_arr(lst):
    return numpy.array(lst)

if __name__ == "__main__":
    print("Micha", "Kobb")
    print(get_numpy_arr([1,2,3,4,5]))