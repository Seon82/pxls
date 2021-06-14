from typing import Union, List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class Palette:
    """
    An object used to represent an ordered color palette.
    """

    palette: List[Dict[str, str]]

    def get_colors(self, formatting: str = "rgb") -> List[Union[str, List[int]]]:
        """
        Get a list of the colors contained in the palette.

        :param formatting: The return formatting. Should be 'rgb', 'rgba', 'hex' or 'name'.
        """
        mapper = {
            "name": lambda c: c["name"],
            "hex": lambda c: c["value"],
            "rgb": lambda c: self.hex_to_rgb(c["value"]),
            "rgba": lambda c: (*self.hex_to_rgb(c["value"]), 255),
        }
        if formatting not in mapper:
            raise ValueError(f"Invalid value for format: {formatting}")
        return [mapper[formatting](c) for c in self.palette]

    @staticmethod
    def hex_to_rgb(hex_num: str) -> Tuple[int, int, int]:
        """
        Convert hex_num to a (R, G, B) tuple containing color components represented
        by integers between 0 and 255.

        :param hex_num: A hex color string with no leading #
        """
        return tuple(int(hex_num[i : i + 2], 16) for i in (0, 2, 4))
