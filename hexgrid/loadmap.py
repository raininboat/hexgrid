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

from hexgrid import global_const

# import hexgrid
from . import gridcls, misc

Node = gridcls.Node
unescape = misc.unescape


class _MapSaveClsTemplate:
    def __init__(self, tag="<unknown>"):
        self.tag = tag
        self.data = []

    def feed_line(self, line: str):
        tmp_lst_1 = line.split("|")
        tmp_lst_2 = []
        for tmp_line in tmp_lst_1:
            tmp_lst_2.append(unescape(tmp_line))
        res = self._data_line(tmp_lst_2)
        self.data.append(res)

    def add_line(self, *arg):
        self._data_line(arg)

    def _data_line(self, this_line_list):
        "override this to set data class"
        return self._MapSaveRow(this_line_list)

    def get_save_iter(self):
        "get an iterator returning save string of the node obj"
        return self._MapSaveIter(self, need_tag=True)

    def get_data_iter(self):
        "get an iterator returning data node obj"
        return self._MapDataIter(self)

    def set_on_pos(self, pos, data):
        "set node data on the pos"
        index = 0
        for i in self.get_data_iter():
            if i.pos == pos:
                self.data[index] = data
                index = -1
                break
            index += 1
        if index != -1:
            self.data.append(data)

    def __iter__(self):
        return self._MapSaveIter(self, need_tag=False)

    class _MapSaveRow(gridcls.MapGridElementTemplate):
        "basic_tamplate"

    class _MapDataIter:
        def __init__(self, map_obj) -> None:
            self.map_obj = map_obj
            self.index = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.index >= len(self.map_obj.data):
                raise StopIteration()
            ret = self.map_obj.data[self.index]
            self.index += 1
            return ret

    class _MapSaveIter:
        __sep = "|"

        def __init__(self, map_obj, need_tag=False):
            self.map_obj = map_obj
            self.index = 0
            if need_tag:
                self.index -= 1

        def __iter__(self):
            return self

        def __next__(self):
            if self.index >= len(self.map_obj.data):
                raise StopIteration()
            if self.index < 0:
                # return tag
                self.index += 1
                return self.map_obj.tag+"\n"
            tmp_data = self.map_obj.data[self.index]
            ret = self.__sep.join(tmp_data)
            self.index += 1
            return ret+"\n"


class MapSave:
    "all the save items loaded, name is just like the gridcls.Node"
    class Color(_MapSaveClsTemplate):
        def __init__(self):
            super().__init__("<color>")

        def has_color(self, strrgb):
            if strrgb in self.data:
                return True
            return False

        def get_color(self, color_id: int):
            "the color string according to the id (#FFFFFF if not exist)"
            if color_id >= len(self.data) or color_id < 0:
                print(f"ERROR, NO COLOR - {color_id}")
                print(self.data)
                print("use default color #FFFFFF")
                return "#FFFFFF"
            return self.data[color_id].color

        def add_color(self, strrgb):
            if self.has_color(strrgb):
                return self.index(strrgb)
            self.feed_line(strrgb)
            return self.index(strrgb)

        def index(self, strrgb):
            if self.has_color(strrgb):
                return self.data.index(strrgb)
            return None

        class _MapSaveRow(Node.Color):
            def __init__(self, row_data_list):
                super().__init__(
                    color=row_data_list[0]
                )

    class Floor(_MapSaveClsTemplate):
        def __init__(self):
            super().__init__("<floor>")

        class _MapSaveRow(Node.Floor):
            def __init__(self, row_data_list):
                super().__init__(
                    pos=gridcls.Pos(row_data_list[0]),
                    color=row_data_list[1]
                )

    class Set(_MapSaveClsTemplate):
        def __init__(self):
            super().__init__("<set>")

        @property
        def x_max(self):
            return self.data[0].x_max

        @property
        def y_max(self):
            return self.data[0].y_max

        @property
        def name(self):
            return self.data[0].name

        @property
        def size(self):
            return self.data[0].size

        def set_data(self, node_set:Node.Set):
            if self.data:
                self.data[0] = node_set
            else:
                self.data = [node_set,]

        class _MapSaveRow(Node.Set):
            def __init__(self, row_data_list):
                super().__init__(
                    x_max=int(row_data_list[0]),
                    y_max=int(row_data_list[1]),
                    _r=int(row_data_list[2]),      # TODO: 存档六角格半径可变
                    name=row_data_list[3],
                )

    class Item(_MapSaveClsTemplate):
        def __init__(self):
            super().__init__(tag="<item>")

        class _MapSaveRow(Node.Item):
            def __init__(self, row_data_list):
                super().__init__(
                    id=row_data_list[0],
                    name=row_data_list[1],
                    color=int(row_data_list[2]),
                    type=int(row_data_list[3]),
                    pos=gridcls.Pos(pos=row_data_list[4]),
                )

    class User(_MapSaveClsTemplate):
        def __init__(self):
            super().__init__(tag="<user>")

        class _MapSaveRow(Node.User):
            def __init__(self, row_data_list):
                super().__init__(
                    uid=row_data_list[0],
                    hash=row_data_list[1],
                )

    class Player(_MapSaveClsTemplate):
        def __init__(self):
            super().__init__(tag="<player>")

        class _MapSaveRow(Node.Player):
            def __init__(self, row_data_list):
                super().__init__(
                    id=row_data_list[0],
                    name=row_data_list[1],
                    uid=row_data_list[2],
                    color=int(row_data_list[3]),
                    type=int(row_data_list[4]),
                    pos=gridcls.Pos(pos=row_data_list[5]),
                )


__tag_class = {
    "<unknown>": _MapSaveClsTemplate,
    "<set>": MapSave.Set,
    "<item>": MapSave.Item,
    "<user>": MapSave.User,
    "<player>": MapSave.Player,
    "<color>": MapSave.Color,
    "<floor>": MapSave.Floor
}

def new_file(data_set_node=None):
    "return an empty grid object of a new file"
    new_file_ = global_const.NEW_FILE_TEMPLATE.splitlines()
    data = init_map_data(new_file_)
    if data_set_node is not None:
        obj_set = MapSave.Set()
        obj_set.data.append(data_set_node)
        data["<set>"] = obj_set
    return data

def load_file(path, encode="utf-8"):
    "load the hexgrid save file"
    with open(path, mode="r", encoding=encode) as file:
        grid = init_map_data(file)
    return grid

def init_map_data(data_string_iter):
    "init the map data from a string seperated by lines"
    re_comp = re.compile(r"^(\<\w+\>)+$")
    this_tag = "init"
    ret = {}
    for line in data_string_iter:
        # remove the enter \n at end of each line
        line = line.rstrip("\n")
        this_match = re_comp.match(line)
        if this_match is not None:
            this_tag = this_match.group()
            if this_tag in __tag_class:
                ret[this_tag] = __tag_class[this_tag]()
            continue
        if this_tag in __tag_class:
            ret[this_tag].feed_line(line)
    grid = gridcls.Grid(ret)
    return grid
