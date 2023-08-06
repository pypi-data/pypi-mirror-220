from zipfile import ZipFile
from io import BytesIO
import math
from typing import Dict, Tuple, Union
from concurrent.futures import ThreadPoolExecutor
import os
import glob

from PIL import Image, ImageStat
from PIL.Image import Image as PILImage
import libimagequant_integrations.PIL as liq_pil
import libimagequant as liq


SUPPORTED_EXTENSIONS = ['.cbz']


def find_files(path: str) -> list:
    """
    This function returns a list of paths that have a 
    supported extension (.cbz, .cbr, .cbt).

    Args:
        path (str): The input string is a path that can refer 
        to a specific file or a group of files.

    Returns:
        list: A list of paths that have an acceptable extension.

    Raises:
        ValueError: If the input string refers to a file with 
        an unsupported extension.
    """
    # Use glob to get all file paths that match the input pattern
    file_paths = glob.glob(path)

    # Filter the file paths to only include those with an acceptable extension
    filtered_file_paths = [file for file in file_paths 
                           if os.path.splitext(file)[1] 
                           in SUPPORTED_EXTENSIONS]

    # If the input string refers to a single file of 
    # an unacceptable extension, raise an error
    if len(filtered_file_paths) == 0:
        raise ValueError("No file(s) with supported extensions found."
                         f"Please use files of type {SUPPORTED_EXTENSIONS}")

    return filtered_file_paths


def extract_image(name: str, input_zip: ZipFile) -> Tuple[str, PILImage]:
    """
    Extract a single image from a zip file and convert it to RGB format.

    Parameters:
    name (str): Name of the image file in the zip.
    input_zip (ZipFile): Input zip file containing images.

    Returns:
    Tuple[str, PILImage]: A tuple where the first element is the image 
    name and the second element is the corresponding RGB image.
    """
    return name, Image.open(BytesIO(input_zip.read(name))).convert("RGB")

def extract_parallel(input_zip: ZipFile) -> Dict[str, PILImage]:
    """
    Extract images from a zip file and convert them to RGB format.

    Parameters:
    input_zip (ZipFile): Input zip file containing images.

    Returns:
    Dict[str, PILImage]: A dictionary where keys are the image names 
    and values are the corresponding RGB images.
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.tiff', '.bmp')
    image_names = [name for name in input_zip.namelist() 
                   if name.lower().endswith(image_extensions)]
    
    with ThreadPoolExecutor() as executor:
        image_dict = dict(executor.map(extract_image, image_names, 
                                       [input_zip]*len(image_names)))
    
    return image_dict


def extract_serial(input_zip: ZipFile) -> Dict[str, PILImage]:
    """
    Extract images from a zip file and convert them to RGB format.

    Parameters:
    input_zip (ZipFile): Input zip file containing images.

    Returns:
    Dict[str, PILImage]: A dictionary where keys are the image names 
    and values are the corresponding RGB images.
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.tiff', '.bmp')
    return {name: Image.open(BytesIO(input_zip.read(name))).convert("RGB") 
            for name in input_zip.namelist() 
            if name.lower().endswith(image_extensions)}


def num_to_bits(x: int) -> int:
    """
    Returns a rounded number of bits that will contain a given number.

    Parameters:
    x (int): Input number.

    Returns:
    int: Number of bits required to represent the input number.
    """
    return int(math.ceil(math.log(x, 2)))


def write_to_cbz(image_dict: Dict[str, Tuple[PILImage, int]], 
                 file_name: str) -> None:
    """
    Write images to a zip file with specified number of colors.

    Parameters:
    image_dict (Dict[str, Tuple[PILImage, int]]): A dictionary where 
    keys are image names and values are tuples of image and number of colors.
    file_name (str): Name of the output zip file.
    """
    with ZipFile(file_name, 'w') as zipf:
        for name, data in image_dict.items():
            image, num_colors = data
            with BytesIO() as output:
                image.save(output, 
                           format="PNG",
                           bits=num_to_bits(num_colors), 
                           optimize=True)
                image_data = output.getvalue()
            zipf.writestr(name, image_data)


