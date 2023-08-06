import numpy as np


def mirror(picture, pos=0.0, axis=0, flip=False):
    """

    :param picture: array, 2d, 3d
    :param pos: Float<0, 1>, Int<0, dimension
    :param axis: 0=horizontal mirror, 1=vertical mirror
    :param flip: bool, flag for flipping other side when mirror is at center
    :return:
    """
    if len(picture.shape) == 3:
        h, w, c = picture.shape
    else:
        h, w = picture.shape

    if isinstance(pos, int):
        if axis == 0:
            center = np.clip(pos, 0, h)
        else:
            center = np.clip(pos, 0, w)

    elif isinstance(pos, float):
        if axis == 0:
            center = np.round(h * pos).astype(int)
        else:
            center = np.round(w * pos).astype(int)
    else:
        raise ValueError("Pos must be int or float")

    if axis == 0:
        "Horizontal Mirror"
        if center == h or center == 0:
            return np.flipud(picture)
        first = picture[:center]
        second = picture[center:]

        size1 = first.shape[0]
        size2 = second.shape[0]

    else:
        "Vertical mirror"
        if center == w or center == 0:
            return np.fliplr(picture)
        first = picture[:, :center]
        second = picture[:, center:]

        size1 = first.shape[1]
        size2 = second.shape[1]

    if size1 > size2:
        if axis == 0:
            mirrored = np.flipud(first)
            second = mirrored[:size2]
        else:
            mirrored = np.fliplr(first)
            second = mirrored[:, :size2]

    elif size2 > size1:
        if axis == 0:
            mirrored = np.flipud(second)
            first = mirrored[-size1:]
        else:
            mirrored = np.fliplr(second)
            first = mirrored[:, -size1:]

    elif flip:
        if axis:
            first = np.fliplr(second)
        else:
            first = np.flipud(second)
    else:
        if axis:
            second = np.fliplr(first)
        else:
            second = np.flipud(first)

    combined = np.concatenate([first, second], axis=axis)

    return combined