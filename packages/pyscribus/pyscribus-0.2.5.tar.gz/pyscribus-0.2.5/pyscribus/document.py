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
Document classes
"""

# Imports ===============================================================#

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

from typing import Union, NoReturn, Optional, Any, List

import lxml
import lxml.etree as ET

import pyscribus.exceptions as exceptions

from pyscribus.common.xml import *

import pyscribus.dimensions as dimensions
import pyscribus.colors as pscolors
import pyscribus.toc as toc
import pyscribus.marks as marks
import pyscribus.pages as pages
import pyscribus.styles as styles
import pyscribus.itemattribute as itemattribute
import pyscribus.patterns as patterns
import pyscribus.layers as layers
import pyscribus.pageobjects as pageobjects
import pyscribus.notes as notes
import pyscribus.printing as printing

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

BoolOrElement = Union[bool, ET.Element]

AppendableToDocument = Union[
    pageobjects.PageObject,
    pages.PageAbstract,
    layers.Layer,
    pscolors.Color,
    styles.StyleAbstract,
]

# Classes ===============================================================#


class Document(PyScribusElement):
    """
    SLA Document (DOCUMENT) in SLA file.

    :type sla_parent: pyscribus.sla.SLA
    :param sla_parent: SLA parent instance
    """

    metadata_xml = {
        "AUTHOR": "author",
        "COMMENTS": "comments",
        "PUBLISHER": "publisher",
        "DOCDATE": "date",
        "DOCTYPE": "type",
        "DOCFORMAT": "format",
        "DOCIDENT": "identifier",
        "DOCSOURCE": "source",
        "DOCLANGINFO": "lang",
        "DOCRELATION": "related",
        "DOCCOVER": "cover",
        "DOCRIGHTS": "rights",
        "TITLE": "title",
        "SUBJECT": "subject",
        "DOCCONTRIB": "contributor",
    }

    ui_show_xml = {
        "SHOWMARGIN": "margins",
        "SHOWBASE": "baseline",
        "SHOWPICT": "images",
        "SHOWLINK": "links",
        "SHOWGRID": "grid",
        "SHOWGUIDES": "guides",
        "showcolborders": "colborders",
        "showrulers": "rulers",
    }

    autoframes_xml = {
        "AUTOSPALTEN": "columns",
        "ABSTSPALTEN": "colgap",
    }

    bleed_xml = {
        "BleedTop": "top",
        "BleedRight": "right",
        "BleedLeft": "left",
        "BleedBottom": "bottom",
    }

    def __init__(self, sla_parent=False):
        super().__init__()

        self.sla_parent = sla_parent

        # ----------------------------------------------

        self.profiles = []
        self.pdf_settings = []
        self.printer_settings = []

        # ----------------------------------------------

        self.colors = []
        self.layers = []
        self.patterns = []
        self.gradients = []

        # ----------------------------------------------

        self.pages = []
        self.page_sets = []
        self.master_pages = []
        self.page_objects = []

        # ----------------------------------------------

        self.tocs = []
        self.marks = []
        self.sections = []

        # ----------------------------------------------

        self.page_number = 0

        # Page dimensions, borders, bleeds

        self.dims = {
            "width": dimensions.Dim(595.275590551181),
            "height": dimensions.Dim(841.889763779528),
        }

        self.borders = {
            "left": dimensions.Dim(40),
            "right": dimensions.Dim(40),
            "top": dimensions.Dim(40),
            "bottom": dimensions.Dim(40),
        }

        self.bleed = {
            "top": dimensions.Dim(0),
            "right": dimensions.Dim(0),
            "left": dimensions.Dim(0),
            "bottom": dimensions.Dim(0),
        }

        # ----------------------------------------------

        self.notes = []
        self.notes_frames = []

        self.styles = {
            "note": [],
            "paragraph": [],
            "character": [],
            "table": [],
            "cell": [],
        }

        # ----------------------------------------------

        self.attributes = []

        # ----------------------------------------------

        self.metadata = {
            "title": "",
            "author": "",
            "subject": "",
            "keywords": [],
            "comments": "",
            "publisher": "",
            "contributor": "",
            "date": "",
            "type": "",
            "format": "",
            "identifier": "",
            "source": "",
            "lang": "",
            "related": "",
            "cover": "",
            "rights": "",
        }

        # ICC color profiles ---------------------------

        self.icc_profiles = {
            "rgb_images": "",
            "cmyk_images": "",
            "rgb_colors": "",
            "cmyk_colors": "",
            "printer": "",
        }

        # ----------------------------------------------

        self.ui_snapping = {"guides": False, "grid": False, "element": False}

        # ----------------------------------------------

        self.ui_show = {
            "margins": True,
            "baseline": False,
            "images": True,
            "links": False,
            "grid": False,
            "guides": True,
            "colborders": True,
            "rulers": True,
        }

        # ----------------------------------------------

        self.calligraphicpen = {
            "angle": dimensions.Dim(0, unit="cdeg", integer=True),
            "line_width": dimensions.Dim(0, unit="pica"),
            "line_shade": dimensions.Dim(100, unit="perc", integer=True),
            "line_color": "",
            "width": dimensions.Dim(0, unit="pica"),
            "style": "1",
            "fill_color": "",
            "fill_shade": dimensions.Dim(100, unit="perc", is_int=True),
        }

        # ----------------------------------------------

        self.autoframes = {
            # Number of Columns in automatic Textframes
            # AUTOSPALTEN = "1"
            "columns": 1,
            # Distance between Columns in automatic Textframes
            # ABSTSPALTEN = "11"
            "colgap": dimensions.Dim(11, unit="pt"),
        }

        # ----------------------------------------------

        # FIXME Not documented -------------------------
        # PRESET="0"

        # FIXME ---- À faire ---------------------------

        self.doc_pages = {
            # (optional) Orientation of the Doc 0 = Portrait 1 = Landscape
            # ORIENTATION = "0"
            "orientation": pages.Orientation.PORTRAIT,
            # Default page name, such as "A4" or "Letter"
            # PAGESIZE = "A4"
            "size": pages.xml_size["A4"],
            # (optional) Which PageSet to use
            # This value is the index of page set used. And it is NOT optional.
            # So by default,
            # 0 is Single page, 1 is Facing pages, 2 is 3-Fold, 3 is 4-Fold
            # BOOK = "0"
            # TODO : Link this value to pages sets in Document object
            "set": 0,
        }

        # (optional) First page number in the Doc
        FIRSTNUM = "1"

        # (optional) Measurement unit for the Doc
        # 0 = Points 1 = Millimeters 2 = Inches 3 = Picas
        UNITS = "1"

        # Default Font
        DFONT = "Arial Regular"
        # Default Fontsize
        DSIZE = "12"

        # (optional) Number of Columns in Textframes
        DCOL = "1"
        # (optional) Default Gap between Columns in Textframes
        DGAP = "0"

        # FIXME Not documented -------------------------
        # TabFill=""

        # Default width for tabs in text frames
        TabWidth = "36"

        # FIXME Not documented -------------------------
        # TextDistLeft="0"
        # TextDistRight="0"
        # TextDistBottom="0"
        # TextDistTop="0"

        # FIXME ---- À faire ---------------------------

        # Percentage for Superscript
        VHOCH = "33"
        # Percentage for scaling of the Glyphs in Superscript
        VHOCHSC = "66"
        # Percentage for Subscript
        VTIEF = "33"
        # Percentage for scaling of the Glyphs in Subscript
        VTIEFSC = "66"
        # Percentage for scaling of the Glyphs in Small Caps
        VKAPIT = "75"

        # (optional) Width of the Baseline Grid
        BASEGRID = "14.4"
        # (optional) Startoffset for the Baseline Grid
        BASEO = "0"

        # FIXME Not documented -------------------------
        # AUTOL="100"
        # UnderlinePos="-1"
        # UnderlineWidth="-1"
        # StrikeThruPos="-1"
        # StrikeThruWidth="-1"

        # (optional) Counter for Groups in the Doc
        GROUPC = "1"
        # (optional) Colormanagement available 0 = off, 1 = on
        HCMS = "0"
        # (optional) Simulate the Printer on Screen 0 = off, 1 = on
        DPSo = "0"

        # FIXME Not documented -------------------------
        # DPSFo="0"

        # (optional) Use Colormanagement 0 = off, 1 = on
        DPuse = "0"
        # (optional) Mark Colors out of Gamut 0 = off, 1 = on
        DPgam = "0"
        # (optional) Use Blackpoint Compensation 0 = off, 1 = on
        DPbla = "1"

        # FIXME Not documented -------------------------
        # DISc="1"
        # DIIm="0"

        # (optional) Active Layer
        ALAYER = "0"

        # (optional) Language of the Doc
        LANGUAGE = "fr"
        # (optional) Automatic Hyphenation 0 = off, 1 = on
        AUTOMATIC = "1"
        # (optional) Automatic Hyphenation during typing 0 = off, 1 = on
        AUTOCHECK = "0"
        # (optional) Guides locked 0 = off, 1 = on
        GUIDELOCK = "0"

        # FIXME ---- À faire ---------------------------

        # (optional) Distance of the minor Gridlines
        MINGRID = "20"
        # (optional) Distance of the major Gridlines
        MAJGRID = "100"

        # FIXME Not documented -------------------------
        # SHOWFRAME="1"
        # SHOWControl="0"
        # SHOWLAYERM="0"

        # FIXME ---- À faire ---------------------------

        # FIXME Not documented -------------------------
        # rulerMode="1"

        # FIXME Not documented -------------------------
        # showBleed="1"
        # rulerXoffset="0"
        # rulerYoffset="0"
        # GuideRad="10"
        # GRAB="4"
        # POLYC="4"
        # POLYF="0.5"
        # POLYR="0"
        # POLYIR="0"
        # POLYCUR="0"
        # POLYOCUR="0"
        # POLYS="0"
        # arcStartAngle="30"
        # arcSweepAngle="300"
        # spiralStartAngle="0"
        # spiralEndAngle="1080"
        # spiralFactor="1.2"
        # AutoSave="1"
        # AutoSaveTime="600000" # milisec ?
        # AutoSaveCount="1"
        # AutoSaveKeep="0"
        # AUtoSaveInDocDir="1"
        # AutoSaveDir=""

        # Space at the bottom of the scratch space, after the last page
        ScratchBottom = "20"
        # Space at the left of the scratch space
        ScratchLeft = "100"
        # Space at the right of the scratch space
        ScratchRight = "100"
        # Space at the top of the scratch space, before the pages
        ScratchTop = "20"

        # FIXME Not documented -------------------------
        # GapHorizontal="0"
        # GapVertical="40"
        # StartArrow="0"
        # EndArrow="0"
        # PEN="Black"
        # BRUSH="None"
        # PENLINE="Black"
        # PENTEXT="Black"
        # StrokeText="Black"
        # TextBackGround="None"
        # TextLineColor="None"
        # TextBackGroundShade="100"
        # TextLineShade="100"
        # TextPenShade="100"
        # TextStrokeShade="100"
        # STIL="1"
        # STILLINE="1"
        # WIDTH="1"
        # WIDTHLINE="1"
        # PENSHADE="100"
        # LINESHADE="100"
        # BRUSHSHADE="100"
        # CPICT="None"
        # PICTSHADE="100"
        # CSPICT="None"
        # PICTSSHADE="100"
        # PICTSCX="1"
        # PICTSCY="1"
        # PSCALE="1"
        # PASPECT="1"
        # EmbeddedPath="0"
        # HalfRes="1"
        # dispX="10"
        # dispY="10"
        # constrain="15"

        # MINORC="#00ff00"
        # MAJORC="#00ff00"
        # GuideC="#000080"
        # BaseC="#c0c0c0"

        # Scribus GUI Page background
        PAGEC = "#ffffff"

        # MARGC="#0000ff"

        # renderStack="2 0 4 1 3"
        # GridType="0"
        # RANDF="0"

        # currentProfile="PDF 1.4"

        # ----------------------------------------------

    # Setting defaults methods ==============================================

    def _default_profiles(self) -> NoReturn:
        """
        Add default checking profiles.
        """

        for def_name in Profile.defaults:
            self.profiles.append(Profile(default=def_name))

    def _default_layer(self) -> NoReturn:
        """
        Add default layer.
        """
        self.layers.append(layers.Layer(default=True))

    def _default_layers(self) -> NoReturn:
        """
        Add default checking profiles.

        Alias for add_default_layer()
        """

        self._default_layer()

    def _default_snapping(self) -> NoReturn:
        """
        Set default UI snapping options.
        """

        self.ui_snapping = {"guides": True, "grid": False, "element": True}

    def _default_note_style(self) -> NoReturn:
        ns = styles.NoteStyle()
        ns.fromdefault()

        self.styles["note"].append(ns)

    def _default_note_styles(self) -> NoReturn:
        self._default_note_style()

    def _default_pages(self) -> bool:
        """
        Add default page.
        """

        page = pages.Page()
        page.fromdefault()
        self.pages.append(page)

        return True

    def _default_page(self) -> NoReturn:
        """
        Alias of default_pages()

        .. sealso: default_pages()
        """

        self._default_pages()

    def _default_icc(self) -> NoReturn:
        """
        Set default ICC colors profiles.
        """
        self.icc_profiles = {
            "rgb_images": "sRGB display profile (ICC v2.2)",
            "cmyk_images": "ISO Coated v2 300% (basICColor)",
            "rgb_colors": "sRGB display profile (ICC v2.2)",
            "cmyk_colors": "ISO Coated v2 300% (basICColor)",
            "printer": "ISO Coated v2 300% (basICColor)",
        }

    def _default_ui_show(self) -> NoReturn:
        """
        Set default UI view options.
        """

        self.ui_show = {
            "margins": True,
            "baseline": False,
            "images": True,
            "links": False,
            "grid": False,
            "guides": True,
            "colborders": True,
            "rulers": True,
        }

    def _default_calligraphic_pen(self) -> NoReturn:
        """
        Set default calligraphic pen options.
        """

        self.calligraphicpen = {
            "angle": dimensions.Dim(0, unit="cdeg", integer=True),
            "line_width": dimensions.Dim(0, unit="pica"),
            "line_shade": dimensions.Dim(100, unit="perc", integer=True),
            "line_color": "",
            "width": dimensions.Dim(0, unit="pica"),
            "style": 1,
            "fill_color": "",
            "fill_shade": dimensions.Dim(100, unit="perc", integer=True),
        }

    def _default_pagesets(self) -> NoReturn:
        """
        Set default page sets.
        """

        self.page_sets = []

        for default in ["Single Page", "Facing Pages", "3-Fold", "4-Fold"]:
            ps = pages.PageSet()

            if (success := ps.fromdefault(default)):
                self.page_sets.append(ps)

    def _default_colors(self) -> NoReturn:
        """
        Set default colors.
        """

        for default in [
            "Black",
            "Blue",
            "Cool Black",
            "Cyan",
            "Green",
            "Magenta",
            "Red",
            "Registration",
            "Rich Black",
            "Warm Black",
            "White",
            "Yellow",
        ]:

            co = pscolors.Color()
            success = co.fromdefault(default)

            if success:
                self.colors.append(co)

    def _default_pdfsettings(self) -> NoReturn:
        """
        Add default PDF settings.
        """

        pdf = printing.PDFSettings()
        pdf.fromdefault()
        self.pdf_settings = [pdf]

    def _default_section(self) -> NoReturn:
        """
        Alias of default_sections()

        .. sealso: default_section()
        """

        self.default_sections()

    def _default_sections(self) -> NoReturn:
        """
        Add default section.
        """

        sec = toc.Section()
        sec.fromdefault()
        self.sections = [sec]

    def _default_paragraph_styles(self) -> NoReturn:
        self.styles["paragraph"].append(
            styles.ParagraphStyle(self, default=True)
        )
        self.styles["paragraph"][-1].is_default = True

    def _default_character_styles(self) -> NoReturn:
        self.styles["character"].append(
            styles.CharacterStyle(self, default=True)
        )
        self.styles["character"][-1].is_default = True

    def fromdefault(self, default: str = "all") -> NoReturn:
        """
        Set default settings from a default list

        :param default: Set of default settings or list of default features
            to set.
        :type default: str,list

        Unlike other fromdefault() methods, Document.fromdefault() default
        parameter can only be "all" or a list of default features to set.

        +-------------------------+-------------------+
        | Default feature         | String            |
        +=========================+===================+
        | Colors                  | colors            |
        +-------------------------+-------------------+
        | Checking profiles       | profiles          |
        +-------------------------+-------------------+
        | Layers                  | layers            |
        +-------------------------+-------------------+
        | UI snapping             | uisnapping        |
        +-------------------------+-------------------+
        | Notes' styles           | nstyles           |
        +-------------------------+-------------------+
        | Paragraph styles        | pstyles           |
        +-------------------------+-------------------+
        | Character styles        | pstyles           |
        +-------------------------+-------------------+
        | Page                    | page, pages       |
        +-------------------------+-------------------+
        | ICC profiles            | icc               |
        +-------------------------+-------------------+
        | UI show                 | uishow            |
        +-------------------------+-------------------+
        | Calligraphic pen        | cpen              |
        +-------------------------+-------------------+
        | Page sets               | pagesets          |
        +-------------------------+-------------------+
        | PDF settings            | pdf               |
        +-------------------------+-------------------+
        | Document sections       | section, sections |
        +-------------------------+-------------------+

        For example, to create a SLA document with default colors, layers,
        but without any other defined defaults :

            fromdefault(["colors", "layers"])
        """

        features = {
            "colors": self._default_colors,
            "cpen": self._default_calligraphic_pen,
            "icc": self._default_icc,
            "layers": self._default_layers,
            "nstyles": self._default_note_styles,
            "pstyles": self._default_paragraph_styles,
            "cstyles": self._default_character_styles,
            "page": self._default_page,
            "pagesets": self._default_pagesets,
            "pdf": self._default_pdfsettings,
            "profiles": self._default_profiles,
            "section": self._default_sections,
            "uisnapping": self._default_snapping,
            "uishow": self._default_ui_show,
        }

        plurals = {"pages": "page", "sections": "section"}

        seq = []

        if default == "all":
            seq = features.keys()
        else:
            for f in default:

                f = f.lower()

                if f in features:
                    seq.append(f)

                else:

                    if f in plurals:
                        seq.append(plurals[f])

        for f in seq:
            features[f]()

    # =======================================================================

    def fromxml(self, xml: ET.Element) -> bool:
        # --- DOCUMENT attributes ----------------------------------------

        # TODO DOCUMENT many attribs…

        for border in ["LEFT", "RIGHT", "TOP", "BOTTM"]:
            if (border_side := xml.get(f"BORDER{border}")) is not None:
                self.borders[border.lower()].value = float(border_side)

        # Pages settings

        if (pagenumber := xml.get("ANZPAGES")) is not None:
            self.page_number = int(pagenumber)

        if (att_value := xml.get("orientation")) is not None:
            if int(att_value):
                self.doc_pages["orientation"] = pages.Orientation.LANDSCAPE
            else:
                self.doc_pages["orientation"] = pages.Orientation.PORTRAIT

        if (att_value := xml.get("PAGESIZE")) is not None:
            for att, human in pages.xml_size.items():
                if att_value == att:
                    self.doc_pages["size"] = pages.xml_size[att_value]
                    break

        for page_dim in ["WIDTH", "HEIGHT"]:
            if (pgdim := xml.get(f"PAGE{page_dim}")) is not None:
                self.dims[page_dim.lower()].value = float(pgdim)

        if (att_value := xml.get("BOOK")) is not None:
            self.doc_pages["set"] = int(att_value)

        # Metadatas

        for att, key in Document.metadata_xml.items():
            if (meta_value := xml.get(att)) is not None:
                self.metadata[key] = meta_value

        if (keywords := xml.get("KEYWORDS")) is not None:
            self.metadata["keywords"] = keywords.split("; ")

        # Auto text frames

        for att, human in Document.autoframes_xml.items():
            if (att_value := xml.get(att)) is not None:
                if human == "colums":
                    self.autoframes[human] = int(att_value)
                if human == "colgap":
                    self.autoframes[human].value = float(att_value)

        # UI snapping

        for snap_thing in ["grid", "guides", "element"]:
            att_name = "SnapTo{}".format(snap_thing.capitalize())

            if (att := xml.get(att_name)) is not None:
                self.ui_snapping[snap_thing] = num_to_bool(att)

        # Bleed settings

        for att, human in Document.bleed_xml.items():
            if (att_value := xml.get(att)) is not None:
                self.bleed[human] = float(att_value)

        # UI show

        for att_name, ui_name in Document.ui_show_xml.items():
            if (att := xml.get(att_name)) is not None:
                self.ui_show[ui_name] = num_to_bool(att)

        # ICC color profiles

        for att_name, icc_key in [
            ["DPIn", "rgb_images"],
            ["DPInCMYK", "cmyk_images"],
            ["DPIn2", "rgb_colors"],
            ["DPIn3", "cmyk_colors"],
            ["DPPr", "printer"],
        ]:
            if (att := xml.get(att_name)) is not None:
                self.icc_profiles[icc_key] = att

        # Calligraphic pen -----------------------------------------------

        for att_base, key in [
            ["Angle", "angle"],
            ["LineColorShade", "line_shade"],
            ["FillColorShade", "fill_shade"],
        ]:
            att_name = f"calligraphicPen{att_base}"

            if (att := xml.get(att_name)) is not None:
                self.calligraphicpen[key].value = int(att)

        for att_base, key in [["LineWidth", "line_width"], ["Width", "width"]]:
            att_name = f"calligraphicPen{att_base}"

            if (att := xml.get(att_name)) is not None:
                self.calligraphicpen[key].value = float(att)

        for att_base, key in [
            ["LineColor", "line_color"],
            ["FillColor", "fill_color"],
            ["PenStyle", "style"],
        ]:

            att_name = f"calligraphicPen{att_base}"

            if (att := xml.get(att_name)) is not None:
                self.calligraphicpen[key] = att

        # --- DOCUMENT childs --------------------------------------------

        for child in xml:

            self.__fromxml_item(child, "CheckProfile", Profile, self.profiles)

            self.__fromxml_item(
                child, "Gradient", pscolors.Gradient, self.gradients
            )

            self.__fromxml_item(child, "COLOR", pscolors.Color, self.colors)

            self.__fromxml_item(
                child, "Pattern", patterns.Pattern, self.patterns
            )

            # TODO FIXME hyphen

            self.__fromxml_item(
                child, "STYLE", styles.ParagraphStyle, self.styles["paragraph"],
                True
            )

            self.__fromxml_item(
                child, "CHARSTYLE", styles.CharacterStyle,
                self.styles["character"], True
            )

            self.__fromxml_item(
                child, "TableStyle", styles.TableStyle, self.styles["table"],
                True
            )

            self.__fromxml_item(
                child, "CellStyle", styles.CellStyle, self.styles["cell"], True
            )

            self.__fromxml_item(
                child, "LAYERS", layers.Layer, self.layers, True
            )

            self.__fromxml_item(
                child, "Printer", printing.PrinterSettings,
                self.printer_settings
            )

            self.__fromxml_item(
                child, "PDF", printing.PDFSettings, self.pdf_settings
            )

            if child.tag == "DocItemAttributes":

                for attribute in child:
                    doc_att_item = itemattribute.DocumentAttribute()

                    if (success := doc_att_item.fromxml(attribute)):
                        self.attributes.append(doc_att_item)

            self.__fromxml_section(
                child,
                "TablesOfContents",
                "TableOfContents",
                toc.TOC,
                self.tocs,
            )

            self.__fromxml_section(
                child,
                "Marks",
                "Mark",
                marks.DocumentMark,
                self.marks,
            )

            self.__fromxml_section(
                child,
                "NotesStyles",
                "notesStyle",
                styles.NoteStyle,
                self.styles["note"],
            )

            if child.tag == "NotesFrames":

                for sub in child:

                    if sub.tag == "FOOTNOTEFRAME":
                        note_frame = notes.NoteFrame()

                        if (success := note_frame.fromxml(sub)):
                            self.notes_frames.append(note_frame)

            self.__fromxml_section(
                child,
                "Notes",
                "Note",
                notes.Note,
                self.notes,
                True
            )

            if child.tag == "PageSets":

                for page_set in child:
                    page_set_item = pages.PageSet()

                    if (success := page_set_item.fromxml(page_set)):
                        self.page_sets.append(page_set_item)

            self.__fromxml_section(
                child,
                "Sections",
                "Section",
                toc.Section,
                self.sections,
            )

            self.__fromxml_item(
                child, "MASTERPAGE", pages.MasterPage, self.master_pages, False
            )

            if child.tag == "PAGE":
                page_item = pages.Page()

                page_item.sla_parent = self.sla_parent
                page_item.doc_parent = self

                if (success := page_item.fromxml(child)):
                    self.pages.append(page_item)

            if child.tag == "PAGEOBJECT":
                ptype = child.get("PTYPE")

                if ptype is None:
                    continue

                try:
                    p_object = pageobjects.new_from_type(
                            ptype, self.sla_parent, self
                    )

                    if (success := p_object.fromxml(child)):
                        self.page_objects.append(p_object)

                except ValueError:
                    pass

        # ----------------------------------------------------------------

        return True

    def toxml(self, optional: bool = True) -> ET.Element:
        xml = ET.Element("DOCUMENT")

        # === DOCUMENT attributes ========================================

        # Pages settings -------------------------------------------------

        xml.attrib["ANZPAGES"] = str(self.page_number)

        xml.attrib["ORIENTATION"] = str(int(self.doc_pages["orientation"]))

        for att, human in pages.xml_size.items():
            if human == self.doc_pages["size"]:
                xml.attrib["PAGESIZE"] = att
                break

        xml.attrib["BOOK"] = str(self.doc_pages["set"])

        # Auto text frames -----------------------------------------------

        for att, human in Document.autoframes_xml.items():

            if human == "columns":
                xml.attrib[att] = str(self.autoframes[human])

            if human == "colgap":
                xml.attrib[att] = self.autoframes[human].toxmlstr(True)

        # Bleed settings -------------------------------------------------

        for att, human in Document.bleed_xml.items():
            xml.attrib[att] = str(self.bleed[human])

        # Dimensions -----------------------------------------------------

        xml.attrib["PAGEWIDTH"] = self.dims["width"].toxmlstr()
        xml.attrib["PAGEHEIGHT"] = self.dims["height"].toxmlstr()

        # Borders --------------------------------------------------------

        for border_side, border_value in self.borders.items():
            att = "BORDER{}".format(border_side.upper())
            xml.attrib[att] = border_value.toxmlstr()

        # Metadatas ------------------------------------------------------

        for att, key in Document.metadata_xml.items():
            xml.attrib[att] = self.metadata[key]

        xml.attrib["KEYWORDS"] = "; ".join(self.metadata["keywords"])

        # UI snapping ----------------------------------------------------

        for att_base, snap_value in self.ui_snapping.items():
            att = "SnapTo{}".format(att_base.capitalize())
            xml.attrib[att] = bool_to_num(snap_value)

        # UI show --------------------------------------------------------

        for att_name, ui_name in Document.ui_show_xml.items():
            xml.attrib[att_name] = bool_to_num(self.ui_show[ui_name])

        # ICC profiles ---------------------------------------------------

        for key_out, key_in in [
            ["DPIn", "rgb_images"],
            ["DPInCMYK", "cmyk_images"],
            ["DPIn2", "rgb_colors"],
            ["DPIn3", "cmyk_colors"],
            ["DPPr", "printer"],
        ]:
            xml.attrib[key_out] = self.icc_profiles[key_in]

        # Calligraphic pen -----------------------------------------------

        for key_out_suffix, key_in, as_string in [
            ["Angle", "angle", True],
            ["LineWidth", "line_width", True],
            ["LineColorShade", "line_shade", True],
            ["LineColor", "line_color", False],
            ["Width", "width", True],
            ["Style", "style", False],
            ["FillColor", "fill_color", False],
            ["FillColorShade", "fill_shade", True],
        ]:

            att_name = f"calligraphicPen{key_out_suffix}"
            att_value = self.calligraphicpen[key_in]

            if as_string:
                att_value = att_value.toxmlstr()

            if key_out_suffix == "Style":
                att_value = str(att_value)

            xml.attrib[att_name] = att_value

        # === DOCUMENT childs ============================================

        # Checking profiles ----------------------------------------------

        for profile in self.profiles:
            profile_xml = profile.toxml()

            if not isinstance(profile_xml, bool):
                xml.append(profile_xml)

        # ----------------------------------------------------------------

        # Colors
        xml = self.__toxml_items(xml, self.colors)

        # TODO FIXME hyphen

        # Styles ---------------------------------------------------------

        for style_type in ["paragraph", "character", "table", "cell"]:

            for style_item in self.styles[style_type]:
                item_xml = style_item.toxml()
                xml.append(item_xml)

        # ----------------------------------------------------------------

        # Layers
        xml = self.__toxml_items(xml, self.layers)

        # Printer settings
        xml = self.__toxml_items(xml, self.printer_settings)

        # PDF settings
        xml = self.__toxml_items(xml, self.pdf_settings)

        # Document attributes
        xml = self.__toxml_section(xml, "DocItemAttributes", self.attributes)

        # Tables of contents
        xml = self.__toxml_section(xml, "TablesOfContents", self.tocs)

        # Marks
        if self.marks:
            xml = self.__toxml_section(xml, "Marks", self.marks)

        # Notes : styles, frames, content --------------------------------

        # Notes styles
        xml = self.__toxml_section(xml, "NotesStyles", self.styles["note"])

        # Notes frames
        if self.notes_frames:
            xml = self.__toxml_section(xml, "NotesFrames", self.notes_frames)

        # Notes content

        if self.notes:
            nx = ET.Element("Notes")

            for note in self.notes:
                # n = note.toxml()
                # nx.append(n)
                pass

            xml.append(nx)

        # ----------------------------------------------------------------

        # Page sets
        xml = self.__toxml_section(xml, "PageSets", self.page_sets)
        # Sections
        xml = self.__toxml_section(xml, "Sections", self.sections)

        # Pages (master, regular) ----------------------------------------

        # Master pages
        xml = self.__toxml_items(xml, self.master_pages)
        # Pages
        xml = self.__toxml_items(xml, self.pages)

        # Pages objects --------------------------------------------------

        xml = self.__toxml_items(xml, self.page_objects)

        # ----------------------------------------------------------------

        return xml

    def __fromxml_item(
        self,
        xml: ET.Element,
        item_tag: str,
        object_class,
        attribute,
        parent: bool = False
    ):
        if xml.tag != item_tag:
            return

        if parent:
            item_object = object_class(self)
        else:
            item_object = object_class()

        if (success := item_object.fromxml(xml)):
            attribute.append(item_object)

    def __fromxml_section(
        self,
        xml,
        section_tag: str,
        item_tag: str,
        object_class,
        attribute,
        parent: bool = False
    ):
        if xml.tag != section_tag:
            return

        for element in xml:

            if element.tag != item_tag:
                continue

            if parent:
                item_object = object_class(self)
            else:
                item_object = object_class()

            if (success := item_object.fromxml(element)):
                attribute.append(item_object)

    def __toxml_items(self, xml: ET.Element, items: list) -> ET.Element:
        """
        Add children nodes from `toxml()` methods of items to node `xml`.

        :type xml: ET.Element
        :type items: list
        :rtype: ET.Element
        """

        for item in items:
            item_xml = item.toxml()
            xml.append(item_xml)

        return xml

    def __toxml_section(
        self,
        xml: ET.Element,
        section_tag: str,
        section_items: list
    ) -> ET.Element:
        """
        Add a node with tag `section_tag` containing the XML representation
        of `sections_items` (accessed through `toxml()` methods) as children,
        to node `xml`.

        :type xml: ET.Element
        :type section_tag: str
        :type section_items: list
        :rtype: ET.Element
        """

        section = ET.Element(section_tag)

        for item in section_items:
            item_xml = item.toxml()
            section.append(item_xml)

        xml.append(section)

        return xml

    # =======================================================================

    def style(
        self,
        name: Optional[str] = None,
        style_type: Optional[str] = None,
        default: bool = False,
    ) -> Union[List[styles.StyleAbstract], styles.StyleAbstract]:

        result = []
        style_types = list(self.styles.keys())

        if style_type is not None:
            if style_type in style_types:
                style_types = [style_type]

        for type_key in style_types:

            for style in self.styles[type_key]:

                if name is None and style_type is not None:

                    # Returns only default style of type X
                    if default and style.is_default:
                        return style

                    # Returns all types of type X
                    result.append(style)
                    continue

                # Request for default style not satisfactory
                if default and not style.is_default:
                    continue

                # Request for style name not satisfactory
                if name != style.name:
                    continue

                result.append(style)

        return result

    def pageobjects(
        self, object_type=False, templatable: bool = False
    ) -> list:
        """
        Return document page objets.

        :type object_type: string,bool
        :param object_type: Page object type to filter, or do not filter at
            all. See pageobjects.po_type_classes for valid values.
        :type templatable: bool
        :param templatable: Only return templatable page objects.
        """

        pos_ret = []

        # If there is a object type filter, we filter before checking
        # if we must return only templatable objects

        if object_type:

            if object_type in pageobjects.po_type_classes:
                pos = []

                for po in self.page_objects:
                    if isinstance(
                        po, pageobjects.po_type_classes[object_type]
                    ):
                        pos.append(po)

        if templatable:

            if self.sla_parent.templating["active"]:
                lookup_set = []
                templatable_set = []

                if object_type:
                    lookup_set = pos
                else:
                    lookup_set = self.page_objects

                for po in lookup_set:
                    # If the page object is a text frame with templatable
                    # stories, we add these templatable stories

                    if isinstance(po, pageobjects.TextObject):
                        po_templatable_stories = po.templatable()

                        if po_templatable_stories:
                            templatable_set.extend(po_templatable_stories)

                    else:
                        # TODO If this page object is another type of page
                        # object, we look its properties and find if it
                        # is templatable through sla.SLA.templating settings

                        if po.templatable():
                            templatable_set.append(po)

                pos_ret = templatable_set

        else:
            if object_type:
                pos_ret = pos
            else:
                pos_ret = self.page_objects

        return pos_ret

    def stories(self) -> list:
        """
        Returns all stories in the document.

        :rtype: list
        :returns: List of stories
        """

        stories = []

        # Text frames stories --------------------------------------------

        filtered = [
            po for po in self.page_objects if po.have_stories and po.stories
        ]

        if filtered:

            for po in filtered:
                stories.extend(po.stories)

        # Table cells stories --------------------------------------------

        tables = [po for po in self.page_objects if po.ptype == "table"]

        if tables:
            cells = []

            for po in tables:
                cells.extend(po.cells)

            for cell in cells:
                if cell.story is not None:
                    stories.append(cell.story)

        # ----------------------------------------------------------------

        return stories

    # =======================================================================

    def page_number(self) -> int:
        """
        Get document pages number.
        """

        pn = 0

        for po in self.pages:
            if po.number > pn:
                pn = po.number

        return pn

    def append(self, sla_object: AppendableToDocument, **kwargs) -> bool:
        """
        Append a page, a page object, layer, style…

        +----------------+---------+-----------------------------------------+
        | Argument name  | Type    | Usage                                   |
        +================+=========+=========================================+
        | check_color    | boolean | If True, check if a document's color    |
        |                |         | already have the same inks as           |
        |                |         | sla_object.                             |
        +----------------+---------+-----------------------------------------+
        | overlap_object | boolean | If True (default) and if sla_object is  |
        |                |         | a page object, sla_object will be added |
        |                |         | even if its coordinates overlap with a  |
        |                |         | document's page object coordinates.     |
        |                |         |                                         |
        |                |         | If False, coordinates of sla_object     |
        |                |         | will be checked against document's page |
        |                |         | objects, and eventually raise           |
        |                |         | OverlappingPageObject.                  |
        +----------------+---------+-----------------------------------------+
        | overlap_layer  | boolean | If True (default) AND overlap_object is |
        |                |         | False, sla_object page object           |
        |                |         | coordinates will only be checked        |
        |                |         | against document's page objects on the  |
        |                |         | same layer.                             |
        +----------------+---------+-----------------------------------------+

        :param kwargs: dict
        :type kwargs: Appending options
        :rtype: boolean
        :returns: True if appending succeed
        """

        # TODO On pourra rajouter des tests ici.
        # Par exemple, si l’objet ajouté n’entre pas en collision
        # avec un autre du même calque, etc.

        if isinstance(sla_object, pageobjects.PageObject):
            if "overlap_object" in kwargs:
                overlap = kwargs["overlap_object"]
            else:
                overlap = True

            add = False

            if overlap:
                add = True
            else:
                if "overlap_layer" in kwargs:
                    same_layer = kwargs["overlap_layer"]
                else:
                    same_layer = True

                if same_layer:
                    page_objets = [
                        po
                        for po in self.page_objets
                        if po.layer == sla_object.layer
                    ]
                else:
                    page_objets = self.page_objects

                for po in page_objets:
                    # TODO FIXME Test coordinates

                    # TODO If coordinates overlaps:
                    # add = False
                    # break

                    pass

            if add:
                sla_object.doc_parent = self
                sla_object.sla_parent = self.sla_parent

                self.page_objects.append(sla_object)

                return True

            return False

        if isinstance(sla_object, pages.PageAbstract):
            # NOTE If sla_object is a page or a master page, its number
            # attribute is only relevant if there is a page number gap.

            # TODO Obtenir les numéros de page actuellement utilisés,
            # puis vérifier s’il y a des pages manquantes.

            page_gaps = []
            page_numbers = sorted([i.number for i in self.pages])
            max_page = page_numbers[-1]

            # TODO FIXME Pas convaincu par cette manière de retrouver
            # les numéros de page manquants.

            last_num = 1
            for num in range(1, max_page + 1):
                idx = num - 1

                if num == 1:
                    if page_numbers[idx] != 1:
                        page_gaps.append(num)

                else:
                    if page_numbers[idx] != last_num + 1:
                        page_gaps.append(num)

                last_num += 1

            # Si le numéros de page de sla_object correspond à une page
            # manquante:
            #   - on ajoute sla_object sans modifier son numéro de page
            #   via insert(index_manquant, sla_object)
            #
            # Si le numéro de page de sla_object ne correspond pas à une
            # page manquante ou n’a aucun putain de sens:
            #   - on définit le numéro de page de sla_object comme étant
            #   le plus grand numéro de page actuel + 1,
            #   - on ajoute via append()

            sla_object.doc_parent = self
            sla_object.sla_parent = self.sla_parent

            if isinstance(sla_object, pages.Page):
                self.pages.append(sla_object)
                return True

            if isinstance(sla_object, pages.MasterPage):
                self.master_pages.append(sla_object)
                return True

        if isinstance(sla_object, layers.Layer):

            for layer in self.layers:

                # If a layer have the same level

                if layer.level == sla_object.level:
                    raise exceptions.ConflictingLayer(
                        "Layer on level {} already exists".format(
                            sla_object.layer
                        )
                    )

                # If a layer have the same name

                if layer.name == sla_object.name:
                    raise exceptions.ConflictingLayer(
                        "Layer with name '{}' already exists".format(
                            sla_object.name
                        )
                    )

            self.layers.append(sla_object)

            return True

        if isinstance(sla_object, pscolors.Color):
            # NOTE check_color can be set to False, as the user might want
            # to use colors with different names, but same colors as a part
            # of his/her graphical chart / layer.

            if "check_color" in kwargs:
                check = kwargs["check_color"]
            else:
                check = False

            if check:
                add = True

                for color in self.colors:
                    if color == sla_object:
                        add = False
                        break

                if add:
                    self.colors.append(sla_object)

                    return True

            else:
                self.colors.append(sla_object)

                return True

        if isinstance(sla_object, styles.StyleAbstract):

            if isinstance(sla_object, styles.NoteStyle):
                self.styles["note"].append(sla_object)
                return True

            else:
                sla_object.doc_parent = self
                # TODO NOTE Maybe we should add a call to a StyleAbstract
                # "hook" for a "added to document" event, to manage style
                # parents. Something like :
                # sla_object.event("added-to-document")

                if isinstance(sla_object, styles.ParagraphStyle):
                    self.styles["paragraph"].append(sla_object)
                    return True

                if isinstance(sla_object, styles.CharacterStyle):
                    self.styles["character"].append(sla_object)
                    return True

                # TODO NOTE Then we should call a "hook" to all styles that
                # may have parents styles to update them as well.
                # Something like :
                #
                # for paragraph_style in self.styles["paragraph"]:
                #     if isinstance(sla_object, styles.CharacterStyle):
                #         paragraph_style.event("charstyle-added-document")
                #     if isinstance(sla_object, styles.ParagraphStyle):
                #         paragraph_style.event("parastyle-added-document")

        return False

    # =======================================================================


class Profile(PyScribusElement):
    """"""

    defaults = [
        "PDF 1.3",
        "PDF 1.4",
        "PDF 1.5",
        "PDF/X-3",
        "PDF/X-4",
        "PostScript",
        "PDF/X-1a",
    ]

    def __init__(self, default=False):
        super().__init__()

        self.pyscribus_defaults = [k for k in Profile.defaults]

        self.name = ""

        self.checks = {
            "auto": False,
            "Glyphs": False,
            "Orphans": False,
            "Overflow": False,
            "Pictures": False,
            "PartFilledImageFrames": False,
            "Resolution": False,
            "Transparency": False,
            "Annotations": False,
            "RasterPDF": False,
            "ForGIF": False,
            "NotCMYKOrSpot": False,
            "DeviceColorsAndOutputIntent": False,
            "FontNotEmbedded": False,
            "FontIsOpenType": False,
            "AppliedMasterDifferentSide": False,
            "EmptyTextFrames": False,
        }

        self.ignores = {"Errors": False, "OffLayers": False}

        self.resolution = {
            "min": dimensions.Dim(0, unit="dpi", integer=True),
            "max": dimensions.Dim(0, unit="dpi", integer=True),
        }

        if default:
            self.fromdefault(default)

    def set_checks(self, checks: list, value=True) -> NoReturn:
        """
        :param checks: List of checks names
        :type checks: list
        :param value: –
        :type value: –
        """
        for check in checks:
            self.checks[check] = value

    def unset_checks(self, checks: list, value=False) -> NoReturn:
        """
        :param checks: List of checks names
        :type checks: list
        :param value: –
        :type value: –

        .. sealso: set_checks()
        """
        self.set_checks(checks, value)

    # PyScribus standard methods -------------------------------

    def toxml(self) -> BoolOrElement:
        if not self.checks:
            return False

        xml = ET.Element("CheckProfile")
        xml.attrib["Name"] = self.name

        xml.attrib["ignoreErrors"] = bool_to_num(self.ignores["Errors"])

        xml.attrib["autoCheck"] = bool_to_num(self.checks["auto"])

        for check in [
            "Glyphs",
            "Orphans",
            "Overflow",
            "Pictures",
            "PartFilledImageFrames",
            "Resolution",
            "Transparency",
        ]:
            xml.attrib[f"check{check}"] = bool_to_num(self.checks[check])

        for res in self.resolution.keys():
            xml.attrib[f"{res}Resolution"] = self.resolution[res].toxmlstr()

        for check in ["Annotations", "RasterPDF", "ForGIF"]:
            xml.attrib[f"check{check}"] = bool_to_num(self.checks[check])

        xml.attrib["ignoreOffLayers"] = bool_to_num(self.ignores["OffLayers"])

        for check in [
            "NotCMYKOrSpot",
            "DeviceColorsAndOutputIntent",
            "FontNotEmbedded",
            "FontIsOpenType",
            "AppliedMasterDifferentSide",
            "EmptyTextFrames",
        ]:
            xml.attrib[f"check{check}"] = bool_to_num(self.checks[check])

        return xml

    def fromxml(self, xml: ET.Element) -> bool:
        name = xml.get("Name")

        if name is not None:
            self.name = name

        autocheck = xml.get("autoCheck")

        if autocheck is not None:
            self.checks["auto"] = num_to_bool(autocheck)

        for check in self.checks.keys():
            value = xml.get("check{}".format(check))

            if value is not None:
                self.checks[check] = num_to_bool(value)

        for ignore in self.ignores.keys():
            value = xml.get("ignore{}".format(ignore))

            if value is not None:
                self.ignores[ignore] = num_to_bool(value)

        for res in self.resolution.keys():
            value = xml.get("{}Resolution".format(res))

            if value is not None:
                self.resolution[res].value = int(value)

        return True

    def fromdefault(self, name: str) -> bool:
        """ """

        if name not in self.pyscribus_defaults:
            return False

        self.name = name

        if name in [
            "PDF 1.3",
            "PDF 1.4",
            "PDF 1.5",
            "PDF/X-1a",
            "PDF/X-3",
            "PDF/X-4",
            "PostScript",
        ]:

            self.ignores = {"Errors": False, "OffLayers": False}
            self.resolution = {
                "min": dimensions.Dim(144, unit="dpi", integer=True),
                "max": dimensions.Dim(2400, unit="dpi", integer=True),
            }

        if name == "PDF 1.3":
            self.set_checks(
                [
                    "auto",
                    "Glyphs",
                    "Orphans",
                    "Overflow",
                    "Pictures",
                    "Resolution",
                    "Transparency",
                    "RasterPDF",
                    "ForGIF",
                    "FontNotEmbedded",
                    "FontIsOpenType",
                    "AppliedMasterDifferentSide",
                    "EmptyTextFrames",
                ]
            )

            self.unset_checks(
                [
                    "Annotations",
                    "PartFilledImageFrames",
                    "NotCMYKOrSpot",
                    "DeviceColorsAndOutputIntent",
                ]
            )

        if name == "PDF 1.4":
            self.set_checks(
                [
                    "auto",
                    "Glyphs",
                    "Orphans",
                    "Overflow",
                    "Pictures",
                    "RasterPDF",
                    "ForGIF",
                    "FontNotEmbedded",
                    "FontIsOpenType",
                    "AppliedMasterDifferentSide",
                    "EmptyTextFrames",
                    "Resolution",
                ]
            )

            self.unset_checks(
                [
                    "checkPartFilledImageFrames",
                    "checkTransparency",
                    "checkAnnotations",
                    "checkNotCMYKOrSpot",
                    "checkDeviceColorsAndOutputIntent",
                ]
            )

        if name == "PDF 1.5":
            self.set_checks(
                [
                    "auto",
                    "Glyphs",
                    "Orphans",
                    "Overflow",
                    "Pictures",
                    "Resolution",
                    "RasterPDF",
                    "ForGIF",
                    "FontNotEmbedded",
                    "FontIsOpenType",
                    "AppliedMasterDifferentSide",
                    "EmptyTextFrames",
                ]
            )

            self.unset_checks(
                [
                    "checkNotCMYKOrSpot",
                    "checkDeviceColorsAndOutputIntent",
                    "checkTransparency",
                    "checkAnnotations",
                    "PartFilledImageFrames",
                ]
            )

        if name == "PDF/X-1a":
            self.set_checks(
                [
                    "auto",
                    "Glyphs",
                    "Orphans",
                    "Overflow",
                    "Pictures",
                    "Resolution",
                    "Transparency",
                    "Annotations",
                    "RasterPDF",
                    "ForGIF",
                    "NotCMYKOrSpot",
                    "FontNotEmbedded",
                    "FontIsOpenType",
                    "AppliedMasterDifferentSide",
                    "EmptyTextFrames",
                ]
            )

            self.unset_checks(
                [
                    "checkPartFilledImageFrames",
                    "checkDeviceColorsAndOutputIntent",
                ]
            )

        if name == "PDF/X-3":
            self.set_checks(
                [
                    "auto",
                    "Glyphs",
                    "Orphans",
                    "Overflow",
                    "Pictures",
                    "Resolution",
                    "Transparency",
                    "Annotations",
                    "RasterPDF",
                    "ForGIF",
                    "DeviceColorsAndOutputIntent",
                    "FontNotEmbedded",
                    "FontIsOpenType",
                    "AppliedMasterDifferentSide",
                    "EmptyTextFrames",
                ]
            )

            self.unset_checks(
                ["checkPartFilledImageFrames", "checkNotCMYKOrSpot"]
            )

        if name == "PDF/X-4":
            self.set_checks(
                [
                    "auto",
                    "Glyphs",
                    "Orphans",
                    "Overflow",
                    "Pictures",
                    "Resolution",
                    "Annotations",
                    "RasterPDF",
                    "ForGIF",
                    "DeviceColorsAndOutputIntent",
                    "FontNotEmbedded",
                    "AppliedMasterDifferentSide",
                    "EmptyTextFrames",
                ]
            )

            self.unset_checks(
                [
                    "checkPartFilledImageFrames",
                    "checkTransparency",
                    "checkNotCMYKOrSpot",
                    "checkFontIsOpenType",
                ]
            )

        if name == "PostScript":
            self.set_checks(
                [
                    "auto",
                    "Glyphs",
                    "Orphans",
                    "Overflow",
                    "Pictures",
                    "Resolution",
                    "Transparency",
                    "RasterPDF",
                    "ForGIF",
                    "AppliedMasterDifferentSide",
                    "EmptyTextFrames",
                ]
            )

            self.unset_checks(
                [
                    "checkPartFilledImageFrames",
                    "checkAnnotations",
                    "checkNotCMYKOrSpot",
                    "checkDeviceColorsAndOutputIntent",
                    "checkFontNotEmbedded",
                    "checkFontIsOpenType",
                ]
            )

        return True


# vim:set shiftwidth=4 softtabstop=4 spl=en:
