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
Layer class.
"""

# Imports ===============================================================#

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

from typing import Union, NoReturn

import lxml
import lxml.etree as ET

import pyscribus.exceptions as exceptions
import pyscribus.dimensions as dimensions

from pyscribus.common.xml import *

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

# Classes ===============================================================#


class Layer(PyScribusElement):
    """
    Layer in SLA (LAYERS)

    :type default: bool
    :param default: Set default attributes for layer
    """

    blendmodes_to_xml = {
        "normal": "0",
        "darken": "1",
        "lighten": "2",
        "multiply": "3",
        "screen": "4",
        "overlay": "5",
        "hard-light": "6",
        "soft-light": "7",
        "substract": "8",
        "exclusion": "9",
        "color-dodge": "10",
        "color-burn": "11",
        "hue": "12",
        "saturation": "13",
        "color": "14",
        "luminosity": "15",
    }

    def __init__(self, default=False):
        super().__init__()

        if default:
            self.fromdefault()
        else:
            self.name = ""
            self.level = 0
            self.number = 0
            self.opacity = dimensions.Dim(1, unit="pcdecim")
            self.visible = True
            self.editable = True
            self.printable = True
            self.color = "#000000"
            self.wireframe = False
            self.blend = "normal"
            self.flow = False
            self.selectable = False

    def fromdefault(self) -> NoReturn:
        self.name = "Fond de page"
        self.level = 0
        self.number = 0
        self.visible = True
        self.editable = True
        self.printable = True
        self.color = "#000000"
        self.wireframe = False
        self.opacity = dimensions.Dim(1, unit="pcdecim")
        self.blend = "normal"
        self.flow = True
        self.selectable = False

    def fromxml(self, xml: ET.Element) -> bool:
        number = xml.get("NUMMER")

        if number is not None:
            self.number = int(number)

            name = xml.get("NAME")
            edit = xml.get("EDIT")
            level = xml.get("LEVEL")
            color = xml.get("LAYERC")
            visible = xml.get("SICHTBAR")
            printable = xml.get("DRUCKEN")
            opacity = xml.get("TRANS")
            wireframe = xml.get("OUTL")

            # Blend mode of layer
            blend = xml.get("BLEND")

            # Habillage des cadres actif
            flow = xml.get("FLOW")

            # Wether the objets on the layout are selectable even if the layer
            # itself is not selected.
            selectable = xml.get("SELECT")

            if color is not None:
                self.color = color

            if name is not None:
                self.name = name

            if level is not None:
                self.level = int(level)

            if edit is not None:
                self.editable = num_to_bool(edit)

            if visible is not None:
                self.visible = num_to_bool(visible)

            if printable is not None:
                self.printable = num_to_bool(printable)

            if opacity is not None:
                self.opacity.value = float(opacity)

            if wireframe is not None:
                self.wireframe = num_to_bool(wireframe)

            if flow is not None:
                self.flow = num_to_bool(flow)

            if selectable is not None:
                self.selectable = num_to_bool(selectable)

            if blend is not None:

                for code, human in Layer.blendmodes_to_xml.items():

                    if code == blend:
                        self.blend = human
                        break

            return True

        return False

    def toxml(self) -> ET.Element:
        xml = ET.Element("LAYERS")

        xml.attrib["NUMMER"] = str(self.number)
        xml.attrib["LEVEL"] = str(self.level)
        xml.attrib["NAME"] = self.name

        for case in [
            ["SICHTBAR", self.visible],
            ["DRUCKEN", self.printable],
            ["EDIT", self.editable],
            ["SELECT", self.selectable],
            ["FLOW", self.flow],
        ]:
            xml.attrib[case[0]] = bool_to_num(case[1])

        xml.attrib["TRANS"] = self.opacity.toxmlstr()
        xml.attrib["BLEND"] = Layer.blendmodes_to_xml[self.blend]
        xml.attrib["OUTL"] = bool_to_num(self.wireframe)
        xml.attrib["LAYERC"] = self.color

        return xml


# vim:set shiftwidth=4 softtabstop=4 spl=en:
