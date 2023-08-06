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
Classes related to marks management
"""

# Imports ===============================================================#

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

from typing import NoReturn, Literal, Optional, Union

import lxml
import lxml.etree as ET

import pyscribus.common.xml as xmlc
import pyscribus.exceptions as exceptions

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

MarkType = Literal["anchor", "objectref", "markref", "variable", "note"]

# Classes ===============================================================#


class DocumentMark(xmlc.PyScribusElement):
    """
    Mark element (DOCUMENT/Marks/Mark)
    """

    type_xml = {
        "anchor": "0",
        "objectref": "1",
        "markref": "2",
        "variable": "3",
        "note": "4",
    }

    def __init__(self):
        super().__init__()

        self.type = ""
        self.name = ""
        self.label = ""

        self.target_object = None
        self.target_mark = {"label": None, "type": "-1"}

        self.pyscribus_defaults = [k for k in DocumentMark.type_xml.keys()]

    def fromdefault(self, default: str) -> bool:
        """
        :type default: string
        :param default: Set of default settings to apply
        :rtype: boolean
        """

        if default in self.pyscribus_defaults:
            self.type = default

            return True

        return False

    def set_type(self, mtype: MarkType) -> bool:
        """
        :type mtype: string
        :param mtype: Mark type in pyscribus.marks.DocumentMark.type_xml keys()
        :rtype: boolean
        :returns: True if setting type succeed
        """

        if mtype in DocumentMark.type_xml.keys():
            self.type = DocumentMark.type_xml[mtype]
            return True

        return False

    def toxml(self) -> ET.Element:
        """
        :rtype: lxml.etree._Element
        :returns: XML representation of document mark
        """
        xml = ET.Element("Mark")

        if self.type:

            # --- Label -----------------------------------------------------

            # When @type is "3" (variable text), @str acts as @label
            # in other @types, and @label acts as a mark identifier.
            #
            # So :
            #   DocumentMark.name  = @label if @type == "3"
            #   DocumentMark.label = @label if @type != "3"

            if self.type == "variable":
                xml.attrib["label"] = self.name
            else:
                xml.attrib["label"] = self.label

            # ---------------------------------------------------------------

            xml.attrib["type"] = DocumentMark.type_xml[self.type]

            if self.type == "variable":
                xml.attrib["str"] = self.label

            if self.type == "objectref":
                xml.attrib["ItemID"] = self.target_object

            if self.type == "markref":
                xml.attrib["MARKlabel"] = self.target_mark["label"]
                xml.attrib["MARKtype"] = DocumentMark.type_xml[
                    self.target_mark["type"]
                ]

        else:
            raise exceptions.InsaneSLAValue("Invalid Marks/Mark @type")

        return xml

    def fromxml(self, xml: ET.Element) -> bool:
        """
        :rtype: boolean
        :returns: True if XML parsing succeed
        """

        if xml.tag != "Mark":
            return False

        mtype = xml.get("type")

        if mtype is not None:
            for human, code in DocumentMark.type_xml.items():
                if mtype == code:
                    self.type = human
                    break

        # --- Name and/or label -----------------------------------------

        # When @type is "3" (variable text), @str acts as @label
        # in other @types, and @label acts as a mark identifier.
        #
        # So :
        #   DocumentMark.name  = @label if @type == "3"
        #   DocumentMark.label = @label if @type != "3"

        if (mlabel := xml.get("label")) is not None:
            if self.type == "variable":
                self.name = mlabel
            else:
                self.label = mlabel

        if self.type == "variable":
            if (mstr := xml.get("str")) is not None:
                self.label = mstr

        # ---------------------------------------------------------------

        if self.type == "objectref":
            if (mitem := xml.get("ItemID")) is not None:
                self.target_object = mitem

        if self.type == "markref":
            if (mtarget_label := xml.get("MARKlabel")) is not None:
                self.target_mark["label"] = mtarget_label

            if (mtarget_type := xml.get("MARKtype")) is not None:

                if mtarget_type in DocumentMark.type_xml.values():
                    self.target_mark["type"] = DocumentMark.type_xml[
                        mtarget_type
                    ]
                else:
                    raise exceptions.InsaneSLAValue("Invalid Marks/Mark @type")

        return True


class StoryMarkAbstract(xmlc.PyScribusElement):
    """
    Abstract class for MARK elements in Scribus stories.

    :type mark_type: str
    :param mark_type: Type of mark
    :type label: str
    :param label: Mark label
    :type features: dict
    :param features: Text formatting features as dict

    .. seealso:: :class:`pyscribus.stories.StoryNoteMark`
    """

    def __init__(
        self,
        mark_type: MarkType,
        label: str = "",
        features: Optional[dict] = False,
    ):
        super().__init__()

        self.features = {
            "inherit": False,
            "superscript": False,
        }

        self.label = label

        if mark_type in DocumentMark.type_xml:
            self.type = mark_type
        else:
            raise ValueError("Unknown mark type")

        if features:
            self.set_features(features)

    def fromxml(self, xml: ET.Element) -> bool:
        if xml.tag != "MARK":
            return False

        if (mtype := xml.get("type")) is not None:
            for human, code in DocumentMark.type_xml.items():
                if mtype == code:
                    self.type = human
                    break

        if (mlabel := xml.get("label")) is not None:
            self.label = mlabel

        if (mfeatures := xml.get("features")) is not None:
            self.set_features(mfeatures)

        return True

    def toxml(self) -> ET.Element:
        xml = ET.Element("MARK")

        xml.attrib["type"] = DocumentMark.type_xml[self.type]
        xml.attrib["label"] = self.label

        have_features = len([f for f in self.features.values() if f])

        if have_features:
            features = []

            for feature_name, feature_value in self.features.items():
                if feature_value:
                    features.append(feature_name)

            features = " ".join(features)

            xml.attrib["FEATURES"] = features

        return xml

    def set_features(self, features: str):
        """
        :type features: str
        :param features: Formatting features as string separated by spaces.
            Ex: ``"inherit superscript"``
        :rtype: bool
        :returns: False if one features was not set.
        """

        features = features.split()

        fset = 0

        for feature in features:
            if feature in self.features:
                self.features[feature] = True
                fset += 1

        return fset == len(features)


class StoryNoteMark(StoryMarkAbstract):
    """
    Mark (MARK) for a (foot|end)note in Scribus stories.
    """

    def __init__(
        self,
        label: str = "",
        features: Optional[dict] = False,
        default: bool = False
    ):
        StoryMarkAbstract.__init__(self, "note", label, features)

        if default:
            self.fromdefault()

    def fromdefault(self) -> NoReturn:
        self.set_features("inherit superscript")

    def __repr__(self):
        return "NOTEMARK|{}|{}".format(
            self.label,
            [k for k in self.features if bool(k)],
        )


class StoryVariableMark(StoryMarkAbstract):
    """
    Variable text mark
    """

    def __init__(self, label: str = ""):
        StoryMarkAbstract.__init__(self, "variable", label, False)


class StoryAnchorMark(StoryMarkAbstract):
    """
    Anchor mark
    """

    def __init__(self, label: str = ""):
        StoryMarkAbstract.__init__(self, "anchor", label, False)


class StoryPageObjectRefMark(StoryMarkAbstract):
    """
    Reference to a page object mark
    """

    def __init__(self, label: str = ""):
        StoryMarkAbstract.__init__(self, "objectref", label, False)


class StoryMarkRefMark(StoryMarkAbstract):
    """
    Reference to a mark... mark
    """

    def __init__(self, label: str = ""):
        StoryMarkAbstract.__init__(self, "markref", label, False)


def story_mark_from_xml(
    xml: ET.Element,
) -> Union[
    StoryAnchorMark,
    StoryPageObjectRefMark,
    StoryMarkRefMark,
    StoryVariableMark,
    StoryNoteMark,
]:
    """
    Return the relevant subclass of StoryMarkAbstract from a story mark
    XML element.
    """

    mark_type = xml.get("type")

    if mark_type is None:
        return False

    # Match StoryMarkAbstract subclass to a mark type encoded in MARK/@type

    mark_class = None

    for human, code in DocumentMark.type_xml.items():
        if mark_type == code:
            mark_class = {
                "anchor": StoryAnchorMark,
                "objectref": StoryPageObjectRefMark,
                "markref": StoryMarkRefMark,
                "variable": StoryVariableMark,
                "note": StoryNoteMark,
            }[human]
            break

    if mark_class is None:
        return False

    # Initialize new mark ---------------------------------

    new_mark = mark_class()
    success = new_mark.fromxml(xml)

    # Or fail to do so

    if not success:
        return False

    return new_mark


# vim:set shiftwidth=4 softtabstop=4 spl=en:
