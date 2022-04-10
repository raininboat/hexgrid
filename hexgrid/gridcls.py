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
from dataclasses import dataclass
from math import log
from typing import Any, overload

# import hexgrid
from . import global_const, misc


class Pos:
    """Position class used for hexgrid locate
    partly based on <https://www.redblobgames.com/grids/hexagons/>
    """

    @overload
    def __init__(self, _x: int, _y: int): ...

    @overload
    def __init__(self, pos: str): ...

    def __init__(self, *args, **kwargs):
        "input the offset pos set like 'A8' or (1, 8)"
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
        _r = re.match(r"([A-Z]+)(\d+)", pos)
        if _r is None:
            raise ValueError(pos)
        x_str, y_str = _r.groups()
        x_tmp = [int(_x - 0x40) for _x in x_str.encode(encoding="utf-8")]
        x_tmp.reverse()
        x_val = 0
        for i, j in enumerate(x_tmp):    # range(len(x_tmp)):
            x_val += j * (26 ** i)
        # x_val = int(x_str.encode(encoding="utf-8")[0]) - 0x40
        y_val = int(y_str)
        self.point_x = x_val
        self.point_y = y_val

    def change_offset_into_cube(self, offset_x: int, offset_y: int):
        """change the offset coordinate like into cube vector (0, 1, -2)
        e.g: B2-(2, 2) => (1, -2, 1)

        the origin point is still on the top-left A1 (currently)
        the positive axis of (x, y, z) is (3, 11, 7 o'clock) to become a right-
        handed coordinate system

        unit vector on absolute px:
            x: (R,      0)
            y: (-R/2,   R*sqrt(3)/2)
            z: (-R/2,   -R*sqrt(2)/2)
        """

    def change_cube_into_offset(self, cube_x, cube_y, _=None):
        """change the cube coordinate back into the offset coordinate
        the left-top A1 mark as (1, 1) so the origin point is not available on 
        the map image
        """


    def offset_cood(self):
        pass

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
        _y = ((self.point_x >> 1 - self.point_x / 2)
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
        x_lst.reverse()         # list in long devide is from lowest to highest
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

    def __eq__(self, __o):
        if isinstance(__o, Pos):  # type(__o) is Pos:
            if self.point_x != __o.point_x or self.point_y != __o.point_y:
                return False
        elif isinstance(__o, tuple):  # type(__o) is tuple:
            if self.point_x != __o[0] or self.point_y != __o[1]:
                return False
        else:
            raise TypeError(type(__o))
        return True

    def __hash__(self) -> int:
        return hash((self.point_x, self.point_y))

    def __str__(self) -> str:
        return self.show_pos


class PosConf:
    "a class showing all the conf on a certain hexagon"
    def __init__(self, pos: Pos, floor=None, item=None, player=None):
        self.pos = pos
        self.floor = floor
        self.item = item
        self.player = player

    def set_data(self, tag, data):
        "use <tag> to set data"
        if tag == "<floor>":
            self.floor = data
        elif tag == "<item>":
            self.item = data
        elif tag == "<player>":
            self.player = data

    def print_on_img(self, map_canvas):
        """draw all the things in this hexagon on canvas
        (`create_grid_pic.MapCanvas`)"""
        if self.floor:
            map_canvas.draw_single_hex_floor(node=self.floor)
        if self.item:
            map_canvas.draw_single_item(self.item)
        if self.player:
            map_canvas.draw_single_player(self.player)


class Grid(dict):
    def __init__(self, map_save_dict: dict = None):
        super().__init__()
        self.update(map_save_dict)
        # self._map_data = self.get_map_data()

    def get_pos(self, pos: Pos):
        "still generates all the map datas"
        map_data = self.get_map_data()
        if pos in map_data:
            return map_data[pos]
        return PosConf(pos=pos)

    def get_map_data(self, gridobj=None):
        "get all markers on the map according to pos"
        if gridobj is None:
            gridobj = self
        tmp_data_dict = {}   # Pos: PosConf
        # tmp_data_dict["color"] = gridobj["<color>"]
        for tag in ["<floor>", "<item>", "<player>"]:
            for data in gridobj[tag].get_data_iter():
                if data.pos in tmp_data_dict:
                    tmp_data_dict[data.pos].set_data(tag=tag, data=data)
                else:
                    this_pos_conf = PosConf(pos=data.pos)
                    this_pos_conf.set_data(tag=tag, data=data)
                    tmp_data_dict[data.pos] = this_pos_conf
        return tmp_data_dict

    def save(self, path, encoding="utf-8"):
        # TODO: save map
        "save the hexmap"
        with open(path, mode="w", encoding=encoding) as file:
            file.writelines(global_const.SAVE_FILE_HEADER)
            tag_list = [
                "<set>", "<color>", "<floor>", "<item>", "<user>", "<player>"
            ]
            for tag in tag_list:
                data = self[tag]
                # print(tag, data)
                file.writelines(data.get_save_iter())


class MapGridElementTemplate:
    "basic hexgrid row element template"
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
    @dataclass
    class Floor(MapGridElementTemplate):
        "the color of a specific hexagon grid"
        pos: Pos
        color: Any

        def __iter__(self):
            return self._RowIter(
                [self.pos, self.color]
            )

    @dataclass
    class Set(MapGridElementTemplate):
        "settings of the map"
        x_max: int
        y_max: int
        _r: int      # TODO: 存档六角格半径可变
        name: str

        @property
        def size(self):
            _x = global_const.PX_R * 1.5 * (self.x_max + 0.7)
            _y = (global_const.PX_R * global_const.PX_RATIO
                  * (self.y_max + 0.5) * 2)
            return (int(_x), int(_y))

        def __iter__(self):
            return self._RowIter([self.x_max, self.y_max,
                                  self._r, self.name])

    @dataclass
    class Item(MapGridElementTemplate):  # TODO: load google icons
        "the items put on the map"
        id: int
        name: str
        color: int
        type: int
        pos: Pos

        def __iter__(self):
            return self._RowIter(
                [str(_x) for _x in (
                    self.id, self.name, self.color,
                    self.type, self.pos
                )]
            )

    @dataclass
    class User(MapGridElementTemplate):  # TODO: user set
        "users on the map (currently useless)"
        uid: str
        hash: str

        def __iter__(self):
            return self._RowIter([self.uid, self.hash])

    @dataclass
    class Player(MapGridElementTemplate):   # TODO: player
        "user players on the map (currently same as `item`)"
        id: int
        name: str
        uid: str
        color: int
        type: int
        pos: Pos

        def __iter__(self):
            return self._RowIter(
                [str(_x) for _x in (
                    self.id, self.name, self.uid,
                    self.color, self.type, self.pos
                )]
            )

    @dataclass
    class Color(MapGridElementTemplate):    # TODO: color save and order
        "colors used by `floor` (and `item`, `player` in the future)"
        # NOTE: UNSTABLE, WILL CHANGE IN THE FUTURE
        # self.id = int(row_data_list[0])
        color: str

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


class GridNode:
    def __init__(self, data=None, pos=None):
        """
        `pos`: the position of the node -> tuple (_x, _y) or pos("a", 0)
        """
        if isinstance(pos, tuple):
            pos = Pos(pos[0], pos[1])
        self.data = data
        self.pos = pos
