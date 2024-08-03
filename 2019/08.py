import numpy as np


with open("./2019/resources/8.txt") as f:
    text = f.read().strip()


def problem_1() -> None:
    img_data = [int(x) for x in text]
    width, height = 25, 6
    img = np.array(img_data).reshape((-1, height, width))
    num_zeros = np.count_nonzero(img == 0, axis=(1, 2))
    layer_idx = np.argmin(num_zeros)
    print(np.count_nonzero(img[layer_idx, :, :] == 1) * np.count_nonzero(img[layer_idx, :, :] == 2))


def problem_2() -> None:
    img_data = [int(x) for x in text]
    width, height = 25, 6
    img = np.array(img_data).reshape((-1, height, width))
    has_black_pixel = np.count_nonzero(img == 0, axis=0) > 0
    has_white_pixel = np.count_nonzero(img == 1, axis=0) > 0
    first_black = np.argmax(img == 0, axis=0)
    first_white = np.argmax(img == 1, axis=0)

    final_image = np.where(has_black_pixel & has_white_pixel, first_white < first_black, has_white_pixel)
    for row in final_image:
        print("".join("█" if char else " " for char in row))
