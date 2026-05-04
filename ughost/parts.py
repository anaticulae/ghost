# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import io

import PIL.Image
import PIL.ImageChops
import PIL.ImageDraw
import utilo

import ughost
import ughost.cli


@dataclasses.dataclass
class Part:
    page: int = None
    bounding: tuple = None
    color: tuple = None
    name: str = None

    def __getitem__(self, index):
        if not index:
            return self.page
        if index == 1:
            return self.bounding
        if index == 2:
            return self.color
        if index == 3:
            return self.name
        raise IndexError


def run(src: str, dst: str, boundings: list) -> list:
    result = []
    extracted = parts(source=src, boundings=boundings)
    for image, bounding in zip(extracted, boundings):
        name = bounding.name
        if name is None:
            name = utilo.tmpname()
        outpath = utilo.join(dst, f'{name}.png')
        utilo.debug(outpath)
        # TODO: SECURITY: BEFORE RELASE: USE PRIVATE LATER
        utilo.file_replace_binary(outpath, content=image)
        result.append(outpath)
    return result


# TODO: HOLY VALUE
DPI_PDF = 72.0


def bounding_convert(pdf: tuple, dpi: int = ughost.cli.DPI) -> tuple:
    """\
    >>> bounding_convert((120, 120, 520, 520))
    (360.0, 360.0, 1560.0, 1560.0)
    """
    assert dpi and DPI_PDF, f'invalid dpi: {dpi}, {DPI_PDF}'
    result = utilo.tuple_mult(
        pdf,
        value=dpi / DPI_PDF,
    )
    return result


def parts(source: str, boundings: list) -> list:
    extracted = extract(
        source=source,
        boundings=boundings,
    )
    result = []
    for item in boundings:
        page, bounding = item.page, item.bounding
        color = item.color
        path = extracted[page]
        part = extract_part(path, bounding, color)
        result.append(part)
    return result


def extract(source, boundings: list) -> dict:
    workdir = utilo.tmpdir(root=ughost.ROOT)
    pages = set(item[0] for item in boundings)
    pages = sorted(pages)
    pagesraw: str = ','.join(str(item) for item in pages)
    cmd = f'{ughost.PROCESS} -i {source} -o {workdir} --pages={pagesraw}'
    utilo.run(cmd)
    files = utilo.file_list(
        workdir,
        absolute=True,
    )
    result = dict(zip(
        pages,
        files,
    ))
    return result


def extract_part(path: str, bounding: tuple, color=None) -> bytes:
    raw = io.BytesIO()
    with PIL.Image.open(path, formats=('png',)) as loaded:
        size = loaded._size  # pylint:disable=W0212
        mask = create_mask(
            bounding,
            size=size,
        )
        image = PIL.ImageChops.multiply(loaded, mask)
        image = colorize(image, color=color)
        image.save(raw, format='png')
    # rewind the buffer
    raw.seek(0)
    # convert to bytes
    result = raw.getvalue()
    return result


def create_mask(bounding: tuple, size: tuple) -> PIL.Image:
    """Color list of rectangles defined in `bounding`."""
    single = isinstance(bounding[0], (int, float))
    if single:
        bounding = [bounding]
    image = PIL.Image.new(
        mode='RGBA',
        size=size,
    )
    draw = PIL.ImageDraw.Draw(image)
    color = (0, 0, 0, 255)
    for bbox in bounding:
        # TODO: VERYIFY OVERLAPPING RECTANLGES
        draw.rectangle(
            bbox,
            fill=color,
        )
    return image


def colorize(image, color):
    if color is None:
        color = (255, 0, 0)
    # split the image into individual bands
    source = image.split()
    alpha = 3
    # select regions where alpha is selected
    mask = source[alpha].point(lambda i: i)
    # process the green band
    for band, col in enumerate(color):
        source[band].paste(
            source[band].point(lambda i: col),  # pylint:disable=cell-var-from-loop
            None,
            mask,
        )
    # build a new multiband image
    image = PIL.Image.merge(image.mode, source)
    return image
