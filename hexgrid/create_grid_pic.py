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

from os.path import isfile
from typing import overload

from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFont

from . import global_const, gridcls


class MapCanvas:
    "the total canvas class"

    def __init__(self, data: gridcls.Grid):
        self.grid_data = data
        self.map_created = False    # lazy create
        self.image = Image.new(
            mode="RGBA", size=self.grid_data["<set>"].size,
            color=(255, 255, 255, 255))
        self._font_title = ImageFont.truetype(
            global_const.FONT_TITLE_PATH, size=global_const.FONT_TITLE_SIZE)
        self._draw = ImageDraw.Draw(self.image, mode="RGBA")

    @overload
    def draw_single_hex_floor(self, node: gridcls.Node.Floor): ...

    @overload
    def draw_single_hex_floor(self, pos: gridcls.Pos, color): ...

    def draw_single_hex_floor(self, *args, **kwargs):
        "draw the single floor (fill the target hexagon grid)"
        if len(args) == 1:
            if isinstance(args[0], gridcls.Node.Floor):
                color_id = args[0].color
                color = self.grid_data["<color>"].get_color(color_id)
                self.__draw_single_hex_floor(
                    pos=args[0].pos, color=color
                )
            else:
                raise TypeError(args, gridcls.Node.Floor)
        elif len(args) == 2:
            self.__draw_single_hex_floor(pos=args[0], color=args[1])
        elif "node" in kwargs:
            node = kwargs["node"]
            if isinstance(node, gridcls.Node.Floor):
                color_id = node.color
                color = self.grid_data["<color>"].get_color(color_id)
                self.__draw_single_hex_floor(
                    pos=node.pos, color=color
                )
            else:
                raise TypeError(node, gridcls.Node.Floor)
        elif "pos" in kwargs and "color" in kwargs:
            self.__draw_single_hex_floor(
                pos=kwargs["pos"], color=kwargs["color"]
            )
        else:
            raise TypeError()

    def __draw_single_hex_floor(self, pos, color):
        if not self.map_created:
            self.craete_map()
        points = pos.point_list_around()
        color_t = ImageColor.getrgb(color)
        self._draw.polygon(points, fill=color_t,
                           outline=(0, 0, 0, 255), width=1)

    def _draw_floors(self):
        for i in self.grid_data["<floor>"].get_data_iter():
            pos = i.pos
            color_id = int(i.color)
            color = self.grid_data["<color>"].get_color(color_id)
            # print(pos, color)
            self.__draw_single_hex_floor(pos=pos, color=color)

    def draw_single_grid(self, pos: gridcls.Pos):
        "draw the outlines of the hexagon and print the pos title"
        self._draw.line(pos.point_list_around(),
                        fill=(0, 0, 0, 255), width=1)
        txt = pos.show_pos
        t_p = pos.coord_text_cood()
        self._draw.text(t_p, text=txt, fill=(
            0, 0, 0, 255), font=self._font_title, anchor="ma")

    def _draw_map_grid(self):
        for i in range(self.grid_data["<set>"].x_max + 1):
            for j in range(1, self.grid_data["<set>"].y_max + 1):
                x = gridcls.Pos(i, j)
                self.draw_single_grid(pos=x)

    def draw_single_stamp(self, stamp_type, stamp_color_id, pos,
                          text=None, mask_alpha=None):
        "draw a single stamp (item or player) on the map"
        # TODO: use google icons
        if not self.map_created:
            self.craete_map()
        stm = load_stamp(
            stamp_type, stamp_color_id
        ).resize(
            (int((1.5 - global_const.PX_RATIO) * global_const.PX_R * 2),
             int((1.5 - global_const.PX_RATIO) * global_const.PX_R * 2))
        )
        paste_bbox = pos.image_paste_box()
        alpha = stm.getchannel("A")
        if mask_alpha is None:
            mask_alpha = 0x7d
        mask_t = Image.new("L", alpha.size, color=mask_alpha)
        mask = ImageChops.darker(alpha, mask_t)  # 整体透明度增加
        self.image.paste(stm, box=paste_bbox, mask=mask)
        mask.close()
        stm.close()
        if text is not None:
            self._draw.text(pos.xy_abs, text=text[0], font=self._font_title,
                            anchor="mm", fill=text[1])

    def draw_single_item(self, item):
        "draw the single item marker on the map from node obj"
        stamp_type = item.type
        stamp_color_id = item.color
        pos = item.pos
        text = f"i-{item.id}"
        self.draw_single_stamp(
            stamp_type=stamp_type, stamp_color_id=stamp_color_id,
            pos=pos, text=(text, (0xff, 0xff, 0xff, 0xff)))

    def _draw_items(self):
        for item in self.grid_data["<item>"].get_data_iter():
            self.draw_single_item(item)
            # stamp_type = item.type
            # stamp_color_id = item.color
            # pos = item.pos
            # text = f"i-{item.id}"
            # self.draw_single_stamp(
            #     stamp_type=stamp_type, stamp_color_id=stamp_color_id,
            #     pos=pos, text=(text, (0xff, 0xff, 0xff, 0xff)))

    def draw_single_player(self, player):
        "draw the single player marker on the map from node obj"
        stamp_type = player.type
        stamp_color_id = player.color
        pos = player.pos
        text = f"p-{player.id}"
        self.draw_single_stamp(
            stamp_type=stamp_type, stamp_color_id=stamp_color_id,
            pos=pos, text=(text, (0xff, 0xff, 0xff, 0xff)),
            mask_alpha=0xff)

    def _draw_players(self):
        for item in self.grid_data["<player>"].get_data_iter():
            self.draw_single_player(item)

    # @timeit.Timer
    def craete_map(self):
        "draw the map according to the data"
        self.map_created = True
        self._draw_floors()
        self._draw_map_grid()
        self._draw_items()
        self._draw_players()

    def draw_from_pos_conf(self, pos_conf: gridcls.PosConf):
        "redraw a single hexagon grid"
        if pos_conf.floor:
            self.draw_single_hex_floor(node=pos_conf.floor)
        else:   # draw a white hexagon to clear the grid
            color = gridcls.Node.Color("#FFFFFF")
            self.draw_single_hex_floor(pos=pos_conf.pos, color=color)
        self.draw_single_grid(pos=pos_conf.pos)
        if pos_conf.item:
            self.draw_single_item(item=pos_conf.item)
        if pos_conf.player:
            self.draw_single_player(player=pos_conf.player)

    def output(self):
        "the resized version for output (save or preview)"
        if not self.map_created:
            self.craete_map()
        size = self.image.size
        img = self.image.resize((size[0]//2, size[1]//2), 1)
        img = img.convert("RGB")
        # im.resize((im.size[0]//2,im.size[1]//2),1)
        return img

    def __del__(self):
        self.image.close()


def load_stamp(stamp_type, stamp_color_id):
    "[WAITING FOR REFORM] load the stamp according to configures"
    path = global_const.RESOURCE_STAMP_PATH.format(
        type=global_const.RESOURCE_STAMP_TYPE[stamp_type],
        color=int(stamp_color_id)
    )
    if isfile(path):
        stm = Image.open(path)
        return stm
    return None
