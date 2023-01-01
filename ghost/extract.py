# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import io
import os

import iamraw
import PIL.Image
import utila

import ghost

DPI = 72
RENDERER = 300


def images(source: str, boundings: iamraw.ImageInformations, dpi=DPI) -> list:
    # ensure that bounding box matches with correct page
    pages = sorted(set(item.page for item in boundings))
    root = ghost.pdfwrite(source, dpi=RENDERER, pages=pages)
    pagenr = {page: index for index, page in enumerate(pages, start=1)}
    loaded = [
        load_image(
            bounding,
            path=os.path.join(root, f'{pagenr[bounding.page]}.png'),
            dpi=dpi,
        ) for bounding in boundings
    ]
    return loaded


def load_image(bounding: iamraw.ImageInformation, path: str, dpi=DPI) -> bytes:
    raw = io.BytesIO()
    with PIL.Image.open(path, formats=('png',)) as loaded:
        # left, upper, right, lower
        bounding = utila.tuple_mult(
            bounding.bounding,
            value=RENDERER / dpi,
        )
        croped = loaded.crop(bounding)
        croped.save(raw, format='png')
    # rewind the buffer
    raw.seek(0)
    # convert to bytes
    result = raw.getvalue()
    return result
