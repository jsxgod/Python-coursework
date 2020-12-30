import sys
import os


def wordcount(file) -> [int]:
    print(file)
    lines = 0
    words = 0
    max_line = 0

    with open(file, 'r') as f:
        for line in f:
            w = line.split()
            lines += 1
            words += len(w)
            if len(line) > max_line:
                max_line = len(line)

    return [os.stat(file).st_size, words, lines, max_line]


data = wordcount(sys.argv[1])
print("liczba bajtow =", data[0])
print("liczba slow =", data[1])
print("liczba linii =", data[2])
print("maksymalna dlugosc linii  =", data[3])
