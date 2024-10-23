from BlazeSudio.elementGen import Image as _Image, types as _Ts
import PIL.ImageChops as _ImageChops

def Overlay(img1, img2):
    """Overlay
    Overlay an image onto another image.

    Args:
        img1 (Image): The image to overlay.
        img2 (Image): The image to overlay.

    Returns:
        Img (Image): The overlayed image.
    """
    return _Image.from_PIL(_ImageChops.overlay(_Ts.convertTo(img1, _Image).to_PIL(), _Ts.convertTo(img2, _Image).to_PIL()))
