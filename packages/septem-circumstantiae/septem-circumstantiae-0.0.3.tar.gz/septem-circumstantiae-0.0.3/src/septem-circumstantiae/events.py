# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""

# https://alxfed.github.io/blog/posts/2019/02/22/Septem-Circumstantiae.html


class Event:
    """"""
    who: str    = ''  # quis
    what: str   = ''  # quid
    when: str   = ''  # quando
    where: str  = ''  # ubi
    why: str    = ''  # cur (for the sake of what?)
    how: str    = ''  # quem ad modum (in what way?)
    by_what_means: str = ''  # quibus adminiculis

    def __init__(self, *args, **kwargs):
        pass
