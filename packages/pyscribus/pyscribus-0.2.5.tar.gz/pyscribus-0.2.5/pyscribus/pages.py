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
Classes for SLA Pages / Master pages.
"""

# " Scribus pages are  arranged in a vast scratch space,  where 1 unit ==
# 1/72 inch.  Positive x is to  the right, and positive  y is downward.
# The positions, width and height in  the elements are in scratch space
# coordinates  with the  exception  of POCOOR  and COCOOR  coordinates,
# which are in the rotated and translated space of a PAGEOBJECT. "

# Imports ===============================================================#

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

from typing import Optional, NoReturn, Literal

from enum import Enum, IntEnum

import lxml
import lxml.etree as ET

import pyscribus.logs as logs
import pyscribus.common.xml as xmlc
import pyscribus.common.math as mathc
import pyscribus.exceptions as exceptions
import pyscribus.dimensions as dimensions

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

PageOrientation = Literal["portrait", "landscape"]

# FIXME Replace with Size(StrEnum) introduced in Python 3.11at some point
# in which the values are separated by commas

xml_size = {
    "A4": 'A4',
    "LETTER": 'letter',
    "CUSTOM": 'custom'
}

# Classes ===============================================================#


class Orientation(IntEnum):
    """
    Enum for DOC/@ORIENTATION values.
    """

    PORTRAIT = 0
    LANDSCAPE = 1


class PageAbstract(xmlc.PyScribusElement):
    """
    Abstract class for pages and master pages.

    Use Page or MasterPage classes instead.

    :type kwargs: dict
    :param kwargs: Quick setting (see kwargs table in Page, MasterPage)

    .. seealso:: :class:`MasterPage`, :class:`Page`
    """

    orientation_xml = {"portrait": "0", "landscape": "1"}
    autoguides_origin_xml = {"page": "0", "margins": "1", "selection": "2"}

    effect_source_xml = {"internal": "0", "external": "1"}
    effect_mobile_line_xml = {"horizontal": "0", "vertical": 1}

    effect_type_xml = {
        "none": "0",
        "masks": "1",
        "box": "2",
        "dissolve": "3",
        "glitter": "4",
        "break": "5",
        "delete": "6",
    }

    # NOTE These directions are in the correct order, but Scribus only allows
    # the user to select "left-to-right" in its GUI.
    effect_direction_xml = {
        "left-to-right": "0",
        "top-to-bottom": "1",
        "bottom-to-top": "2",
        "right-to-left": "3",
        "tl-to-br": "4",
    }

    def __init__(self, **kwargs):
        xmlc.PyScribusElement.__init__(self)

        self.box = dimensions.DimBox()

        self.borders = {
            "top": dimensions.Dim(40),
            "left": dimensions.Dim(40),
            "right": dimensions.Dim(40),
            "bottom": dimensions.Dim(40),
        }

        self.name = ""
        self.master_name = ""

        self.orientation = "portrait"

        self.paper_size = ""

        self.number = -1

        # FIXME Tester pour savoir comment constituer les listes ---------

        self.guides = {"horizontal": [], "vertical": []}

        # ----------------------------------------------------------------

        # @LEFT - For multipage spreads, which page in the spread is the left most
        self.is_leftest = False

        # FIXME Not documented -------------------------------------------

        # PRESET="0"

        # Auto guides ----------------------------------------------------

        self.auto_guides = {
            "lines": {
                # @AGhorizontalAutoCount
                "count": 0,
                # @AGhorizontalAutoGap
                "gap": dimensions.Dim(0),
                # @AGhorizontalAutoRefer
                "origin": "page"
            },
            "columns": {
                # @AGverticalAutoCount
                "count": 0,
                # @AGverticalAutoGap
                "gap": dimensions.Dim(0),
                # @AGverticalAutoRefer
                "origin": "page",
            },
            # @AGSelection
            # In XML, this is a string of floats X, Y, Width, Height separated
            # by spaces.
            "selection": {
                "posx": dimensions.Dim(0),
                "posy": dimensions.Dim(0),
                "width": dimensions.Dim(0),
                "height": dimensions.Dim(0),
            }
        }

        # PDF effects ----------------------------------------------------

        self.effect = {
            # @pageEffectDuration
            "duration": dimensions.Dim(1, unit="sec"),
            # @pageViewDuration
            "view-duration": dimensions.Dim(1, unit="sec"),
            # @effectType
            "type": "none",
            # @Dm
            "mobile-lines": "horizontal",
            # @M
            "source": "internal",
            # @Di
            "direction": "left-to-right",
        }

        # FIXME Not documented -------------------------------------------

        # Same as DOCUMENT/PDF/Effekte (PDF display effects) attributes ?

        # ----------------------------------------------------------------

        if kwargs:
            self._quick_setup(kwargs)

    def _quick_setup(self, settings: dict) -> NoReturn:
        """
        Method for defining (master)page settings from class
        instanciation kwargs.

        :type settings: dict
        :param settings: Kwargs dictionnary
        """

        if settings:
            xmlc.PyScribusElement._quick_setup(self, settings)

            for setting_name, setting_value in settings.items():

                # (Master) page box -------------------------------------------

                if setting_name == "posx":
                    self.box.setx("top-left", float(setting_value))

                if setting_name == "posy":
                    self.box.sety("top-left", float(setting_value))

                if setting_name == "width":
                    self.box.dims["width"].value = float(setting_value)

                if setting_name == "height":
                    self.box.dims["height"].value = float(setting_value)

                # Borders -----------------------------------------------------

                if setting_name in [
                    "rightborder",
                    "leftborder",
                    "topborder",
                    "bottomborder",
                ]:
                    side = setting_name.split("border")[0]
                    self.borders[side].value = float(setting_value)

                if setting_name == "borders":
                    # NOTE We solve borders settings like CSS margin property
                    # If only one value : same border for all sides
                    # If two values: vertical and horizontal borders
                    # If three values: top horizontal bottom
                    # If four values: top right bottom left

                    if isinstance(setting_value, list):
                        setting_len = len(setting_value)

                        if setting_len == 1:

                            for side in ["top", "right", "bottom", "left"]:
                                self.borders[side].value = float(
                                    setting_value[0]
                                )

                        if setting_len == 2:
                            sides = zip(
                                [["top", "bottom"], ["right", "left"]],
                                setting_value,
                            )

                            for side in sides:
                                for s in side[0]:
                                    self.borders[s].value = float(side[1])

                        if setting_len == 3:
                            self.borders["top"].value = float(setting_value[0])

                            for side in ["right", "left"]:
                                self.borders[side].value = float(
                                    setting_value[1]
                                )

                            self.borders["bottom"].value = float(
                                setting_value[2]
                            )

                        if setting_len == 4:
                            sides = zip(
                                ["top", "right", "bottom", "left"],
                                setting_value,
                            )

                            for side in sides:
                                self.borders[side[0]].value = float(side[1])

                # -------------------------------------------------------------

    def set_orientation(self, orientation: PageOrientation) -> bool:
        """
        Set (master) page orientation.

        :type orientation: string
        :param orientation: "portrait" or "landscape"
        :rtype: boolean
        :returns: boolean
        """

        if orientation.lower() in PageAbstract.orientation_xml.keys():
            self.orientation = orientation.lower()
            # FIXME TODO Modify (master) page box accordingly

            return True

        raise ValueError(
            "orientation parameter of set_orientation must be "
            "portrait' or 'landscape'"
        )

    def fromxml(self, xml: ET.Element, master: bool = False) -> bool:
        """
        Set (master) page attributes according to LXML Element

        :type xml: lxml.etree._Element
        :param xml: (Master) page source as XML element
        :type master: boolean
        :param master: If the page is a master page or not
        :rtype: boolean
        :returns: boolean
        """

        tag = {True: "MASTERPAGE", False: "PAGE"}[bool(master)]

        if xml.tag != tag:
            return False

        # Box settings ----------------------------------------

        posx = xml.get("PAGEXPOS")
        posy = xml.get("PAGEYPOS")
        dim_width = xml.get("PAGEWIDTH")
        dim_height = xml.get("PAGEHEIGHT")

        valid_box = 0

        for test in [posx, posy, dim_width, dim_height]:
            if test is not None:
                valid_box += 1

        if valid_box == 4:

            self.box.set_box(
                top_lx=posx, top_ly=posy, width=dim_width, height=dim_height
            )

        if (is_leftest := xml.get("LEFT")) is not None:
            self.is_leftest = xmlc.num_to_bool(is_leftest)

        # Name / Master page name -----------------------------

        self.name = xml.get("NAM")
        self.master_name = xml.get("MNAM")

        # Page number -----------------------------------------

        page_number = xml.get("NUM")

        if page_number is not None:
            # NOTE Page 0 is the first page so we adjust to a human
            # readable count
            self.number = int(page_number) + 1

        # Paper size name and orientation ---------------------

        if (paper_size := xml.get("Size")) is not None:
            self.paper_size = paper_size

        if (orientation := xml.get("Orientation")) is not None:

            for h, x in PageAbstract.orientation_xml.items():
                if orientation == x:
                    self.orientation = h
                    break

        # Borders ---------------------------------------------

        for b in ["left", "top", "bottom", "right"]:
            att = "BORDER{}".format(b.upper())
            self.borders[b] = dimensions.Dim(float(xml.get(att)))

        # Guides ----------------------------------------------

        for guide_type in ["vertical", "horizontal"]:

            att_name = "{}Guides".format(guide_type.capitalize())

            if (att := xml.get(att_name)) is not None:
                if att:
                    # NOTE Example of att value : "42.5197 56.6929 "

                    guides_list = []
                    guides_values = [g.strip() for g in att.split(" ")]

                    for g in guides_values:

                        if g:
                            guides_list.append(dimensions.Dim(float(g)))

                    self.guides[guide_type] = guides_list

        # Auto guides -----------------------------------------

        for case in [["lines", "horizontal"], ["columns", "vertical"]]:
            ag_count = xml.get("AG{}AutoCount".format(case[1]))
            ag_gap = xml.get("AG{}AutoGap".format(case[1]))
            ag_origin = xml.get("AG{}AutoRefer".format(case[1]))

            if ag_count is not None:
                ag_count = int(ag_count)
                self.auto_guides[case[0]]["count"] = ag_count

            if ag_gap is not None:
                ag_gap = float(ag_gap)
                self.auto_guides[case[0]]["gap"].value = ag_gap

            if ag_origin is not None:

                for human, code in PageAbstract.autoguides_origin_xml.items():
                    if ag_origin == code:
                        self.auto_guides[case[0]]["origin"] = human

        if (ag_selection := xml.get("AGSelection")) is not None:
            agx, agy, agw, agh = [float(dim) for dim in ag_selection.split()]

            self.auto_guides["selection"]["posx"].value = agx
            self.auto_guides["selection"]["posy"].value = agy
            self.auto_guides["selection"]["width"].value = agw
            self.auto_guides["selection"]["height"].value = agh

        # PDF effects ----------------------------------------------------

        if (duration := xml.get("pageEffectDuration")) is not None:
            self.effect["duration"].value = int(duration)

        if (view_duration := xml.get("pageViewDuration")) is not None:
            self.effect["view-duration"].value = int(view_duration)

        if (effect_type := xml.get("effectType")) is not None:
            for human, code in PageAbstract.effect_type_xml.items():
                if effect_type == code:
                    self.effect["type"] = human
                    break

        if (effect_lines := xml.get("Dm")) is not None:
            for human, code in PageAbstract.effect_mobile_line_xml.items():
                if effect_lines == code:
                    self.effect["mobile-lines"] = human
                    break

        if (effect_source := xml.get("M")) is not None:
            for human, code in PageAbstract.effect_source_xml.items():
                if effect_source == code:
                    self.effect["source"] = human
                    break

        if (effect_direction := xml.get("Di")) is not None:
            for human, code in PageAbstract.effect_direction_xml.items():
                if effect_direction == code:
                    self.effect["direction"] = human
                    break

        # FIXME This records undocumented attributes ----------

        self.undocumented = xmlc.all_undocumented_to_python(xml)

        return True

    def toxml(self, master: bool = False) -> ET.Element:
        """
        Returns (master) page as LXML Element

        :type master: bool
        :param master: If the page is a master page or not
        :rtype: lxml.etree._Element
        :returns: xml
        """

        # Appropriate tag if master page or page --------------

        tag = {True: "MASTERPAGE", False: "PAGE"}[bool(master)]

        xml = ET.Element(tag)

        # Position and dimensions -----------------------------

        xml.attrib["PAGEXPOS"] = self.box.coords["top-left"][0].toxmlstr()
        xml.attrib["PAGEYPOS"] = self.box.coords["top-left"][1].toxmlstr()

        xml.attrib["PAGEWIDTH"] = self.box.dims["width"].toxmlstr()
        xml.attrib["PAGEHEIGHT"] = self.box.dims["height"].toxmlstr()

        xml.attrib["LEFT"] = xmlc.bool_to_num(self.is_leftest)

        # Borders ---------------------------------------------

        for b in ["left", "right", "top", "bottom"]:
            att = "BORDER{}".format(b.upper())
            xml.attrib[att] = self.borders[b].toxmlstr(True)

        # Page number -----------------------------------------

        if self.number > 0:
            # NOTE Page 0 is the first page so we adjust back
            # from human counting to computer counting
            xml.attrib["NUM"] = str(self.number - 1)

        # Page name and master page name ----------------------

        xml.attrib["NAM"] = self.name
        xml.attrib["MNAM"] = self.master_name

        # (Master) page size name and orientation -------------

        xml.attrib["Size"] = self.paper_size
        xml.attrib["Orientation"] = PageAbstract.orientation_xml[
            self.orientation
        ]

        # Guides ----------------------------------------------

        for guide_type, guides in self.guides.items():
            att_name = "{}Guides".format(guide_type.capitalize())

            # NOTE Example of att value : "42.5197 56.6929 "

            guides_str = " ".join([g.toxmlstr(True) for g in guides])

            if guides_str.strip():
                xml.attrib[att_name] = guides_str
            else:
                xml.attrib[att_name] = ""

        # Auto guides -----------------------------------------

        for items, orientation in [
                ["lines", "horizontal"], ["columns", "vertical"]]:
            # Page lines / columns count
            # AGhorizontalAutoCount="2"
            # AGverticalAutoCount="3"
            count_att = f"AG{orientation}AutoCount"

            # Page lines / columns gap (gouttière)
            # AGhorizontalAutoGap="17.007874015748"
            # AGverticalAutoGap="22.6771653543307"
            gap_att = f"AG{orientation}AutoGap"

            # Page lines / columns origin
            # 0 = Page 1 = Margins
            # AGhorizontalAutoRefer="0"
            # AGverticalAutoRefer="0"
            orig_att = f"AG{orientation}AutoRefer"

            xml.attrib[count_att] = str(self.auto_guides[items]["count"])
            xml.attrib[gap_att] = self.auto_guides[items]["gap"].toxmlstr()
            xml.attrib[orig_att] = PageAbstract.autoguides_origin_xml[
                self.auto_guides[items]["origin"]
            ]

        # Check if auto guides if different from default value
        # If the X, Y, W, H of the selection are 0, then it is not custom

        custom_ag_selection = [
            dim.value
            for dim in self.auto_guides["selection"].values()
            if dim.value == 0.0
        ]
        custom_ag_selection = len(custom_ag_selection) != 4

        if custom_ag_selection:
            ag_selection = " ".join(
                [
                    mathc.truncate(self.auto_guides["selection"][number], 3)
                    for number in ["posx", "posy", "width", "height"]
                ]
            )

        else:
            ag_selection = "0 0 0 0"

        xml.attrib["AGSelection"] = ag_selection

        # --- PDF effects -------------------------------------------------

        xml.attrib["pageEffectDuration"] = self.effect["duration"].toxmlstr()
        xml.attrib["pageViewDuration"] = self.effect[
            "view-duration"
        ].toxmlstr()
        xml.attrib["effectType"] = PageAbstract.effect_type_xml[
            self.effect["type"]
        ]
        xml.attrib["Dm"] = PageAbstract.effect_mobile_line_xml[
            self.effect["mobile-lines"]
        ]
        xml.attrib["M"] = PageAbstract.effect_source_xml[self.effect["source"]]
        xml.attrib["Di"] = PageAbstract.effect_direction_xml[
            self.effect["direction"]
        ]

        # --- FIXME This exports undocumented attributes -------

        try:
            xml, undoc_attribs = xmlc.all_undocumented_to_xml(
                xml, self.undocumented, True, tag, logger=logs.getLogger()
            )

        except AttributeError:
            # NOTE If fromxml was not used
            pass

        return xml

    def fromdefault(self, master: bool = False, default: Optional[str]=False) -> NoReturn:
        """
        Set (master) page attributes according to known defaults.

        :type master: bool
        :param master: If the page is a master page or not
        :type default: str
        :param default: Name of the set of defaults ("a4", "letter")
        """

        for border in self.borders.values():
            border.value = 40

        dim_default = "a4"

        if default:
            for format_name in ["a4", "letter"]:
                if default.lower() == format_name:
                    dim_default = format_name
                    break

        self.master_name = "Normal"

        self.box.dims["width"].fromdefault("{}-width".format(dim_default))
        self.box.dims["height"].fromdefault("{}-height".format(dim_default))

        self.box.set_box(
            top_lx=100.0,
            top_ly=20.0,
            width=self.box.dims["width"].value,
            height=self.box.dims["height"].value,
        )


class Page(PageAbstract):
    """
    Page in SLA

    To add objects to this page, use Document.append()

    :type kwargs: dict
    :param kwargs: Quick setting (see kwargs table)

    +--------------+---------------------------------+------------+
    | Kwargs       | Setting                         | Value type |
    +==============+=================================+============+
    | default      | Equivalent to a ``fromdefault`` | boolean    |
    |              | call.                           | or string  |
    |              |                                 |            |
    |              | Value being True or the name of |            |
    |              | the default set.                |            |
    +--------------+---------------------------------+------------+
    | posx         | X position of the page          | float      |
    +--------------+---------------------------------+------------+
    | posy         | Y position of the page          | float      |
    +--------------+---------------------------------+------------+
    | width        | Page width                      | float      |
    +--------------+---------------------------------+------------+
    | height       | Page height                     | float      |
    +--------------+---------------------------------+------------+
    | borders      | Shorthand for :                 | List of    |
    |              |                                 | floats     |
    |              | *rightborder*, *leftborder*,    |            |
    |              | *topborder*, *bottomborder*     |            |
    |              |                                 |            |
    |              | Read like the CSS margin        |            |
    |              | property:                       |            |
    |              |                                 |            |
    |              | **With 1 float in the list :**  |            |
    |              |                                 |            |
    |              | [top & right & bottom & left]   |            |
    |              |                                 |            |
    |              | **With 2 float in the list :**  |            |
    |              |                                 |            |
    |              | [top & bottom, right & left]    |            |
    |              |                                 |            |
    |              | **With 3 float in the list :**  |            |
    |              |                                 |            |
    |              | [top, right & left, bottom]     |            |
    |              |                                 |            |
    |              | **With 4 float in the list :**  |            |
    |              |                                 |            |
    |              | [top, right, bottom, left]      |            |
    +--------------+---------------------------------+------------+
    | rightborder  | Right border                    | float      |
    +--------------+---------------------------------+------------+
    | leftborder   | Left border                     | float      |
    +--------------+---------------------------------+------------+
    | topborder    | Top border                      | float      |
    +--------------+---------------------------------+------------+
    | bottomborder | Bottom border                   | float      |
    +--------------+---------------------------------+------------+
    """

    def __init__(self, **kwargs):
        PageAbstract.__init__(self)
        PageAbstract._quick_setup(self, kwargs)

    def toxml(self) -> ET.Element:
        """
        Returns page as LXML Element

        :returns: xml
        :rtype: lxml.etree._Element
        """
        return PageAbstract.toxml(self, False)

    def fromxml(self, xml: ET.Element) -> bool:
        """
        Set page attributes according to LXML Element

        :type xml: lxml.etree._Element
        :param xml: Page source as XML element
        :rtype: bool
        :returns: bool
        """
        return PageAbstract.fromxml(self, xml, False)

    def fromdefault(self, default: Optional[str]=False) -> NoReturn:
        """
        Set page attributes according to known defaults.

        :type default: str
        :param default: Name of the set of defaults ("a4", "letter")
        """
        PageAbstract.fromdefault(self, False, default)

    def set_orientation(self, orientation: PageOrientation) -> bool:
        """
        Set page orientation.

        :type orientation: str
        :param orientation: "portrait" or "landscape"
        :rtype: bool
        :returns: bool
        """
        return PageAbstract.set_orientation(self, orientation)


class MasterPage(PageAbstract):
    """
    Master page in SLA

    To add objects to this master page, use Document.append()

    :type kwargs: dict
    :param kwargs: Quick setting (see kwargs table)

    +--------------+---------------------------------+------------+
    | Kwargs       | Setting                         | Value type |
    +==============+=================================+============+
    | default      | Equivalent to a ``fromdefault`` | boolean    |
    |              | call.                           | or string  |
    |              |                                 |            |
    |              | Value being True or the name of |            |
    |              | the default set.                |            |
    +--------------+---------------------------------+------------+
    | posx         | X position of the page          | float      |
    +--------------+---------------------------------+------------+
    | posy         | Y position of the page          | float      |
    +--------------+---------------------------------+------------+
    | width        | Page width                      | float      |
    +--------------+---------------------------------+------------+
    | height       | Page height                     | float      |
    +--------------+---------------------------------+------------+
    | borders      | Shorthand for :                 | List of    |
    |              |                                 | floats     |
    |              | *rightborder*, *leftborder*,    |            |
    |              | *topborder*, *bottomborder*     |            |
    |              |                                 |            |
    |              | Read like the CSS margin        |            |
    |              | property:                       |            |
    |              |                                 |            |
    |              | **With 1 float in the list :**  |            |
    |              |                                 |            |
    |              | [top & right & bottom & left]   |            |
    |              |                                 |            |
    |              | **With 2 float in the list :**  |            |
    |              |                                 |            |
    |              | [top & bottom, right & left]    |            |
    |              |                                 |            |
    |              | **With 3 float in the list :**  |            |
    |              |                                 |            |
    |              | [top, right & left, bottom]     |            |
    |              |                                 |            |
    |              | **With 4 float in the list :**  |            |
    |              |                                 |            |
    |              | [top, right, bottom, left]      |            |
    +--------------+---------------------------------+------------+
    | rightborder  | Right border                    | float      |
    +--------------+---------------------------------+------------+
    | leftborder   | Left border                     | float      |
    +--------------+---------------------------------+------------+
    | topborder    | Top border                      | float      |
    +--------------+---------------------------------+------------+
    | bottomborder | Bottom border                   | float      |
    +--------------+---------------------------------+------------+
    """

    def __init__(self, **kwargs):
        PageAbstract.__init__(self)
        PageAbstract._quick_setup(self, kwargs)

    def toxml(self) -> ET.Element:
        """
        Returns master page object as LXML Element

        :returns: xml
        :rtype: lxml.etree._Element
        """
        return PageAbstract.toxml(self, True)

    def fromxml(self, xml: ET.Element) -> bool:
        """
        Set master page attributes according to LXML Element

        :type xml: lxml.etree._Element
        :param xml: Master page source as XML element
        :rtype: bool
        :returns: bool
        """
        return PageAbstract.fromxml(self, xml, True)

    def fromdefault(self, default: Optional[str]=False) -> NoReturn:
        """
        Set master page attributes according to known defaults.

        :param default: Name of the set of defaults ("a4", "letter")
        :type default: str
        """
        PageAbstract.fromdefault(self, True, default)

    def set_orientation(self, orientation: PageOrientation):
        """
        Set master page orientation.

        :type orientation: str
        :param orientation: "portrait" or "landscape"
        :rtype: bool
        :returns: bool
        """
        return PageAbstract.set_orientation(self, orientation)


class PageSet(xmlc.PyScribusElement):
    """
    Page set object.

    DOCUMENT/PageSets/Set
    """

    DEFAULTS = {
        "Single Page": {"first": 0, "rows": 1, "columns": 1, "names": []},
        "Facing Pages": {
            "first": 1,
            "rows": 1,
            "columns": 2,
            "names": ["Left Page", "Right Page"],
        },
        "3-Fold": {
            "first": 0,
            "rows": 1,
            "columns": 3,
            "names": ["Left Page", "Middle", "Right Page"],
        },
        "4-Fold": {
            "first": 0,
            "rows": 1,
            "columns": 4,
            "names": [
                "Left Page",
                "Middle Left",
                "Middle Right",
                "Right Page",
            ],
        },
    }

    def __init__(self):
        xmlc.PyScribusElement.__init__(self)

        self.pyscribus_defaults = [k for k in PageSet.DEFAULTS.keys()]

        self.name = ""
        self.first_page = 0
        self.rows = 0
        self.columns = 0
        self.pages = []

    def fromdefault(self, default: str) -> bool:

        if default in self.pyscribus_defaults:

            accurate = PageSet.DEFAULTS[default]

            self.name = default
            self.rows = accurate["rows"]
            self.pages = accurate["names"]
            self.columns = accurate["columns"]
            self.first_page = accurate["first"]

            return True

        return False

    def toxml(self) -> ET.Element:
        """
        :rtype: lxml.etree._Element
        :returns: xml
        """

        xml = ET.Element("Set")

        # -----------------------------------------------------

        xml.attrib["Name"] = self.name
        xml.attrib["FirstPage"] = str(self.first_page)
        xml.attrib["Rows"] = str(self.rows)
        xml.attrib["Columns"] = str(self.columns)

        # Page names ------------------------------------------

        if self.pages:

            for page_name in self.pages:

                pnx = ET.Element("PageNames")
                pnx.attrib["Name"] = page_name
                xml.append(pnx)

        # FIXME This exports undocumented attributes ----------

        try:
            xml = xmlc.undocumented_to_xml(xml, self.undocumented, no_none=True)
        except AttributeError:
            # NOTE If fromxml was not used
            pass

        return xml

    def fromxml(self, xml: ET._Element) -> bool:
        """
        :type xml: lxml.etree._Element
        :param xml: Page set as XML element
        :rtype: bool
        :returns: bool
        """

        if xml.tag != "Set":
            return False

        # -----------------------------------------------------

        if (name := xml.get("Name")) is not None:
            self.name = name

        # -----------------------------------------------------

        for att in ["FirstPage", "Rows", "Columns"]:

            if (atx := xml.get(att)) is not None:

                try:
                    atx = int(atx)
                except ValueError:
                    raise exceptions.InsaneSLAValue(
                        "Page set @{} must be a number.".format(atx)
                    )

        if (first := xml.get("FirstPage")) is not None:
            self.first_page = int(first)

        if (rows := xml.get("Rows")) is not None:
            self.rows = int(rows)

        if (columns := xml.get("Columns")) is not None:
            self.columns = int(columns)

        # Page names ------------------------------------------

        for child in xml:
            if child.tag == "PageNames":
                page_name = child.get("Name")

                if page_name not in self.pages:
                    self.pages.append(page_name)

        # FIXME This records undocumented attributes ----------

        self.undocumented = xmlc.undocumented_to_python(
            xml, ["GapBelow", "GapHorizontal", "GapVertical"]
        )

        return True


# vim:set shiftwidth=4 softtabstop=4 spl=en:
