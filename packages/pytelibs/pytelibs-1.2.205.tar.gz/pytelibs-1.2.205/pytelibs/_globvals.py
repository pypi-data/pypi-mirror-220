# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from typing import Set, List, Dict


_DELAY_MSG: Dict[int, List[int]] = {}
_SCHEDULE_MSG: Dict[int, List[int]] = {}
_GCAST_LOCKED: Set[int] = set()


def get_values(d, key):
    return d.get(key, [])

