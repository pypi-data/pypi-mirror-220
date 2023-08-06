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
Mathematics related values, functions and enumerations.
"""

# Imports ===============================================================#

import enum
import math

from typing import Union

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

# 1 pica point = 25,4/72 milimeters
PICA_TO_MM = 25.4 / 72

INCH_TO_MM = 25.4

# Classes ===============================================================#


class FloatEnum(enum.Enum):
    """
    Enum class usable with float() function / method.
    """

    def __float__(self):
        if isinstance(self.value, float):
            return self.value

        return float(self.value)


# Fonctions =============================================================#


def truncate(number, digits) -> float:
    """
    Truncate value `number` to X `digits` digits.

    From Stack Overflow.

    <https://stackoverflow.com/questions/8595973/truncate-to-three-decimals-in-python>

    :type number: float
    :type digits: int
    :rtype: float
    """

    dec_number = len(str(number).split('.')[1])

    if dec_number <= digits:
        return number

    stepper = 10.0 ** digits

    return math.trunc(stepper * number) / stepper


def necessary_float(f: float) -> Union[float, int]:
    """
    Return **integer** if float f has no decimals, else returns **float**.

    :type f: float
    :param f: Float value
    :rtype: int,float
    :returns: Integer if float f has no decimals, else float.
    """

    if float(f) == int(f):
        return int(f)

    return float(f)


def mm(milimeters: Union[int, float]) -> float:
    """
    Returns milimeters in pica points.

    :type milimeters: int,float
    :param milimeters: Milimeters
    """

    return float(milimeters) / PICA_TO_MM


# vim:set shiftwidth=4 softtabstop=4:
