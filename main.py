import math
import os

import cv2
import inquirer
from bing_image_downloader import downloader

# TODO: add a readme file (how to use the script, how to install the dependencies, how to run the script)

DATASET_DIR = f'{os.getcwd()}/dataset'

TOLERANCE = 150

IMAGE_FORMATS = [
    'png',
    'jpg',
    'jpeg'
]

IMAGE_TYPES = [
    'banners',
    'covers'
]

BANNER_RATIOS = [
    '2:1',
    '5:3',
    '16:9',
    '19:10',
    '150:89',
    '300:157'
    '320:183',
    '1920:883'
]

COVER_RATIOS = [
    '4:3',
    '2:3'
    '27:40'
    '1:1'
    '750:1061'

]


def validate_dir(dirname):
    if os.path.exists(dirname):
        print(f'Dataset directory: {dirname}')
    else:
        print("There was an error with the dataset directory")
        print("Please try again using other query string or limit.")
        exit(1)


def download_images(media_type, query_string, dataset_limit):
    # Here we define limit based on the dataset_limit parameter
    if (dataset_limit == 'Small'):
        limit = 33
    elif (dataset_limit == 'Medium'):
        limit = 67
    elif (dataset_limit == 'Large'):
        limit = 100

    for img_type in IMAGE_TYPES:
        query = f'{query_string} {media_type} {img_type}'
        output_dir = f'{DATASET_DIR}/{query}'
        downloader.download(query, limit=limit)
        validate_dir(output_dir)
        process_images(query, output_dir, limit, img_type)


def pass_tolerance(img_width, img_height, dimension_width, dimension_height):
    return (abs(img_width - int(dimension_width)) <= TOLERANCE and abs(img_height - int(dimension_height)) <= TOLERANCE)


def calculate_ratio(width: int, height: int) -> str:
    r = math.gcd(width, height)
    x = int(width / r)
    y = int(height / r)
    return f"{x}:{y}"


def process_images(query, output_dir, count, img_type):

    print(f'Processing {img_type}...')
    valid_img_num = 0
    valid_img_name = query.lower().replace(' ', '_')

    for x in range(1, count + 1):

        current_image = ''

        for img_format in IMAGE_FORMATS:
            if (os.path.exists(f'{output_dir}/Image_{x}.{img_format}')):
                current_image = f'{output_dir}/Image_{x}.{img_format}'
                break

        if (current_image == ''):
            continue

        img = cv2.imread(current_image)

        img_height = img.shape[0]
        img_width = img.shape[1]

        print(calculate_ratio(img_width, img_height))

        if img_type == 'banners':
            valid_img = False
            for ratio in BANNER_RATIOS:
                if (ratio == calculate_ratio(img_width, img_height)):
                    print('Banner found!')
                    valid_img = True
                    valid_img_num += 1
                    os.rename(
                        current_image, f'{output_dir}/{valid_img_name}_{valid_img_num}.{img_format}')
                    continue
            if (not valid_img):
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

        # TODO: Set dataset limit parameters

        query_string = input(f'Enter the {media_type} name: ')

        dataset_limit_questions = [
            inquirer.List('dataset_limit',
                          message="Select the dataset of images to download",
                          choices=['Small', 'Medium', 'Large'],)
        ]

        dataset_limit_answers = inquirer.prompt(dataset_limit_questions)
        dataset_limit = dataset_limit_answers['dataset_limit']

        download_images(media_type, query_string, dataset_limit)

    except Exception as e:
        if (e.__class__.__name__ == 'ValueError'):
            print(
                "There was an error with the limit value. Please try again using a valid limit.")
        else:
            print(e)
        exit(1)
