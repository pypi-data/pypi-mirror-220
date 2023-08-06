from dataclasses import dataclass
import openpyxl.styles as openpyxl


@dataclass(frozen=True)
class Color:
    hex: str

    @staticmethod
    def fromRGBO(r: int, g: int, b: int, opacity: float) -> 'Color':
        """
        r, g, b: 0 - 255
        opacity: 0.0 - 1.0
        """
        if opacity < 0 or opacity > 1:
            raise Exception(
                "Opacity out of range: The opacity needs to be between 0 inclusive and 1 inclusive")
        if r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255:
            raise Exception(
                "RGB out of range: The values for r,g and b need to be between 0 inclusive and 255 inclusive")
        r_hex: str = hex(r)[2:]
        g_hex: str = hex(g)[2:]
        b_hex: str = hex(b)[2:]
        opacity_hex: str = hex(round(opacity*255))[2:]
        return Color(opacity_hex + r_hex + g_hex + b_hex)

    def to_openpyxl(self):
        return openpyxl.Color(rgb=self.hex)


@dataclass(frozen=True)
class ColorGroup(Color):
    darkest: Color
    darker: Color
    dark: Color
    light: Color
    lighter: Color
    lightest: Color


class Colors:
    black = Color("FF000000")
    white = Color("FFFFFFFF")
    grey = ColorGroup(
        darkest=Color("FF11100F"),
        darker=Color("FF1B1A19"),
        dark=Color("FF252423"),
        hex="FF323130",
        light=Color("FF484644"),
        lighter=Color("FF797775"),
        lightest=Color("FF979593")
    )
    yellow = ColorGroup(
        darkest=Color("fff9a825"),
        darker=Color("fffbc02d"),
        dark=Color("fffdd835"),
        hex="ffffeb3b",
        light=Color("ffffee58"),
        lighter=Color("fffff176"),
        lightest=Color("fffff59d")
    )
    orange = ColorGroup(
        darkest=Color("ff993d07"),
        darker=Color("ffac4508"),
        dark=Color("ffd1540a"),
        hex="fff7630c",
        light=Color("fff87a30"),
        lighter=Color("fff99154"),
        lightest=Color("fffa9e68")
    )
    red = ColorGroup(
        darkest=Color("ff8f0a15"),
        darker=Color("ffa20b18"),
        dark=Color("ffb90d1c"),
        hex="ffe81123",
        light=Color("ffec404f"),
        lighter=Color("ffee5865"),
        lightest=Color("fff06b76")
    )
    magenta = ColorGroup(
        darkest=Color("ff6f0061"),
        darker=Color("ff7e006e"),
        dark=Color("ff90007e"),
        hex="ffb4009e",
        light=Color("ffc333b1"),
        lighter=Color("ffca4cbb"),
        lightest=Color("ffd060c2")
    )
    purple = ColorGroup(
        darkest=Color("ff472f68"),
        darker=Color("ff513576"),
        dark=Color("ff644293"),
        hex="FF744da9",
        light=Color("ff8664b4"),
        lighter=Color("ff9d82c2"),
        lightest=Color("ffa890c9")
    )
    blue = ColorGroup(
        darkest=Color("ff004a83"),
        darker=Color("ff005494"),
        dark=Color("ff0066b4"),
        hex="ff0078d4",
        light=Color("ff268cda"),
        lighter=Color("ff4ca0e0"),
        lightest=Color("ff60abe4")
    )
    teal = ColorGroup(
        darkest=Color("ff006e5b"),
        darker=Color("ff007c67"),
        dark=Color("ff00977d"),
        hex="ff00b294",
        light=Color("ff26bda4"),
        lighter=Color("ff4cc9b4"),
        lightest=Color("ff60cfbc")
    )
    green = ColorGroup(
        darkest=Color("ff094c09"),
        darker=Color("ff0c5d0c"),
        dark=Color("ff0e6f0e"),
        hex="ff107c10",
        light=Color("ff278927"),
        lighter=Color("ff4b9c4b"),
        lightest=Color("ff6aad6a")
    )
