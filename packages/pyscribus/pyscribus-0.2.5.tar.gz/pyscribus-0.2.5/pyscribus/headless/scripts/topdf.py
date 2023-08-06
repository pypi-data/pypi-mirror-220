#!/usr/bin/python3
# -*- coding:Utf-8 -*-

"""
Converts an SLA file to PDF with headless Scribus execution.

From Scribus wiki: <https://wiki.scribus.net/canvas/Command_line_scripts>

Usage in Pyscribus:

:Example:

.. code:: python

   from pyscribus.headless import run_pyh_script
   run_pyh_script("topdf", sla_input="/home/user/example.sla")

Usage in command-line:

.. code:: bash

   scribus -g -py to-pdf.py -- file.sla

"""

# Imports ===============================================================#

import sys

from pathlib import Path

# Variables =============================================================#

PATH = __file__
SYNTAX = ["scribus", "-g", "-py", "SCRIPT_PATH", "--", "SLA_INPUT"]

# Program ===============================================================#

# NOTE `scribus` is loaded at Scribus execution.

if __name__ == "__main__":

    if not scribus.haveDoc() :
        print("No file opened.")
        sys.exit(0)

    filepath = Path(scribus.getDocName())

    pdf_filepath = filepath.parent / "{}.pdf".format(filepath.stem)

    pdf = scribus.PDFfile()
    pdf.file = str(pdf_filepath)

    pdf.save()

    sys.exit(0)

# vim:set shiftwidth=4 softtabstop=4:
