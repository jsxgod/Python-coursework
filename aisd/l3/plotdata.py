import sys
import numpy as np
import matplotlib.pyplot as plt

file_names = [file for file in sys.argv[1:]]

column_names = []
fig, axs = plt.subplots(3)
fig.tight_layout(pad=3.0)

axs[0].set_title("Comparisons")
axs[1].set_title("Swaps")
axs[2].set_title("Time")

for file in file_names:
    with open(file) as f:
        lines = f.readlines()
        for column in lines[0].split(" "):
            column_names.append(column)
        sizes = [int(line.split()[0]) for line in lines[1:]]
        comparisons = [int(line.split()[1]) for line in lines[1:]]
        swaps = [int(line.split()[2]) for line in lines[1:]]
        times = [float(line.split()[3]) for line in lines[1:]]

    # PLOTS #
    axs[0].plot(sizes, comparisons, label=file + ' Comparisons')

    axs[1].plot(sizes, swaps, label=file + ' Swaps')

    axs[2].plot(sizes, times, label=file + ' Times')

for ax in axs.flat:
    ax.legend()
plt.legend()
plt.show()

for file in file_names:
    with open(file) as f:
        lines = f.readlines()
        for column in lines[0].split(" "):
            column_names.append(column)
        sizes = [int(line.split()[0]) for line in lines[1:]]
        comparisons = [int(line.split()[1]) for line in lines[1:]]
        swaps = [int(line.split()[2]) for line in lines[1:]]
    cn = []
    sn = []
    for i in range(len(sizes)):
        cn.append(comparisons[i] / sizes[i])
        sn.append(swaps[i] / sizes[i])

    plt.plot(sizes, cn, label=file + ' c/n')
    plt.plot(sizes, sn, label=file + ' s/n')

plt.legend()
plt.show()




