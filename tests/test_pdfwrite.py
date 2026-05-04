# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import tests
import ughost


@tests.ughostscript
@utilatest.longrun
def test_pdfwrite_all():
    source = power.TECH019_PDF
    path = ughost.pdfwrite(source)
    extracted = utila.file_list(path)
    assert len(extracted) == 19


@tests.ughostscript
def test_pdfwrite_pages():
    """ughost script page numbers are ascending instead of names by page
    number."""
    source = power.TECH019_PDF
    path = ughost.pdfwrite(source, pages=(3, 7))
    extracted = utila.file_list(path)
    expected = ['1.png', '2.png']
    assert extracted == expected
    loaded = [
        utila.file_read_binary(os.path.join(path, item)) for item in extracted
    ]
    # verify that page number converting works
    utilatest.assert_bin(loaded[0], (3201675645, 1609777475))
    utilatest.assert_bin(loaded[1], (1204049905, 3839788996))


@tests.ughostscript
def test_pdfwrite_with_spaces(td):
    dst = td.tmpdir.join('space with space.pdf')
    utila.file_copy(src=power.TECH019_PDF, dst=dst)
    ughost.pdfwrite(dst, root=td.tmpdir, pages=1)
    assert len(utila.file_list(path=td.tmpdir)) == 2
