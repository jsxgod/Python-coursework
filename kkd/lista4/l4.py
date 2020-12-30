import math
import sys
from collections import defaultdict


colors = ['general', 'red', 'green', 'blue']
best_results_dict = dict()
for color in colors:
    best_results_dict[color] = (1000000, -1)


prediction_schemes = [
    lambda n, w, nw: w,
    lambda n, w, nw: n,
    lambda n, w, nw: nw,
    lambda n, w, nw: n+w-nw,
    lambda n, w, nw: n+(w-nw)//2 % 256,
    lambda n, w, nw: w+(n-nw)//2 % 256,
    lambda n, w, nw: (n+w)//2 % 256,
    lambda n, w, nw:
        Pixel(
            red=min(n.red, w.red) if nw.red >= max(n.red, w.red) else max(n.red, w.red) if nw.red <= min(n.red, w.red) else w.red+n.red-nw.red,
            green=min(n.green, w.green) if nw.green >= max(n.green, w.green) else max(n.green, w.green) if nw.green <= min(n.green, w.green) else w.green+n.green-nw.green,
            blue=min(n.blue, w.blue) if nw.blue >= max(n.blue, w.blue) else max(n.blue, w.blue) if nw.blue <= min(n.blue, w.blue) else w.blue+n.blue-nw.blue
        )
]


class Pixel:
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return str(self.red) + str(self.green) + str(self.blue)

    def __sub__(self, pixel2):
        return Pixel(red=self.red - pixel2.red, green=self.green - pixel2.green, blue=self.blue - pixel2.blue)

    def __add__(self, pixel2):
        return Pixel(red=self.red + pixel2.red, green=self.green + pixel2.green, blue=self.blue + pixel2.blue)

    def __mod__(self, value):
        return Pixel(red=self.red % value, green=self.green % value, blue=self.blue % value)

    def __floordiv__(self, value):
        return Pixel(red=self.red // value, green=self.green // value, blue=self.blue // value)


def image_to_bitmap(img, height, width):
    parsed = []
    row = []
    for p_i in range(width*height):
        row.append(Pixel(
            blue=img[p_i * 3],
            green=img[p_i * 3 + 1],
            red=img[p_i * 3 + 2],
        ))

        # reset row list if current row is done
        if len(row) == width:
            parsed.insert(0, row)
            row = []

    return parsed


def entropy(bitmap, color):
    color_occurrences = defaultdict(int)
    total = 0
    for row in bitmap:
        for pixel in row:
            if color == 'red':
                color_occurrences[pixel.red] += 1
                total += 1
            elif color == 'green':
                color_occurrences[pixel.green] += 1
                total += 1
            elif color == 'blue':
                color_occurrences[pixel.blue] += 1
                total += 1
            else:  # color == 'general'
                color_occurrences[pixel.red] += 1
                color_occurrences[pixel.green] += 1
                color_occurrences[pixel.blue] += 1
                total += 3

    result = 0
    for val, c in color_occurrences.items():
        result += c * math.log(c, 2)

    return math.log(total, 2) - (result / total)


def jpeg_loseless(bitmap, prediction_scheme):
    # we need the empty pixel because there cannot be a row above row 0 and pixel left to the pixel 0
    empty_pixel = Pixel(red=0, green=0, blue=0)
    result = []
    for row_index, row in enumerate(bitmap):
        row_encoded = []
        for pixel_index, pixel in enumerate(row):
            if row_index == 0:
                north = empty_pixel
            else:
                north = bitmap[row_index-1][pixel_index]

            if pixel_index == 0:
                west = empty_pixel
            else:
                west = bitmap[row_index][pixel_index-1]

            if row_index == 0 or pixel_index == 0:
                north_west = empty_pixel
            else:
                north_west = bitmap[row_index-1][pixel_index-1]

            encoding = (pixel - prediction_scheme(north, west, north_west)) % 256
            row_encoded.append(encoding)

        result.append(row_encoded)

    return result


def calculate_enc_entropies(enc) -> list:
    red_entropy = entropy(enc, 'red')
    green_entropy = entropy(enc, 'green')
    blue_entropy = entropy(enc, 'blue')
    general_entropy = entropy(enc, 'general')

    return [(red_entropy, 'red'), (green_entropy, 'green'), (blue_entropy, 'blue'), (general_entropy, 'general')]



def print_entropies(bitmap, file=None):
    if file:
        print('#---------##---------##---------#', file=file)
        for color in colors:
            print(color + ' entropy: ', entropy(bitmap, color), file=file)
        print('#---------##---------##---------#', file=file)
    else:
        print('#---------##---------##---------#')
        for color in colors:
            print(color + ' entropy: ', entropy(bitmap, color))
        print('#---------##---------##---------#')


path = sys.argv[1]

with open(path, 'rb') as f:
    image = f.read()

h = image[15]*256 + image[14]
w = image[13]*256 + image[12]

bitmap = image_to_bitmap(image[18:-26], h, w)

print('Picture entropy')
print_entropies(bitmap)

print('*----------------**----------------*')
for s_number, s in enumerate(prediction_schemes, 1):
    print('*----------------*')
    print('Prediction Scheme: ', s_number)
    encoded = jpeg_loseless(bitmap, s)

    entropies = calculate_enc_entropies(encoded)
    for ent_data in entropies:
        print(ent_data[1] + ': ', ent_data[0])

        if ent_data[0] < best_results_dict[ent_data[1]][0]:
            best_results_dict[ent_data[1]] = (ent_data[0], s_number)
print('*----------------**----------------*')


print('\nBest schemes')
for color, data in best_results_dict.items():
    print('Best ' + color + ': ', data[1])
