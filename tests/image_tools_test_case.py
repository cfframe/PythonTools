from unittest import TestCase

import datetime
import filecmp
import numpy as np
import os
import shutil
import unittest

from pathlib import Path
from PIL import Image
from src.file_tools import FileTools
from src.image_tools import ImageTools


class ImageToolsTestCase(TestCase):
    """Test names are generally self-explanatory and so docstrings not provided on an individual basis other
    than by exception.

    Keyword arguments:
    TestCase -- standard class required for tests based on unittest.case
    """

    def setUp(self):
        """Fixtures used by tests."""
        self.Root = Path(__file__).parent

        self.TestFilePath = os.path.join(self.Root, 'TestFile.txt')
        self.SourceImagesDir = os.path.join(self.Root, 'source_files')
        self.ImageList = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg']
        self.NewImagesFolder = os.path.join(self.Root, 'new_images')
        self.SquareImagePaths = [os.path.join(self.SourceImagesDir, i) for i in self.ImageList]
        self.WideImagesDir = os.path.join(self.Root, 'wide_images')
        self.WideImagePaths = [os.path.join(self.WideImagesDir, i) for i in self.ImageList]
        self.HighImagesDir = os.path.join(self.Root, 'high_images')
        self.HighImagePaths = [os.path.join(self.HighImagesDir, i) for i in self.ImageList]

        FileTools.ensure_empty_directory(self.NewImagesFolder)

    def tearDown(self) -> None:
        FileTools.ensure_empty_directory(self.NewImagesFolder)

    def test_pad_images_array_to_aspect_ratio(self):
        images = [np.array(Image.open(image_path)) for image_path in self.SquareImagePaths]
        new_paths = [os.path.join(self.NewImagesFolder, i) for i in self.ImageList]

        with self.subTest(self, testing_for='pad to high rectangle'):
            new_images = ImageTools.pad_images_array_to_aspect_ratio(images, (3, 4))
            for i in range(len(new_images)):
                img = Image.fromarray(new_images[i], 'RGB')
                img.save(new_paths[i])

            ref_image_path = os.path.join(self.SourceImagesDir, 'image1high.jpg')

            self.assertTrue(filecmp.cmp(new_paths[0], ref_image_path))

        with self.subTest(self, testing_for='pad to wide rectangle'):
            new_images = ImageTools.pad_images_array_to_aspect_ratio(images, (4, 3))
            for i in range(len(new_images)):
                img = Image.fromarray(new_images[i], 'RGB')
                img.save(new_paths[i])
            ref_image_path = os.path.join(self.SourceImagesDir, 'image1wide.jpg')

            self.assertTrue(filecmp.cmp(new_paths[0], ref_image_path))

        with self.subTest(self, testing_for='pad wide rectangle to square'):
            images = [np.array(Image.open(image_path)) for image_path in self.WideImagePaths]
            new_images = ImageTools.pad_images_array_to_aspect_ratio(images, (1, 1))
            for i in range(len(new_images)):
                img = Image.fromarray(new_images[i], 'RGB')
                img.save(new_paths[i])
            ref_image_path = os.path.join(self.SourceImagesDir, 'image1bigsquare1.jpg')

            self.assertTrue(filecmp.cmp(new_paths[0], ref_image_path))

        with self.subTest(self, testing_for='pad high rectangle to square'):
            images = [np.array(Image.open(image_path)) for image_path in self.HighImagePaths]
            new_images = ImageTools.pad_images_array_to_aspect_ratio(images, (1, 1))
            for i in range(len(new_images)):
                img = Image.fromarray(new_images[i], 'RGB')
                img.save(new_paths[i])
            ref_image_path = os.path.join(self.SourceImagesDir, 'image1bigsquare2.jpg')

            self.assertTrue(filecmp.cmp(new_paths[0], ref_image_path))

    def test_crop_images_array_to_squares(self):
        new_paths = [os.path.join(self.NewImagesFolder, i) for i in self.ImageList]

        with self.subTest(self, testing_for='wide rectangle to square'):
            images = [np.array(Image.open(image_path)) for image_path in self.WideImagePaths]
            images = np.asarray(images, dtype='uint8')

            square_images = ImageTools.crop_images_array_to_squares(images)

            for i in range(len(square_images)):
                img = Image.fromarray(square_images[i], 'RGB')
                img.save(new_paths[i])

            ref_image_path = os.path.join(self.SourceImagesDir, 'image1square1.jpg')

            self.assertTrue(filecmp.cmp(new_paths[0], ref_image_path))

        with self.subTest(self, testing_for='high rectangle to square'):
            images = [np.array(Image.open(image_path)) for image_path in self.HighImagePaths]
            images = np.asarray(images, dtype='uint8')

            square_images = ImageTools.crop_images_array_to_squares(images)

            for i in range(len(square_images)):
                img = Image.fromarray(square_images[i], 'RGB')
                img.save(new_paths[i])

            ref_image_path = os.path.join(self.SourceImagesDir, 'image1square2.jpg')

            self.assertTrue(filecmp.cmp(new_paths[0], ref_image_path))

    def test_crop_images_centre(self):
        new_paths = [os.path.join(self.NewImagesFolder, i) for i in self.ImageList]

        with self.subTest(self, testing_for='wide rectangle to square'):
            images = [Image.open(image_path) for image_path in self.WideImagePaths]

            square_images = ImageTools.crop_images_centre(images)

            for i in range(len(square_images)):
                img = square_images[i]
                img.save(new_paths[i])

            ref_image_path = os.path.join(self.SourceImagesDir, 'image1square1.jpg')

            self.assertTrue(filecmp.cmp(new_paths[0], ref_image_path))

        with self.subTest(self, testing_for='wide rectangle to circle'):
            images = [Image.open(image_path) for image_path in self.WideImagePaths]

            square_images = ImageTools.crop_images_centre(images, make_circle=True)

            for i in range(len(square_images)):
                img = square_images[i]
                img.save(new_paths[i])

            ref_image_path = os.path.join(self.SourceImagesDir, 'image1circle2.jpg')

            self.assertTrue(filecmp.cmp(new_paths[0], ref_image_path))

    def test_circle_crop_square_images(self):
        new_paths = [os.path.join(self.NewImagesFolder, i) for i in self.ImageList]

        images = [Image.open(image_path) for image_path in self.SquareImagePaths]

        circle_images = ImageTools.circle_crop_square_images(images)

        for i in range(len(circle_images)):
            img = circle_images[i]
            img.save(new_paths[i])

        ref_image_path = os.path.join(self.SourceImagesDir, 'image1circle.jpg')

        self.assertTrue(filecmp.cmp(new_paths[0], ref_image_path))

    def test_random_rotate_image(self):
        # todo: refactor so that can test rotation with padding on a fixed rotational value, which could be testable
        new_paths = [os.path.join(self.NewImagesFolder, i) for i in self.ImageList]
        count = 5
        images = [Image.open(image_path) for image_path in self.WideImagePaths]
        for i in range(len(images)):
            rotated_images = ImageTools.random_rotate_image(images[i], count=count)

            for j in range(count):
                img = rotated_images[j]
                img.convert('RGB').save(new_paths[i].replace('.jpg', f'_{j}.jpg'))

        print('done')
