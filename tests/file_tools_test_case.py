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

    def test_ensure_empty_sub_directory__when_dirpath_is_none__returns_value_error(self):
        with self.subTest(self):
            with self.assertRaises(ValueError):
                dummy = FileTools.ensure_empty_sub_directory(None)

    def test_ensure_empty_sub_directory__when_dirpath_exists__returns_exists_message(self):
        root = self.Root
        sub = 'test_folder'
        dir_path = os.path.join(self.Root, sub)
        expected = 'Directory exists'
        actual = FileTools.ensure_empty_sub_directory(dir_path)[:len(expected)]

        self.assertTrue(expected == actual)

    def test_ensure_empty_sub_directory__when_path_not_exists__returns_create_message(self):
        root = self.Root
        sub = 'temp_test_folder'
        dir_path = os.path.join(self.Root, sub)

        expected = 'Creating directory'
        actual = FileTools.ensure_empty_sub_directory(dir_path)

        self.assertTrue(expected == actual)

        # Clean up
        os.rmdir(dir_path)

    def test_ensure_empty_sub_directory__when_subdir_not_exists__creates_directory(self):
        root = self.Root
        sub = 'temp_test_folder'
        dir_path = os.path.join(root, sub)

        FileTools.ensure_empty_sub_directory(dir_path)

        self.assertTrue(Path(dir_path).exists())

        # Clean up after
        if Path(dir_path).exists():
            Path(dir_path).rmdir()
            if Path(dir_path).exists():
                fn = 'test_ensure_empty_sub_directory__when_subdir_not_exists__creates_directory'
                raise Exception('Unexpected error in {}'.format(fn))

    def test_ensure_empty_sub_directory__when_subdir_not_empty__removes_content(self):
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
        FileTools.ensure_empty_sub_directory(dir_path)
        expected = 0
        actual = len(os.listdir(dir_path))

        self.assertTrue(expected == actual)

        # Clean up
        shutil.rmtree(dir_path)

    def test_make_datetime_named_archive__returns_file_path_in_desired_format(self):
        root = self.Root
        sub = 'test_for_archive'
        test_file_name = 'TestFile.txt'
        dir_path = os.path.join(root, sub)
        src_file = os.path.join(root, test_file_name)
        test_file = os.path.join(dir_path, test_file_name)
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        shutil.copy(src_file, test_file)
        archive_format = 'zip'

        expected = datetime.datetime.now().strftime('%y%m%d_%H%M_') + sub + '.' + archive_format

        actual = Path(FileTools.make_datetime_named_archive(base_name=dir_path, format=archive_format,
                                                            root_dir=root, base_dir=sub)).name

        self.assertTrue(actual == expected)

        # clean up

        archive_path = os.path.join(root, actual)
        os.unlink(archive_path)

    def test_save_command_args_to_file__saves_expected_file(self):
        script = 'python_file'
        args = {'a_boolean': True, 'a_string': 'Some_string', 'a_number': 123}
        actual_save_path = os.path.join(self.Root, 'actual_command.txt')
        expected_save_path = os.path.join(self.Root, 'expected_command.txt')

        FileTools.save_command_args_to_file(script, args, actual_save_path)
        actual_save_path = Path(actual_save_path)

        with self.subTest(self, testing_for="saved file exists"):
            self.assertTrue(Path.exists(actual_save_path))

        with self.subTest(self, testing_for="saves expected content"):
            self.assertTrue(filecmp.cmp(expected_save_path, actual_save_path))

        # Clean up
        os.unlink(actual_save_path)


if __name__ == '__main__':
    unittest.main()
