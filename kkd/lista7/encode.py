import sys
import functools

from utils import check_sys_arguments

check_sys_arguments(3)


def hamming(bits):
    idxs_list = [
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3]
    ]

    parity_list = [parity(bits, idxs) for idxs in idxs_list]

    result = parity_list[0] + parity_list[1] + bits[0] + parity_list[2] + bits[1:]
    p = parity(result, range(7))

    return result + p


def parity(bitstring, indices):
    return str(
        functools.reduce(lambda acc, index: acc + (bitstring[index] == "1"), indices, 0) % 2
    )


def encode(bytes_):
    bitstring = "".join(format(byte, "08b") for byte in bytes_)

    result = ""
    while len(bitstring) >= 4:
        result += hamming(bitstring[0:4])
        bitstring = bitstring[4:]

    return bytes(int(result[i:i + 8], 2) for i in range(0, len(result), 8))


input_file = sys.argv[1]
output_file = sys.argv[2]


with open(input_file, "rb") as f1:
    with open(output_file, "wb") as f2:
        f2.write(encode(f1.read()))
