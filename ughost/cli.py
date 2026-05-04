# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdflog
import utilo
import utilo.cli

import ughost

DESCRIPTION = ''
CONFIG = utilo.ParserConfiguration(
    inputparameter=True,
    outputparameter=True,
    prefix=False,
    multiprocessed=False,
    cacheflag=False,
    waitingflag=False,
)
DPI = 216.0


@utilo.saveme
def main():
    inpath, outpath, dpi, pages = eval_cli()
    write_images(
        inpath,
        outpath=outpath,
        dpi=dpi,
        pages=pages,
    )
    return utilo.SUCCESS


def eval_cli():
    parser = utilo.cli.create_parser(
        config=CONFIG,
        description=DESCRIPTION,
        todo=[
            utilo.Parameter(
                longcut='dpi',
                message='use 216 as default',
                args=dict(default=DPI),
            )
        ],
        prog=ughost.PROCESS,
        version=ughost.__version__,
    )
    args = utilo.parse(parser)
    inpath, outpath = utilo.sources(args, singleinput=True)  # pylint:disable=W0632
    # It is only single path supported. Run program multiple times if more
    # than one analysis is required.
    inpath = inpath[0]
    dpi = args.get('dpi', DPI)
    pages = parse_pages(
        args.get('pages', None),
        inpath=inpath,
    )
    return inpath, outpath, dpi, pages


def write_images(inpath, outpath, dpi: float, pages: tuple = None):
    root = ughost.pdfwrite(
        source=inpath,
        dpi=dpi,
        pages=pages,
    )
    written = utilo.file_list(root, include='png', absolute=True)
    for path, filename in zip(written, pages):
        filename = f'{str(filename).zfill(3)}.png'
        dst = utilo.join(outpath, filename)
        utilo.debug(f'write {dst}')
        utilo.file_copy(path, dst=dst)


def parse_pages(pages: tuple, inpath: str) -> tuple:
    pagecount = pdflog.pagecount(inpath)
    if not pages:
        return utilo.rtuple(pagecount)
    pages = utilo.parse_pages(
        pages[0],
        pagecount=pagecount,
    )
    return pages
