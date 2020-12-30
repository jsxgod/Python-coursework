from math import ceil
import sys

from utils import check_sys_arguments

check_sys_arguments(3)


def files_difference(file, file_):
    bits1 = "".join(format(b, "08b") for b in file)
    bits2 = "".join(format(b, "08b") for b in file_)

    length_difference = ceil(abs(len(bits1) - len(bits2)) / 4)
    result = length_difference
    for i in range(0, len(bits1), 4):
        if bits1[i:i+4] != bits2[i:i+4]:
            result += 1

    return result


file1 = sys.argv[1]
file2 = sys.argv[2]

with open(file1, "rb") as f1:
    with open(file2, "rb") as f2:
        difference = files_difference(f1.read(), f2.read())
        if difference == 0:
            print("Pliki są takie same.")
        else:
            print("Pliki różnią się w ", difference, " 4-bitowych blokach.")
