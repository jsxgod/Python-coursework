import numpy as np
from collections import defaultdict
import math


def calculate_byte_occurrences(file_bytes):
    byte_dictionary = defaultdict()
    byte_pairs_dictionary = defaultdict()

    # Start with the byte preceding the first set to 0 (it does not exist hence setting it manually to 0)
    prev_byte = np.int8(0).tobytes()

    # Keep in mind that the last byte wont be added to the dictionary or it's occurrence will be short
    # by one so we have to check it manually after the loop
    for byte in file_bytes:
        if (prev_byte, byte) in byte_pairs_dictionary:
            byte_pairs_dictionary[(prev_byte, byte)] += 1
        else:
            byte_pairs_dictionary[(prev_byte, byte)] = 1

        if prev_byte in byte_dictionary:
            byte_dictionary[prev_byte] += 1
        else:
            byte_dictionary[prev_byte] = 1

        # increment prev byte by one to the right before starting over
        prev_byte = byte

    # here we take care of the last byte manually
    # prev_byte is now the last byte
    if prev_byte in byte_dictionary:
        byte_dictionary[prev_byte] += 1
    else:
        byte_dictionary[prev_byte] = 1

    return byte_dictionary, byte_pairs_dictionary


files = [
    'test1.bin', 'test2.bin', 'test3.bin',
    'pan-tadeusz-czyli-ostatni-zajazd-na-litwie.txt',
    'gif1.gif',
    'yakul.jpg',
    'pycharm64.exe',
    '[JAVA][Effective Java 3rd Edition].pdf'
]

for filename in files:

    byte_data = [e.tobytes() for e in np.fromfile(filename, dtype=np.int8)]
    byte_dict, byte_pairs_dict = calculate_byte_occurrences(byte_data)

    # Calculate entropy
    entropy = 0
    # Go over occurrences for each byte
    for byte_occ in byte_dict.values():
        entropy += byte_occ * math.log(byte_occ / len(byte_data), 2)  # log(a) - log(b) = log(a/b)
    entropy = -entropy / len(byte_data)
    entropy = round(float(entropy), 1)

    # Calculate conditional entropy
    c_entropy = 0
    # pairs - byte pairs
    # value - number of occurrences
    # Note: pairs[0][0] returns the first element of the tuple (byte1, byte2) - byte1.
    for pair, pair_occ in byte_pairs_dict.items():
        first_byte = np.int8(pair[0][0]).tobytes()
        c_entropy += pair_occ * math.log(pair_occ / byte_dict[first_byte], 2)   # log(a) - log(b) = log(a/b)
    c_entropy = -c_entropy / (len(byte_data) - 1)
    c_entropy = round(float(c_entropy), 1)

    difference = entropy - c_entropy

    print("File:", filename)
    print("Entropy: ", entropy)
    print("Conditional Entropy: ", c_entropy)
    print("Difference: ", difference)
    print("--------------------------------------")
