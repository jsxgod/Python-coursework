import sys

assert len(sys.argv) == 2
file = sys.argv[1]

with open(file) as f:
    size = sum([int(line.split()[-1]) for line in f.readlines()])

print("Całkowita liczba bajtów: ", size)