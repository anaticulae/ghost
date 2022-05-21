# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utila.cli

import ghost

DESCRIPTION = ''
CONFIG = utila.ParserConfiguration(
    inputparameter=True,
    outputparameter=True,
    prefix=False,
    multiprocessed=False,
    pages=True,
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
    return utila.SUCCESS
