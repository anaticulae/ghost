# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Optimize PDF
============

Use GhostScript to optimize pdf file.
"""

import utila

import ghost.utils


def small(source: str, destination: str, pages: tuple = None):
    pages = ghost.utils.gpages_fromtuple(pages)
    config = '-sDEVICE=pdfwrite -dBATCH -dNOPAUSE -SAFE'
    source = f'"{source}"'
    cmd = f'{ghost.utils.GHOST} {config} {pages} -sOutputFile={destination} {source}'
    utila.run(cmd)
