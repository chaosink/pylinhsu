import numpy as np
import colorsys
import skimage.color as color


FLOAT_TYPE = np.float64


def linear_to_gamma(img_in, gamma=2.2):
    img = img_in.copy()
    img[..., :3] = img[..., :3] ** (1/gamma)
    if img_in.shape[-1] == 4:
        img[..., 3] = img_in[..., 3]
    return img


def gamma_to_linear(img_in, gamma=2.2):
    img = img_in.copy()
    img[..., :3] = img[..., :3] ** gamma
    if img_in.shape[-1] == 4:
        img[..., 3] = img_in[..., 3]
    return img


def linear_to_srgb(img_in, gamma=2.4):
    img = img_in.copy()
    a = 0.055
    img[img_in <= 0.0031308] = 12.92 * img[img_in <= 0.0031308]
    img[img_in > 0.0031308] = (
        (1 + a) * (img[img_in > 0.0031308] ** (1/gamma)) - a)
    if img_in.shape[-1] == 4:
        img[..., 3] = img_in[..., 3]
    return img


def srgb_to_linear(img_in, gamma=2.4):
    img = img_in.copy()
    a = 0.055
    img[img_in <= 0.04045] = img[img_in <= 0.04045] / 12.92
    img[img_in > 0.04045] = ((img[img_in > 0.04045] + a) / (1 + a)) ** gamma
    if img_in.shape[-1] == 4:
        img[..., 3] = img_in[..., 3]
    return img


def hdr_to_ldr(img):
    return np.clip(np.floor(img * 255 + 0.5), 0, 255).astype(np.uint8)


def ldr_to_hdr(img):
    return (img / 255.0).astype(FLOAT_TYPE)


def linear_hdr_to_gamma_ldr(img_in, div_alpha=True, gamma=2.2):
    img = img_in
    if img.shape[-1] == 4 and div_alpha:
        img = img.copy()
        img[..., :3][img[..., 3] != 0] /= img[..., 3:][img[..., 3] != 0]
    return hdr_to_ldr(linear_to_gamma(img, gamma))


def gamma_ldr_to_linear_hdr(img_in, mul_alpha=False, gamma=2.2):
    img = gamma_to_linear(ldr_to_hdr(img_in), gamma)
    if img.shape[-1] == 4 and mul_alpha:
        img[..., :3] *= img[..., 3:]
    return img


def linear_hdr_to_srgb_ldr(img_in, div_alpha=True, gamma=2.4):
    img = img_in
    if img.shape[-1] == 4 and div_alpha:
        img = img.copy()
        img[..., :3][img[..., 3] != 0] /= img[..., 3:][img[..., 3] != 0]
    return hdr_to_ldr(linear_to_srgb(img, gamma))


def srgb_ldr_to_linear_hdr(img_in, mul_alpha=False, gamma=2.4):
    img = srgb_to_linear(ldr_to_hdr(img_in), gamma)
    if img.shape[-1] == 4 and mul_alpha:
        img[..., :3] *= img[..., 3:]
    return img


def hsv_to_rgb(x):
    def _hsv_to_rgb(x):
        return colorsys.hsv_to_rgb(*x)
    return np.apply_along_axis(_hsv_to_rgb, -1, x)


def rgb_to_hsv(x):
    def _rgb_to_hsv(x):
        return colorsys.rgb_to_hsv(*x)
    return np.apply_along_axis(_rgb_to_hsv, -1, x)


def hls_to_rgb(x):
    def _hls_to_rgb(x):
        return colorsys.hls_to_rgb(*x)
    return np.apply_along_axis(_hls_to_rgb, -1, x)


def rgb_to_hls(x):
    def _rgb_to_hls(x):
        return colorsys.rgb_to_hls(*x)
    return np.apply_along_axis(_rgb_to_hls, -1, x)


# Flawed. Don't use!
def complement_hue(x):
    r = 5/3

    # if x < 1/r:
    #     return (x + 1) / r
    # else:
    #     return (x - 1/r) * r
    # return (x < 1/r) * (x + 1) / r + (x > 1/r) * (x - 1/r) * r

    return (x < 1/r) * \
        (-1.1939*(x+1)**4 + 8.7596*(x+1)**3 - 20.411*(x+1)**2 + 19.587*(x+1) - 6.1415) \
        + (x >= 1/r) * \
        (-1.1939*x**4 + 8.7596*x**3 - 20.411*x**2 + 19.587*x - 6.1415)


# Flawed. Don't use!
def complement(rgb):
    hsv = rgb_to_hsv(rgb)
    hsv[0] = complement_hue(hsv[0])
    return hsv_to_rgb(hsv)


convert_colorspace = color.convert_colorspace
colorspaces = ['rgb', 'hsv', 'rgb cie', 'xyz', 'yuv', 'yiq', 'ypbpr', 'ycbcr', 'ydbdr']
