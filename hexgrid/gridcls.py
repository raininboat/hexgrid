# -*- encoding: utf-8 -*-
# from PIL import Image, ImageDraw, ImageColor, ImageTk, ImageFont

from math import log
import re
from typing import overload
import hexgrid


class Pos(object):

    @overload
    def __init__(self, x: int, y: int):
        pass    # see ._init_xy()

    @overload
    def __init__(self, pos: str):
        pass    # see ._init_pos()

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self._init_pos(args[0])
        elif len(args) == 2:
            self._init_xy(args[0], args[1])
        elif "pos" in kwargs.keys():
            self._init_pos(kwargs["pos"])
        elif "x" in kwargs.keys() and "y" in kwargs.keys():
            self._init_xy(x=kwargs["x"], y=kwargs["y"])
        else:
            raise ValueError(args, kwargs)

    def _init_xy(self, x: int, y: int):
        x_val = int(x)
        y_val = int(y)
        self.x = x_val
        self.y = y_val

    def _init_pos(self, pos: str):
        pos = pos.upper()
        r = re.match(r"([A-Z]+)(\d)+", pos)
        if r is None:
            raise ValueError(pos)
        x_str, y_str = r.groups()
        x_tmp = [int(x - 0x40) for x in x_str.encode(encoding="utf-8")]
        x_tmp.reverse()
        x_val = 0
        for i in range(len(x_tmp)):
            x_val += x_tmp[i] * (26 ** i)
        # x_val = int(x_str.encode(encoding="utf-8")[0]) - 0x40
        y_val = int(y_str)
        self.x = x_val
        self.y = y_val

    def goto(self, vector=(0, 0)):
        x = self.x + vector[0]
        y = self.y + vector[1]
        return Pos(x, y)

    def point_list_around(self):
        "return the 6 points of the grid lines around the pos"
        t = []
        xy = self.px
        x = xy[0]
        y = xy[1]
        R = hexgrid.global_const.PX_R
        h = hexgrid.global_const.PX_RATIO * R
        t = [
            (x - R, y),
            (x - R / 2, y + h),
            (x + R / 2, y + h),
            (x + R, y),
            (x + R / 2, y - h),
            (x - R / 2, y - h),
            (x - R, y)
        ]
        return t

    def coord_text_cood(self):
        x, y = self.px
        t_x = x
        t_y = y - hexgrid.global_const.PX_RATIO * hexgrid.global_const.PX_R
        return (t_x, t_y)

    @property
    def px(self):
        "absolute coordinate on the canvas (for drawing)"
        x = self.x * hexgrid.global_const.PX_R * 1.5
        y = ((self.x / 2 - self.x // 2) * hexgrid.global_const.PX_R * 2 * hexgrid.global_const.PX_RATIO +
             2 * self.y * hexgrid.global_const.PX_R * hexgrid.global_const.PX_RATIO)
        return (x, y)

    @property
    def str_x(self):
        "the text version of x coordinate"
        if self.x <= 0:
            return ""
        x_lst = []
        tmp_x = self.x
        for i in range(int(log(self.x, 26))+1):
            tmp_x, this = divmod(tmp_x, 26)
            x_lst.append(this + 0x40)
        x_ascii = bytes(x_lst.__iter__())
        return x_ascii.decode(encoding="utf-8")

    @property
    def pos_tuple(self):
        return (self.x, self.y)

    @property
    def show_pos(self):
        if self.x <= 0:
            return ""
        return "{0}{1}".format(self.str_x, self.y)

    def __eq__(self, __o: object):
        if type(__o) is Pos:
            if self.x != __o.x:
                return False
            elif self.y != __o.y:
                return False
        elif type(__o) is tuple:
            if self.x != __o[0]:
                return False
            elif self.y != __o[1]:
                return False
        else:
            raise TypeError(type(__o))
        return True

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return self.show_pos


class Grid(object):
    def __init__(self, map_save_dict=None):
        if map_save_dict is None:
            map_save_dict = {}
        self.map_dict = {
            "<item>": {},
            "<player>": {},
            "<floor>" : {}
        }
        self.cfg = None
        self.user = {}
        self.color = {}
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
                for i in data:
                    self.user[i.uid] = i
            elif tag == "<color>":
                for i in data:
                    self.color[i.id] = i
            else:
                print("unknown tag '{0}'".format(tag))


class GridNode(object):
    def __init__(self, data=None, pos=None):
        """
        `pos`: the position of the node -> tuple (x, y) or pos("a", 0)
        """
        if type(pos) is tuple:
            pos = Pos(pos[0], pos[1])
        self.data = data
        self.pos = pos


if __name__ == "__main__":
    t = "Z"
    while 1:
        t = t + "0"
        a = Pos(t)
        print(a.pos_tuple)
        print(a.str_x)
        t = input("> ")
