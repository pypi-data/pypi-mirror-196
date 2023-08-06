import numpy as np

from PIL import Image
import cv2

from yasiu_image.filters import mirror


def read_gif_frames(path):
    img = Image.open(path, )
    ind = 0
    # sequence = []
    # img = img.convert("RGBA")
    img.seek(0)
    # fr = np.array(img, dtype=np.uint8)
    while True:
        fr = np.array(img, dtype=np.uint8).copy()
        # print(f"Read shape: {fr.shape}")
        # sequence.append(fr)
        yield fr

        ind += 1
        try:
            img.seek(ind)
        except EOFError:
            # print(f"Breaking at: {ind}")
            break


def read_webp_frames(path):
    img = Image.open(path)
    ind = 0

    img.seek(0)
    # fr = np.array(img, dtype=np.uint8)
    while True:
        fr = np.array(img, dtype=np.uint8).copy()
        yield fr

        ind += 1
        try:
            img.seek(ind)
        except EOFError:
            # print(f"Breaking at: {ind}")
            break


def save_image_list_to_gif(frames, exp_path, use_rgba=False, duration=40, quality=100, disposal=2):
    """

    Args:
        frames:
        exp_path: path to export file with ".gif" ending
        use_rgba: bool,
        duration: int, default 40, [ms], preferable in range <20, 80>
        quality: 100
        disposal: int, default 2 = clear

    Returns:

    """

    if not (exp_path.endswith("gif") or exp_path.endswith("GIF")):
        exp_path += ".gif"

    if use_rgba:
        for img in frames:
            print(img.shape)
            assert img.shape[2] == 3, f"Image must have alpha channel! But has: {img.shape}"

        pil_frames = [Image.fromarray(fr).convert("RGBA") for fr in frames]

        for pil_fr, fr in zip(pil_frames, frames):
            alpha_pil = Image.fromarray(fr[:, :, 3])
            pil_fr.putalpha(alpha_pil)

    else:
        pil_frames = [Image.fromarray(fr).convert("RGB") for fr in frames]

    pil_frames[0].save(
            exp_path, save_all=True, append_images=pil_frames[1:],
            optimize=False, loop=0,
            # background=(0, 0, 0, 255),
            quality=quality, duration=duration,
            disposal=disposal,
    )
    return 0


def resize_with_aspect_ratio(orig, resize_key='outer', new_dim=150):
    """

    :param sequence:
    :param resize_key:
        - outer
        - inner
        - height
        - width

    :param new_dim:
    :return:
    """
    h, w, c = orig.shape

    h_w_ratio = h / w
    w_h_ratio = w / h

    if h >= w and resize_key == 'outer':
        new_h = new_dim
        new_w = new_dim * w_h_ratio

    elif w >= h and resize_key == 'outer':
        new_w = new_dim
        new_h = new_dim * h_w_ratio

    elif resize_key == "height":
        new_h = new_dim
        new_w = new_dim * w_h_ratio

    elif resize_key == "width":
        new_w = new_dim
        new_h = new_dim * h_w_ratio

    elif h < w and resize_key == 'inner':
        new_h = new_dim
        new_w = new_dim * w_h_ratio
    else:
        new_w = new_dim
        new_h = new_dim * h_w_ratio

    new_h = np.round(new_h).astype(int)
    new_w = np.round(new_w).astype(int)

    # print(f"Resize: kwarg: {kwarg}")
    # sequence = [imutils.resize(fr, **kwarg) for fr in sequence]
    ret = cv2.resize(orig, (new_w, new_h))
    return ret


