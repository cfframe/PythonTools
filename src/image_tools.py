# image_tools.py

import numpy as np


class ImageTools:
    """Utilities for manipulating images"""

    @staticmethod
    def pad_images_array_to_aspect_ratio(images: np.array, aspect_ratio: tuple) -> np.array:
        """Reshape rectangle with padding based on image edges. Assume colour images.

        :param images: array of images
        :param aspect_ratio: aspect ratio (x, y) of padded image using Cartesian coordinates
        :return: array of padded images
        """

        yi, xi = images.shape[-3], images.shape[-2]

        xj, yj = aspect_ratio

        new_images = []
        swap_axes = False
        to_process_images = False
        if yi >= xi and xj > yj:
            # Square or vertical rectangle to horizontal rectangle
            to_process_images = True
        elif xi >= yi and yj > xj:
            # Square or horizontal rectangle to vertical rectangle
            swap_axes = True
            to_process_images = True
            # Swap x and y dimensions
            images = np.transpose(images, axes=(0, 2, 1, 3))
            xi, yi = yi, xi
            xj, yj = yj, xj

        if to_process_images:
            yk = yi
            xk = (xj * yi) // yj
            delta_x = xk - xi

            for img in images:
                add_1 = img[:, 0, :]
                add_2 = img[:, -1, :]

                # Accommodate odd-numbered delta_x with xk - xi - delta_x // 2. Could end up with opposite sides
                # being appended with a difference of one strip of pixels
                axis = 1
                add_1n = np.tile(add_1[:, np.newaxis, :], (1, delta_x // 2, 1))
                add_2n = np.tile(add_2[:, np.newaxis, :], (1, xk - xi - delta_x // 2, 1))
                new_image = np.concatenate(
                    (add_1n,
                     img,
                     add_2n),
                    axis=axis)
                new_images.append(new_image)

            if swap_axes:
                new_images = np.transpose(new_images, axes=(0, 2, 1, 3))

        return new_images

    @staticmethod
    def crop_images_array_to_squares(images: np.array) -> np.array:
        """Crop rectangles to shorter dimension.

        :param images: array of images
        :return: array of cropped images
        """

        yi, xi = images.shape[-3], images.shape[-2]

        new_images = []
        swap_axes = False
        to_process_images = False

        if xi > yi:
            # Horizontal rectangle
            to_process_images = True
        elif yi > xi:
            # Vertical rectangle
            swap_axes = True
            to_process_images = True
            # Swap x and y dimensions
            images = np.transpose(images, axes=(0, 2, 1, 3))
            xi, yi = yi, xi

        if to_process_images:
            left_strip = (xi - yi) // 2
            for img in images:
                new_image = img[:, left_strip:left_strip + yi, :]
                new_images.append(new_image)

            if swap_axes:
                new_images = np.transpose(new_images, axes=(0, 2, 1, 3))

        return new_images