def write_image_to_zip(name: str, data: Tuple[PILImage, int], 
                       zipf: ZipFile) -> None:
    """
    Write a single image to a zip file.

    Parameters:
    name (str): Name of the image.
    data (Tuple[PILImage, int]): Tuple of image and number of colors.
    zipf (ZipFile): Zip file to write the image to.
    """
    image, num_colors = data
    with BytesIO() as output:
        image.save(output, 
                   format="PNG",
                   bits=num_to_bits(num_colors), 
                   optimize=True)
        image_data = output.getvalue()
    zipf.writestr(name, image_data)


def write_to_cbz_parallel(image_dict: Dict[str, Tuple[PILImage, int]], 
                          file_name: str) -> None:
    """
    Write images to a zip file with specified number of colors in parallel.

    Parameters:
    image_dict (Dict[str, Tuple[PILImage, int]]): A dictionary where 
    keys are image names and values are tuples of image and number of colors.
    file_name (str): Name of the output zip file.
    """
    with ZipFile(file_name, 'w') as zipf:
        with ThreadPoolExecutor() as executor:
            for name, data in image_dict.items():
                executor.submit(write_image_to_zip, name, data, zipf)


def is_grayscale(img: PILImage, tolerance: int = 10) -> bool:
    """
    Check if an image is grayscale within a certain tolerance.

    Parameters:
    img (PILImage): Input image.
    tolerance (int): Tolerance for grayscale check.

    Returns:
    bool: True if the image is grayscale within the tolerance, False otherwise.
    """
    if img.mode != 'RGB':
        img = img.convert('RGB')
    stat = ImageStat.Stat(img)
    
    # Calculate the difference between the color channels
    diff = abs(sum(stat.sum)/3 - stat.sum[0])

    # Check if the maximum difference is within the tolerance
    return diff < tolerance


def resize_image(img: PILImage, resize_height: int) -> PILImage:
    """
    Resize an image to a specified height while maintaining aspect ratio.

    Parameters:
    img (PILImage): Input image.
    resize_height (int): Desired height of the resized image.

    Returns:
    PILImage: Resized image.
    """
    w, h = img.size
    resize_width = int(resize_height * w / h)
    img.thumbnail((resize_width, resize_height), Image.BICUBIC)
    return img


def process_image(height: Union[int, None], 
                  grayscale_ncolors: int, 
                  color_ncolors: int, 
                  file_name_img_tuple: Tuple[str, PILImage]
                  ) -> Tuple[str, Tuple[PILImage, int]]:
    """
    Process an image: resize if necessary, quantize, 
    and return in a tuple with its filename.

    Parameters:
    height (int or None): Desired height of the resized image. 
    No resizing on None.
    grayscale_ncolors (int): Number of colors for grayscale images.
    color_ncolors (int): Number of colors for color images.
    file_name_img_tuple (Tuple[str, PILImage]): Tuple of filename and image.

    Returns:
    Tuple[str, Tuple[PILImage, int]]: Tuple of filename and a tuple of 
    processed image and number of colors.
    """
    file_name, img = file_name_img_tuple
    img_is_grayscale = is_grayscale(img)

    # Resize large images to height while maintaining aspect ratio
    if height is not None and img.size[1] > height:
        img = resize_image(img, height)

    attr = liq.Attr()
    # Quantize an image down to this number of colors
    if img_is_grayscale:
        num_colors = grayscale_ncolors
    else:
        num_colors = color_ncolors
    
    attr.max_colors = num_colors

    img = liq_pil.to_liq(img, attr)

    result = img.quantize(attr)
    # Same gamma as PNGQuant
    result.output_gamma = 0.45455
    # Dither with Floyd-Steinberg
    result.dithering_level = 1.0

    new_img = liq_pil.from_liq(result, img)

    return file_name, (new_img, num_colors)
