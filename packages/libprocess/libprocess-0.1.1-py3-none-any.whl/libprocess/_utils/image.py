import hashlib
import os
from os import listdir
from os.path import isfile
from typing import List, Union

import imagehash
from PIL import Image, UnidentifiedImageError

Image.MAX_IMAGE_PIXELS = 5e8


def uuid2filename(uuid: str, img_dir: str) -> Union[str, None]:
    """
    Given the uuid of an image and the directory storing the image,
    returns its filename.
    """

    matches = [d for d in listdir(img_dir) if d.startswith(uuid)]
    assert len(matches) <= 1, f"Multiple files with the same uuid: {uuid}"
    return None if len(matches) == 0 else matches[0]


def get_shape_by_path(image_path: str) -> Union[List[int], None]:
    try:
        return list(Image.open(image_path).size)
    except (FileNotFoundError, UnidentifiedImageError):
        return None


def get_shape_by_uuid(uuid: str, img_dir: str) -> Union[List[int], None]:
    filename = uuid2filename(uuid, img_dir)
    return get_shape_by_path(f"{img_dir}/{filename}")


def get_storage_size_by_path(image_path: str) -> Union[int, None]:
    """
    Compute storage size given the path to a file.
    The storage size will be None when the file doesn't exist.
    """

    if not isfile(image_path):
        return None
    return os.stat(image_path).st_size


def get_storage_size_by_uuid(uuid: str, img_dir: str) -> Union[int, None]:
    """
    Compute storage size given the uuid of an image and the directory storing the image.
    The storage size will be None when the file doesn't exist.
    """

    filename = uuid2filename(uuid, img_dir)
    return get_storage_size_by_path(f"{img_dir}/{filename}")


def get_md5_by_path(image_path: str) -> Union[str, None]:
    """
    Compute md5 given the path to an image.
    The md5 will be None when the file doesn't exist.
    """

    if not isfile(image_path):
        return None

    with open(image_path, "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    return md5


def get_md5_by_uuid(uuid: str, img_dir: str) -> Union[str, None]:
    """
    Compute md5 given the uuid of an image and the directory storing the image.
    The md5 will be None when the file doesn't exist.
    """

    filename = uuid2filename(uuid, img_dir)
    return get_md5_by_path(f"{img_dir}/{filename}")


def get_phash_by_path(image_path: str) -> Union[str, None]:
    """
    Compute phash given the path to an image.
    The phash will be None in the following conditions:
    1. The file doesn't exist.
    2. The file is not an image.
    3. The file is corrupted/truncated.
    """

    try:
        return str(imagehash.phash(Image.open(image_path), hash_size=8))
    except (UnidentifiedImageError, OSError):
        return None


def get_phash_by_uuid(uuid: str, img_dir: str) -> Union[str, None]:
    """
    Compute phash given the uuid of an image and the directory storing the image.
    The phash will be None in the following conditions:
    1. The file doesn't exist.
    2. The file is not an image.
    3. The file is corrupted.
    """

    filename = uuid2filename(uuid, img_dir)
    return get_phash_by_path(f"{img_dir}/{filename}")
