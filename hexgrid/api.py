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

from . import create_grid_pic, global_const, gridcls, loadmap


class MapObj:
    """a map savefile operation interface
    (useful when link hexgrid as module)"""

    def __init__(self, *, load_file_path=None, new_map_set_node=None):
        "init a map object (load file or create new file)"
        if load_file_path is not None:
            data = loadmap.load_file(path=load_file_path)
        else:
            data = loadmap.new_file(data_set_node=new_map_set_node)
        self.data = data

    def save(self, output_path):
        "save map data into file (.hgdata)"
        self.data.save(output_path)

    def render(self, path=None):
        "render the picture"
        canvas = create_grid_pic.MapCanvas(data=self.data)
        img = canvas.output()
        if path is not None:
            img.save(path)
        return img

    def add_floor(self, pos, color):
        "add a floor into data (but do not generate it on map img)"
        if isinstance(pos, (tuple, str)):
            pos = gridcls.Pos(pos)
        color_id = self._get_color_id_from_str(color)
        floor_node = gridcls.Node.Floor(pos, color_id)
        self.data["<floor>"].set_on_pos(pos, floor_node)

    def add_item(self, pos_, marker, color, name):
        "add an item into data"
        pos = gridcls.Pos(pos_)
        if marker in global_const.RESOURCE_STAMP_TYPE:
            stamp_id = global_const.RESOURCE_STAMP_TYPE.index(marker)
        elif marker.isdecimal():
            stamp_id = int(marker)
        else:
            raise TypeError(marker)
        color_id = self._get_color_id_from_str(color)
        item_id = len(self.data["<item>"].data) + 1
        item_node = gridcls.Node.Item(
            id=item_id, name=name, color=color_id, type=stamp_id, pos=pos
        )
        self.data["<item>"].set_on_pos(pos, item_node)

    def add_player(self, pos_, marker, color, name, user_id):
        "add a player into data"
        pos = gridcls.Pos(pos_)
        if marker in global_const.RESOURCE_STAMP_TYPE:
            stamp_id = global_const.RESOURCE_STAMP_TYPE.index(marker)
        elif marker.isdecimal():
            stamp_id = int(marker)
        else:
            raise TypeError(marker)
        color_id = self._get_color_id_from_str(color)
        item_id = len(self.data["<player>"].data) + 1
        item_node = gridcls.Node.Player(
            id=item_id, name=name, color=color_id, type=stamp_id, pos=pos,
            uid=user_id
        )
        self.data["<player>"].set_on_pos(pos, item_node)

    def add_color(self, color):
        "add color into data (can be existing ones), return index of it"
        color_id = self._get_color_id_from_str(color)
        return color_id

    def _get_color_id_from_str(self, color):
        if not isinstance(color, gridcls.Node.Color):
            if not isinstance(color, str):
                raise TypeError(color)
            # color_id = None
            if color.isdecimal():
                color_id = int(color)
            elif color.startswith("#"):
                if color in self.data["<color>"]:
                    color_id = self.data["<color>"].index(color)
                else:
                    color_id = self.data["<color>"].add_color(color)
            else:
                raise Exception("input error", color)
        else:
            if color in self.data["<color>"].data:
                color_id = self.data["<color>"].index(color=color.color)
            else:
                self.data["<color>"].data.append(color)
                color_id = len(self.data["<color>"].data) - 1
        return color_id
