# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdfinfo.pages
import utila
import utila.cli

import ghost

DESCRIPTION = ''
CONFIG = utila.ParserConfiguration(
    inputparameter=True,
    outputparameter=True,
    prefix=False,
    multiprocessed=False,
    cacheflag=False,
    waitingflag=False,
)


@utila.saveme
def main():
    inpath, outpath, dpi, pages = eval_cli()
    write_images(
        inpath,
        outpath=outpath,
        dpi=dpi,
        pages=pages,
    )
    return utila.SUCCESS


def eval_cli():
    parser = utila.cli.create_parser(
        config=CONFIG,
        description=DESCRIPTION,
        todo=[
            utila.Parameter(
                longcut='dpi',
                message='use 216 as default',
                args=dict(default=216.0),
            )
        ],
        version=ghost.__version__,
    )
    args = utila.parse(parser)
    inpath, outpath = utila.sources(args, singleinput=True)  # pylint:disable=W0632
    # It is only single path supported. Run program multiple times if more
    # than one analysis is required.
    inpath = inpath[0]
    dpi = args.get('dpi', 216.0)
    pages = parse_pages(
        args.get('pages', None),
        inpath=inpath,
    )
    return inpath, outpath, dpi, pages


def write_images(inpath, outpath, dpi: float, pages: tuple = None):
    root = ghost.pdfwrite(
        source=inpath,
        dpi=dpi,
        pages=pages,
    )
    written = utila.file_list(root, include='png', absolute=True)
    written.sort(key=lambda x: utila.file_name(x).zfill(4))
    for path, filename in zip(written, pages):
        filename = f'{str(filename).zfill(3)}.png'
        dst = utila.join(outpath, filename)
        utila.debug(f'write {dst}')
        utila.file_copy(path, dst=dst)


def parse_pages(pages: tuple, inpath: str) -> tuple:
    pagecount = pdfinfo.pages.determine(inpath)
    if not pages:
        return utila.rtuple(pagecount)
    pages = utila.parse_pages(
        pages[0],
        pagecount=pagecount,
    )
    return pages
