# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import io
import os

import iamraw
import PIL.Image

import ghost


def images(source: str, boundings: iamraw.ImageInformations) -> list:
    pages = set(item.page for item in boundings)
    pagenr = {page: index for index, page in enumerate(pages, start=1)}
    root = ghost.pdfwrite(source, pages=pages)
    loaded = [
        load_image(
            bounding,
            path=os.path.join(root, f'{pagenr[bounding.page]}.png'),
        ) for bounding in boundings
    ]
    return loaded


def load_image(bounding: iamraw.ImageInformation, path: str) -> bytes:
    raw = io.BytesIO()
    with PIL.Image.open(path, formats=('png',)) as loaded:
        left, upper, right, lower = bounding.bounding
        croped = loaded.crop((left, upper, right, lower))
        croped.save(raw, format='png')
    # rewind the buffer
    raw.seek(0)
    # convert to bytes
    result = raw.getvalue()
    return result
