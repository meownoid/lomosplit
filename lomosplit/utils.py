import os
from operator import itemgetter
from typing import List, Tuple

import numpy as np
from natsort import natsorted


IMAGE_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'tiff', 'bmp'
}


def is_image(filename: str) -> bool:
    _, ext = os.path.splitext(filename)

    return ext.strip('.') in IMAGE_EXTENSIONS


def get_grouped_images(path: str) -> List[Tuple[str, List[str]]]:
    result = []

    for root, _, files in os.walk(path):
        local_result = []

        for filename in files:
            if not is_image(filename):
                continue

            local_result.append(filename)

        local_result = natsorted(local_result)

        if local_result:
            result.append((os.path.relpath(root, path), local_result))

    return natsorted(result, key=itemgetter(0))


def consecutive(data: np.ndarray, step_size: int = 1):
    return np.split(data, np.where(np.diff(data) != step_size)[0]+1)


def rotate_left(image: np.ndarray) -> np.ndarray:
    return np.transpose(image, axes=[1, 0, 2])[::-1, :, :]


def rotate_right(image: np.ndarray) -> np.ndarray:
    return np.transpose(image, axes=[1, 0, 2])[:, ::-1, :]


def rotate(image: np.ndarray, how: str) -> np.ndarray:
    if how == 'left':
        return rotate_left(image)
    elif how == 'right':
        return rotate_right(image)
    else:
        raise ValueError(f'Unknown rotation specification, expected left or right')


def pad_vertical(image: np.ndarray, height: int) -> np.ndarray:
    return np.pad(
        image,
        pad_width=[
            (height//2+1, height//2+1),
            (0, 0),
            (0, 0)
        ],
        mode='constant'
    )
