import math
import os

import cv2
from bing_image_downloader import downloader

# TODO: add a readme file (how to use the script, how to install the dependencies, how to run the script)

DATASET_DIR = f'{os.getcwd()}/dataset'

IMAGE_FORMATS = [
    'png',
    'jpg',
    'jpeg'
]

BANNER_RATIOS = [
    '16:9',

]

COVER_DIMENSIONS = [
    '400x600',
    '500x750',
    '600x900',
    '800x1200'
]

TOLERANCE = 150


def validate_dir(dirname):
    if os.path.exists(dirname):
        print(f'Dataset directory: {dirname}')
    else:
        print("There was an error with the dataset directory")
        print("Please try again using other query string or limit.")
        exit(1)


def download_images(query_string, limit):
    output_dir = f'{DATASET_DIR}/{query_string}'
    downloader.download(query_string, limit=limit,  output_dir='dataset',
                        adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
    validate_dir(output_dir)
    process_images(output_dir, limit)


def pass_tolerance(img_width, img_height, dimension_width, dimension_height):
    return (abs(img_width - int(dimension_width)) <= TOLERANCE and abs(img_height - int(dimension_height)) <= TOLERANCE)


def calculate_aspect(width: int, height: int) -> str:
    r = math.gcd(width, height)
    x = int(width / r)
    y = int(height / r)
    return f"{x}:{y}"


def process_images(output_dir, count):

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

        print(calculate_aspect(img_width, img_height))

        # TODO: set a tolerance for the real image size and the banner/cover size
        # TODO: check if the image is a banner or a cover
        # TODO: if the image doesn't pass the check then delete it
        # TODO: then based on the reaming images, iterate again an search more images

        """ for dimension in BANNER_DIMENSIONS:
            dimension_width, dimension_height = dimension.split('x')
            if (pass_tolerance(img_width, img_height, dimension_width, dimension_height)):
                print(f'Image {current_image} is a banner')
                break
         """

        """ for dimension in COVER_DIMENSIONS:
            dimension_width, dimension_height = dimension.split('x')
            if (pass_tolerance(img_width, img_height, dimension_width, dimension_height)):
                print(f'Image {current_image} is a cover')
                break

        print(f'Image {current_image} is not a banner or a cover') """


if __name__ == '__main__':
    try:
        query_string = input("Enter the query string: ")
        limit = int(input("Enter the number of images to download: "))
        download_images(query_string, limit)

    except Exception as e:
        if (e.__class__.__name__ == 'ValueError'):
            print(
                "There was an error with the limit value. Please try again using a valid limit.")
        else:
            print("Please try again using a valid query string and limit.")
        exit(1)
