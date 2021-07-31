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
    pages = {item.page for item in boundings}
    root = ghost.pdfwrite(source, pages=pages)
    loaded = [load_images(bounding, root=root) for bounding in boundings]
    return loaded


def load_images(bounding: iamraw.ImageInformation, root: str) -> bytes:
    page = bounding.page
    path = os.path.join(root, f'{page+1}.png')
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
