# get_dataset.py
"""
Description: This script downloads and unzips (if a zip) files from the given source.

Example usage:

python get_dataset.py --help
python get_dataset.py -d data
python get_dataset.py -d data -rd -rt
python get_dataset.py -d data -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_Input.zip

Datasets for ISIC:

python get_dataset.py --help
python get_dataset.py -d data
python get_dataset.py -d data -rd -ruc
python get_dataset.py -d data -wd isic2018 -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_Input.zip
python get_dataset.py -d data -wd isic2018 -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_LesionGroupings.csv
python get_dataset.py -d data -wd isic2018 -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_GroundTruth.zip
python get_dataset.py -d data -wd isic2018 -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Validation_Input.zip
python get_dataset.py -d data -wd isic2018 -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Validation_GroundTruth.zip
python get_dataset.py -d data -wd isic2018 -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Test_Input.zip
python get_dataset.py -d data -s http://bergerlab-downloads.csail.mit.edu/spatial-vae/mnist_rotated.tar.gz
python get_dataset.py -d data -rd -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_LesionGroupings.csv
"""

import argparse
import os
from src.download_helper import DownloadHelper
from src.file_tools import FileTools

DOWNLOAD_URL = 'https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_LesionGroupings.csv'


def parse_args():
    parser = argparse.ArgumentParser(description='Download the target training dataset')
    parser.add_argument('-d', '--data_dir', type=str, help="Path to the root target data directory")
    parser.add_argument('-rd', '--replace_download', action='store_true',
                        help="Flag to overwrite existing download file")
    parser.add_argument('-ruc', '--replace_unzip_content', action='store_true',
                        help="Flag to replace existing unzip folder content")
    parser.add_argument('-s', '--src_url', type=str, default=DOWNLOAD_URL,
                        help="Source URL for download")
    parser.add_argument('-i', '--is_isic', action='store_true',
                        help='Indicate download is an ISIC dataset following ISIC conventions')
    parser.add_argument('-wd', '--working_dir', type=str, default='',
                        help='Target directory for extraction etc (optional)')
    parser.add_argument('-u', '--unsupervised', action='store_true',
                        help="Indicate if for unsupervised learning - has a different folder structure")

    args = parser.parse_args()

    return args


def download_and_extract_file(args):

    extraction_dir, working_dir = DownloadHelper.download_dataset(
        data_dir=args.data_dir,
        replace_download=args.replace_download, replace_unzip_content=args.replace_unzip_content,
        src_url=args.src_url, is_isic=args.is_isic, working_dir=args.working_dir)

    return extraction_dir, working_dir


def main():
    args = parse_args()

    extraction_dir, working_dir = download_and_extract_file(args)

    if not args.is_isic:
        result = FileTools.create_numpy_archive_from_images_dir(
            src_dir=extraction_dir, target_path=extraction_dir, new_shape=(64, 64), suffix='.jpg')

        print(result)


if __name__ == "__main__":
    main()
