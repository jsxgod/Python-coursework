import sys
import linde_buzo_gray as lbg
import util
import image_util as iu

assert len(sys.argv) == 4

input_file = sys.argv[1]
output_file = sys.argv[2]
colors = sys.argv[3]


with open(input_file, 'rb') as f:
    image = f.read()

top = image[:18]
bottom = image[-26:]
height = image[15] * 256 + image[14]
width = image[13] * 256 + image[12]

bitmap = iu.image_to_bitmap(image[18:-26], height, width)

code_book = lbg.prepare_code_book(bitmap, 2 ** int(colors))

bitmap2 = iu.quantify_bitmap(bitmap, code_book)
bitmap2_bytes = iu.bitmap_to_bytes(bitmap2)

ms_error = util.mean_square_error(bitmap, bitmap2)
sn_ratio = util.signal_noise_ratio(bitmap, ms_error)

print("Mean Square Error:", ms_error)
print("Signal Noise Ratio:", sn_ratio)

with open(output_file, "wb") as f:
    f.write(top + bitmap2_bytes + bottom)
