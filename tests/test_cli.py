# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import utilo
import utilotest

import tests


def test_help(mp):
    tests.run('--help', mp=mp)


@tests.ughostscript
def test_run(td, mp):
    outpath = td.tmpdir
    cmd = f'-i {hoverpower.TECH019_PDF} -o {outpath} --pages=3:8,12:15'
    tests.run(cmd, mp=mp)
    assert utilo.file_count(outpath) == 8


@tests.ughostscript
@utilotest.longrun
def test_all(td, mp):
    outpath = td.tmpdir
    cmd = f'-i {hoverpower.BACHELOR032_PDF} -o {outpath}'
    tests.run(cmd, mp=mp)
    assert utilo.file_count(outpath) == 32
