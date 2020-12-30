import sys

mode = sys.argv[1]

def encode_six(six) -> str:
    code = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    index = int(''.join(six), 2)

    return code[index]


def encode(file, file_write) -> str:
    result = ""
    six = []
    n = 0

    with open(file, 'r') as f:
        while True:
            f.seek(n)
            six = list(f.read(6))
            if not six:
                break
            result += encode_six(six)
            n += 6
        f.close()

    f = open(file_write, 'w')
    f.write(result)
    f.close()

    return result


def decode(file, file_write) -> str:
    code = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    result = ""
    with open(file, 'r') as f:
        while True:
            c = f.read(1)
            if not c:
                break
            binary = str(format(code.index(c), '06b'))
            result += binary
        f.close()

    f = open(file_write, 'w')
    f.write(result)
    f.close()
    return result


if mode == "--encode":
    assert ''.join(sys.argv[2][-4:]) == ".bin"
    e = encode(sys.argv[2], sys.argv[3])
    print(e)

if mode == "--decode":
    assert ''.join(sys.argv[2][-4:]) == ".txt"
    d = decode(sys.argv[2], sys.argv[3])
    print(d)