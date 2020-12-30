import util


def image_to_bitmap(img, h, w) -> list:
    b_map = []

    for i in range(h*w):
        rgb = (img[i * 3], img[i * 3 + 1], img[i * 3 + 2])
        b_map.append(rgb)

    return b_map


def quantify_bitmap(b_map, c_book) -> list:
    quantified = []
    for p in b_map:
        distances = [util.squared_euclid_distance(p, c) for c in c_book]
        min_distance = min(distances)
        min_distance_index = util.get_index(distances, min_distance)
        assert min_distance_index != -1
        quantified.append(c_book[min_distance_index])

    return quantified


def bitmap_to_bytes(b_map):
    result = []
    for x in b_map:
        for i in x:
            result.append(i)
    return bytes(result)
