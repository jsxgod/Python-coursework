import sys
import numpy as np
import matplotlib.pyplot as plt

file_names = [file for file in sys.argv[1:]]

column_names = []

for file in file_names:
    with open(file) as f:
        lines = f.readlines()
        for column in lines[0].split(" "):
            column_names.append(column)
        sizes = [int(line.split()[0]) for line in lines[1:]]
        times = [float(line.split()[3]) for line in lines[1:]]

    # PLOTS #
    plt.plot(sizes, times, label=file + ' Times')

plt.legend()
plt.show()

