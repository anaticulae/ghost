#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import utilo

from ughost.extract import images
from ughost.optimize import small
from ughost.parts import Part
from ughost.parts import bounding_convert
from ughost.parts import run
from ughost.utils import pdfwrite

__version__ = '0.9.1'

ROOT = os.path.abspath(utilo.join(os.path.dirname(__file__), '..'))
PROCESS = 'ughost'

CMDLINE = 'gs ghostscript gswin64c'.split()


def cmdline() -> str | None:
    """\
    >>> cmdline()
    'gs'
    """
    for item in CMDLINE:
        if not utilo.hasprog(item):
            continue
        return item
    return None


GS = cmdline()
INSTALLED = GS is not None
HAS_GHOST = INSTALLED
