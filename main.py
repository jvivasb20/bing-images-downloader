import math
import os

import cv2
import inquirer
from bing_image_downloader import downloader

# Constants
DATASET_DIR = f'{os.getcwd()}/dataset'
IMAGE_FORMATS = ['png', 'jpg', 'jpeg']
IMAGE_TYPES = ['banners', 'covers']
BANNER_RATIOS = ['2:1', '5:3', '16:9', '19:10',
                 '150:89', '300:157', '320:183', '1920:883']
COVER_RATIOS = ['1:1', '2:3', '4:3', '27:40', '200:129', '750:1061']
DATASET_LIMITS = {'Small': 33, 'Medium': 67, 'Large': 100}


def validate_dir(dirname):
    """Validate if the directory exists."""
    if os.path.exists(dirname):
        print(f'Dataset directory: {dirname}')
    else:
        raise ValueError("The dataset directory does not exist.")


def print_images_path(dirname):
    """Print the path of the images."""
    for img_type in IMAGE_TYPES:
        print(f'{img_type} images path: {dirname} {img_type}')


def download_images(media_type, query_string, dataset_limit):
    """Download images based on the media type and query string."""
    limit = DATASET_LIMITS.get(dataset_limit, 33)

    for img_type in IMAGE_TYPES:
        query = f'{query_string} {media_type} {img_type}'
        output_dir = f'{DATASET_DIR}/{query}'
        downloader.download(query, limit=limit, verbose=False)
        validate_dir(output_dir)
        process_images(query, output_dir, limit, img_type)

    print_images_path(f'{DATASET_DIR}/{query_string} {media_type}')


def calculate_ratio(width: int, height: int) -> str:
    """Calculate the aspect ratio of an image."""
    r = math.gcd(width, height)
    x = int(width / r)
    y = int(height / r)
    return f"{x}:{y}"


def process_images(query, output_dir, count, img_type):
    """Process images based on the aspect ratio and image type."""
    print(f'Processing {img_type}...')
    valid_img_num = 0
    valid_img_name = query.lower().replace(' ', '_')

    ratios = BANNER_RATIOS if img_type == 'banners' else COVER_RATIOS

    for x in range(1, count + 1):

        current_image = ''
        valid_img = False

        for img_format in IMAGE_FORMATS:
            if os.path.exists(f'{output_dir}/Image_{x}.{img_format}'):
                current_image = f'{output_dir}/Image_{x}.{img_format}'
                break

        if current_image == '':
            continue

        img = cv2.imread(current_image)
        img_height = img.shape[0]
        img_width = img.shape[1]

        for ratio in ratios:
            if ratio == calculate_ratio(img_width, img_height):
                print('Cover found!' if img_type ==
                      'covers' else 'Banner found!')
                valid_img = True
                valid_img_num += 1
                os.rename(
                    current_image, f'{output_dir}/{valid_img_name}_{valid_img_num}.{img_format}')
                break

        if not valid_img:
            os.remove(current_image)


if __name__ == '__main__':
    try:
        media_type_questions = [
            inquirer.List('media_type',
                          message="Select the media type",
                          choices=['Movie', 'Serie'],
                          ),
        ]
        media_type_answers = inquirer.prompt(media_type_questions)
        media_type = media_type_answers['media_type']

        query_string = input(f'Enter the {media_type} name: ')

        dataset_limit_questions = [
            inquirer.List('dataset_limit',
                          message="Select the dataset of images to download",
                          choices=list(DATASET_LIMITS.keys()),)
        ]

        dataset_limit_answers = inquirer.prompt(dataset_limit_questions)
        dataset_limit = dataset_limit_answers['dataset_limit']

        download_images(media_type, query_string, dataset_limit)

    except ValueError as ve:
        print(ve)
        exit(1)
    except Exception as e:
        print("An error occurred:", e)
        exit(1)
