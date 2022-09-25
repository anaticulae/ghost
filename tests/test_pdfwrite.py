# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import ghost
import tests


@tests.ghostscript
@utilatest.longrun
def test_pdfwrite_all():
    source = power.TECH019_PDF
    path = ghost.pdfwrite(source)
    extracted = utila.file_list(path)
    assert len(extracted) == 19


@tests.ghostscript
def test_pdfwrite_pages():
    """Ghost script page numbers are ascending instead of names by page
    number."""
    source = power.TECH019_PDF
    path = ghost.pdfwrite(source, pages=(3, 7))
    extracted = utila.file_list(path)
    expected = ['1.png', '2.png']
    assert extracted == expected
    loaded = [
        utila.file_read_binary(os.path.join(path, item)) for item in extracted
    ]
    # verify that page number converting works
    utilatest.assert_bin(loaded[0], 3201675645)
    utilatest.assert_bin(loaded[1], 1204049905)


@tests.ghostscript
def test_pdfwrite_with_spaces(td):
    dst = td.tmpdir.join('space with space.pdf')
    utila.file_copy(src=power.TECH019_PDF, dst=dst)
    ghost.pdfwrite(dst, root=td.tmpdir, pages=1)
    assert len(utila.file_list(path=td.tmpdir)) == 2
