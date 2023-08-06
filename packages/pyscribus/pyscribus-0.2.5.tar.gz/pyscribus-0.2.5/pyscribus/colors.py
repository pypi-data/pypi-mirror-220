#!/usr/bin/python3
# -*- coding:Utf-8 -*-

# PyScribus, python library for Scribus SLA
# Copyright (C) 2020-2023 Étienne Nadji
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
PyScribus classes for colors and gradients.
"""

# Imports ===============================================================#

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

from typing import Union, NoReturn, Literal, List

import lxml
import lxml.etree as ET

import pyscribus.common.xml as xmlc
import pyscribus.common.math as pmath
import pyscribus.exceptions as exceptions
import pyscribus.dimensions as dimensions

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

ColorSpace = Literal["cmyk", "rgb"]

# Classes ===============================================================#


class Color(xmlc.PyScribusElement):
    """
    SLA Color (COLOR)

    :type kwargs: dict
    :param kwargs: Quick setting (see kwargs table)

    +------------+---------------------------------+-----------+
    | Kwargs     | Setting                         | Type      |
    +============+=================================+===========+
    | default    | Equivalent to a ``fromdefault`` | boolean   |
    |            | call.                           | or string |
    |            |                                 |           |
    |            | Value being True or the name of |           |
    |            | the default set.                |           |
    +------------+---------------------------------+-----------+
    | name       | Color name                      | string    |
    +------------+---------------------------------+-----------+
    | space      | Color space.                    | string    |
    |            |                                 |           |
    |            | Either "rgb" or "cmyk".         |           |
    +------------+---------------------------------+-----------+
    | cmyk       | Inks in C, M, Y, K order.       | list of   |
    |            |                                 | floats    |
    +------------+---------------------------------+-----------+
    | rgb        | Inks in R, G, B order.          | list of   |
    |            |                                 | floats    |
    +------------+---------------------------------+-----------+
    """

    defaults = {
        "Black": {"space": "cmyk", "colors": [0, 0, 0, 100]},
        "Blue": {"space": "rgb", "colors": [0, 0, 255]},
        "Cool Black": {"space": "cmyk", "colors": [60, 0, 0, 100]},
        "Cyan": {"space": "cmyk", "colors": [100, 0, 0, 0]},
        "Green": {"space": "rgb", "colors": [0, 255, 0]},
        "Magenta": {"space": "cmyk", "colors": [0, 100, 0, 0]},
        "Red": {"space": "rgb", "colors": [255, 0, 0]},
        "Registration": {
            "space": "cmyk",
            "colors": [100, 100, 100, 100],
            "register": True,
        },
        "Rich Black": {"space": "cmyk", "colors": [60, 40, 40, 100]},
        "Warm Black": {
            "space": "cmyk",
            "colors": [0, 60, 29.8039215686275, 100],
        },
        "White": {"space": "cmyk", "colors": [0, 0, 0, 0]},
        "Yellow": {"space": "cmyk", "colors": [0, 0, 100, 0]},
    }

    rgb = lambda s: s.lower() == "rgb"
    cmyk = lambda s: s.lower() == "cmyk"

    def __init__(
        self,
        name: str = "Black",
        space: str = "CMYK",
        colors: list = [0, 0, 0, 100],
        register: str = "0",
        **kwargs,
    ):
        super().__init__()

        self.pyscribus_defaults = [k for k in Color.defaults.keys()]

        self.name = name
        self.register = register

        self.colors = {}
        self.is_cmyk = False
        self.is_rgb = False

        self.set_space_colors(space, colors)

        self._quick_setup(kwargs)

    # Color management -----------------------------------------

    def space(self):
        try:
            return {True: "cmyk", False: "rgb"}[self.is_cmyk]
        except KeyError:
            return None

    def set_space_colors(
        self, space: ColorSpace, colors: List[float]
    ) -> NoReturn:
        """
        Set color space and color inks of the colors.

        :type space: string
        :param space: Color space. Either "cmyk" or "rgb".
        :type colors: list
        :param colors: List of inks values (float).

        :Example:

        .. code:: python

           # Green RGB
           color.set_space_colors("rgb", [0, 255, 0])

           # White CMYK
           color.set_space_colors("cmyk", [0, 0, 0, 0])

        """

        spaced = self.set_space(space)

        if spaced:
            self.set_colors(colors, self.space())

    def set_colors(
        self, colors: List[float], space: Union[ColorSpace, bool]
    ) -> bool:
        """
        :type colors: list
        :param colors: List of inks values (float).
        :type space: string
        :param space: Optionnal. Color space. Either "cmyk" or "rgb".
        :rtype: bool
        """

        if not space:
            space = {True: "cmyk", False: "rgb"}[self.is_cmyk]

        if space.lower() in ["cmyk", "rgb"]:

            if Color.cmyk(space):

                self.colors = {
                    "C": float(colors[0]),
                    "M": float(colors[1]),
                    "Y": float(colors[2]),
                    "K": float(colors[3]),
                }

                # Avoid invalid values

                for ink in ["C", "M", "Y", "K"]:

                    if self.colors[ink] > float(100.0):
                        self.colors[ink] = 100.0

                    if self.colors[ink] < float(0.0):
                        self.colors[ink] = 0.0

            if Color.rgb(space):
                self.colors = {
                    "R": float(colors[0]),
                    "G": float(colors[1]),
                    "B": float(colors[2]),
                }

                # Avoid invalid values

                for ink in ["R", "G", "B"]:
                    if self.colors[ink] > float(255.0):
                        self.colors[ink] = 255.0

                for ink in ["R", "G", "B"]:
                    if self.colors[ink] < float(0.0):
                        self.colors[ink] = 0.0

            return True

        return False

    def set_space(self, space: ColorSpace) -> bool:
        """
        Set the color space (CMYK / RGB) of the color.

        :type space: string
        :param space: Color space. Either "cmyk" or "rgb".
        :rtype: bool
        """

        space = space.lower()

        if space in ["cmyk", "rgb"]:
            self.is_cmyk = Color.cmyk(space)
            self.is_rgb = Color.rgb(space)

            return True

        return False

    # PyScribus standard methods -------------------------------

    def fromdefault(self, default: str = "Black") -> bool:
        """
        Set default attributes for this color.

        :Example:

        .. code:: python

           # with fromdefault method :
           black = Color()
           black.fromdefault("Black")

           # with quick setup :
           blue = Color(default="Blue")

        .. seealso::
            **For fromdefault explanation**:
            `pyscribus.common.xml.PyScribusElement.fromdefault`

            **For current class default sets**:
            `pyscribus.colors.Color.listdefaults`

        """

        if default in self.pyscribus_defaults:

            self.name = default

            self.set_space_colors(
                Color.defaults[default]["space"],
                Color.defaults[default]["colors"],
            )

            if "register" in Color.defaults[default]:
                self.register = True

            return True

        return False

    def fromxml(self, xml: ET.Element) -> bool:
        """
        :type xml: lxml.etree._Element
        :param xml: XML source of color
        :rtype: boolean
        :returns: True if XML parsing succeed
        """

        space = xml.get("SPACE")

        if space is None:
            return False

        # Name -------------------------------------------------------

        if (name := xml.get("NAME")) is not None:
            self.name = name

        # Space ------------------------------------------------------

        if space.lower() in ["cmyk", "rgb"]:
            self.set_space(space)

            # Colors -------------------------------------------------

            if self.is_cmyk:
                colors = [xml.get(c) for c in ["C", "M", "Y", "K"]]
            else:
                colors = [xml.get(c) for c in ["R", "G", "B"]]

            if not colors:
                raise exceptions.InvalidColor("No inks.")

            if None in colors:
                raise exceptions.InvalidColor(
                    "Invalid inks <{}>.".format(",".join(colors))
                )

            self.set_colors(colors, self.space())

        # Register ---------------------------------------------------

        if (reg := xml.get("Register")) is None:
            self.register = False
        else:
            if int(reg):
                self.register = True
            else:
                self.register = False

        # ------------------------------------------------------------

        return True

    def toxml(self) -> ET.Element:
        """
        :rtype: lxml.etree._Element
        :returns: Color as XML element
        """

        xml = ET.Element("COLOR")
        xml.attrib["NAME"] = self.name

        if self.is_cmyk:
            xml.attrib["SPACE"] = "CMYK"

            for color in ["C", "M", "Y", "K"]:
                color_value = pmath.necessary_float(self.colors[color])
                xml.attrib[color] = str(color_value)

        else:
            xml.attrib["SPACE"] = "RGB"

            for color in ["R", "G", "B"]:
                color_value = pmath.necessary_float(self.colors[color])
                xml.attrib[color] = str(color_value)

        if self.register:
            xml.attrib["Register"] = "1"

        return xml

    def _quick_setup(self, settings: dict) -> NoReturn:
        """
        Method for defining gradient stop settings from class
        instanciation kwargs.

        :type settings: dict
        :param settings: Kwargs dictionnary
        """

        if settings:
            xmlc.PyScribusElement._quick_setup(self, settings)

            # Color space is treated first. ------------------------------

            if "space" in settings:
                self.set_space(str(settings["space"]))
                settings.pop("space")

            for setting_name, setting_value in settings.items():

                # Color name ---------------------------------------------

                if setting_name == "name":
                    self.name = str(setting_value)

                # Setting colors -----------------------------------------

                if setting_name == "rgb":
                    if len(setting_value) < 3:
                        while len(setting_value) < 3:
                            setting_value.append(float(0))

                    setting_value = setting_value[:3]
                    self.set_colors(setting_value, self.space())

                if setting_name == "cmyk":
                    if len(setting_value) < 4:
                        while len(setting_value) < 4:
                            setting_value.append(float(0))

                    setting_value = setting_value[:4]
                    self.set_colors(setting_value, self.space())

    def same_space(self, other: Color) -> bool:
        """
        Is that color and other color share the same color space ?

        :param other: Color instance to compare.
        :type other: pyscribus.colors.Color
        :returns: True if both color share the same color space.
        :rtype: bool
        """

        # NOTE Obviously we don't translate colors of different spaces
        # to compare their inks, as RVB and CMYK color spectrums are
        # not the same.

        if self.is_cmyk and other.is_cmyk:
            return True
        if self.is_rgb and other.is_rgb:
            return True

        return False

    # Python __ methods ----------------------------------------

    def __iadd__(self, other: Color) -> Color:
        if not self.same_space(other):
            raise exceptions.ColorMixing(
                f"Colors {self} and {other} do not share the same color space."
            )

        # FIXME TODO Implement that !

        return self

    def __eq__(self, other: Color) -> bool:
        """
        Equality operator.

        Doesn’t check if RVB color can be an equivalent in CMYK.
        """

        if not self.same_space(other):
            return False

        # NOTE Self colors and other colors are in the same space, so
        # inks dicts have the same keys. So we get a list of
        # [(R1,R2)…] or [(C1,C2)…]. Having one ink different is enough.
        inks = zip(self.colors.values(), other.values())

        for ink in inks:
            if ink[0] != ink[1]:
                return False

        return True

    def __repr__(self):
        space_name = {True: "CMYK", False: "RGB"}[self.is_cmyk]
        inks = {True: ["C", "M", "Y", "K"], False: ["R", "G", "B"]}[
            self.is_cmyk
        ]

        return "{}:{}:{}:{}".format(
            self.name,
            space_name,
            ";".join([str(self.colors[ink]) for ink in inks]),
            self.register,
        )


class GradientColorStop(xmlc.PyScribusElement):
    """
    Gradient color stop (Gradient/CSTOP)

    :type kwargs: dict
    :param kwargs: Quick setting (see kwargs table)

    +------------+---------------------------------+-----------+
    | Kwargs     | Setting                         | Type      |
    +============+=================================+===========+
    | default    | Equivalent to a ``fromdefault`` | boolean   |
    |            | call.                           | or string |
    |            |                                 |           |
    |            | Value being True or the name of |           |
    |            | the default set.                |           |
    +------------+---------------------------------+-----------+
    | opacity    | Percentage of opacity,          | float     |
    |            | from 0 to 1.                    |           |
    +------------+---------------------------------+-----------+
    | name       | Color name                      | string    |
    +------------+---------------------------------+-----------+
    | position   |                                 |           |
    +------------+---------------------------------+-----------+
    | shade      |                                 |           |
    +------------+---------------------------------+-----------+

    :Example:

    .. code:: python

       cstop1 = colors.GradientColorStop(
           color="Black", shade=100, position=0, opacity=1
       )

    """

    def __init__(self, **kwargs):
        super().__init__()

        self.name = None
        self.shade = None
        self.opacity = None
        self.position = None

        self._quick_setup(kwargs)

    def __eq__(self, other) -> bool:
        """
        Equality operator.
        """

        def compare_property(a, b):
            if a is None:
                return b is not None

            if other.position is not None:
                return a.value != b.value

            return False

        if self.name != other.name:
            return False

        if compare_property(self.position, other.position):
            return False

        if compare_property(self.shade, other.shade):
            return False

        if compare_property(self.opacity, other.opacity):
            return False

        return True

    def _quick_setup(self, settings: dict) -> NoReturn:
        """
        Method for defining gradient stop settings from class
        instanciation kwargs.

        :type settings: dict
        :param settings: Kwargs dictionnary
        """

        if settings:
            xmlc.PyScribusElement._quick_setup(self, settings)

            for setting_name, setting_value in settings.items():

                if setting_name == "name":
                    self.name = setting_value

                if setting_name == "position":
                    self.position = dimensions.Dim(
                        float(setting_value), unit="pcdecim"
                    )

                if setting_name == "opacity":
                    self.opacity = dimensions.Dim(
                        float(setting_value), unit="pcdecim"
                    )

                if setting_name == "shade":
                    self.shade = dimensions.Dim(float(setting_value), unit="pc")

    def fromdefault(self) -> NoReturn:
        self.opacity = dimensions.Dim(100, unit="pc")
        self.position = dimensions.Dim(0, unit="pcdecim")

    def fromxml(self, xml: ET._Element):
        if xml.tag == "CSTOP":
            if (name := xml.get("NAME")) is not None:
                self.name = name

            if (shade := xml.get("SHADE")) is not None:
                self.shade = dimensions.Dim(float(shade), unit="pc")

            if (ramp := xml.get("RAMP")) is not None:
                self.position = dimensions.Dim(float(ramp), unit="pcdecim")

            if (opacity := xml.get("TRANS")) is not None:
                self.opacity = dimensions.Dim(float(opacity), unit="pcdecim")

            return True

        return False

    def toxml(self) -> ET.Element:
        xml = ET.Element("CSTOP")

        if self.position is not None:
            xml.attrib["RAMP"] = self.position.toxmlstr()

        xml.attrib["NAME"] = self.name

        if self.shade is None:
            xml.attrib["SHADE"] = "100"
        else:
            xml.attrib["SHADE"] = self.shade.toxmlstr(True)

        if self.opacity is None:
            xml.attrib["TRANS"] = "1"
        else:
            xml.attrib["TRANS"] = self.opacity.toxmlstr(True)

        return xml


class Gradient(xmlc.PyScribusElement):
    """
    Gradient in SLA (Gradient)
    """

    # <Gradient Name="Orange, Jaune" Ext="3">
    # </Gradient>

    def __init__(self):
        super().__init__()

        self.name = None
        self.stops = []

    def _sorted_stops(self) -> list:
        return sorted(self.stops, key=lambda s: s.position.value)

    def fromxml(self, xml: ET.Element) -> bool:
        if xml.tag == "Gradient":

            if (name := xml.get("Name")) is not None:
                self.name = name

            # TODO FIXME Ext

            for element in xml:
                if element.tag == "CSTOP":
                    grs = GradientColorStop()

                    if success := grs.fromxml(element):
                        self.stops.append(grs)

            return True

        return False

    def append_stop(self, stop: GradientColorStop, sort: bool = False) -> bool:
        """
        Append a gradient color stop.

        Avoids duplicates. Can sort stops by color stop position.

        :type stop: pyscribus.colors.GradientColorStop
        :param stop: Gradient color stop to append
        :type sort: boolean
        :param sort: Sort gradient color stops by position.
        """

        if isinstance(stop, GradientColorStop):

            duplicate = [cs for cs in self.stops if cs == stop]

            if not duplicate:

                self.stops.append(stop)

                if sort:
                    self.stops = self._sorted_stops()

                return True

        return False

    def toxml(self) -> ET.Element:
        xml = ET.Element("Gradient")

        xml.attrib["Name"] = self.name

        # TODO FIXME Ext

        if self.stops:

            # Sort the color stops of the gradient by their position in
            # the gradient spectrum, ranging from 0 to 100%

            for stop in self._sorted_stops():
                stop_xml = stop.toxml()
                xml.append(stop_xml)

        return xml


# vim:set shiftwidth=4 softtabstop=4 spl=en:
