import os
import numpy as np
import cv2


def combine_pngs(path, output_path, extended_border=3):
    def iter_ij(path):
        for file in os.listdir(path):
            i, j = tuple(file.split('.')[0].split('_'))
            yield int(i) // 2, int(j) // 2

    max_i = 0
    max_j = 0
    for i, j in iter_ij(path):
        max_i = max(i + 1 + extended_border, max_i)
        max_j = max(j + 1 + extended_border, max_j)

    sample_image = cv2.imread(path + "0_0.png")
    image_height, image_width, _ = sample_image.shape
    output_width = image_width * max_j
    output_height = image_height * max_i
    print("max_i:{}, max_j:{}, image_width:{}, image_height:{}, output_width:{}, output_height:{}".format(
        max_i,
        max_j,
        image_width,
        image_height,
        output_width,
        output_height)
    )

    output_image = np.zeros((output_height, output_width, 3), np.uint8)
    for i in range(max_i):
        for j in range(max_j):
            file_path = path + '{}_{}.png'.format(i * 2, j * 2)
            sub_image = cv2.imread(file_path) if os.path.exists(file_path) else sample_image
            output_image[i * image_height:(i + 1) * image_height, j * image_width:(j + 1) * image_width, :] = sub_image[
                                                                                                              :, :, :]

    cv2.imwrite(output_path, output_image)


combine_pngs("C:\\Users\\sdq\\pngs\\", "C:\\Users\\sdq\\combined.png")
