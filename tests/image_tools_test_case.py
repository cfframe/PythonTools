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
from tqdm import tqdm


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
        self.CornerImagesDir = os.path.join(self.Root, 'corner_images')
        self.CornerImagePaths = [os.path.join(self.CornerImagesDir, i)
                                 for i in ['black.jpg', 'multicoloured.jpg', 'ISIC_0034505.jpg']]

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

    def test_image_corner_colours(self):
        new_paths = [os.path.join(self.NewImagesFolder, i) for i in self.ImageList]
        images = [Image.open(image_path) for image_path in self.CornerImagePaths]
        for i in range(len(images)):
            has_black_corners = ImageTools.are_image_corners_black(images[i])
            print(f'File {images[i].filename}, black corners? {has_black_corners}')

    def test_NOT_A_TEST(self):

        src_dir = 'C://GitHub//cfframe//spatial-skin-vae//data//isic2018_unclassed//train//unknown'
        trg_dir = 'C://GitHub//cfframe//PythonTools//tests//temp'
        FileTools.ensure_empty_directory(trg_dir)
        image_files = []
        for root, dirs, files in os.walk(src_dir, topdown=False):
            image_files = [os.path.join(src_dir, file) for file in files if file.endswith('.jpg')]

        progress_bar = tqdm(total=len(image_files) // 100)
        i = 0
        while i * 100 < len(image_files):
            images = [Image.open(image_path) for image_path
                      in image_files[i * 100: np.min([(i + 1) * 100, len(image_files)])]]
            for image in images:
                if ImageTools.are_image_corners_black(image):
                    shutil.copyfile(image.filename, image.filename.replace(src_dir, trg_dir))

            i += 1
            progress_bar.update(1)

        progress_bar.close()

        print('done')
