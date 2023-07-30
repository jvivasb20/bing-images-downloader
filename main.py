import os

from bing_image_downloader import downloader

DATASET_DIR = f'{os.getcwd()}/dataset'


def validate_dir(dirname):
    if os.path.exists(dirname):
        print(f'Dataset directory: {dirname}')
    else:
        print("There was an error with the dataset directory")
        print("Please. Try again using other query string or limit.")
        exit(1)


def downlad_images(query_string, limit):
    output_dir = f'{DATASET_DIR}/{query_string}'
    downloader.download(query_string, limit=limit,  output_dir='dataset',
                        adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
    validate_dir(output_dir)


if __name__ == '__main__':
    try:
        query_string = input("Enter the query string: ")
        limit = int(input("Enter the number of images to download: "))
        downlad_images(query_string, limit)
    except Exception as e:
        if (e.__class__.__name__ == 'ValueError'):
            print(
                "There was an error with the limit value. Please try again using a valid limit.")
        else:
            print("Please try again using a valid query string and limit.")
        exit(1)
