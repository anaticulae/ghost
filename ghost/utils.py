# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
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


def pdfwrite(source: str, dpi: int = 300, pages: tuple = None):
    root = utila.tmpdir(root=ghost.ROOT)
    destination = os.path.join(root, '%d.png')
    if pages:
        # -sPageList=1,3,5
        pages = tuple_plus(pages, value=1)
        pages: str = utila.from_tuple(pages, separator=',')
        pages = f'-sPageList={pages}'
    else:
        pages = ''
    config = f'-sDEVICE=png16m -r{dpi} -dBATCH -dNOPAUSE -SAFE'
    cmd = f'{GHOST} {config} {pages} -sOutputFile={destination} {source}'
    utila.run(cmd)
    return root


def tuple_plus(items, value):
    """\
    >>> tuple_plus((4, 6, 10), 5)
    (9, 11, 15)
    """
    return tuple(item + value for item in items)
