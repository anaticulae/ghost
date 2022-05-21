# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import painter
import power

import ghost.parts


def test_parts(testdir):
    source = power.BACHELOR028_PDF
    boundings = [
        ghost.parts.Part(
            page=0,
            bounding=(800.0, 1000.0, 1000.0, 1800),
        )
    ]
    extracted = ghost.parts.parts(
        source=source,
        boundings=boundings,
    )
    assert len(extracted) == 1
    painter.show_figure(extracted[0])


def test_run_extractor(testdir):
    source = power.BACHELOR028_PDF
    boundings = [
        ghost.parts.Part(
            page=0,
            bounding=(800.0, 1000.0, 1000.0, 1800),
        )
    ]
    extracted = ghost.parts.run(
        src=source,
        dst=testdir.tmpdir,
        boundings=boundings,
    )
    assert len(extracted) == 1
