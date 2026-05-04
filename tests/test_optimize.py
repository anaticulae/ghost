# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pdfinfo
import power

import tests
import ughost


@tests.ughostscript
def test_optimize_small(td):
    """Shrink pdf to given number of pages."""
    source = power.PAPER06B_PDF
    outpath = os.path.join(td.tmpdir, 'optimo.pdf')
    ughost.small(source, outpath, pages=(3, 4))
    pages = pdfinfo.pagecount(outpath)
    assert pages == 2
