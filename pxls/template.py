from io import BytesIO
from urllib.parse import parse_qs
from PIL import Image
import numpy as np
import requests


class Template(np.ndarray):
    """
    A class representing template images.
    """

    def __new__(cls, image: np.ndarray, x: int, y: int):
        """Initialize new template."""
        obj = image.view(cls)
        obj.x = x
        obj.y = y
        return obj
    
    def __array_finalize__(self, obj):
        """Numpy internals."""
        if obj is None: return
        self.x = getattr(obj, "x", None)
        self.y = getattr(obj, "y", None)

    @staticmethod
    def parse_url(url: str):
        """
        Parse a pxls.space template link.
        """
        url_dict = parse_qs(url)
        if "template" in url_dict.keys():
            return {
                "template": url_dict["template"][0],
                "width": int(url_dict["tw"][0]),
                "x": int(url_dict["ox"][0]),
                "y": int(url_dict["oy"][0]),
            }

        return {
            "template": url_dict["https://pxls.space/#template"][0],
            "width": int(url_dict["tw"][0]),
            "x": int(url_dict["ox"][0]),
            "y": int(url_dict["oy"][0]),
        }

    @classmethod
    def from_url(cls, url: str):
        """
        Generate a template from a pxls.space template link. \
        Supports pxls.fiddle templates.
        """
        # Parse the url to get parameters
        metadata = Template.parse_url(url)
        response = requests.get(metadata["template"])
        # Raise error if not 200
        response.raise_for_status()
        # Get a numpy array from the raw binary response
        img_raw = np.array(Image.open(BytesIO(response.content)).convert("RGBA"))
        # Each pixel from the original image was
        # replaced by a square block of pixels using template styles.
        # The code below reshapes the image to capture these blocks.
        block_size = img_raw.shape[1] // metadata["width"]
        blocks = img_raw.reshape(
            (
                img_raw.shape[0] // block_size,
                block_size,
                img_raw.shape[1] // block_size,
                block_size,
                4,
            )
        ).swapaxes(1, 2)
        # block -> pixel conversion
        img = np.max(blocks, axis=(2, 3))
        # Transparency sanitation
        transparency = img[:, :, 3]
        transparency[transparency < 255] = 0
        return cls(image=img, x=metadata["x"], y=metadata["y"])
