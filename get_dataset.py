# get_dataset.py
"""
Description: This script downloads and unzips (if a zip) files from the given source.

Example usage:

python get_dataset.py --help
python get_dataset.py -d data -rd n
python get_dataset.py -d data -rd y -rt y
python get_dataset.py -d data -rd n -ruc n -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_Input.zip

Datasets for ISIC:

python get_dataset.py --help
python get_dataset.py -d data
python get_dataset.py -d data -rd -rt
python get_dataset.py -d data -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_Input.zip
python get_dataset.py -d data -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_LesionGroupings.csv
python get_dataset.py -d data -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_GroundTruth.zip
python get_dataset.py -d data -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Validation_Input.zip
python get_dataset.py -d data -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Validation_GroundTruth.zip
python get_dataset.py -d data -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Test_Input.zip
python get_dataset.py -d data -s http://bergerlab-downloads.csail.mit.edu/spatial-vae/mnist_rotated.tar.gz
python get_dataset.py -d data -rd -i -s https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_LesionGroupings.csv
"""

import argparse
from src.download_helper import DownloadHelper
from src.file_tools import FileTools

DOWNLOAD_URL = 'https://isic-challenge-data.s3.amazonaws.com/2018/ISIC2018_Task3_Training_LesionGroupings.csv'


def parse_args():
    parser = argparse.ArgumentParser(description='Download the target training dataset')
    parser.add_argument('--data_dir', '-d', type=str, help="Path to the root target data director")
    parser.add_argument('--replace_download', '-rd', action='store_true',
                        help="Flag to overwrite existing download file")
    parser.add_argument('--replace_unzip_content', '-ruc', action='store_true',
                        help="Flag to replace existing unzip folder content")
    parser.add_argument('--src_url', '-s', type=str, default=DOWNLOAD_URL,
                        help="Source URL for download")
    parser.add_argument('--is_isic', '-i', action='store_true',
                        help='Indicate download is an ISIC dataset following ISIC conventions')

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    extraction_dir = DownloadHelper.download_dataset(**args.__dict__)
    final_file_path = FileTools.save_numpy_image_array_of_images_dir(
        src_dir=extraction_dir, target_path=extraction_dir, new_shape=(64, 64), suffix='.jpg')

    print(f'Saved images file at {final_file_path}')


if __name__ == "__main__":
    main()
