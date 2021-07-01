from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

import os
from pathlib import Path

# Photo by Giulio Magnifico on Unsplash
# https://unsplash.com/@giuliomagnifico?utm_source=medium&utm_medium=referral

image_path = os.path.join(Path(__file__).parent.parent, 'images/dewdrop.jpg')
img = Image.open(image_path)
img.load()
img_array = np.asarray(img, dtype='int32')

print(f'img_array.shape: {img_array.shape}')

#  Show effects of minimising and maximising rgb
test1 = True
if test1:
    for channel in range(3):
        temp_image = np.copy(img_array)
        for colour_factor in range(2):
            brightness = 255 * colour_factor
            print(f'channel: {channel};  brightness: {brightness}')
            temp_image[:, :, channel] = brightness
            plt.imshow(temp_image)
            plt.show()

# Downsampling - from https://scikit-image.org/docs/dev/auto_examples/transform/plot_rescale.html
# - monochrome

import skimage
from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean
import math

test2 = True
if test2:

    image = color.rgb2gray(np.copy(img_array))

    image_rescaled = rescale(image, 0.25, anti_aliasing=False)
    image_resized = resize(image, (image.shape[0] // 4, image.shape[1] // 4),
                           anti_aliasing=True)
    image_downscaled = downscale_local_mean(image, (4, 3))

    fig, axes = plt.subplots(nrows=2, ncols=2)

    ax = axes.ravel()

    ax[0].imshow(image, cmap='gray')
    ax[0].set_title("Original image")

    ax[1].imshow(image_rescaled, cmap='gray')
    ax[1].set_title("Rescaled image (no aliasing)")

    ax[2].imshow(image_resized, cmap='gray')
    ax[2].set_title("Resized image (aliasing)")

    ax[3].imshow(image_downscaled, cmap='gray')
    ax[3].set_title("Downscaled image (no aliasing)")

    plt.tight_layout()
    plt.show()

# Downsampling - as above, but reworked for colour
test3 = True
if test3:

    image = np.copy(img_array)
    print(f'image pixel max: {np.max(image)}; pixel min: {np.min(image)}')
    # NB from scikit v0.19 on, multichannel is deprecated in favour of channel_axis
    image_rescaled = np.array(
        rescale(image, (0.25, 0.25), anti_aliasing=False, preserve_range=True, multichannel=True),
        dtype=int)
    temp_image = image_rescaled
    print('{} pixel max: {}; pixel min: {}; shape = {}'.format(
        'image_rescaled', np.max(temp_image), np.min(temp_image), temp_image.shape))

    # original example had anti_aliasing=True
    image_resized = np.array(
        resize(image, (64, 64, 3), preserve_range=True, anti_aliasing=False),
        dtype=int)
    temp_image = image_resized
    print('{} pixel max: {}; pixel min: {}; shape = {}'.format(
        'image_resized', np.max(temp_image), np.min(temp_image), temp_image.shape))

    # x_fact = math.floor(image.shape[0]/64)
    # y_fact = math.floor(image.shape[1]/64)
    # x_fact = math.ceil(image.shape[0]/64)
    # y_fact = math.ceil(image.shape[1]/64)
    x_fact = int(np.round(image.shape[0]/64))
    y_fact = int(np.round(image.shape[1]/64))
    # With downscale, cannot guarantee getting exactly 64 x 64
    image_downscaled = np.array(
        downscale_local_mean(image, (x_fact, y_fact, 1)),
        dtype=int)
    temp_image = image_downscaled
    print('{} pixel max: {}; pixel min: {}; shape = {}'.format(
        'image_downscaled', np.max(temp_image), np.min(temp_image), temp_image.shape))

    fig, axes = plt.subplots(nrows=2, ncols=2)

    ax = axes.ravel()

    ax[0].imshow(image)
    ax[0].set_title("Original image")

    ax[1].imshow(image_rescaled)
    ax[1].set_title("Rescaled image (no aliasing)")

    ax[2].imshow(image_resized)
    ax[2].set_title("Resized image (no aliasing)")

    ax[3].imshow(image_downscaled)
    ax[3].set_title("Downscaled image (no aliasing)")

    plt.tight_layout()
    plt.show()

