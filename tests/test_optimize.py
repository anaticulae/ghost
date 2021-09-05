# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pdfinfo.pages
import power

import ghost


def test_optimize_small(testdir):
    """Shrink pdf to given number of pages."""
    source = power.PAPER06B_PDF
    outpath = os.path.join(testdir.tmpdir, 'optimo.pdf')
    ghost.small(source, outpath, pages=(3, 4))
    pages = pdfinfo.pages.determine(outpath)
    assert pages == 2
