#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import utila

from ghost.extract import images
from ghost.optimize import small
from ghost.parts import Part
from ghost.parts import bounding_convert
from ghost.parts import run
from ghost.utils import pdfwrite

__version__ = '0.9.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROCESS = 'ghost'

INSTALLED = utila.hasprog('gs') or utila.hasprog('gswin64c')
HAS_GHOST = INSTALLED
