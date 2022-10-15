import numpy as np

float_type = np.float64

def Gamma(img_in, gamma=2.2):
    img = img_in.copy()
    img[:,:,:3] = img[:,:,:3] ** (1/gamma)
    return img

def Linear2Srgb(img_in, gamma=2.4):
    img = img_in.copy()
    a = 0.055
    img[img_in <= 0.0031308] =     12.92 * img[img_in <= 0.0031308]
    img[img_in >  0.0031308] = ((1 + a) * (img[img_in >  0.0031308] ** (1/gamma)) - a)
    img[:,:,3] = img_in[:,:,3]
    return img

def Srgb2Linear(img_in, gamma=2.4):
    img = img_in.copy()
    a = 0.055
    img[img_in <= 0.04045] =   img[img_in <= 0.04045] / 12.92
    img[img_in >  0.04045] = ((img[img_in >  0.04045] + a) / (1 + a)) ** gamma
    img[:,:,3] = img_in[:,:,3]
    return img

def Hdr2Ldr(img):
    return np.clip(np.floor(img * 255 + 0.5), 0, 255).astype(np.uint8)

def Ldr2Hdr(img):
    return (img / 255.0).astype(float_type)

def LinearHdr2SrgbLdr(img_in, div_alpha=True, gamma=2.4):
    img = img_in
    if div_alpha:
        img = img.copy()
        img[:,:,:3][img[:,:,3] != 0] /= img[:,:,3:][img[:,:,3] != 0]
    return Hdr2Ldr(Linear2Srgb(img, gamma))

def SrgbLdr2LinearHdr(img_in, mul_alpha=False, gamma=2.4):
    img = Srgb2Linear(Ldr2Hdr(img_in), gamma)
    if mul_alpha:
        img[:,:,:3] *= img[:,:,3:]
    return img
