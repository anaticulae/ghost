# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import power
import utila
import utilatest

import ghost
import tests


@tests.ghostscript
def test_images(td):
    boundings = [
        iamraw.ImageInformation(
            page=0,
            bounding=(250, 250, 1000, 1000),
        ),
    ]
    loaded = ghost.images(
        source=power.BACHELOR051_PDF,
        boundings=boundings,
    )
    assert len(loaded) == 1
    png = os.path.join(td.tmpdir, 'test.png')
    image = loaded[0]
    utila.file_create_binary(png, content=image)
    # verify result
    utilatest.assert_bin(image, (3555017284, 3680991176))
