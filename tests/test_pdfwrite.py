# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower
import utilo
import utilotest

import tests
import ughost


@tests.ughostscript
@utilotest.longrun
def test_pdfwrite_all():
    source = hoverpower.TECH019_PDF
    path = ughost.pdfwrite(source)
    extracted = utilo.file_list(path)
    assert len(extracted) == 19


@tests.ughostscript
def test_pdfwrite_pages():
    """ughost script page numbers are ascending instead of names by page
    number."""
    source = hoverpower.TECH019_PDF
    path = ughost.pdfwrite(source, pages=(3, 7))
    extracted = utilo.file_list(path)
    expected = ['1.png', '2.png']
    assert extracted == expected
    loaded = [
        utilo.file_read_binary(os.path.join(path, item)) for item in extracted
    ]
    # verify that page number converting works
    utilotest.assert_bin(loaded[0], (3201675645, 1609777475, 2024650708))
    utilotest.assert_bin(loaded[1], (1204049905, 3839788996, 2476290319))


@tests.ughostscript
def test_pdfwrite_with_spaces(td):
    dst = td.tmpdir.join('space with space.pdf')
    utilo.file_copy(src=hoverpower.TECH019_PDF, dst=dst)
    ughost.pdfwrite(dst, root=td.tmpdir, pages=1)
    assert len(utilo.file_list(path=td.tmpdir)) == 2
