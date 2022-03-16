# test_download_helper.py

import os
import shutil
import unittest

from pathlib import Path
from src.download_helper import DownloadHelper


class DownloadHelperTestCase(unittest.TestCase):
    """Test names are generally self-explanatory and so docstrings not provided on an individual basis other
    than by exception.

    Keyword arguments:
    TestCase -- standard class required for tests based on unittest.case
    """

    def setUp(self):
        """Fixtures used by tests."""
        self.Root = Path(__file__).parent
        self.FakePath = os.path.join(self.Root, "FakeTestFile.zip")
        self.RealFilePath = os.path.join(self.Root, "TestFile.txt")
        self.TestDestinationDir = os.path.join(self.Root, "test_folder")
        self.TestDestinationFile = os.path.join(self.TestDestinationDir, "TestFile.txt")
        self.EmptyFolder = os.path.join(self.Root, "empty_folder")
        self.NonEmptyFolder = os.path.join(self.Root, "test_for_archive")

    def test_can_download__when_target_is_not_file__returns_true(self):
        test_file = self.FakePath

        with self.subTest(self, testing_for='use default replace_download'):
            self.assertTrue(DownloadHelper.can_download(target_download_path=test_file))
        with self.subTest(self, testing_for='replace_download is False'):
            self.assertTrue(DownloadHelper.can_download(target_download_path=test_file, replace_download=False))
        with self.subTest(self, testing_for='replace_download is True'):
            self.assertTrue(DownloadHelper.can_download(target_download_path=test_file, replace_download=True))

    def test_can_download__when_target_is_file__uses_replace_download(self):
        test_file = self.RealFilePath

        # Not testing user input route yet, would need to fake it
        with self.subTest(self, testing_for='replace_download is False'):
            self.assertFalse(DownloadHelper.can_download(target_download_path=test_file, replace_download=False))
        with self.subTest(self, testing_for='replace_download is True'):
            self.assertTrue(DownloadHelper.can_download(target_download_path=test_file, replace_download=True))

    def test_can_extract_to_extraction_dir__when_target_is_not_dir__returns_true(self):
        test_path = self.FakePath

        with self.subTest(self):
            self.assertTrue(DownloadHelper.can_extract_to_extraction_dir(unzip_dir=test_path))
        with self.subTest(self):
            self.assertTrue(DownloadHelper.can_extract_to_extraction_dir(unzip_dir=test_path,
                                                                         replace_content=False))
        with self.subTest(self):
            self.assertTrue(DownloadHelper.can_extract_to_extraction_dir(unzip_dir=test_path,
                                                                         replace_content=True))

    def test_can_extract_to_extraction_dir__when_empty_target_exists__uses_replace_destination_dir(self):
        test_path = self.TestDestinationDir

        # Not testing user input route - would need to fake it
        with self.subTest(self):
            # Start with empty test dir
            self.assertTrue(DownloadHelper.can_extract_to_extraction_dir(unzip_dir=test_path,
                                                                         replace_content=False))
            self.assertTrue(DownloadHelper.can_extract_to_extraction_dir(unzip_dir=test_path,
                                                                         replace_content=True))

    def test_can_extract_to_extraction_dir__when_non_empty_target_exists__uses_replace_destination_dir(self):
        test_path = self.TestDestinationDir
        # Add temp file
        shutil.copy(self.RealFilePath, self.TestDestinationDir)

        # Not testing user input route - would need to fake it
        with self.subTest(self):
            # Start with empty test dir
            self.assertFalse(DownloadHelper.can_extract_to_extraction_dir(unzip_dir=test_path,
                                                                          replace_content=False))
            self.assertTrue(DownloadHelper.can_extract_to_extraction_dir(unzip_dir=test_path,
                                                                         replace_content=True))

        # Clean up - remove test file
        os.remove(self.TestDestinationFile)

    def test_get_extraction_isic_dir_path__when_known_file_endswith__returns_path(self):
        test_path = self.TestDestinationDir
        dir_name = 'training_input'
        filename = 'dummy' + dir_name + '.zip'
        filepath = Path(DownloadHelper.get_extraction_isic_dir_path(test_path, filename))
        self.assertTrue(filepath.name == dir_name)

    def test_get_extraction_isic_dir_path__when_unknown_file_endswith__returns_empty_string(self):
        test_path = self.TestDestinationDir
        dir_name = 'fred'
        filename = 'dummy' + dir_name + '.zip'
        filepath = Path(DownloadHelper.get_extraction_isic_dir_path(test_path, filename))
        self.assertTrue(filepath.name == '')

    def test_get_extraction_dir_path__returns_expected_path(self):
        test_path = self.TestDestinationDir

        with self.subTest(self, testing_for='zip file'):
            filename = 'dummy.zip'
            filepath = Path(DownloadHelper.get_extraction_dir_path(test_path, filename))
            self.assertTrue(filepath.name == Path(filename).stem)

        with self.subTest(self, testing_for='numpy archive file'):
            filename = 'dummy.tar.gz'
            filepath = Path(DownloadHelper.get_extraction_dir_path(test_path, filename))
            self.assertTrue(filepath.name == Path(Path(filename).stem).stem)

    def test_to_download(self):
        with self.subTest(self, testing_for='non-archive file'):
            target_path = self.EmptyFolder
            replace_download = True
            can_extract_to_extraction_dir = False
            extraction_dir = ''
            actual = DownloadHelper.to_download(target_download_path=target_path, replace_download=replace_download,
                                                can_extract_to_extraction_dir=can_extract_to_extraction_dir,
                                                extraction_dir=extraction_dir)
            self.assertTrue(actual)

        with self.subTest(self, testing_for='archive file, replace download'):
            target_path = self.EmptyFolder
            replace_download = True
            can_extract_to_extraction_dir = True
            extraction_dir = self.EmptyFolder
            actual = DownloadHelper.to_download(target_download_path=target_path, replace_download=replace_download,
                                                can_extract_to_extraction_dir=can_extract_to_extraction_dir,
                                                extraction_dir=extraction_dir)
            self.assertTrue(actual)

        with self.subTest(self, testing_for='archive file, do not replace download, file existing'):
            target_path = self.RealFilePath
            replace_download = False
            can_extract_to_extraction_dir = True
            extraction_dir = self.EmptyFolder
            actual = DownloadHelper.to_download(target_download_path=target_path, replace_download=replace_download,
                                                can_extract_to_extraction_dir=can_extract_to_extraction_dir,
                                                extraction_dir=extraction_dir)
            self.assertFalse(actual)

        with self.subTest(self, testing_for='archive file, do replace download, file existing'):
            target_path = self.RealFilePath
            replace_download = True
            can_extract_to_extraction_dir = True
            extraction_dir = self.NonEmptyFolder
            actual = DownloadHelper.to_download(target_download_path=target_path, replace_download=replace_download,
                                                can_extract_to_extraction_dir=can_extract_to_extraction_dir,
                                                extraction_dir=extraction_dir)
            self.assertTrue(actual)

        with self.subTest(self, testing_for='archive file, do replace download, cannot do extraction'):
            target_path = self.RealFilePath
            replace_download = True
            can_extract_to_extraction_dir = False
            extraction_dir = self.NonEmptyFolder
            actual = DownloadHelper.to_download(target_download_path=target_path, replace_download=replace_download,
                                                can_extract_to_extraction_dir=can_extract_to_extraction_dir,
                                                extraction_dir=extraction_dir)
            self.assertFalse(actual)


if __name__ == '__main__':
    unittest.main()
