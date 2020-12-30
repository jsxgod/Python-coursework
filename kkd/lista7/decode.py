import sys
from utils import check_sys_arguments

check_sys_arguments(3)

codes = [
    "00000000",
    "11010010",
    "01010101",
    "10000111",
    "10011001",
    "01001011",
    "11001100",
    "00011110",
    "11100001",
    "00110011",
    "10110100",
    "01100110",
    "01111000",
    "10101010",
    "00101101",
    "11111111",
]


def hamming(byte):
    for c in codes:
        error_count = 0
        for bit, code_bit in zip(byte, c):
            if bit != code_bit:
                error_count += 1

        if error_count == 0:
            return byte[2] + byte[4] + byte[5] + byte[6]

        if error_count == 1:
            return c[2] + c[4] + c[5] + c[6]

    return None


def decode(bytes_):
    bitstring = "".join(format(b, "08b") for b in bytes_)
    result = ""
    error_count = 0

    while len(bitstring) >= 8:
        from_hamming = hamming(bitstring[0:8])
        result += from_hamming or "0000"
        error_count += from_hamming is None
        bitstring = bitstring[8:]

    print("Liczba bloków z więcej niż jednym błędem: ", error_count)

    return bytes(int(result[i:i+8], 2) for i in range(0, len(result), 8))


input_file = sys.argv[1]
output_file = sys.argv[2]


with open(input_file, "rb") as f1:
    with open(output_file, "wb") as f2:
        f2.write(decode(f1.read()))
