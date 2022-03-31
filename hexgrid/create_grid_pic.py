import hexgrid
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageChops
import timeit


class MapCanvas(object):
    def __init__(self, data: hexgrid.gridcls.Grid):
        self.grid_data = data
        self.image = Image.new(
            mode="RGBA", size=self.grid_data.cfg.size,
            color=(255, 255, 255, 255))
        self._font_title = ImageFont.truetype(
            hexgrid.global_const.FONT_TITLE_PATH, size=8)
        self._draw = ImageDraw.Draw(self.image, mode="RGBA")

    def draw_single_hex_floor(self, pos: hexgrid.gridcls.Pos, color):
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
                x = hexgrid.gridcls.Pos(i, v)
                self._draw.line(x.point_list_around(),
                                fill=(0, 0, 0, 255), width=1)
                txt = x.show_pos
                t_p = x.coord_text_cood()
                self._draw.text(t_p, text=txt, fill=(
                    0, 0, 0, 255), font=self._font_title, anchor="ma")

    def draw_single_stamp(self, stamp_type, stamp_color_id, pos,
                         text=None, mask_alpha=None):
        stm = load_stamp(
            stamp_type,
            stamp_color_id
        ).resize(
                (int((1.5 - hexgrid.global_const.PX_RATIO) *
                     hexgrid.global_const.PX_R * 2),
                 int((1.5 - hexgrid.global_const.PX_RATIO) *
                     hexgrid.global_const.PX_R * 2))
        )
        paste_bbox = pos.image_paste_box(image=stm)
        a = stm.getchannel("A")
        if mask_alpha is None:
            mask_alpha = 0x7d
        mask_t = Image.new("L", a.size, color=mask_alpha)
        mask = ImageChops.darker(a, mask_t)  # 整体透明度增加
        self.image.paste(stm, box=paste_bbox, mask=mask)
        mask.close()
        stm.close()
        if text is not None:
            self._draw.text(pos.px, text=text[0], font=self._font_title,
                            anchor="mm", fill=text[1])

    def _draw_items(self):
        for item in self.grid_data.map_dict["<item>"].values():
            stamp_type = item.type
            stamp_color_id = item.color
            pos = item.pos
            text = "i-{0}".format(item.id)
            self.draw_single_stamp(
                stamp_type=stamp_type, stamp_color_id=stamp_color_id,
                pos=pos, text=(text, (0x7d, 0, 0, 0xff)))

    def _draw_players(self):
        for item in self.grid_data.map_dict["<player>"].values():
            stamp_type = item.type
            stamp_color_id = item.color
            pos = item.pos
            text = "p-{0}".format(item.id)
            self.draw_single_stamp(
                stamp_type=stamp_type, stamp_color_id=stamp_color_id,
                pos=pos, text=(text, (0, 0, 0x7d, 0xff)), mask_alpha=0xff)

    # @timeit.Timer
    def craete_map(self, save_path=None):
        self._draw_floors()
        self._draw_map_grid()
        self._draw_items()
        self._draw_players()
        if save_path is None:
            save_path = "./tmp/tmp_map.png"
        self.image.save(save_path)

    def __del__(self):
        self.image.close()


def load_stamp(stamp_type, stamp_color_id):
    path = hexgrid.global_const.RESOURCE_STAMP_TYPE[stamp_type].format(
        color=int(stamp_color_id))
    stm = Image.open(path)
    return stm


if __name__ == "__main__":
    path = "./sample/save.hgdata"
    file = hexgrid.loadmap.load_file(path)
    a = MapCanvas(file)
    a.craete_map()
