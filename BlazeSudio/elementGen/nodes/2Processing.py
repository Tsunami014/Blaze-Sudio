from BlazeSudio.elementGen import Image, types
from PIL import ImageChops

__all__ = [
    'Overlay'
]

def Overlay(img1, img2):
    """Overlay
    Overlay an image onto another image.

    Args:
        img1 (Image): The image to overlay.
        img2 (Image): The image to overlay.

    Returns:
        Img (Image): The overlayed image.
    """
    return Image.from_PIL(ImageChops.overlay(types.convertTo(img1, Image).to_PIL(), types.convertTo(img2, Image).to_PIL()))
