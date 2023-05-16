# test_file_tools.py

import datetime
import filecmp
import numpy as np
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
        self.TestExcelWorkbookPath = os.path.join(self.Root, 'TestExcelWorkbook.xlsx')
        # self.TestList = ['124.115.0.158', '119.230.103.254', '208.70.189.142']
        self.TestList = ['fred', 'woz', 'ere']
        self.ClassedFileListFile = os.path.join(self.Root, 'ClassedFileList.csv')
        self.FolderList = ['Class 1', 'Class 2', 'Class 3', 'Class 4']
        self.SourceImagesDir = os.path.join(self.Root, 'source_files')
        self.NewFolderRoot = os.path.join(self.Root, 'test_for_new_folders')
        self.ImagesFolder = os.path.join(self.Root, 'source_files')
        self.UnclassedParentFolder = os.path.join(self.Root, 'unclassed_parent')
        self.TrainingRawFolder = os.path.join(self.Root, 'training_raw')
        self.ShallowFolder = os.path.join(self.Root, 'test_folder')
        self.DeepFolder = os.path.join(self.ShallowFolder, 'nested')
        self.DeepSourceFiles = os.path.join(self.Root, 'deep_source_files')
        self.DeepSourceFilesSuffixed = os.path.join(self.Root, 'deep_source_files_suffixed')
        self.CollatedFolder = os.path.join(self.Root, 'collated_folder')
        self.NotebookFilePath = os.path.join(self.Root, 'notebooks', 'TestNotebook.ipynb')
        FileTools.ensure_empty_directory(self.NewFolderRoot)
        FileTools.ensure_empty_directory(self.TrainingRawFolder)
        shutil.copytree(self.SourceImagesDir, self.TrainingRawFolder, dirs_exist_ok=True)
        FileTools.ensure_empty_directory(self.DeepFolder)
        shutil.copy(self.TestFilePath, os.path.join(self.DeepFolder, Path(self.TestFilePath).name))
        FileTools.ensure_empty_directory(self.CollatedFolder)

    def tearDown(self) -> None:
        FileTools.ensure_empty_directory(self.NewFolderRoot)
        FileTools.ensure_empty_directory(self.UnclassedParentFolder)
        FileTools.ensure_empty_directory(self.ShallowFolder)
        FileTools.ensure_empty_directory(self.CollatedFolder)

    def test_chunks_generator__yields_expected_lists(self):
        chunk_size = 2
        chunks = FileTools.chunks_generator(self.TestList, chunk_size)

        actual = next(chunks)
        expected = self.TestList[0:2]
        self.assertEqual(actual, expected)

        actual = next(chunks)
        expected = self.TestList[2:3]
        self.assertEqual(actual, expected)

    def test_copy_files_to_class_dirs__files_copied(self):
        info_file_path = self.ClassedFileListFile
        separator = ','
        src_root = self.SourceImagesDir
        targ_root = self.NewFolderRoot

        FileTools.copy_files_to_class_dirs(info_file_path=info_file_path, separator=separator,
                                           src_root=src_root, target_root=targ_root, extension='jpg')

        with self.subTest(self, testing_for='image1.jpg copied to dir Class 2'):

            file_path = Path(os.path.join(self.NewFolderRoot, 'Class 2', 'image1.jpg'))
            self.assertTrue(Path.exists(file_path))

        with self.subTest(self, testing_for='image4.jpg copied to dir Class 1'):

            file_path = Path(os.path.join(self.NewFolderRoot, 'Class 2', 'image1.jpg'))
            self.assertTrue(Path.exists(file_path))

    def test_copy_file_splits_to_class_dirs__files_copied_in_splits(self):
        info_file_path = self.ClassedFileListFile
        separator = ','
        src_root = self.SourceImagesDir
        split1 = os.path.join(self.NewFolderRoot, 'split1')
        split2 = os.path.join(self.NewFolderRoot, 'split2')
        split3 = os.path.join(self.NewFolderRoot, 'split3')
        targ_roots = [split1, split2, split3]
        targ_splits = [1, 3, 2]

        FileTools.copy_file_splits_to_class_dirs(info_file_path=info_file_path, separator=separator, src_root=src_root,
                                                 split_roots=targ_roots,
                                                 splits=targ_splits,
                                                 extension='jpg')

        split_class = 'Class 1'
        split_folder = 'split1'
        expected = 1
        with self.subTest(self, testing_for=f'{split_folder} {split_class}'):
            actual = len(os.listdir(os.path.join(os.path.join(self.NewFolderRoot, split_folder), split_class)))
            self.assertEqual(actual, expected)

        split_folder = 'split2'
        expected = 3
        with self.subTest(self, testing_for=f'{split_folder} {split_class}'):
            actual = len(os.listdir(os.path.join(os.path.join(self.NewFolderRoot, split_folder), split_class)))
            self.assertEqual(actual, expected)

        split_folder = 'split3'
        expected = 2
        with self.subTest(self, testing_for=f'{split_folder} {split_class}'):
            actual = len(os.listdir(os.path.join(os.path.join(self.NewFolderRoot, split_folder), split_class)))
            self.assertEqual(actual, expected)

    def test_create_dirs_from_file_header__returns_folder_list(self):
        actual = FileTools.create_dirs_from_file_header(self.ClassedFileListFile, ',', self.NewFolderRoot)
        expected = self.FolderList

        self.assertEqual(actual, expected)

    def test_create_dirs_from_file_header__creates_dirs(self):
        dir_names = FileTools.create_dirs_from_file_header(self.ClassedFileListFile, ',', self.NewFolderRoot)

        with self.subTest(self, testing_for='first folder'):
            dir_path = Path(os.path.join(self.NewFolderRoot, dir_names[0]))
            self.assertTrue(Path.exists(dir_path))

        with self.subTest(self, testing_for='last folder'):
            dir_path = Path(os.path.join(self.NewFolderRoot, dir_names[-1]))
            self.assertTrue(Path.exists(dir_path))
        
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

    def test_make_datetime_named_archive__default_datestamp__returns_file_path_in_desired_format(self):
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

        datestamp = datetime.datetime.now()
        expected = f'{datestamp.strftime("%y%m%d_%H%M")}_{sub}.{archive_format}'

        actual = Path(FileTools.make_datetime_named_archive(
            src_path_to_archive=path_of_dir_to_archive,
            base_target_path=base_path_of_final_archive_file,
            format=archive_format)).name

        self.assertTrue(actual == expected)

        # clean up

        archive_path = os.path.join(root, actual)
        os.unlink(archive_path)

    def test_make_datetime_named_archive__supplied_datestamp__returns_file_path_in_desired_format(self):
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

        datestamp = datetime.datetime(2022, 1, 1, 0, 1)
        expected = f'{datestamp.strftime("%y%m%d_%H%M")}_{sub}.{archive_format}'

        actual = Path(FileTools.make_datetime_named_archive(
            src_path_to_archive=path_of_dir_to_archive,
            base_target_path=base_path_of_final_archive_file,
            format=archive_format,
            datestamp=datestamp
        )).name

        self.assertTrue(actual == expected)

        # clean up

        archive_path = os.path.join(root, actual)
        os.unlink(archive_path)

    def test_save_command_args_to_file__saves_expected_content(self):
        args = {'a_boolean': True, 'a_string': 'Some_string', 'a_number': 123}

        actual_save_path = os.path.join(self.Root, 'actual_command.txt')
        expected_save_path = os.path.join(self.Root, 'expected_command.txt')

        # Calls to save_command_args_to_file saves the calling command in the first line. As such, can't verify the
        # first line consistently in tests as calling tests via the Terminal saves a different command to calling
        # them via the IDE - so, compare the content after the first line, not the files themselves.

        FileTools.save_command_args_to_file(args, actual_save_path)
        actual_save_path = Path(actual_save_path)

        with self.subTest(self, testing_for='saved file exists'):
            self.assertTrue(Path.exists(actual_save_path))

        # Both files have two lines at the start which cannot be compared in all scenarios, so ignore them
        with open(actual_save_path, 'r') as actual_file:
            actual_lines = actual_file.readlines()[2:]
        with open(expected_save_path, 'r') as expected_file:
            expected_lines = expected_file.readlines()[2:]

        with self.subTest(self, testing_for='saves expected content'):
            self.assertEqual(expected_lines, actual_lines)

        # Clean up
        os.unlink(actual_save_path)

    def test_create_numpy_archive_from_images_dir__saves_file(self):
        images_file_path = os.path.join(self.NewFolderRoot, 'images')

        FileTools.create_numpy_archive_from_images_dir(self.ImagesFolder, images_file_path, (12, 12), '.jpg')

        final_images_file_path = images_file_path + '.npy'
        with self.subTest(self, testing_for="image file saved"):
            self.assertTrue(Path.exists(Path(final_images_file_path)))

        with self.subTest(self, testing_for='saved file has images'):
            images = np.load(final_images_file_path)
            print(images.shape)

    def test_create_numpy_archive_from_images_dir__when_using_defaults__saves_file(self):
        images_file_path = os.path.join(self.NewFolderRoot, 'images')

        FileTools.create_numpy_archive_from_images_dir(self.ImagesFolder, images_file_path)

        final_images_file_path = images_file_path + '.npy'
        with self.subTest(self, testing_for="image file saved"):
            self.assertTrue(Path.exists(Path(final_images_file_path)))

        with self.subTest(self, testing_for='saved file has images'):
            images = np.load(file=final_images_file_path, allow_pickle=True)
            print(images.shape)

    def test_path_of_first_file_of_type__when_found__returns_path(self):

        with self.subTest(self, testing_for='file exists'):
            extension = '.jpg'
            expected = os.path.join(self.SourceImagesDir, 'image1.jpg')
            actual = FileTools.path_of_first_file_of_type(directory=self.SourceImagesDir, extension=extension)

            self.assertTrue(actual.lower() == expected.lower())

        with self.subTest(self, testing_for='no file with extension exists'):
            extension = '.xxx'
            expected = ''
            actual = FileTools.path_of_first_file_of_type(directory=self.SourceImagesDir, extension=extension)

            self.assertTrue(actual.lower() == expected.lower())

        with self.subTest(self, testing_for='deeper nested directory'):
            extension = '.txt'
            expected = os.path.join(self.DeepFolder, 'TestFile.txt')
            actual = FileTools.path_of_first_file_of_type(directory=self.ShallowFolder, extension=extension)

            self.assertTrue(actual.lower() == expected.lower())

    def test_dataset_type_from_name(self):
        expected = 'invalid'
        with self.subTest(self, testing_for=expected):
            actual = FileTools.dataset_type_from_name('fred')
            self.assertEqual(actual, expected)
        expected = 'train'
        with self.subTest(self, testing_for=expected):
            actual = FileTools.dataset_type_from_name('training stuff')
            self.assertEqual(actual, expected)
        expected = 'validation'
        with self.subTest(self, testing_for=expected):
            actual = FileTools.dataset_type_from_name('validation stuff')
            self.assertEqual(actual, expected)
        expected = 'test'
        with self.subTest(self, testing_for=expected):
            actual = FileTools.dataset_type_from_name('test stuff')
            self.assertEqual(actual, expected)

    def test_copy_dir_as_unclassed(self):
        with self.subTest(self, testing_for='Invalid'):
            actual = FileTools.copy_dir_as_unclassed(self.SourceImagesDir, self.UnclassedParentFolder)
            expected = 'Invalid'
            self.assertTrue(actual == expected)
        with self.subTest(self, testing_for='Copied'):
            target_dir = FileTools.copy_dir_as_unclassed(self.TrainingRawFolder, self.UnclassedParentFolder)
            actual = len(os.listdir(target_dir))
            expected = len(os.listdir(self.SourceImagesDir))
            self.assertTrue(actual == expected)

    # def test_collate_files_by_low_level_dir_name(self):
    #     source_dir = self.DeepSourceFiles
    #     target_dir = self.CollatedFolder
    #     source_name = Path(source_dir).name
    #     target_name = Path(target_dir).name
    #     low_level_dir_name = 'Start'
    #     path_parts_re = [[source_name, target_name],
    #                      [r'\\Ch\d+', ''],
    #                      [r'\\Start\\', r'\\']]
    #
    #     data = FileTools.collate_files_by_low_level_dir_name(source_dir, low_level_dir_name, path_parts_re)
    #
    #     # Expected number of files found
    #     with self.subTest(self):
    #         self.assertTrue(len(data) == 5)
    #
    #     # Copied file exists
    #     with self.subTest(self):
    #         self.assertTrue(Path(data[0]['CopyPath']).exists())

    def test_collate_files_by_low_level_dir_name__with_suffix(self):
        source_dir = self.DeepSourceFilesSuffixed
        target_dir = self.CollatedFolder
        source_name = Path(source_dir).name
        target_name = Path(target_dir).name
        low_level_dir_name = 'start'
        path_parts_re = [[source_name, target_name]]

        data = FileTools.collate_files_by_low_level_dir_name(source_dir, low_level_dir_name, path_parts_re)

        # Expected number of files found
        with self.subTest(self):
            self.assertTrue(len(data) == 5)

        # Copied file exists
        with self.subTest(self):
            self.assertTrue(Path(data[0]['CopyPath']).exists())

    def test_df_from_excel_workbook(self):
        df = FileTools.df_from_excel_workbook(self.TestExcelWorkbookPath, ['SheetToIgnore'])
        with self.subTest(self, testing_for='Number of rows'):
            actual = len(df)
            expected = 12
            self.assertTrue(actual == expected)

    def test_df_list_from_excel_workbook(self):
        df = FileTools.df_list_from_excel_workbook(self.TestExcelWorkbookPath, ['SheetToIgnore'])
        with self.subTest(self, testing_for='Number of DataFrames'):
            actual = len(df)
            expected = 3
            self.assertTrue(actual == expected)

    def test_list_lines_with_term(self):

        with self.subTest(self, testing_for='basic test'):
            term_list = FileTools.list_lines_with_term(self.NotebookFilePath, 'import')
            actual = len(term_list)
            expected = 3
            self.assertTrue(actual == expected)

        with self.subTest(self, testing_for='exceptions'):
            except_hash = '#'
            term_list = FileTools.list_lines_with_term(self.NotebookFilePath, 'import', except_hash)
            expected = (except_hash in term_list[0])

            self.assertTrue(expected)


if __name__ == '__main__':
    unittest.main()
