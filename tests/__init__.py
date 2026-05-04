#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import pytest
import utilatest

import ughost

run, fail = utilatest.create_cli_runner(ughost)

ughostscript = pytest.mark.skipif(
    not ughost.HAS_GHOST,
    reason='install ughostscript',
)
