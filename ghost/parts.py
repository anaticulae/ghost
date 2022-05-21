# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import io

import PIL.Image
import PIL.ImageChops
import PIL.ImageDraw
import utila

import ghost


@dataclasses.dataclass
class Part:
    page: int = None
    bounding: tuple = None
    color: tuple = None

    def __getitem__(self, index):
        if not index:
            return self.page
        if index == 1:
            return self.bounding
        if index == 2:
            return self.color
        raise IndexError


def parts(source: str, boundings: list) -> list:
    extracted = extract(
        source=source,
        boundings=boundings,
    )
    result = []
    for item in boundings:
        page, bounding = item.page, item.bounding
        path = extracted[page]
        part = extract_part(path, bounding)
        result.append(part)
    return result


def extract(source, boundings: list) -> dict:
    workdir = utila.tmpdir(root=ghost.ROOT)
    pages = set(item[0] for item in boundings)
    pages = sorted(pages)
    pagesraw: str = ','.join(str(item) for item in pages)
    cmd = f'{ghost.PROCESS} -i {source} -o {workdir} --pages={pagesraw}'
    utila.run(cmd)
    files = utila.file_list(
        workdir,
        absolute=True,
    )
    result = dict(zip(
        pages,
        files,
    ))
    return result


def extract_part(path: str, bounding: tuple) -> bytes:
    raw = io.BytesIO()
    with PIL.Image.open(path, formats=('png',)) as loaded:
        size = loaded._size  # pylint:disable=W0212
        mask = create_mask(bounding, size=size)
        image = PIL.ImageChops.multiply(loaded, mask)
        image.save(raw, format='png')
    # rewind the buffer
    raw.seek(0)
    # convert to bytes
    result = raw.getvalue()
    return result


def create_mask(bounding: tuple, size: tuple) -> PIL.Image:
    image = PIL.Image.new(mode='RGBA', size=size)
    draw = PIL.ImageDraw.Draw(image)
    draw.rectangle(bounding, fill='black')
    return image
