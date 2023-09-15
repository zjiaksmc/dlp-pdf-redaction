"""
Utils to process images are listed in this file
"""
import io

import numpy as np
from PIL import Image, ImageEnhance
import logging
# import cv2
# from deskew import determine_skew
import math
from typing import Tuple, Union


def _load_image(image_data):
    if isinstance(image_data, bytes):
        image_data = io.BytesIO(image_data)
    if isinstance(image_data, io.BytesIO):
        return Image.open(image_data)
    if isinstance(image_data, Image.Image):
        return image_data
    raise TypeError(f"Unsupported image type: {type(image_data).__qualname__}.")


def convert_image(image_data, color_mode, format):
    img = _load_image(image_data)
    if img.mode != color_mode:
        logging.info(f'Image has color mode {img.mode}. Converting to {color_mode}...')
        img = img.convert(mode=color_mode)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format=format)
    return imgByteArr.getvalue()


def to_grayscale(image_data):
    """
    Convert to grayscale
    """
    return convert_image(image_data, "L")


def crop_image(image_data, vects, format="TIFF"):
    """
    Crop images from the source document image
    """
    img = _load_image(image_data)

    width, height = img.size
    left = width * vects[0]["x"]
    top = height * vects[0]["y"]
    right = width * vects[1]["x"]
    bottom = height * vects[1]["y"]

    annotation_img = img.crop((left, top, right, bottom))

    imgByteArr = io.BytesIO()
    annotation_img.save(imgByteArr, format=format)

    return imgByteArr.getvalue()


# def _rotate(
#         image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
# ) -> np.ndarray:
#     old_width, old_height = image.shape[:2]
#     angle_radian = math.radians(angle)
#     width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
#     height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

#     image_center = tuple(np.array(image.shape[1::-1]) / 2)
#     rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
#     rot_mat[1, 2] += (width - old_width) / 2
#     rot_mat[0, 2] += (height - old_height) / 2
#     return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)


# def deskew(image_data):
#     img = _load_image(image_data)
#     if img.mode != "L":
#         # img = img.convert("L")
#         return img
#     np_img = image_to_nparray(img)
#     angle = determine_skew(np_img)
#     if angle == 0.0:
#         return img
#     rotated = _rotate(np_img, angle, (0, 0, 0))
#     pilImage = Image.fromarray(rotated)
#     return pilImage


def enhance_image(
    image_data,
    contrast_factor=2,
    brightness_factor=1.5,
    mode="L",
    format="PNG",
    # image_data, contrast_factor=None, brightness_factor=None, mode=None, format="PNG"
):
    """
    Enhance the image by increasing the contrast and brightness,
    change the image from RGB to Grayscale
    """
    img = _load_image(image_data)
    # img = ImageOps.grayscale(img)
    # Grayscale
    # img: Image = img.convert("L")
    # Threshold
    # threshold = 100
    # img = img.point(lambda p: 255 if p > threshold else 0)

    # img = img.filter(ImageFilter.SMOOTH)
    # img = img.filter(ImageFilter.SHARPEN)
    # img = img.filter(ImageFilter.MedianFilter(size=5))
    # img = img.filter(ImageFilter.EDGE_ENHANCE)
    if contrast_factor:
        contrast_enhancer = ImageEnhance.Contrast(img)
        try:
            img = contrast_enhancer.enhance(contrast_factor)
        except ValueError:
            logging.warning(f"Image may have wrong mode {img.mode}", exc_info=True)
    if brightness_factor:
        brightness_enhancer = ImageEnhance.Brightness(img)
        try:
            img = brightness_enhancer.enhance(brightness_factor)
        except ValueError:
            logging.warning(f"Image may have wrong mode {img.mode}", exc_info=True)
    if mode:
        img = img.convert(mode)

    # To mono
    # img = img.convert("1")

    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format=format)

    return imgByteArr.getvalue()


def resize_image(image_data, size, format="PNG"):
    """
    Reduce the size of the image
    """
    if size is None:
        return image_data
    img = _load_image(image_data)

    img.thumbnail(size, Image.LANCZOS)

    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format=format)

    return imgByteArr.getvalue()


def image_to_nparray(image_data):
    """
    Convert image bytes to numpy array
    """
    img = _load_image(image_data)

    return np.array(img)


def reformat_image(image_data, format="TIFF"):
    """
    Convert image into another format
    """
    img = _load_image(image_data)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format=format)
    return imgByteArr.getvalue()