# image_tools.py

import numpy as np
from PIL import Image, ImageDraw
import random


class ImageTools:
    """Utilities for manipulating images"""

    @staticmethod
    def pad_images_array_to_aspect_ratio_reflect(images: np.array, aspect_ratio: tuple) -> np.array:
        """Reshape rectangle with padding based on image edges using reflection. Assume colour images.

        :param images: array of images
        :param aspect_ratio: aspect ratio (x, y) of padded image using Cartesian coordinates
        :return: array of padded images
        """

        images = np.asarray(images, dtype='uint8')

        yi, xi = images.shape[-3], images.shape[-2]

        xj, yj = aspect_ratio

        new_images = []
        swap_axes = False
        to_process_images = False
        if float(yi)/xi > float(yj)/xj:
            # Square or vertical rectangle to horizontal rectangle
            # or vertical rectangle to square
            to_process_images = True
        elif float(yi)/xi < float(yj)/xj:
            # Square or horizontal rectangle to vertical rectangle
            # or horizontal rectangle to square
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
        else:
            # No change, so return original images
            new_images = images

        return new_images

    @staticmethod
    def pad_images_array_to_aspect_ratio(images: np.array, aspect_ratio: tuple) -> np.array:
        """Reshape rectangle with padding based on image edges. Assume colour images.

        :param images: array of images
        :param aspect_ratio: aspect ratio (x, y) of padded image using Cartesian coordinates
        :return: array of padded images
        """

        images = np.asarray(images, dtype='uint8')

        yi, xi = images.shape[-3], images.shape[-2]

        xj, yj = aspect_ratio

        new_images = []
        swap_axes = False
        to_process_images = False
        if float(yi)/xi > float(yj)/xj:
            # Square or vertical rectangle to horizontal rectangle
            # or vertical rectangle to square
            to_process_images = True
        elif float(yi)/xi < float(yj)/xj:
            # Square or horizontal rectangle to vertical rectangle
            # or horizontal rectangle to square
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
        else:
            # No change, so return original images
            new_images = images

        return new_images

    @staticmethod
    def crop_images_array_to_squares(images: np.array) -> np.array:
        """Crop rectangles to shorter dimension.

        :param images: array of images
        :return: array of cropped images
        """

        images = np.asarray(images, dtype='uint8')
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

    @staticmethod
    def crop_images_centre(pil_images: list, make_circle: bool = False):
        """Crop images to shorter dimension.

        Assumes all source images are the same dimension

        :param pil_images: list of images
        :param make_circle: flag for whether to crop to circle (default: False)
        :return: list of cropped images
        """

        img_width, img_height = pil_images[0].size
        crop_size = np.min((img_width, img_height))

        cropped_images = []
        for pil_image in pil_images:
            cropped_images.append(
                pil_image.crop(
                    ((img_width - crop_size) // 2,
                     (img_height - crop_size) // 2,
                     (img_width + crop_size) // 2,
                     (img_height + crop_size) // 2)
                )
            )

        if make_circle:
            cropped_images = ImageTools.circle_crop_square_images(cropped_images)

        return cropped_images

    @staticmethod
    def circle_crop_square_images(pil_images: list):
        """Circle crop images

        Assumes all source images are the square

        :param pil_images: list of images
        :return: list of cropped images
        """

        circle_images = []
        pil_image = pil_images[0]
        background = Image.new(pil_image.mode, pil_image.size, 0)
        mask = Image.new('L', pil_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, pil_image.size[0], pil_image.size[1]), fill=255)

        for pil_image in pil_images:

            circle_images.append(
                Image.composite(pil_image, background, mask)
            )

        return circle_images

    @staticmethod
    def random_rotate_image(pil_image, count: int):
        """Generate rotated versions of a list of images, with padding based on outer edges.

        :param pil_image: PIL image
        :param count: number of output images
        :return: list of rotated images
        """
        # todo: refactor so that can test rotation with padding on a fixed rotational value, which could be testable

        # Enlarge to a rectangle based on diagonal, enlarge to a square, rotate then crop to original dimensions.
        x, y = size = pil_image.size

        diagonal = int(np.ceil(np.sqrt(pil_image.size[0] ** 2 + pil_image.size[1] ** 2)))
        pil_image = [np.array(pil_image)]

        aspect_ratio = (diagonal, y)

        pil_image = ImageTools.pad_images_array_to_aspect_ratio(pil_image, aspect_ratio)
        pil_image = ImageTools.pad_images_array_to_aspect_ratio(pil_image, (1, 1))
        pil_image = Image.fromarray(pil_image[0])

        rotated_images = []
        rotations = [random.random() * 360 for dummy in range(count)]
        for rot in range(count):
            rot_image = pil_image.rotate(rotations[rot])
            # Crop to original size
            left = (rot_image.size[0] - size[0]) // 2
            right = left + size[0]
            upper = (rot_image.size[1] - size[1]) // 2
            lower = upper + size[1]
            rot_image = rot_image.crop((left, upper, right, lower))
            rotated_images.append(rot_image)

        return rotated_images

    @staticmethod
    def image_corner_colours(pil_image) -> list:
        np_image = [np.array(pil_image)]
        width, height = pil_image.size
        pixels = pil_image.getdata()
        # Corners at (0, 0), (width, 0), (0, height), (width, height). Allow for zero based coordinates
        corners = [pixels[0], pixels[width - 1], pixels[width * (height - 1)], pixels[width * height - 1]]

        return corners

    @staticmethod
    def are_image_corners_black(pil_image) -> bool:
        # Arbitrary choice of rgb values of <10 being considered as black
        colours = ImageTools.image_corner_colours(pil_image)
        are_black = True
        for colour in colours:
            are_black = are_black and colour[0] < 10 and colour[1] < 10 and colour[2] < 10

        return are_black

