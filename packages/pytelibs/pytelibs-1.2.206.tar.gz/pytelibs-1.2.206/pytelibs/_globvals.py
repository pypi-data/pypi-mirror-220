# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from typing import Set


_DELAY_MSG: dict = {}
_SCHEDULE_MSG: dict = {}
_GCAST_LOCKED: Set[int] = set()


def get_values(d, key: int):
    return d.get(int(key), [])
