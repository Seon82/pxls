from typing import Tuple, Dict, Any, Optional
from dataclasses import dataclass
import requests
from requests.compat import urljoin
import numpy as np
from .palette import Palette


@dataclass
class PxlsConnector:
    """
    An object used to easily fetch information from a pxls.space-like website.

    :param url: The url of the website.
    """

    url: str

    def _get_json(self, route: str) -> Dict[str, Any]:
        """Fetch the json data at self.url/route."""
        response = requests.get(urljoin(self.url, route))
        # Raise error if not 200
        response.raise_for_status()
        return response.json()

    def _get_metadata(self) -> Dict[str, Any]:
        """Fetch the canvas metadata from the /info endpoint."""
        return self._get_json("info")

    def get_palette(self) -> Palette:
        """Get the current color palette."""
        return Palette(self._get_metadata()["palette"])

    def get_shape(self) -> Tuple[int, int]:
        """
        Get the current canvas' shape.

        :return: (width, height)
        """
        metadata = self._get_metadata()
        return metadata["width"], metadata["height"]

    def get_stats(self) -> Dict[str, Any]:
        """Get the raw stats dictionary."""
        # TODO: implement custom Stats object
        return self._get_json("stats/stats.json")

    def get_canvas(
        self,
        palette: Optional[Palette] = None,
        canvas_shape: Optional[Tuple[int, int]] = None,
    ) -> np.ndarray:
        """
        Get the current canvas image.

        :param palette: *(optional)* The canvas' color palette.\
            Will fetched automatically if left unspecified.
        :param canvas_shape: *(optional)* A (canvas_width, canvas_height) tuple.\
            Will fetched automatically if left unspecified.
        """
        # Get raw board
        response = requests.get(urljoin(self.url, "boarddata?"))
        # Raise error if not 200
        response.raise_for_status()
        if canvas_shape is None:
            canvas_shape = self.get_shape()
        if palette is None:
            palette = self.get_palette()
        colors_dict = dict(enumerate(palette.get_colors("rgba")))
        colors_dict[255] = (0, 0, 0, 0)

        # We're getting a list of ints of length canvas_height*canvas_width from pxls.space
        # We then map each int these to their rgba color using colors_dict,
        # then reshape the output into an image.
        sort_idx = list(range(len(colors_dict)))
        arr = list(response.content)
        idx = np.searchsorted(sort_idx, arr, sorter=sort_idx)
        out = np.asarray(list(colors_dict.values()))[sort_idx][idx]
        img = out.reshape((canvas_shape[1], canvas_shape[0], 4))
        return img
