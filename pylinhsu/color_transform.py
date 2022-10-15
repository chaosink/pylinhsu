import numpy as np


float_type = np.float64


def gamma(img_in, gamma=2.2):
    img = img_in.copy()
    img[:, :, :3] = img[:, :, :3] ** (1/gamma)
    return img


def linear_to_srgb(img_in, gamma=2.4):
    img = img_in.copy()
    a = 0.055
    img[img_in <= 0.0031308] = 12.92 * img[img_in <= 0.0031308]
    img[img_in > 0.0031308] = (
        (1 + a) * (img[img_in > 0.0031308] ** (1/gamma)) - a)
    img[:, :, 3] = img_in[:, :, 3]
    return img


def srgb_to_linear(img_in, gamma=2.4):
    img = img_in.copy()
    a = 0.055
    img[img_in <= 0.04045] = img[img_in <= 0.04045] / 12.92
    img[img_in > 0.04045] = ((img[img_in > 0.04045] + a) / (1 + a)) ** gamma
    img[:, :, 3] = img_in[:, :, 3]
    return img


def hdr_to_ldr(img):
    return np.clip(np.floor(img * 255 + 0.5), 0, 255).astype(np.uint8)


def ldr_to_hdr(img):
    return (img / 255.0).astype(float_type)


def linear_hdr_to_srgb_ldr(img_in, div_alpha=True, gamma=2.4):
    img = img_in
    if div_alpha:
        img = img.copy()
        img[:, :, :3][img[:, :, 3] != 0] /= img[:, :, 3:][img[:, :, 3] != 0]
    return hdr_to_ldr(linear_to_srgb(img, gamma))


def srgb_ldr_to_linear_hdr(img_in, mul_alpha=False, gamma=2.4):
    img = srgb_to_linear(ldr_to_hdr(img_in), gamma)
    if mul_alpha:
        img[:, :, :3] *= img[:, :, 3:]
    return img
