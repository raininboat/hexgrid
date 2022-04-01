# -*- encoding: utf-8 -*-
"""
   Hexgrid by Thunderain Zhou
   Copyright 2022 Thunderain Zhou

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import re
from math import log
from typing import overload

# import hexgrid
from hexgrid import global_const, misc


class Pos:
    "Position class used for hexgrid locate"

    @overload
    def __init__(self, _x: int, _y: int): ...

    @overload
    def __init__(self, pos: str): ...

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self._init_pos(args[0])
        elif len(args) == 2:
            self._init_xy(args[0], args[1])
        elif "pos" in kwargs:
            self._init_pos(kwargs["pos"])

        elif "_x" in kwargs and "_y" in kwargs:
            self._init_xy(_x=kwargs["_x"], _y=kwargs["_y"])
        else:
            raise ValueError(args, kwargs)

    def _init_xy(self, _x: int, _y: int):
        x_val = int(_x)
        y_val = int(_y)
        self.point_x = x_val
        self.point_y = y_val

    def _init_pos(self, pos: str):
        pos = pos.upper()
        _r = re.match(r"([A-Z]+)(\d)+", pos)
        if _r is None:
            raise ValueError(pos)
        x_str, y_str = _r.groups()
        x_tmp = [int(_x - 0x40) for _x in x_str.encode(encoding="utf-8")]
        x_tmp.reverse()
        x_val = 0
        for i in range(len(x_tmp)):
            x_val += x_tmp[i] * (26 ** i)
        # x_val = int(x_str.encode(encoding="utf-8")[0]) - 0x40
        y_val = int(y_str)
        self.point_x = x_val
        self.point_y = y_val

    # def goto(self, vector=(0, 0)):
    #     _x = self.point_x + vector[0]
    #     _y = self.point_y + vector[1]
    #     return Pos(_x, _y)

    def point_list_around(self):
        "return the 6 points of the grid lines around the pos"
        _t = []
        _x, _y = self.xy_abs
        _r = global_const.PX_R
        _h = global_const.PX_RATIO * _r
        _t = [
            (_x - _r, _y),
            (_x - _r / 2, _y + _h),
            (_x + _r / 2, _y + _h),
            (_x + _r, _y),
            (_x + _r / 2, _y - _h),
            (_x - _r / 2, _y - _h),
            (_x - _r, _y)
        ]
        return _t

    def coord_text_cood(self):
        "cood for grid title"
        _x, _y = self.xy_abs
        t_x = _x
        t_y = _y - global_const.PX_RATIO * global_const.PX_R
        return (t_x, t_y)

    def image_paste_box(self):
        "the cood where image should paste (left-top)"
        _x, _y = map(int, self.xy_abs)
        _d = int(
            (1.5 - global_const.PX_RATIO)
            * global_const.PX_R
        )
        return (_x - _d, _y - _d)

    @property
    def xy_abs(self):
        "absolute coordinate on the canvas (for drawing)"
        _x = self.point_x * global_const.PX_R * 1.5
        _y = ((self.point_x // 2 - self.point_x / 2)
              * global_const.PX_R * 2
              * global_const.PX_RATIO + 2 * self.point_y
              * global_const.PX_R * global_const.PX_RATIO)
        return (_x, _y)

    @property
    def str_x(self):
        "the text version of _x coordinate"
        if self.point_x <= 0:
            return ""
        x_lst = []
        tmp_x = self.point_x
        for _ in range(int(log(self.point_x, 26))+1):
            tmp_x, this = divmod(tmp_x, 26)
            x_lst.append(this + 0x40)
        x_ascii = bytes(x_lst.__iter__())
        return x_ascii.decode(encoding="utf-8")

    @property
    def pos_tuple(self):
        "the position tuple on the grid"
        return (self.point_x, self.point_y)

    @property
    def show_pos(self) -> str:
        "the output version of pos on the grid"
        if self.point_x <= 0:
            return ""
        return f"{self.str_x}{self.point_y}"

    def __eq__(self, __o: object):
        if type(__o) is Pos:
            if self.point_x != __o._x or self.point_y != __o._y:
                return False
        elif type(__o) is tuple:
            if self.point_x != __o[0] or self.point_y != __o[1]:
                return False
        else:
            raise TypeError(type(__o))
        return True

    def __hash__(self) -> int:
        return hash((self.point_x, self.point_y))

    def __str__(self) -> str:
        return self.show_pos


class Grid(object):
    def __init__(self, map_save_dict=None):
        if map_save_dict is None:
            map_save_dict = {}
        self.map_dict = {
            "<item>": {},
            "<player>": {},
            "<floor>": {}
        }
        self.cfg = None
        self.user = {}
        self.color = None
        for i in map_save_dict.values():
            tag = i.tag
            data = i.data
            if tag in ("<item>", "<player>", "<floor>"):
                for j in data:
                    pos = j.pos
                    self.map_dict[tag][pos] = j
            elif tag == "<set>":
                self.cfg = data[-1]
            elif tag == "<user>":
                for j in data:
                    self.user[j.uid] = j
            elif tag == "<color>":
                self.color = i
            else:
                print("unknown tag '{0}'".format(tag))

    def save(self, path):
        # TODO: save map
        "save the hexmap"
        print(f"""{misc.COLOR.YELLOW}save map is currently not \
