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

import cmd
import platform
import time

from objprint import op

from . import (__version__, create_grid_pic, global_const, gridcls, loadmap,
               misc)

system = platform.system()
FLAG_GUI: bool = False
if system in ("Windows", "Darwin"):     # windows and mac os
    FLAG_GUI = True
    from tkinter import Tk, colorchooser, filedialog
else:
    misc.LogCls.log(system, level=40, msg="""GUI module (tkinter) not \
available in this platform. Platform name: [{0}]""")


class MapEditInterface(cmd.Cmd):
    "The Command Line User Interface of Hexgrid"
    intro = f"""{global_const.TERMCOLOR.GREEN}\
Welcome to Map Editor of hexgrid V{__version__}{global_const.TERMCOLOR.DEFAULT}
This is a terminal based interface of map editor
Use 'help' to see help ...\
"""
    prompt = "\033[32mhexgrid \033[0m> "

    def __init__(self, completekey=None, stdin=None, stdout=None) -> None:
        super().__init__(completekey, stdin, stdout)
        self.data = None
        self.mapcanvas = None
        self.log = misc.LogCls()

    def emptyline(self):
        return False

    def do_load(self, arg: str):
        "load [path]|'tk'"
        # print(arg.split())
        arg_lst = arg.split()
        if self.data is not None:
            self.do_clear(None)
        path: str = None
        if not arg_lst or "-tk" in arg_lst:
            if FLAG_GUI:
                root = Tk()
                root.withdraw()
                # root.
                root.wm_attributes('-topmost', 1)
                path = filedialog.askopenfilename(initialdir=".", filetypes=[(
                    "hexgrid save file", ".hgdata"), ("all files", ".*")],
                    parent=root, title="select hex grid save file")
                root.destroy()
            else:
                self.log.info("Cannot find module 'tkinter', input path by \
terminal line instead")
                path = input(f"""hexmap file (*.hgdata) path: \
{global_const.TERMCOLOR.DEFAULT}""")
        else:
            path = arg
        if path == "":
            self.log.info("cancelled")
            return False
        self.log.info("- load start -")
        _t = time.time()
        self.data = loadmap.load_file(path)
        self.mapcanvas = create_grid_pic.MapCanvas(self.data)
        self.log.info("time used: {0}", time.time() - _t)
        # color_print(f"time used - {time.time()-_t}", lvl=2)
        return False

    def do_show(self, args: str):
        "show map configs\nshow (default: set)| color | floor | item | player"
        if self.data is None:
            self.log.error("please load the map first")
            return
        arg_list = args.split()
        if not arg_list or arg_list[0] == "set":
            data = self.data["<set>"].data[0]
            ret = f"""HEXGRID Map Data
name:{data.name}, x_max:{data.x_max}, y_max:{data.y_max}"""
            self.log.info(ret)
            return
        if arg_list[0] == "color":
            data_list = self.data["<color>"].data
            tmp_reply_lst = []
            for i, j in enumerate(data_list):
                tmp_reply_lst.append(f"{i}: \t{j.color}")
            self.log.info("map data color list:\n" + "\n".join(tmp_reply_lst))
            return
        if arg_list[0] == "floor":
            data_list = self.data["<floor>"].data
            tmp_reply_lst = []
            for floor in data_list:
                tmp_reply_lst.append(f"{floor.pos.show_pos}: \t\
color-{floor.color}")
            self.log.info("map data floor list:\n" + "\n".join(tmp_reply_lst))
            return
        if arg_list[0] == "item":
            data_list = self.data["<item>"].data
            tmp_reply_lst = []
            for item in data_list:
                tmp_reply_lst.append(f"{item.pos.show_pos}: \t\
id-{item.id}, name-{item.name}, color-{item.color}, type-{item.type}")
            self.log.info("map data item list:\n" + "\n".join(tmp_reply_lst))
            return
        if arg_list[0] == "player":
            data_list = self.data["<player>"].data
            tmp_reply_lst = []
            for player in data_list:
                tmp_reply_lst.append(f"{player.pos.show_pos}: \t\
id-{player.id}, name-{player.name}, uid:{player.uid}, color-{player.color}, \
type-{player.type}")
            self.log.info("map data player list:\n" + "\n".join(tmp_reply_lst))
            return

    def do_status(self, *args):
        "return status"
        op(self.data, args)

    def do_clear(self, _):
        if self.data is not None:
            self.data = None
        if self.mapcanvas is None:
            # self.log.debug("map unload")
            return
        if not self.mapcanvas.map_created:
            self.mapcanvas = None
        else:
            self.mapcanvas.image.close()
        self.log.info("map cleared")

    def do_preview(self, *_):
        "preview the hexmap picture"
        if self.mapcanvas is not None:
            self.log.info("- preview start -")
            _t = time.time()
            if not self.mapcanvas.map_created:
                self.mapcanvas.craete_map()
            img = self.mapcanvas.output()
            # img.show()
            self.log.info(f"time used: {time.time() - _t}")
            # img.show()
            self.mapcanvas.image.show()
            img.close()
            # self.mapcanvas.image.show("image preview")
        else:
            self.log.error("please (load) file first")

    def do_add(self, raw_arg: str):
        """\
添加元素
add [type <'item'|'floor'|'player'>] [Pos: str "A0"] ...
    item : add item A0 [marker_type "star"] [color_id 0~7] [name: abc]
    player: add player A0 [marker_type] [color_id] [user_id] [pc_name]
    floor: add floor A0 [color id | hex #rgb]
"""
        arg = raw_arg.split()
        if arg[0] == "floor":
            if len(arg) < 3:
                self.log.error("Input ERROR")
                self.do_help("add")
                return
            pos = gridcls.Pos(pos=arg[1])
            color_raw = arg[2]
            color_id = None
            if color_raw.startswith("#"):
                if color_raw in self.data["<color>"]:
                    color_id = self.data["<color>"].index(color_raw)
                else:
                    color_id = self.data["<color>"].add_color(color_raw)
            elif color_raw.isalnum():
                color_id = int(color_raw)
            floor_elem = gridcls.Node.Floor(pos, color_id)
            self.data["<floor>"][pos] = floor_elem
            self.mapcanvas.draw_single_hex_floor(
                pos, self.data["<color>"][color_id]
            )

        # TODO
        elif arg[0] == "color":
            if len(arg) == 1 or "--tk" in arg:
                root = Tk()
                root.withdraw()
                color, string = colorchooser.askcolor("#FF0000")
                self.log.debug("color choosed - {0}: {1}", string, color)

    def do_save(self, arg: str):
        "save the map file"
        arg_lst = arg.split()
        if "--path" in arg_lst:
            path_index = arg_lst.index("--path")
            path = arg_lst[path_index + 1]
        else:
            if FLAG_GUI:
                root = Tk()
                root.withdraw()
                root.wm_attributes('-topmost', 1)
                path = filedialog.asksaveasfilename(initialdir=".", filetypes=[
                    ("hexgrid data file", ".hgdata"), ("all files", ".*")],
                    parent=root, title="select hex grid save file",
                    defaultextension='.hgdata')
                print(path)
                root.destroy()
            else:
                self.log.info("Cannot find module 'tkinter', input path by \
terminal line instead")
                path = input(f"""hexmap file (*.hgdata) path: \
{global_const.TERMCOLOR.DEFAULT}""")
        if path == "":
            self.log.info("cancelled")
            return
        self.data.save(path)

    def do_render(self, arg: str):
        "render the map picture (.png) and save it"
        arg_lst = arg.split()
        if "--path" in arg_lst:
            path_index = arg_lst.index("--path")
            path = arg_lst[path_index + 1]
        else:
            if FLAG_GUI:
                root = Tk()
                root.withdraw()
                # root.
                root.wm_attributes('-topmost', 1)
                path = filedialog.asksaveasfilename(
                    initialdir=".",
                    filetypes=[("jpg file", ".jpg"), ("png file", ".png"),
                               ("all files", ".*"), ],
                    parent=root, title="select hex grid save file",
                    defaultextension=".png")
                print(path)
                root.destroy()
            else:
                print(f"""{global_const.TERMCOLOR.YELLOW}Cannot find module \
'tkinter', input path by terminal line instead""")
                path = input(f"""hexmap file (*.hgdata) path: \
{global_const.TERMCOLOR.DEFAULT}""")
        if path == "":
            self.log.info("cancelled")
            return
        self.log.info("- render start -")
        _t = time.time()
        if not self.mapcanvas.map_created:
            self.mapcanvas.craete_map()
        if "--raw" in arg_lst:
            img = self.mapcanvas.image.convert("RGB")
            img.save(path)
            img.close()
        else:
            img = self.mapcanvas.output()
            img.save(path)
            img.close()
        self.log.info(f"time used - {time.time()-_t}")

    @classmethod
    def do_exit(cls, *_):
        "exit the terminal"
        return True


if __name__ == "__main__":
    a = MapEditInterface()
    a.cmdloop()
