import numpy as np
import imageio as iio

import pylinhsu.color_transform as ct


def dim2_to_dim3(img):
    if img.ndim == 2:
        img = np.repeat(img, 3).reshape((*img.shape, -1))
    return img


def remove_alpha(img):
    if img.ndim == 2 or img.shape[2] < 4:
        return img
    ldr = img.dtype == np.uint8
    if ldr:
        img = ct.srgb_ldr_to_linear_hdr(img)
    img = img[:, :, :3]
    if ldr:
        img = ct.linear_hdr_to_srgb_ldr(img)
    return img


def add_alpha(img, alpha_map=None):
    img = dim2_to_dim3(img)
    if img.shape[2] == 1:
        img = np.repeat(img, 3, axis=-1)
    if img.shape[2] == 4 and alpha_map is None:
        return img
    ldr = img.dtype == np.uint8
    if ldr:
        img = ct.srgb_ldr_to_linear_hdr(img)
    if img.shape[2] == 4:
        img = remove_alpha(img)
    if alpha_map is None:
        alpha_map = np.ones(img.shape[:2])
    elif alpha_map.dtype == np.uint8:
        alpha_map = (alpha_map / 255.0).astype(np.float64)
    result = np.zeros((*img.shape[:2], 4))
    result[:, :, :img.shape[2]] = img
    result[:, :, 3] = alpha_map
    if ldr:
        result = ct.linear_hdr_to_srgb_ldr(result)
    return result


