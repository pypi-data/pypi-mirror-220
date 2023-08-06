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
PyScribus module for PDF & printing settings / elements.
"""

# Imports ===============================================================#

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

import collections

from typing import NoReturn, Union

import lxml
import lxml.etree as ET

import pyscribus.exceptions as exceptions

from pyscribus.common.xml import *

import pyscribus.dimensions as dimensions

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

# Classes ===============================================================#


class PDFSettings(PyScribusElement):
    """
    Class for PDF export settings in SLA
    """

    imgcomp_method_xml = {"automatic": 0, "jpeg": 1, "flate": 2, "none": 3}

    imgcomp_quality_xml = {
        "max": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
        "min": 4,
    }

    def __init__(self):
        super().__init__()

        self.lpi = []
        self.use_lpi = False

        self.text_compression = True
        self.image_compression = {"method": "automatic", "quality": "max"}

        # ------------------------------------------------------

        # Flag, set to 1 when Presentation effects should be used
        PresentMode = "0"

        # ------------------------------------------------------

        # Flag, set to 1 when Downsample Images is checked in the PDF-Options Dialog
        RecalcPic = "0"
        # Resolution for downsampling Images
        PicRes = "300"
        # Resolution for embedded EPS-Pictures or PDF's
        Resolution = "300"

        # ------------------------------------------------------

        # (optional) Flag, set to 1 when Output should be in RGB
        RGBMode = "1"

        # TODO : fromxml / toxml of this dict

        self.profiles = {
            "colors": {
                # (optional) Flag, set to 1 when ICC-Profiles should be used
                # for solid colours
                # UseProfiles="0"
                "used": False,
                # (optional) ICC-Profile for solid colours
                # SolidP="sRGB IEC61966-2.1"
                "name": "sRGB IEC61966-2.1",
            },
            "images": {
                # (optional) Flag, set to 1 when ICC-Profiles should be used
                # for images
                # UseProfiles2="0"
                "used": False,
                # ICC-Profile for images ?
                # ImageP="sRGB IEC61966-2.1"
                "name": "sRGB IEC61966-2.1",
            },
            "printer": {
                # (optional) ICC-Profile for the Printer, only used for
                # PDF-X/3 output
                # PrintP="Fogra27L CMYK Coated Press"
                "name": "Fogra27L CMYK Coated Press"
            },
        }

        # ------------------------------------------------------

        self.bleeds = collections.OrderedDict()
        self.bleeds["top"] = dimensions.Dim(0)
        self.bleeds["left"] = dimensions.Dim(0)
        self.bleeds["right"] = dimensions.Dim(0)
        self.bleeds["bottom"] = dimensions.Dim(0)
        self.bleeds["document"] = False

        # ------------------------------------------------------

        self.marks = {
            # bool as 0 or 1

            # bleedMarks (dimensions of bleeds in self.bleeds)
            "bleeds": False,
            # cropMarks, cuting marks
            "croping": False,
            # docInfoMarks, page infos
            "infos": False,
            # colorMarks, color reference
            "colors": False,
            # registrationMarks, page alignment
            "alignment": False,

            # pica dims

            # markOffset
            "offset": dimensions.Dim(0),
            # markLength, 7.056mm but encoded in pics => roughly 20
            "length": dimensions.Dim(20),
        }

        # ------------------------------------------------------

        # All         : -2359300
        # None        : -2359360
        # Only print  : -2359356
        # Only modify : -2359352
        # Only copy   : -2359344
        # Only annoto : -2359328

        self.encryption = {
            "pass": {"owner": "", "user": ""},
            "settings": {"permissions": "-4", "encrypted": False},
        }

        # FIXME Documented but to organize ----------------------

        # Binding for the PDF-Document 0 = Left Binding 1 = Right Binding
        Binding = "0"

        # PDF version -------------------------------------------

        self.version = "13"

        # FIXME Documented but to organize ----------------------

        self.objects = {
            # Flag, set to 1 when Generate Thumbnails is checked in the
            # PDF-Options Dialog
            # Thumbnails = "0"
            "thumbnails": False,
            # Flag, set to 1 when include Bookmarks is checked in the
            # PDF-Options Dialog
            # Bookmarks = "0"
            "bookmarks": False,
            # Flag, set to 1 when use PDF-Articles is checked in the
            # PDF-Options Dialog
            # Articles = "0"
            "articles": False,
            # EmbedPDF="0"
            "embedded_pdf": False,
        }

        # FIXME Undocumented, managed with undocumented funs ----

        # ImagePr="0"
        # UseLayers="0"
        # UseSpotColors="1"
        # doMultiFile="0"
        # displayBookmarks="0"
        # displayFullscreen="0"
        # displayLayers="0"
        # displayThumbs="0"
        # hideMenuBar="0"
        # hideToolBar="0"
        # fitWindow="0"
        # openAfterExport="0"
        # PageLayout="0"
        # openAction=""
        # Intent="1"
        # Intent2="0"
        # InfoString=""
        # FontEmbedding="0"
        # Grayscale="0"
        # firstUse="1"
        # Clip="0"
        # rangeSel="0"
        # rangeTxt=""

        # Transformation ----------------------------------------

        self.transformation = {
            # RotateDeg="0"
            # Four values: 0, 90, 180, 270
            "rotation": dimensions.Dim(0, unit="deg", integer=True),
            # MirrorH="0"
            "mirror_h": False,
            # MirrorV="0"
            "mirror_v": False,
        }

    def set_version(self, version: Union[str, int, float]):
        # We should check against Scribus version because
        # PDF-X-3, PDF-X-4, PDF-X-1a seems not available in Scribus 1.5.

        # 12 = PDF-X/3
        # 13 = PDF-1.3 (Acrobat 4)
        # 14 = PDF-1.4 (Acrobat 5)
        # 15 = PDF-1.5 (Acrobat 6)
        # 16 = PDF-1.6 (Acrobat 7)

        new_version = None

        if isinstance(version, float):

            if int(version) in [13, 14, 15, 16]:
                self.version = str(int(version))
                return True

            if version in [1.3, 1.4, 1.5, 1.6]:
                new_version = str(version)
                self.version = new_version.replace(".", "")
                return True

        if isinstance(version, int):

            if version in [13, 14, 15, 16]:
                self.version = str(version)
                return True

        if isinstance(version, str):

            if version in ["1.3", "1.4", "1.5", "1.6"]:
                new_version = version
                self.version = new_version.replace(".", "")
                return True

            if version.startswith("acrobat-"):
                acro_version = version.split("acrobat-")[-1]

                if not acro_version:
                    return False

                try:
                    self.version = {
                        "4": "13",
                        "5": "14",
                        "6": "15",
                        "7": "16",
                    }[acro_version]
                    return True
                except KeyError:
                    return False

            if version == "X/3":
                self.version = "12"
                return True

        return False

    def fromxml(self, xml: ET.Element) -> bool:

        if xml.tag != "PDF":
            return False

        # TODO

        text_comp = xml.get("Compress")

        if text_comp is not None:
            self.text_compression = num_to_bool(text_comp)

        # Image compression : method and quality -----------

        for sett in [
            [xml.get("CMethod"), "method", PDFSettings.imgcomp_method_xml],
            [xml.get("Quality"), "quality", PDFSettings.imgcomp_quality_xml],
        ]:

            if (att := xml.get(sett[0])) is not None:
                if int(att) in sett[2].values():
                    for human, code in sett[2].items():
                        self.image_compression[sett[1]] = human
                        break
                else:
                    raise exceptions.InsaneSLAValue(
                        "Unknown image compression {}.".format(sett[1])
                    )

        # Bleed settings -----------------------------------

        for edge in ["top", "left", "right", "bottom"]:
            att_name = f"B{edge.capitalize()}"

            if (att := xml.get(att_name)) is not None:
                self.bleeds[edge].value = float(att)

        udb = xml.get("useDocBleeds")

        if udb is not None:
            self.bleeds["document"] = num_to_bool(udb)

        # PDF marks settings -------------------------------

        for mark_tag, mark_key in [
                ["bleedMarks", "bleeds"],
                ["cropMarks", "croping"],
                ["docInfoMarks", "infos"],
                ["colorMarks", "colors"],
                ["registrationMarks", "alignment"]]:

            if (attrib := xml.get(mark_tag)) is not None:
                self.marks[mark_key] = num_to_bool(attrib)

        for mark_tag, mark_key in [
                ["markOffset", "offset"],
                ["markLength", "length"]]:
            if (attrib := xml.get(mark_tag)) is not None:
                self.marks[mark_key].value = float(attrib)

        # Version --------------------------------------------------------

        version = xml.get("Version")

        if version is not None:
            self.version = version

        # Objects to embed / generate ------------------------------------

        embedded_pdf = xml.get("EmbedPDF")
        thumbnails = xml.get("Thumbnails")
        bookmarks = xml.get("Bookmarks")
        articles = xml.get("Articles")

        for att_value, human in [
                [thumbnails, "thumbnails"], [bookmarks, "bookmarks"],
                [articles, "articles"], [embedded_pdf, "embedded_pdf"]]:
            if att_value is None:
                continue

            self.objects[human] = num_to_bool(att_value)

        # Transformation ----------------------------------------

        rotation = xml.get("RotateDeg")

        if rotation is not None:
            try:
                rotation = int(rotation)

                if rotation in [0, 90, 180, 270]:
                    self.transformation["rotation"].value = rotation
                else:
                    raise exceptions.InsaneSLAValue(
                        "PDF settings Rotation: "
                        "Allowed values are 0, 90, 180, 270. "
                        f"Got {rotation}."
                    )
            except ValueError:
                raise exceptions.InsaneSLAValue(
                    "PDF settings Rotation: "
                    "Requires an integer. "
                    f"Got {rotation}."
                )

        mirrorh = xml.get("MirrorH")
        mirrorv = xml.get("MirrorV")

        for att_value, human in [
                [mirrorh, "mirror_h"],  [mirrorv, "mirror_v"]]:
            if att_value is None:
                continue

            self.transformation[human] = num_to_bool(att_value)

        # PDF encryption settings-----------------------------------------

        encrypt = xml.get("Encrypt")
        encrypt_perm = xml.get("Permissions")

        for pass_key, pass_tag in [["owner", "PassOwner"], ["user", "PassUser"]]:
            if (attrib := xml.get(pass_tag)) is not None:
                self.encryption["pass"][pass_key] = attrib

        if encrypt is not None:
            self.encryption["settings"]["encrypted"] = num_to_bool(encrypt)

        if encrypt_perm is not None:
            self.encryption["settings"]["permissions"] = encrypt_perm

        # Line per inch settings ---------------------------

        # Flag, set to 1 when the informations in the LPI tags should be used
        # for Linescreening
        # IT IS NOT OPTIONAL
        uselpi = xml.get("UseLpi")
        if uselpi is not None:
            self.use_lpi = num_to_bool(uselpi)

        for element in xml:
            if element.tag != "LPI":
                continue

            lpi_item = LPI()
            success = lpi_item.fromxml(element)

            if success:
                self.lpi.append(lpi_item)

        # FIXME This records undocumented attributes ----------

        self.undocumented = undocumented_to_python(
            xml,
            [
                "ImagePr",
                "UseLayers",
                "UseSpotColors",
                "doMultiFile",
                "displayBookmarks",
                "displayFullscreen",
                "displayLayers",
                "displayThumbs",
                "hideMenuBar",
                "hideToolBar",
                "fitWindow",
                "openAfterExport",
                "PageLayout",
                "openAction",
                "Intent",
                "Intent2",
                "InfoString",
                "FontEmbedding",
                "Grayscale",
                "firstUse",
                "Clip",
                "rangeSel",
                "rangeTxt",
            ],
        )

        return True

    def toxml(self) -> ET.Element:
        xml = ET.Element("PDF")

        xml.attrib["Compress"] = bool_to_num(self.text_compression)

        xml.attrib["CMethod"] = str(
            PDFSettings.imgcomp_method_xml[self.image_compression["method"]]
        )

        xml.attrib["Quality"] = str(
            PDFSettings.imgcomp_quality_xml[self.image_compression["quality"]]
        )

        # Bleed settings -----------------------------------

        for bleed_config, bleed_value in self.bleeds.items():

            if bleed_config != "document":
                att_name = "B{}".format(bleed_config.capitalize())
                # FIXME Sometimes raises errors (when PDF/@BTop="0") because
                # not a list
                try:
                    xml.attrib[att_name] = bleed_value[0].toxmlstr()
                except:
                    xml.attrib[att_name] = bleed_value.toxmlstr()

        xml.attrib["useDocBleeds"] = bool_to_num(self.bleeds["document"])

        # PDF marks settings -------------------------------

        for mark_tag, mark_key in [
                ["bleedMarks", "bleeds"],
                ["cropMarks", "croping"],
                ["docInfoMarks", "infos"],
                ["colorMarks", "colors"],
                ["registrationMarks", "alignment"]]:
            xml.attrib[mark_tag] = bool_to_num(self.marks[mark_key])

        for mark_tag, mark_key in [
                ["markOffset", "offset"],
                ["markLength", "length"]]:
            xml.attrib[mark_tag] = self.marks[mark_key].toxmlstr(True)

        # PDF encryption settings---------------------------

        xml.attrib["PassOwner"] = self.encryption["pass"]["owner"]
        xml.attrib["PassUser"] = self.encryption["pass"]["user"]
        xml.attrib["Permissions"] = self.encryption["settings"]["permissions"]
        xml.attrib["Encrypt"] = bool_to_num(
            self.encryption["settings"]["encrypted"]
        )

        # Version ------------------------------------------

        xml.attrib["Version"] = str(self.version)

        # Objects to embed / generate ------------------------------------

        for code, human in [
                ["Thumbnails", "thumbnails"], ["Bookmarks", "bookmarks"],
                ["Articles", "articles"], ["EmbedPDF", "embedded_pdf"]]:
            xml.attrib[code] = bool_to_num(self.objects[human])

        # Transformation ----------------------------------------

        xml.attrib["RotateDeg"] = self.transformation["rotation"].toxmlstr(True)

        for code, human in [["MirrorH", "mirror_h"], ["MirrorV", "mirror_v"]]:
            xml.attrib[code] = bool_to_num(self.transformation[human])

        # Line per Inch children ---------------------------

        xml.attrib["UseLpi"] = bool_to_num(self.use_lpi)

        for lpi_item in self.lpi:
            lpi_xml = lpi_item.toxml()

            if lpi_xml is not None:
                xml.append(lpi_xml)

        # FIXME This exports undocumented attributes ----------

        try:
            xml = undocumented_to_xml(xml, self.undocumented)
        except AttributeError:
            pass

        return xml

    def fromdefault(self) -> NoReturn:
        self.text_compression = True
        self.image_compression = {"method": "automatic", "quality": "max"}

        # Default line per each settings

        self.lpi = []

        for dlpi in LPI.DEFAULTS:
            lobj = LPI()
            lobj.fromdefault(dlpi[0])

            self.lpi.append(lobj)


class LPI(PyScribusElement):
    """
    Lines per Inch settings (LPI) in SLA
    """

    spot_xml = {
        "dot": "0",
        "line": "1",
        "round": "2",
        "ellipse": "3",
    }

    DEFAULTS = [
        ["Black", 133, 45, "ellipse"],
        ["Cyan", 133, 105, "ellipse"],
        ["Magenta", 133, 75, "ellipse"],
        ["Yellow", 133, 90, "ellipse"],
    ]

    def __init__(self):
        super().__init__()

        self.pyscribus_defaults = [lpi_def[0] for lpi_def in LPI.DEFAULTS]

        # Linescreening angle
        self.angle = dimensions.Dim(0, unit="deg")

        # Name of the Colour for which these settings are ment
        self.color = ""

        # How many lines per Inch are used
        self.frequency = dimensions.Dim(133, unit="lpi", integer=True)

        # Code for the used Spotfunction
        self.spot = "ellipse"

    # PyScribus standard methods -------------------------------

    def fromdefault(self, default: str) -> NoReturn:

        if default in self.pyscribus_defaults:

            self.color = default

            for lpd in LPI.DEFAULTS:

                if lpd[0] == default:
                    self.frequency.value = lpd[1]
                    self.angle.value = lpd[2]

                    if lpd[3] in LPI.spot_xml:
                        self.spot = lpd[3]
                    else:
                        self.spot = "ellipse"

                    break

    def fromxml(self, xml: ET.Element) -> bool:

        if xml.tag != "LPI":
            return False

        if (color := xml.get("Color")) is not None:
            self.color = color

        if (freq := xml.get("Frequency")) is not None:
            self.frequency.value = int(freq)

        if (angle := xml.get("Angle")) is not None:
            self.angle.value = float(angle)

        if (spot := xml.get("SpotFunction")) is not None:

            for human, code in LPI.spot_xml.items():
                if code == spot:
                    self.spot = human
                    break

        return True

    def toxml(self) -> Union[ET.Element, None]:
        xml = ET.Element("LPI")

        if not self.color:
            return None

        xml.attrib["Color"] = self.color
        xml.attrib["Frequency"] = self.frequency.toxmlstr(True)
        xml.attrib["Angle"] = self.angle.toxmlstr(True)
        xml.attrib["SpotFunction"] = LPI.spot_xml[self.spot]

        return xml


class PrinterSettings(PyScribusElement):
    def __init__(self):
        super().__init__()

        self.mirror_pages = {"horizontal": False, "vertical": False}

        self.marks = {
            "crop": False,
            "bleed": False,
            "registration": False,
            "color": False,
        }

        firstUse = "1"

        # Print to file
        toFile = "0"
        useAltPrintCommand = "0"
        outputSeparations = "0"

        # Whether to use spot colors
        useSpotColors = "0"
        useColor = "0"

        # Use ICC color profiles
        useICC = "0"
        # Whether to have grey component replacement
        doGCR = "0"

        doClip = "0"
        setDevParam = "0"

        includePDFMarks = "0"

        # The postscrip level
        PSLevel = "0"

        # Which printer description language
        PDLanguage = "0"
        markLength = "7.185302734375"
        markOffset = "0"

        # --- Bleeds --------------------------------------------

        self.bleeds = collections.OrderedDict()

        self.bleeds["top"] = (dimensions.Dim(0),)
        self.bleeds["left"] = (dimensions.Dim(0),)
        self.bleeds["right"] = (dimensions.Dim(0),)
        self.bleeds["bottom"] = (dimensions.Dim(0),)
        self.bleeds["document"] = False

        # -------------------------------------------------------

        printer = ""
        filename = ""
        separationName = ""
        printerCommand = ""

    # --- PyScribus standard methods ----------------------------

    def fromxml(self, xml: ET.Element) -> bool:

        if xml.tag != "Printer":
            return False

        # --- Page mirroring ------------------------------------

        if (mrh := xml.get("mirrorH")) is not None:
            self.mirror_pages["horizontal"] = num_to_bool(mrh)

        if (mrv := xml.get("mirrorV")) is not None:
            self.mirror_pages["vertical"] = num_to_bool(mrv)

        # --- Marks ---------------------------------------------

        for case in ["crop", "bleed", "registration", "color"]:
            att_name = f"{case}Marks"

            if (att := xml.get(att_name)) is not None:
                self.marks[case] = num_to_bool(att)

        # --- Printer bleeds ------------------------------------

        for case in ["top", "left", "right", "bottom"]:
            att_name = "Bleed{}".format(case.capitalize())

            if (att := xml.get(att_name)) is not None:
                self.bleeds[case][0].value = float(att)

        if (udb := xml.get("useDocBleeds")) is not None:
            self.bleeds["document"] = num_to_bool(udb)

        # -------------------------------------------------------

        return True

    def toxml(self) -> ET.Element:
        xml = ET.Element("Printer")

        # TODO

        for bleed_config, bleed_value in self.bleeds.items():

            if bleed_config != "document":
                att_name = "Bleed{}".format(bleed_config.capitalize())
                xml.attrib[att_name] = bleed_value[0].toxmlstr()

        xml.attrib["mirrorH"] = bool_to_num(self.mirror_pages["horizontal"])
        xml.attrib["mirrorV"] = bool_to_num(self.mirror_pages["vertical"])

        xml.attrib["useDocBleeds"] = bool_to_num(self.bleeds["document"])

        for key, value in self.marks.items():
            att_name = f"{key}Marks"

            xml.attrib[att_name] = bool_to_num(value)

        return xml


# vim:set shiftwidth=4 softtabstop=4 spl=en:
