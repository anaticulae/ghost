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
    parser = utila.cli.create_parser(
        config=CONFIG,
        description=DESCRIPTION,
        todo=[],
        version=ghost.__version__,
    )
    args = utila.parse(parser)
    inpath, outpath = utila.sources(args, singleinput=True)  # pylint:disable=W0632
    # It is only single path supported. Run program multiple times if more
    # than one analysis is required.
    inpath = inpath[0]
    pagecount = pdfinfo.pages.determine(inpath)
    pages = args.get('pages', None)
    if pages:
        pages = utila.parse_pages(pages[0], pagecount=pagecount)
    else:
        pages = utila.rtuple(pagecount)
    write_images(
        inpath,
        outpath=outpath,
        pages=pages,
    )
    return utila.SUCCESS


def write_images(inpath, outpath, pages: tuple = None):
    root = ghost.pdfwrite(source=inpath, pages=pages)
    written = utila.file_list(root, include='png', absolute=True)
    written.sort(key=lambda x: utila.file_name(x).zfill(4))
    for path, filename in zip(written, pages):
        filename = f'{str(filename).zfill(3)}.png'
        dst = utila.join(outpath, filename)
        utila.debug(f'write {dst}')
        utila.file_copy(path, dst=dst)
