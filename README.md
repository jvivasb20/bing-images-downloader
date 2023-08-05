## Dependencies

- Python 3.x
- [Bing Image Downloader](https://pypi.org/project/bing-image-downloader/)
- [Inquirer](https://pypi.org/project/inquirer/)
- [OpenCV](https://pypi.org/project/opencv-python/)

## Installation

1. Clone or download the repository to your local machine.
2. Install the required dependencies using pip:
   ```
   pip install bing_image_downloader inquirer opencv-python
   ```

## Usage

1. Run the script:

   ```
   python image_downloader.py
   ```

2. The script will prompt you to select the media type (movie or series) and enter the name of the movie or series you want to download images for.

3. Next, choose the dataset of images to download (small, medium, or large). The script will then start downloading the images and organizing them into separate folders for banners and covers based on their aspect ratio.

4. After the download is complete, the script will display the paths of the downloaded images for both banners and covers.

## Aspect Ratio Support

The script supports the following aspect ratios for banners and covers:

### Banners:

- 2:1
- 5:3
- 16:9
- 19:10
- 150:89
- 300:157
- 320:183
- 1920:883

### Covers:

- 1:1
- 2:3
- 4:3
- 27:40
- 200:129
- 750:1061

## Dataset Directory

The downloaded images will be stored in the 'dataset' directory within the same folder as the script. The images will be further organized into subdirectories based on the media type and query string.
