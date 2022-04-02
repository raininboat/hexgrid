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

    def get_line_save(self):
        return self._MapSaveIter(self, needTag=True)

    def __iter__(self):
        return self._MapSaveIter(self, needTag=False)

    class _MapSaveRow(gridcls.MapGridElementTemplate):
        "basic_tamplate"

    class _MapSaveIter:
        __sep = "|"

        def __init__(self, MapObj, needTag=False):
            self.MapObj = MapObj
            self.index = 0
            if needTag:
                self.index -= 1

        def __iter__(self):
            return self

        def __next__(self):
            if self.index >= len(self.MapObj.data):
                raise StopIteration()
            if self.index < 0:
                # return tag
                self.index += 1
                return self.MapObj.tag
            tmp_data = self.MapObj.data[self.index]
            ret = self.__sep.join(tmp_data)
            self.index += 1
            return ret


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
            if color_id >= len(self.data):
                print("ERROR, NO COLOR - {}".format(color_id))
                import objprint
                objprint.op(self)
                return None
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
                self.color = row_data_list[0]

    class Floor(_MapSaveClsTemplate):
        def __init__(self):
            super().__init__("<floor>")

        class _MapSaveRow(Node.Floor):
            def __init__(self, row_data_list):
                self.pos = gridcls.Pos(row_data_list[0])
                self.color = row_data_list[1]

    class Set(_MapSaveClsTemplate):
        def __init__(self):
            super().__init__("<set>")

        class _MapSaveRow(Node.Set):
            def __init__(self, row_data_list):
                # super().__init__(*row_data_list)
                self.x_max = int(row_data_list[0])
                self.y_max = int(row_data_list[1])
                self.r = int(row_data_list[2])      # TODO: 存档六角格半径可变
                self.name = row_data_list[3]

    class Item(_MapSaveClsTemplate):
        def __init__(self):
            super().__init__(tag="<item>")

        class _MapSaveRow(Node.Item):
            def __init__(self, row_data_list):
                self.id = row_data_list[0]
                self.name = row_data_list[1]
                self.color = int(row_data_list[2])
                self.type = int(row_data_list[3])
                self.pos = gridcls.Pos(pos=row_data_list[4])

    class User(_MapSaveClsTemplate):
        def __init__(self):
            super().__init__(tag="<user>")

        class _MapSaveRow(Node.User):
            def __init__(self, row_data_list):
                self.uid = row_data_list[0]
                self.hash = row_data_list[1]

    class Player(_MapSaveClsTemplate):
        def __init__(self):
            super().__init__(tag="<player>")

        class _MapSaveRow(Node.Player):
            def __init__(self, row_data_list):
                self.id = row_data_list[0]
                self.name = row_data_list[1]
                self.uid = row_data_list[2]
                self.color = int(row_data_list[3])
                self.type = int(row_data_list[4])
                self.pos = gridcls.Pos(pos=row_data_list[5])


__tag_class = {
    "<unknown>": _MapSaveClsTemplate,
    "<set>": MapSave.Set,
    "<item>": MapSave.Item,
    "<user>": MapSave.User,
    "<player>": MapSave.Player,
    "<color>": MapSave.Color,
    "<floor>": MapSave.Floor
}


def load_file(path, encode="utf-8"):
    "load the hexgrid save file"
    with open(path, mode="r", encoding=encode) as f:
        p = re.compile(r"^(\<\w+\>)+$")
        this_tag = "init"
        ret = {}
        for line in f:
            # remove the enter \n at end of each line
            line = line.rstrip("\n")
            this_match = p.match(line)
            if this_match is not None:
                this_tag = this_match.group()
                if this_tag in __tag_class.keys():
                    ret[this_tag] = __tag_class[this_tag]()
                continue
            if this_tag in __tag_class.keys():
                ret[this_tag].feed_line(line)
    grid = gridcls.Grid(ret)
    return grid


if __name__ == "__main__":
    demo_path = "./sample/save.hgdata"
    file = load_file(demo_path)
    print(file)
    # print("\n".join(file["<set>"].get_line_save()))
