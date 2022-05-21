# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila
import utilatest

import tests


def test_help(monkeypatch):
    tests.run('--help', monkeypatch=monkeypatch)


def test_run(testdir, monkeypatch):
    outpath = testdir.tmpdir
    cmd = f'-i {power.TECH019_PDF} -o {outpath} --pages=3:8,12:15'
    tests.run(cmd, monkeypatch=monkeypatch)
    assert utila.file_count(outpath) == 8


@utilatest.longrun
def test_all(testdir, monkeypatch):
    outpath = testdir.tmpdir
    cmd = f'-i {power.BACHELOR032_PDF} -o {outpath}'
    tests.run(cmd, monkeypatch=monkeypatch)
    assert utila.file_count(outpath) == 32
