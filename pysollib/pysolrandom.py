#!/usr/bin/env python
# -*- mode: python; coding: utf-8; -*-
# ---------------------------------------------------------------------------##
#
# Copyright (C) 1998-2003 Markus Franz Xaver Johannes Oberhumer
# Copyright (C) 2003 Mt. Hood Playing Card Co.
# Copyright (C) 2005-2009 Skomoroh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------##


# imports
import re

import pysol_cards
assert getattr(pysol_cards, 'VERSION', (0, 0, 0)) >= (0, 8, 16), (
    "Newer version of https://pypi.org/project/pysol-cards is required.")
import pysol_cards.random  # noqa: I100
import pysol_cards.random_base  # noqa: I100
from pysol_cards.random import LCRandom31, match_ms_deal_prefix  # noqa: I100
from pysol_cards.random import CUSTOM_BIT, MS_LONG_BIT  # noqa: I100


class CustomRandom(pysol_cards.random_base.RandomBase):
    def __init__(self, seed=None):
        self.initial_seed = self.seed = MS_LONG_BIT | CUSTOM_BIT
        self.origin = self.ORIGIN_UNKNOWN
        self.setSeedAsStr('Custom')

    def reset(self):
        pass

    def shuffle(self, seq):
        pass


PysolRandom = pysol_cards.random.MTRandom


# ************************************************************************
# * PySol support code
# ************************************************************************


# construct Random from seed string
def constructRandom(s):
    if s == 'Custom':
        return CustomRandom()
    m = match_ms_deal_prefix(s)
    if m is not None:
        seed = m
        if 0 <= seed <= LCRandom31.MAX_SEED:
            ret = LCRandom31(seed)
            assert ret.seed
            assert ret.seedx
            assert ret.initial_seed
            # ret.setSeedAsStr(s)
            return ret
        else:
            raise ValueError("ms seed out of range")
    # cut off "L" from possible conversion to int
    s = re.sub(r"L$", "", str(s))
    s = re.sub(r"[\s\#\-\_\.\,]", "", s.lower())
    if not s:
        return None
    seed = int(s)
    if 0 <= seed < 32000:
        return LCRandom31(seed)
    # print("MTRandom", seed)
    ret = pysol_cards.random.MTRandom(seed)
    init_state = ret.getstate()
    ret.initial_seed = initial_seed = seed

    def _reset(self=ret):
        # print("called reset")
        ret.setSeed(initial_seed)
        return
        ret.seed = ret.initial_seed
        ret.setstate(init_state)
    ret.reset = _reset
    return ret


# test
if __name__ == '__main__':
    r = constructRandom('12345')
    print(r.randint(0, 100))
    print(r.random())
    print(type(r))
