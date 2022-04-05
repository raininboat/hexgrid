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

from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFont

from . import global_const, gridcls, loadmap


class MapCanvas:
    def __init__(self, data: gridcls.Grid):
        self.grid_data = data
        self.map_created = False    # lazy create
        self.image = Image.new(
            mode="RGBA", size=self.grid_data.cfg.size,
            color=(255, 255, 255, 255))
        self._font_title = ImageFont.truetype(
            global_const.FONT_TITLE_PATH, size=24)
        self._draw = ImageDraw.Draw(self.image, mode="RGBA")

    def draw_single_hex_floor(self, pos: gridcls.Pos, color):
        "draw the single floor (fill the target hexagon grid)"
        if not self.map_created:
            self.craete_map()
        points = pos.point_list_around()
        color_t = ImageColor.getrgb(color)
        self._draw.polygon(points, fill=color_t,
                           outline=(0, 0, 0, 255), width=1)

    def _draw_floors(self):
        for v in self.grid_data.map_dict["<floor>"].values():
            pos = v.pos
            color_id = int(v.color)
            color = self.grid_data.color.get_color(color_id)
            self.draw_single_hex_floor(pos, color)

    def _draw_map_grid(self):
        for i in range(self.grid_data.cfg.x_max + 1):
            for v in range(1, self.grid_data.cfg.y_max + 1):
                x = gridcls.Pos(i, v)
                self._draw.line(x.point_list_around(),
                                fill=(0, 0, 0, 255), width=1)
                txt = x.show_pos
                t_p = x.coord_text_cood()
                self._draw.text(t_p, text=txt, fill=(
                    0, 0, 0, 255), font=self._font_title, anchor="ma")

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

    def _draw_items(self):
        for item in self.grid_data.map_dict["<item>"].values():
            stamp_type = item.type
            stamp_color_id = item.color
            pos = item.pos
            text = f"i-{item.id}"
            self.draw_single_stamp(
                stamp_type=stamp_type, stamp_color_id=stamp_color_id,
                pos=pos, text=(text, (0x7d, 0, 0, 0xff)))

    def _draw_players(self):
        for item in self.grid_data.map_dict["<player>"].values():
            stamp_type = item.type
            stamp_color_id = item.color
            pos = item.pos
            text = f"p-{item.id}"
            self.draw_single_stamp(
                stamp_type=stamp_type, stamp_color_id=stamp_color_id,
                pos=pos, text=(text, (0, 0, 0x7d, 0xff)), mask_alpha=0xff)

    # @timeit.Timer
    def craete_map(self):
        "draw the map according to the data"
        self.map_created = True
        self._draw_floors()
        self._draw_map_grid()
        self._draw_items()
        self._draw_players()

    def output(self):
        "the resized version for output (save or preview)"
        size = self.image.size
        img = self.image.resize((size[0]//2,size[1]//2),1)
        img = img.convert("RGB")
        # im.resize((im.size[0]//2,im.size[1]//2),1)
        return img

    def __del__(self):
        self.image.close()


def load_stamp(stamp_type, stamp_color_id):
    path = global_const.RESOURCE_STAMP_TYPE[stamp_type].format(
        color=int(stamp_color_id))
    stm = Image.open(path)
    return stm


if __name__ == "__main__":
    test_path = "./sample/save.hgdata"
    file = loadmap.load_file(test_path)
    a = MapCanvas(file)
    a.craete_map()
