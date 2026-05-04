# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import upainter

import tests
import ughost.parts


@tests.ughostscript
def test_parts(td):  # pylint:disable=W0613
    source = hoverpower.BACHELOR028_PDF
    boundings = [
        ughost.parts.Part(
            page=0,
            bounding=(800.0, 1000.0, 1000.0, 1800),
        )
    ]
    extracted = ughost.parts.parts(
        source=source,
        boundings=boundings,
    )
    assert len(extracted) == 1
    upainter.show_figure(extracted[0])


@tests.ughostscript
def test_run_extractor(td):
    source = hoverpower.BACHELOR028_PDF
    boundings = [
        ughost.parts.Part(
            page=0,
            bounding=(800.0, 1000.0, 1000.0, 1800),
        )
    ]
    extracted = ughost.parts.run(
        src=source,
        dst=td.tmpdir,
        boundings=boundings,
    )
    assert len(extracted) == 1
