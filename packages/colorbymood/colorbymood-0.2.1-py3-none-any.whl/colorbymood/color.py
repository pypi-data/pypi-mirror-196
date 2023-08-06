"""handles import and conversion of color values."""
from colorsys import hls_to_rgb
from typing import TypeAlias, Union

from matplotlib.colors import rgb2hex

from colorbymood.io import load_dicts_from_yaml

frequency_dict: TypeAlias = dict[str, Union[str, float, list[tuple[float, ...]]]]


def get_colors_from_yaml() -> dict[str, dict[str, Union[list[float], frequency_dict]]]:
    colordict = load_dicts_from_yaml(filename="color.yaml")
    return colordict


def hls_to_hex(hue: float, luminance: float, saturation: float) -> str:
    rgb = hls_to_rgb(h=hue, l=luminance, s=saturation)
    return rgb2hex(c=rgb)


def get_hexf_from_key(
    color_key: str,
) -> tuple[str, dict[str, Union[str, float, list[tuple[float, ...]]]]]:
    colordict = get_colors_from_yaml()[color_key]
    hsl: list[float] = colordict["hls"]
    frequency: frequency_dict = colordict["frequency"]
    return (
        hls_to_hex(
            hue=hsl[0] / 360,
            saturation=hsl[1] / 100,
            luminance=hsl[2] / 100,
        ),
        frequency,
    )
