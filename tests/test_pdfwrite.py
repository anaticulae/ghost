# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila
import utilatest

import ghost


@utilatest.longrun
def test_pdfwrite():
    source = power.TECH019_PDF
    path = ghost.pdfwrite(source)
    extracted = utila.file_list(path)
    assert len(extracted) == 19
