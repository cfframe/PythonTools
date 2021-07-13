import os
import shutil
import tarfile
import urllib.request
import zipfile

from pathlib import Path
from src.download_progress_bar import DownloadProgressBar


class DownloadHelper:

    @staticmethod
    def can_download(target_download_path,
                     replace_download=None) -> bool:
        """Determine whether or not downloading is an option

        Keyword arguments:
        :param target_download_path: str -- target file path for prospective download
        :param replace_download: bool -- flag for whether to replace file if already exists
        """

        if Path(target_download_path).is_file():
            if replace_download is None:
                replace_download = input('File {} exists, replace it (y/n and enter)?'
                                         .format(target_download_path))[0].lower()
                replace_download = True if replace_download == 'y' else False
            result = replace_download
            message = 'Overwriting "{}".'.format(target_download_path) if result \
                else 'Not replacing "{}".'.format(target_download_path)
        else:
            message = 'Saving new file "{}".'.format(target_download_path)
            result = True

        print(message)
        return result

    @staticmethod
    def can_extract_to_extraction_dir(
            unzip_dir: str,
            replace_content: bool = False) -> bool:
        """Determine whether or not should be able to extract content from an archive file

        Keyword arguments:
        :param unzip_dir: final directory for extracted files
        :param replace_content: flag - replace content of directory
        :return: can_extract_to_dir
        """
        if unzip_dir == '':
            can_extract_to_dir = False
            message = 'No directory for extraction, so nothing to be extracted.'

        elif unzip_dir and Path(unzip_dir).is_dir() and len(os.listdir(unzip_dir)) > 0:

            can_extract_to_dir = replace_content

            message = 'Will replace {}.'.format(unzip_dir) if can_extract_to_dir \
                else 'Will not replace content of "{}".'.format(unzip_dir)

        else:
            message = 'Extracted file(s) will be saved at {}.'.format(unzip_dir)
            can_extract_to_dir = True

        print(message)
        return can_extract_to_dir

    @staticmethod
    def to_download(target_download_path: str,
                    replace_download: bool,
                    can_extract_to_extraction_dir: bool,
                    extraction_dir: str,
                    ) -> bool:
        """Determine whether or not to download file

        Keyword arguments:

        :param target_download_path: target file path for prospective download
        :param replace_download: flag - replace file if already exists
        :param can_extract_to_extraction_dir: whether extraction can occur
        :param extraction_dir: target directory for unzip content
        :return: to_download
        """

        # Download may not be an archive, hence a nuanced check.
        is_extraction_pre_check_ok = \
            True if extraction_dir == '' or can_extract_to_extraction_dir \
            else False

        to_download = is_extraction_pre_check_ok and DownloadHelper.can_download(target_download_path, replace_download)

        return to_download

    @staticmethod
    def download_url(url, target_path):
        target_directory = Path(target_path).parent.absolute()
        if not target_directory.exists():
            Path(target_directory).mkdir(parents=True, exist_ok=True)

        with DownloadProgressBar(unit='B', unit_scale=True,
                                 miniters=1, desc=url.split('/')[-1]) as t:
            urllib.request.urlretrieve(url, filename=target_path, reporthook=t.update_to)

    @staticmethod
    def get_extraction_dir_path(data_dir: str, filename: str) -> str:
        """Derive extraction directory

        :param data_dir: Root data directory
        :param filename: Source filename
        :return: extraction_dir_path
        """
        filename = filename.lower()
        extraction_dir_path = 'extracted'
        suffices = ('.zip', '.tar', '.tar.gz')

        p = Path(filename)
        file_stem = p.stem
        suffix_found = False

        for suffix in suffices:
            if p.name.endswith('.tar.gz'):
                # Numpy archive
                file_stem = Path(file_stem).stem
                suffix_found = True
                break
            elif suffix == p.suffix:
                suffix_found = True
                break

        extraction_dir_path = os.path.join(data_dir, file_stem)

        if not suffix_found:
            raise ValueError(f'{p.name} is not a handled archive type.')

        return extraction_dir_path

    @staticmethod
    def get_extraction_isic_dir_path(data_dir: str, filename: str) -> str:
        """Derive extraction directory

        :param data_dir: Root data directory
        :param filename: Source filename
        :return: extraction_dir_path
        """
        filename = filename.lower()
        extraction_dir_path = ''
        file_types = ('training_input', 'training_groundtruth',
                      'validation_input', 'validation_groundtruth',
                      'test_input')
        suffices = ('zip', 'tar')

        for file_type in file_types:
            for suffix in suffices:
                if filename.endswith(file_type + '.' + suffix):
                    p = Path(file_type)
                    extraction_dir_path = os.path.join(data_dir, p.stem)

        return extraction_dir_path

    @staticmethod
    def download_file(data_dir: str, replace_download: bool, src_url: str, is_isic: bool, replace_unzip_content: bool,
                      working_dir: str = ''):
        """Download file from give URL to given directory with chosen name. Check if download is required.

        Keyword arguments:

        :param data_dir: Target root data directory
        :param replace_download: flag, whether to replace an existing download of same name
        :param src_url: Source URL
        :param is_isic: flag, whether to be processed as an ISIC file that follows ISIC conventions
        :param replace_unzip_content: flag, whether to replace existing extraction content
        :param working_dir: (optional) working directory for extraction of download
        :return: can_extract_to_extraction_dir, working_dir, final_extraction_dir, download_file_path
        """
        print('Parameters (download_file): \ndata_dir: {}'
              '\nreplace_download: {}\nsrc_url: {}\nis_isic: {}\nworking_dir: {}'.
              format(data_dir, replace_download, src_url, is_isic, working_dir))

        src_path = Path(src_url)
        target_filename = src_path.name

        download_dir = os.path.join(data_dir, 'downloads')

        download_file_path = os.path.join(download_dir, target_filename)
        working_dir = data_dir if working_dir == '' else os.path.join(data_dir, working_dir)

        final_extraction_dir = \
            DownloadHelper.get_extraction_isic_dir_path(data_dir=working_dir, filename=target_filename) if is_isic \
            else DownloadHelper.get_extraction_dir_path(data_dir=working_dir, filename=target_filename)

        # No need to download when any one of these:
        # - download file already exists and replace_download == False
        # - unzip dir already exists with files and replace_content == False
        # - no unzipping needed (unzip dir = ''))
        can_extract_to_extraction_dir = DownloadHelper.can_extract_to_extraction_dir(
            unzip_dir=final_extraction_dir, replace_content=replace_unzip_content
        )

        to_download = DownloadHelper.to_download(
            target_download_path=download_file_path, replace_download=replace_download,
            can_extract_to_extraction_dir=can_extract_to_extraction_dir,
            extraction_dir=final_extraction_dir
        )

        if to_download:
            # Clear target unzip dir, if required
            if not final_extraction_dir == '' \
                    and Path(final_extraction_dir).exists() and Path(final_extraction_dir).is_dir():
                print('Removing dir {}.'.format(final_extraction_dir))
                shutil.rmtree(final_extraction_dir)
            DownloadHelper.download_url(src_url, download_file_path)

        return can_extract_to_extraction_dir, working_dir, final_extraction_dir, download_file_path

    @staticmethod
    def unzip_archive(archive_file_path: str, data_dir: str, final_extraction_dir: str):
        """Extract archive content

        Keyword arguments:

        :param archive_file_path: Path to archive
        :param data_dir: Target root data directory
        :param final_extraction_dir: path to final directory of unzipped content
        # :param unsupervised: (optional) if set, then use a different folder structure
        """
        print('Parameters (unzip_archive): \narchive_file_path: {}\ndata_dir: {}\nfinal_extraction_dir: {}'.
              format(archive_file_path, data_dir, final_extraction_dir))

        target_filename = Path(archive_file_path).name
        file_type = Path(archive_file_path).suffix
        if target_filename.endswith('.tar.gz'):
            file_type = '.tar.gz'

        # Remove temp dir if exists, will recreate later if needed
        temp_extraction_dir = os.path.join(data_dir, 'temp')
        if Path(temp_extraction_dir).exists():
            print('Removing dir tree {}'.format(temp_extraction_dir))
            shutil.rmtree(temp_extraction_dir)

        initial_extraction_dir_name = ''

        Path(temp_extraction_dir).mkdir(parents=True, exist_ok=True)
        if file_type == '.tar.gz':
            tar_ref = tarfile.open(archive_file_path, 'r|gz')
            print(f'Extracting {archive_file_path} to {temp_extraction_dir}')
            tar_ref.extractall(path=temp_extraction_dir)
            # Assume that everything is inside a single top level folder.
            initial_extraction_dir_name = Path(tar_ref.members[0].name).parts[0]
            tar_ref.close()
        elif file_type == '.gz':
            # Not handled yet
            print(f'*** Not handling {file_type} archives yet ***')
            exit()
        elif file_type == '.tar' or file_type == '.zip':
            with zipfile.ZipFile(archive_file_path, 'r') as zip_ref:
                print(f'Extracting {zip_ref.filename} to {temp_extraction_dir}')
                zip_ref.extractall(path=temp_extraction_dir)
                # Assume that everything is inside a single top level folder.
                initial_extraction_dir_name = Path(zip_ref.filelist[0].filename).parts[0]

        # Remove target dir then rename/move unzipped dir
        if Path(final_extraction_dir).exists():
            print('Removing dir tree {}'.format(final_extraction_dir))
            shutil.rmtree(final_extraction_dir)

        extraction_dir = os.path.join(temp_extraction_dir, initial_extraction_dir_name)
        print(f'Moving dir "{extraction_dir}" to "{final_extraction_dir}"')
        Path(Path(final_extraction_dir).parent).mkdir(parents=True, exist_ok=True)
        os.rename(extraction_dir, final_extraction_dir)

        return

    @staticmethod
    def move_non_archive_file_to_working_dir(download_file_path: str, working_dir: str):
        file_type = Path(download_file_path).suffix
        if download_file_path.endswith('.tar.gz'):
            file_type = '.tar.gz'
        archive_file_types = ['.tar.gz', '.tar', '.gz', '.zip']
        if file_type in archive_file_types:
            print('Archive file, not moving to target folder.')
        else:
            os.rename(download_file_path, os.path.join(working_dir, Path(download_file_path).name))
