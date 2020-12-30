from bitstring import ConstBitStream
import bitstring
import filecmp

import entropy
import sys
import statistics


def _to_Bytes(data):
    b = bytearray()
    concat = ""
    for s in data:
        concat += s
    for i in range(0, len(concat), 8):
        bit_string = concat[i:i + 8]
        if len(bit_string) == 8:
            v = int(concat[i:i + 8].rjust(8, '0'), 2)
            b.append(v)
        else:
            v = int(concat[i:i + 8].ljust(8, '0'), 2)
            b.append(v)
    return bytes(b)


def encode(path):
    bits = 9
    limit = pow(2, int(bits))
    file = open(path, encoding='utf-8')
    data = file.read()

    word = data[0]
    data = data[1:]

    dictionary = {chr(i): i for i in range(256)}
    results = []

    for symbol in data:
        w_s = word + symbol
        if w_s in dictionary:
            word = w_s
        else:
            if len(dictionary) == limit:
                limit *= 2
                bits += 1

            results.append(bin(dictionary[word])[2:].rjust(bits, '0'))
            dictionary[w_s] = len(dictionary)

            word = symbol
    if word in dictionary:
        results.append(bin(dictionary[word])[2:].rjust(bits, '0'))

    with open('encoded.bin', "wb") as f:
        f.write(_to_Bytes(results))

    file.close()


def decode(path):
    f = ConstBitStream(filename=path)

    bits = 9
    limit = pow(2, int(bits))

    dictionary = {i: chr(i) for i in range(256)}

    with open('decoded.txt', "w", encoding="utf-8") as exit_file:
        b = f.read(bits)
        value = b.uint
        current = chr(value)
        exit_file.write(current)

        while True:
            if len(dictionary) == limit - 1:
                limit *= 2
                bits += 1

            try:
                b = f.read(bits)
            except bitstring.ReadError:
                break

            if not b:
                break

            value = b.uint

            if value in dictionary:
                output = dictionary[value]
            else:
                output = current + current[0]

            exit_file.write(output)
            dictionary[len(dictionary)] = current + output[0]

            current = output


assert len(sys.argv) in [3, 4]

mode = sys.argv[1]
assert mode in ['--encode', '--decode']

input_file = sys.argv[2]
compare_file = ""

if len(sys.argv) == 4:
    compare_file = sys.argv[3]

if mode == '--encode':
    encode(input_file)

    print('--------------------')
    o_s, c_s, percentage = statistics.calculate_compression(input_file, 'encoded.bin')
    print('Kompresja:', percentage, '% rozmiaru pliku przed kompresją.')
    print('Przed: ', o_s, 'bajtow.')
    print('Po: ', c_s, 'bajtow.')
    print('--------------------')
    print('Dlugosc pliku wejsciowego: ', statistics.file_length(input_file))
    print('Dlugosc pliku zakodowanego: ', statistics.file_length('encoded.bin'))
    print('--------------------')
    entropy.calculate([input_file, 'encoded.bin'])
elif mode == '--decode':
    decode(input_file)
    if compare_file:
        print('Wynik porownania plikow: ', filecmp.cmp(compare_file, 'decoded.txt'))