def downscale_with_aspect_ratio(orig, resize_key='outer', max_dimension=150):
    """
    Scales picture down if size exceeds give dimension.


    :param orig:


    :param resize_key: specify which axis to resize
    :type resize_key: float

    resize_key:
        #. `outer` : resize bigger axis
        #. `inner` : resize smaller axis
        #. `height`: check height size
        #. `width` : check width size
    :type: str


    :type resize_key: str

    :param max_dimension:
    :return:
    """
    h, w, c = orig.shape

    h_w_ratio = h / w
    w_h_ratio = w / h

    if h >= w and resize_key == 'outer' and h > max_dimension:
        new_h = max_dimension
        new_w = max_dimension * w_h_ratio

    elif w >= h and resize_key == 'outer' and w > max_dimension:
        new_w = max_dimension
        new_h = max_dimension * h_w_ratio

    elif resize_key == "height" and h > max_dimension:
        new_h = max_dimension
        new_w = max_dimension * w_h_ratio

    elif resize_key == "width" and w > max_dimension:
        new_w = max_dimension
        new_h = max_dimension * h_w_ratio

    elif h < w and resize_key == 'inner' and h < max_dimension:
        new_h = max_dimension
        new_w = max_dimension * w_h_ratio
    elif w < h and resize_key == 'inner' and w < max_dimension:
        new_w = max_dimension
        new_h = max_dimension * h_w_ratio
    else:
        return orig

    new_h = np.round(new_h).astype(int)
    new_w = np.round(new_w).astype(int)

    # print(f"Resize: kwarg: {kwarg}")
    # sequence = [imutils.resize(fr, **kwarg) for fr in sequence]
    ret = cv2.resize(orig, (new_w, new_h))
    return ret


def stack_images_to_grid(
        images, labels=None, font_scale=1.2, font_thickness=3,
        border=2,
        auto_convert_monochannel=True,
        pics_in_row=3
):
    h, w, c = images[0].shape

    if labels is None:
        labels = [''] * len(images)
    elif len(labels) != len(images):
        raise ValueError("Lables size does not match images number")

    output_pic = None
    row_pic = None

    for ind, (ch, lb) in enumerate(zip(images, labels)):
        if len(ch.shape) == 2 and auto_convert_monochannel:
            ch = ch[:, :, np.newaxis]
            rgb = np.concatenate([ch, ch, ch], axis=2)

        elif ch.shape[2] == 4:
            rgb = ch[:, :, :3]

        elif ch.shape[2] == 1:
            rgb = np.concatenate([ch, ch, ch], axis=2)

        else:
            # print("WHAT? What i missed?")
            # print(ch.shape)
            rgb = ch

        rgb = rgb.astype(np.uint8)

        rgb = cv2.putText(
                rgb, lb, (5, 30),
                fontScale=font_scale, fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(50, 50, 0),
                thickness=font_thickness + 5,
        )
        rgb = cv2.putText(
                rgb, lb, (5, 30),
                fontScale=font_scale, fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(50, 255, 0),
                thickness=font_thickness,
        )

        # print(f"row: {row_pic.shape}, rgb: {rgb.shape}")
        if row_pic is None:
            row_pic = rgb
        else:
            row_pic = np.concatenate([row_pic, rgb], 1)

        # print(f"Row Pic: {row_pic.shape}")

        if not ((ind + 1) % pics_in_row) and ind != 0:
            if output_pic is None:
                output_pic = row_pic
            else:
                output_pic = np.concatenate([output_pic, row_pic], axis=0)
            row_pic = None

    if row_pic is not None:
        if output_pic is None:
            output_pic = row_pic
        else:
            _, match_w, _ = output_pic.shape
            blank = np.zeros((h, match_w, c), dtype=np.uint8)
            cur_h, cur_w, _ = row_pic.shape
            blank[:cur_h, :cur_w] = row_pic
            output_pic = np.concatenate([output_pic, blank], axis=0)

    return output_pic


__all__ = ['read_webp_frames', 'read_gif_frames', 'save_image_list_to_gif','resize_with_aspect_ratio','stack_images_to_grid']

if __name__ == "__main__":
    cat_pic = cv2.imread("cat.jpg", 1)
    cat_pic = downscale_with_aspect_ratio(cat_pic, resize_key='outer', max_dimension=500)
    out = mirror(cat_pic, 0.2, axis=1, flip=True)

    # cv2.imshow("Cat orig", cat_pic)
    cv2.imshow("Cat mirrored", out)
    cv2.waitKey()