def crop_circle(img, radius=None):
    '''32x16 -> the center 16x16'''
    size = np.array(img.shape[:2])
    if not radius:
        radius = min(size) // 2
    m = (size // 2 - radius).astype(np.int32)
    M = (size // 2 + radius + size % 2).astype(np.int32)
    return img[m[0]:M[0], m[1]:M[1]]


def get_circle_mask(img, radius=None):
    '''32x16 -> 32x16 of bool, with only the center circle with radius 16 being True'''
    size = np.array(img.shape[:2])
    if not radius:
        radius = min(size) / 2
    radius2 = radius**2
    center = size / 2

    coordinates = np.indices(size).transpose((1, 2, 0)) + 0.5
    vec = coordinates - center
    dist2 = np.sum(vec**2, axis=-1)
    mask = dist2 < radius2
    return mask


circle_mask_sampled_cache = {}


def get_circle_mask_sampled(img, radius=None, sample_count=1024**2):
    '''32x16 -> 32x16 with only the center circle with radius 16 having non-zero SAMPLED alpha (max 1 for HDR, max 255 for LDR)'''
    cache_key = (img.shape[:2], radius)
    if cache_key in circle_mask_sampled_cache:
        mask = circle_mask_sampled_cache[cache_key]
        if img.dtype == np.uint8:
            mask = ct.hdr_to_ldr(mask)
        return mask

    size = np.array(img.shape[:2])
    same_odevity = not np.logical_xor.reduce(size % 2)
    if not radius:
        radius = min(size) / 2
    radius2 = radius**2
    center = size / 2

    coordinates = np.indices(size).transpose((1, 2, 0))
    in_out = np.zeros(size)
    for offset in ([0, 0], [0, 1], [1, 0], [1, 1]):
        vec = coordinates + offset - center
        dist2 = np.sum(vec**2, axis=-1)
        sign = dist2 < radius2
        in_out += sign
    mask = np.zeros(size)
    mask += (in_out == 4) * 1
    border = np.logical_and(in_out > 0, in_out < 4)
    r = np.random.rand(sample_count, 2)

    # Slow version.
    # for x in range(size[0]):
    #     for y in range(size[1]):
    #         if border[x, y]:
    #             pixel_center = np.array([x, y]) + 0.5
    #             pixel_center_vec = pixel_center - center
    #             vec = r + [x, y] - center
    #             dist2 = np.sum(vec**2, axis=-1)
    #             mask[x, y] = np.sum(dist2 < radius2) / sample_count

    # Fast version, 4x/8x speedup for same_odevity == False/True.
    for x in range(size[0]):
        for y in range(size[1]):
            if border[x, y]:
                pixel_center = np.array([x, y]) + 0.5
                pixel_center_vec = pixel_center - center
                if pixel_center_vec[0] >= 0 and pixel_center_vec[1] >= 0:
                    if same_odevity:
                        if pixel_center_vec[0] <= pixel_center_vec[1]:
                            vec = r + [x, y] - center
                            dist2 = np.sum(vec**2, axis=-1)
                            for p in (
                                    [x, y],
                                    [int(2 * center[0] - x - 0.5), y],
                                    [x, int(2 * center[1] - y - 0.5)],
                                    [int(2 * center[0] - x - 0.5), int(2 * center[1] - y - 0.5)]):
                                mask[p[0], p[1]] = np.sum(
                                    dist2 < radius2) / sample_count
                                mask[int(p[1] + 0.5 - center[1] + center[0]),
                                     int(p[0] + 0.5 - center[0] + center[1])] = mask[p[0], p[1]]
                    else:
                        vec = r + [x, y] - center
                        dist2 = np.sum(vec**2, axis=-1)
                        for p in (
                                [x, y],
                                [int(2 * center[0] - x - 0.5), y],
                                [x, int(2 * center[1] - y - 0.5)],
                                [int(2 * center[0] - x - 0.5), int(2 * center[1] - y - 0.5)]):
                            mask[p[0], p[1]] = np.sum(
                                dist2 < radius2) / sample_count
    circle_mask_sampled_cache[cache_key] = mask
    if img.dtype == np.uint8:
        mask = ct.hdr_to_ldr(mask)
    return mask


def mask_circle(img, radius=None):
    '''32x16 -> 16x16 with alpha, with only the center circle with radius 16 having max alpha (1 for HDR, 255 for LDR)'''
    img = crop_circle(img, radius)
    mask = get_circle_mask(img, radius)
    result = add_alpha(img)
    result = mask.reshape((mask.shape[0], mask.shape[1], 1)) * result
    return result


def mask_circle_sampled(img, radius=None, sample_count=1024**2):
    '''32x16 -> 16x16 with alpha, with only the center circle with radius 16 having non-zero SAMPLED alpha'''
    img = crop_circle(img, radius)
    ldr = img.dtype == np.uint8
    if ldr:
        img = ct.srgb_ldr_to_linear_hdr(img)
    mask = get_circle_mask_sampled(img, radius, sample_count)
    # img = np.concatenate([img[:, :, :3], mask[..., np.newaxis]], axis=-1)
    img = add_alpha(img, mask)
    if ldr:
        img = ct.linear_hdr_to_srgb_ldr(img)
    return img


def alpha_gradient_hdr_without_border(size=101):
    '''return size x size image with verticle HDR alpha gradient and border with color border_color and width 1'''
    img = np.ones((size, size, 4))
    alpha = np.linspace(0, 1, size)
    img = np.einsum('ijk,i->ijk', img, alpha)
    return img


def alpha_gradient_hdr(size=101, border=True, border_color=(1.0, 0.0, 0.0, 1.0)):
    '''return (size+2) x (size+2) image with verticle HDR alpha gradient and border with color border_color and width 1'''
    img = alpha_gradient_hdr_without_border(size)
    if border:
        img_with_border = np.full(
            (size+2, size+2, 4), border_color, dtype=np.float64)
        img_with_border[1:size+1, 1:size+1, :] = img
        img = img_with_border
    return img


def alpha_gradient_srgb_ldr(size=101, border=True, border_color=(255, 0, 0, 255)):
    '''return (size+2) x (size+2) image with verticle LDR alpha gradient and border with color border_color and width 1'''
    img = alpha_gradient_hdr_without_border(size)
    img = ct.linear_hdr_to_srgb_ldr(img)
    if border:
        img_with_border = np.full(
            (size+2, size+2, 4), border_color, dtype=np.uint8)
        img_with_border[1:size+1, 1:size+1, :] = img
        img = img_with_border
    return img


def blend(img_front, img_back):
    img_front = dim2_to_dim3(img_front)
    img_back = dim2_to_dim3(img_back)
    if img_front.shape[2] < 4 and img_back.shape[2] < 4:
        return img_front
    assert img_front.dtype == img_back.dtype
    ldr = img_front.dtype == np.uint8
    if ldr:
        img_front = ct.srgb_ldr_to_linear_hdr(img_front)
        img_back = ct.srgb_ldr_to_linear_hdr(img_back)
    img_front = add_alpha(img_front)
    img_back = add_alpha(img_back)
    img = img_front + (1 - img_front[:, :, 3:]) * img_back
    if ldr:
        img = ct.linear_hdr_to_srgb_ldr(img)
    return img


def lerp(a, b, t):
    if type(t) is not np.ndarray:
        t = np.array([t])
    y = np.einsum('i,...->i...', 1-t, a) + np.einsum('i,...->i...', t, b)
    if y.ndim == 2:
        y = y[np.newaxis, :]
    elif y.ndim == 3:
        y = np.moveaxis(y, 0, -2)
    else:
        assert y.ndim == 4
    return y
