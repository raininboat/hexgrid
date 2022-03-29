import hexgrid
from PIL import Image, ImageDraw, ImageFont, ImageColor


class MapCanvas(object):
    def __init__(self, data: hexgrid.gridcls.Grid):
        self.grid_data = data
        self.image = Image.new(
            mode="RGBA", size=self.grid_data.cfg.size, color=(255, 255, 255, 255))
        self._font = ImageFont.truetype(hexgrid.global_const.FONT_PATH,size=8)
        self._draw = ImageDraw.Draw(self.image)

    def draw_single_hex_floor(self, pos:hexgrid.gridcls.Pos, color):
        points = pos.point_list_around()
        self._draw.polygon(points,fill=ImageColor.getrgb(color))

    def _draw_floors(self):
        for v in self.grid_data.map_dict["<floor>"].values():
            pos = v.pos
            color_id = int(v.color)
            color = self.grid_data.color[color_id].color
            self.draw_single_hex_floor(pos, color)

    def _draw_map_grid(self):
        for i in range(self.grid_data.cfg.x_max + 1):
            for v in range(self.grid_data.cfg.y_max):
                x = hexgrid.gridcls.Pos(i, v)
                print(x.pos_tuple, x.show_pos)
                # print(x.point_list_around())
                self._draw.line(x.point_list_around(), fill=(0, 0, 0, 255), width=1)
                txt = x.show_pos
                t_p = x.coord_text_cood()
                self._draw.text(t_p, text=txt, fill=(0, 0, 0, 255), font=self._font, anchor="ma")

    def draw_single_item(self,item:hexgrid.loadmap.MapSave_item):
        pass

    def _draw_items(self):
        pass

    def draw_single_player(self, player:hexgrid.loadmap.MapSave_player):
        pass

    def _draw_players(self):
        pass

    def craete_map(self, save_path=None):
        self._draw_floors()
        self._draw_map_grid()
        self._draw_items()
        self._draw_players()
        if save_path is None:
            save_path = "./tmp/tmp_map.png"
        self.image.save(save_path)


if __name__ == "__main__":
    path = "./sample/save.hgdata"
    file = hexgrid.loadmap.load_file(path)
    a = MapCanvas(file)
    a.craete_map()
