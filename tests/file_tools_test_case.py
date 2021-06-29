# file_tools_test_case.py

import datetime
import filecmp
import os
import shutil
import unittest

from pathlib import Path
from src.file_tools import FileTools


class FileToolsTestCase(unittest.TestCase):
    """Test names are generally self-explanatory and so docstrings not provided on an individual basis other
    than by exception.

    Keyword arguments:
    TestCase -- standard class required for tests based on unittest.case
    """

    def setUp(self):
        """Fixtures used by tests."""
        self.Root = Path(__file__).parent

        self.TestFilePath = os.path.join(self.Root, 'TestFile.txt')
        # self.TestList = ['124.115.0.158', '119.230.103.254', '208.70.189.142']
        self.TestList = ['fred', 'woz', 'ere']

    def test_chunks_generator__yields_expected_lists(self):
        chunk_size = 2
        chunks = FileTools.chunks_generator(self.TestList, chunk_size)

        actual = next(chunks)
        expected = self.TestList[0:2]
        self.assertEqual(actual, expected)

        actual = next(chunks)
        expected = self.TestList[2:3]
        self.assertEqual(actual, expected)

    def test_ensure_empty_directory__when_dirpath_is_none__returns_value_error(self):
        with self.subTest(self):
            with self.assertRaises(ValueError):
                dummy = FileTools.ensure_empty_directory(None)

    def test_ensure_empty_directory__when_dirpath_exists__returns_exists_message(self):
        root = self.Root
        sub = 'test_folder'
        dir_path = os.path.join(self.Root, sub)
        expected = 'Directory exists'
        actual = FileTools.ensure_empty_directory(dir_path)[:len(expected)]

        self.assertTrue(expected == actual)

    def test_ensure_empty_directory__when_path_not_exists__returns_create_message(self):
        root = self.Root
        sub = 'temp_test_folder'
        dir_path = os.path.join(self.Root, sub)

        expected = 'Creating directory'
        actual = FileTools.ensure_empty_directory(dir_path)

        self.assertTrue(expected == actual)

        # Clean up
        os.rmdir(dir_path)

    def test_ensure_empty_directory__when_subdir_not_exists__creates_directory(self):
        root = self.Root
        sub = 'temp_test_folder'
        dir_path = os.path.join(root, sub)

        FileTools.ensure_empty_directory(dir_path)

        self.assertTrue(Path(dir_path).exists())

        # Clean up after
        if Path(dir_path).exists():
            Path(dir_path).rmdir()
            if Path(dir_path).exists():
                fn = 'test_ensure_empty_directory__when_subdir_not_exists__creates_directory'
                raise Exception('Unexpected error in {}'.format(fn))

    def test_ensure_empty_directory__when_subdir_not_empty__removes_content(self):
        root = self.Root
        sub = 'fred'
        test_file_name = 'TestFile.txt'
        dir_path = os.path.join(root, sub)
        src_file = os.path.join(root, test_file_name)
        target_file = os.path.join(dir_path, test_file_name)

        # Set up - ensure test dir exists with a file and a sub-dir with a file
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        shutil.copy(src_file, target_file)
        sub_dir_path = os.path.join(dir_path, sub)
        Path(sub_dir_path).mkdir(parents=True, exist_ok=True)
        target_file = os.path.join(sub_dir_path, test_file_name)
        shutil.copy(src_file, target_file)

        # Main test: To ensure content deleted if non empty directory
        FileTools.ensure_empty_directory(dir_path)
        expected = 0
        actual = len(os.listdir(dir_path))

        self.assertTrue(expected == actual)

        # Clean up
        shutil.rmtree(dir_path)

    def test_lines_list_from_file__returns_list(self):
        path = self.TestFilePath

        expected = self.TestList
        actual = FileTools.lines_list_from_file(path)
        self.assertListEqual(expected, actual)

    def test_make_datetime_named_archive__returns_file_path_in_desired_format(self):
        root = self.Root
        sub = 'test_for_archive'
        test_file_name = 'TestFile.txt'
        base_path_of_final_archive_file = os.path.join(root, sub)
        path_of_dir_to_archive = os.path.join(root, sub)
        src_file = os.path.join(root, test_file_name)
        test_file = os.path.join(base_path_of_final_archive_file, test_file_name)
        Path(base_path_of_final_archive_file).mkdir(parents=True, exist_ok=True)
        shutil.copy(src_file, test_file)
        archive_format = 'zip'

        expected = datetime.datetime.now().strftime('%y%m%d_%H%M_') + sub + '.' + archive_format

        actual = Path(FileTools.make_datetime_named_archive(base_name=base_path_of_final_archive_file,
                                                            format=archive_format,
                                                            dir_path_to_archive=path_of_dir_to_archive)).name

        self.assertTrue(actual == expected)

        # clean up

        archive_path = os.path.join(root, actual)
        os.unlink(archive_path)

    def test_save_command_args_to_file__saves_expected_file(self):
        args = {'a_boolean': True, 'a_string': 'Some_string', 'a_number': 123}

        actual_save_path = os.path.join(self.Root, 'actual_command.txt')
        expected_save_path = os.path.join(self.Root, 'expected_command.txt')

        # Note calls to sys.argv will show the test runner file in unittest, so can't verify the first line correctly.
        FileTools.save_command_args_to_file(args, actual_save_path)
        actual_save_path = Path(actual_save_path)

        with self.subTest(self, testing_for="saved file exists"):
            self.assertTrue(Path.exists(actual_save_path))

        with self.subTest(self, testing_for="saves expected content"):
            self.assertTrue(filecmp.cmp(expected_save_path, actual_save_path))

        # Clean up
        os.unlink(actual_save_path)


if __name__ == '__main__':
    unittest.main()
