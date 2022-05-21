# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import ghost

GHOST = 'gswin64c' if os.name == 'nt' else 'gs'

# ensure that ghost script is installed
utila.run(f'where {GHOST}')


def pdfwrite(
    source: str,
    dpi: int = 300,
    formats: str = 'pngalpha',
    root: str = None,
    pages: tuple = None,
):
    root = utila.tmpdir(root=ghost.ROOT) if root is None else root
    if isinstance(pages, int):
        destination = os.path.join(root, f'{pages}.png')
    else:
        destination = os.path.join(root, '%d.png')
    pages = gpages_fromtuple(pages)
    config = f'-sDEVICE={formats} -r{dpi} -dBATCH -dNOPAUSE -SAFE'
    source = f'"{source}"'
    cmd = f'{GHOST} {config} {pages} -sOutputFile={destination} {source}'
    utila.run(cmd)
    return root


def gpages_fromtuple(pages: tuple = None) -> str:
    """\
    >>> gpages_fromtuple((1, 2, 3))
    '-sPageList=2,3,4'
    >>> gpages_fromtuple()
    ''
    """
    if pages is None:
        return ''
    if isinstance(pages, int):
        pages = (pages,)
    # ghost requires sorted page numbers
    pages = sorted(pages)
    # -sPageList=1,3,5
    pages = utila.tuple_plus(pages, value=1)
    pages: str = utila.from_tuple(pages, separator=',')
    pages = f'-sPageList={pages}'
    return pages
