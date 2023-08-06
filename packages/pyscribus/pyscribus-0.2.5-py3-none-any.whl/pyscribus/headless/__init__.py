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
Pyscribus submodule for Scribus' headless execution.
"""

# Imports ===============================================================#

import copy
import subprocess

from pathlib import Path

import pyscribus.headless.scripts.topdf as script_to_pdf

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

SCRIPTS = {
    "topdf": script_to_pdf,
}

# Fonctions =============================================================#


def run_pyh_script(script_id: str, **kwargs) -> subprocess.Popen:
    """
    Execute Scribus scripts in command-line.

    :type script_id: str
    :param script_id: ID of the script to run. Must be a
        `pyscribus.headless.SCRIPTS` key.
    :type kwargs: dict
    :param kwargs: Additionnal parameters. See kwargs table.
    :rtype: subprocess.Popen

    +--------------+------------------------------------+
    | Kwargs       | Parameter                          |
    +==============+====================================+
    | sla_input    | Filepath of a SLA file.            |
    +--------------+------------------------------------+
    | stdout       | Output stdout. False by default.   |
    +--------------+------------------------------------+
    | stderr       | Output stderr. False by default.   |
    +--------------+------------------------------------+
    """

    script = SCRIPTS.get(script_id)

    if script is None:
        return False

    base_args = copy.deepcopy(script.SYNTAX)
    current_args = []

    sla_input = kwargs.get("sla_input")

    for arg in base_args:

        if arg == "SCRIPT_PATH":
            current_args.append(script.PATH)
            continue

        if arg == "SLA_INPUT":

            if sla_input is None:
                break

            sla_input = Path(sla_input).resolve(True)

            current_args.append(str(sla_input))
            continue

        current_args.append(arg)

    if not current_args:
        return False

    command = " ".join(current_args)

    if len(current_args) != len(base_args):
        return False

    # stdout & stderr -----------------------------------------------

    get_stdout, get_stderr = kwargs.get("stdout"), kwargs.get("stderr")
    stdout_file, stderr_file = subprocess.DEVNULL, subprocess.DEVNULL

    for std in [[get_stdout, stdout_file], [get_stderr, stderr_file]]:
        if std[0] is not None:
            if std[0]:
                std[1] = subprocess.PIPE

    # ---------------------------------------------------------------

    return subprocess.Popen(
        command,
        shell=True,
        stderr=stderr_file,
        stdout=stdout_file,
    )

# vim:set shiftwidth=4 softtabstop=4:
