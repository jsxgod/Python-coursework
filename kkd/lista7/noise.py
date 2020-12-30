import sys
import random

from utils import check_sys_arguments

check_sys_arguments(4)

input_probability = float(sys.argv[1])
input_file = sys.argv[2]
output_file = sys.argv[3]

with open(input_file, "rb") as f:
    byte_content = f.read()

bit_string = ''.join("{0:08b}".format(byte) for byte in byte_content)
new_bit_string = ''.join(
                        str(int(not int(b))) if random.random() <= input_probability else b
                        for b in bit_string
                    )

output = bytes(int(new_bit_string[i:i + 8], 2) for i in range(0, len(new_bit_string), 8))

with open(output_file, "wb") as f:
    f.write(output)