supported{misc.COLOR.DEFAULT} - {misc.COLOR.GREEN}path: {path}\
""")


class _MapGridElementTemplate:
    # def __init__(self, row_data_list):
    #     "the init method should be override"
    #     self.data = row_data_list

    # def __iter__(self):
    #     return self._RowIter(self.data)

    class _RowIter:
        # "the iter generater class, write __iter__ in the main cls to use it"
        def __init__(self, data_list):
            self.data = data_list
            self.index = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.index >= len(self.data):
                raise StopIteration()
            tmp_data = str(self.data[self.index])
            self.index += 1
            return misc.escape(tmp_data)


class Node:
    "All the map nodes, the lines in the save file"
    class Floor(_MapGridElementTemplate):
        def __init__(self, pos: Pos, color_id):
            self.pos = pos
            self.color = color_id

        def __iter__(self):
            return self._RowIter(
                [self.pos, self.color]
            )

    class Set(_MapGridElementTemplate):
        def __init__(self, x_max, y_max, _r, name):
            self.x_max = int(x_max)
            self.y_max = int(y_max)
            self._r = int(_r)      # TODO: 存档六角格半径可变
            self.name = name

        @property
        def size(self):
            _x = global_const.PX_R * 1.5 * (self.x_max + 0.7)
            _y = (global_const.PX_R * global_const.PX_RATIO
                  * (self.y_max + 0.5) * 2)
            return (int(_x), int(_y))

        def __iter__(self):
            return self._RowIter([self.x_max, self.y_max,
                                  self._r, self.name])

    class Item(_MapGridElementTemplate):
        def __init__(self, id_, name, color_id, type_id, pos: Pos):
            self.id = id_
            self.name = name
            self.color = int(color_id)
            self.type = int(type_id)
            self.pos = pos

        # @property
        # def stamp_file_name(self):
        #     _t = stamp_load.RESOURCE_STAMP_TYPE[self.type]
        #     c = self.color
        #     return _t.format_map(color=c)

        def __iter__(self):
            return self._RowIter(
                [str(_x) for _x in (
                    self.id, self.name, self.color,
                    self.type, self.pos
                )]
            )

    class User(_MapGridElementTemplate):
        def __init__(self, uid, hash_):
            self.uid = uid
            self.hash = hash_

        def __iter__(self):
            return self._RowIter([self.uid, self.hash])

    class Player(_MapGridElementTemplate):
        def __init__(self, id_, name, uid, color_id, type_id, pos: Pos):
            self.id = id_
            self.name = name
            self.uid = uid
            self.color = int(color_id)
            self.type = int(type_id)
            self.pos = pos

        # @property
        # def stamp_file_name(self):
        #     _t = stamp_load.RESOURCE_STAMP_TYPE[self.type]
        #     c = self.color
        #     return _t.format_map(color=c)

        def __iter__(self):
            return self._RowIter(
                [str(_x) for _x in (
                    self.id, self.name, self.uid,
                    self.color, self.type, self.pos
                )]
            )

    class Color(_MapGridElementTemplate):
        def __init__(self, color):
            # self.id = int(row_data_list[0])
            self.color = color

        def setcolor(self, new_color):
            self.color = new_color

        @property
        def deleted(self):
            return self.color == "_DELETED_"

        def delcolor(self):
            self.color = "_DELETED_"

        def __eq__(self, __o: object):
            if self.color == "_DELETED_":
                return False
            return self.color == __o

        def __iter__(self):
            return self._RowIter(
                [self.color]
            )


class GridNode(object):
    def __init__(self, data=None, pos=None):
        """
        `pos`: the position of the node -> tuple (_x, _y) or pos("a", 0)
        """
        if type(pos) is tuple:
            pos = Pos(pos[0], pos[1])
        self.data = data
        self.pos = pos
