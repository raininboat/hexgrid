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
import time

from objprint import op

from . import __version__, create_grid_pic, global_const, gridcls, loadmap

flag_has_tk: bool = True
try:
    from tkinter import Tk, filedialog
except ImportError:
    flag_has_tk: bool = False


class MapEditInterface(cmd.Cmd):
    "The Command Line User Interface of Hexgrid"
    intro = f"""{global_const.TERMCOLOR.GREEN}\
Welcome to Map Editor of hexgrid V{__version__}{global_const.TERMCOLOR.DEFAULT}
This is a terminal based interface of map editor
Use 'help' to see help ...\
"""
    prompt = "\033[32mhexgrid \033[0m> "
    data = None
    mapcanvas = None

    def emptyline(self):
        return False

    def do_load(self, arg: str):
        "load [path]|'tk'"
        # print(arg.split())
        # args = arg.split()
        if self.data is not None:
            self.data = None
        path: str = None
        if len(arg) == 0 or arg == "tk":
            if flag_has_tk:
                root = Tk()
                root.withdraw()
                # root.
                root.wm_attributes('-topmost', 1)
                path = filedialog.askopenfilename(initialdir=".", filetypes=[(
                    "hexgrid save file", ".hgdata"), ("all files", ".*")],
                    parent=root, title="select hex grid save file")
                root.destroy()
            else:
                print(f"""{global_const.TERMCOLOR.YELLOW}Cannot find module \
'tkinter', input path by terminal line instead""")
                path = input("hexmap file (*.hgdata) path: ")
        else:
            path = arg
        if path == "":
            color_print("cancelled", lvl=1)
            return False
        color_print("- start -", lvl=2)
        _t = time.time()
        self.data = loadmap.load_file(path)
        self.mapcanvas = create_grid_pic.MapCanvas(self.data)
        self.mapcanvas.craete_map()
        color_print(f"time used - {time.time()-_t}", lvl=2)
        return False

    def do_status(self, *args):
        "return status"
        op(self.data, args)

    def do_preview(self, *_):
        "preview the hexmap picture"
        if self.mapcanvas is not None:
            color_print("- start -", lvl=2)
            _t = time.time()
            preview = self.mapcanvas.image.copy()
            size = self.mapcanvas.image.size
            preview.resize((int(size[0] / 1.5), int(size[1] / 1.5)), 1)
            preview.show()
            color_print(f"time used - {time.time() - _t}", lvl=2)

            # self.mapcanvas.image.show("image preview")
        else:
            color_print("please (load) file first", lvl=3)

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
                color_print("Input ERR", lvl=5)
                self.do_help("add")
                return
            pos = gridcls.Pos(pos=arg[1])
            color_raw = arg[2]
            color_id = None
            if color_raw.startswith("#"):
                if color_raw in self.data.color:
                    color_id = self.data.color.index(color_raw)
                else:
                    color_id = self.data.color.add_color(color_raw)
            elif color_raw.isalnum():
                color_id = int(color_raw)
            floor_elem = gridcls.Node.Floor(pos, color_id)
            self.data.map_dict["<floor>"][pos] = floor_elem
            self.mapcanvas.draw_single_hex_floor(pos,
                                                 self.data.color[color_id])
            # self.data.color.append(loadmap.MapSave_color.MapSave_row([color_raw]))

    def do_save(self, arg: str):
        "save the map file"
        arg_lst = arg.split()
        if len(arg_lst) == 0 or arg_lst[0] == "tk":
            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            path = filedialog.asksaveasfilename(initialdir=".", filetypes=[(
                "hexgrid data file", ".hgdata"), ("all files", ".*")],
                parent=root, title="select hex grid save file",
                defaultextension='.hgdata')
            print(path)
            root.destroy()
        else:
            path = arg
        self.data.save(path)

    def do_render(self, arg: str):
        "render the map picture (.png) and save it"
        arg_lst = arg.split()
        if len(arg_lst) == 0 or arg_lst[0] == "tk":
            root = Tk()
            root.withdraw()
            # root.
            root.wm_attributes('-topmost', 1)
            path = filedialog.asksaveasfilename(initialdir=".", filetypes=[(
                "png file", ".png"), ("all files", ".*")],
                parent=root, title="select hex grid save file",
                defaultextension=".png")
            print(path)
            root.destroy()
        else:
            path = arg
        color_print("- start -", lvl=2)
        _t = time.time()
        self.mapcanvas.image.save(path)
        color_print(f"time used - {time.time()-_t}", lvl=2)

    @classmethod
    def do_exit(cls, *_):
        "exit the terminal"
        return True


def color_print(text, lvl=None):
    """
    `default` -> `None`
    `green` -> 0
    `blue` -> 1
    `cyan` -> 2
    `yellow` -> 3
    `purple` -> 4
    `red` -> 5
    `white` -> -1
    """
    tc = global_const.TERMCOLOR
    if lvl is None:
        print(tc.DEFAULT, text, tc.DEFAULT)
    elif lvl == 0:
        print(tc.GREEN, text, tc.DEFAULT)
    elif lvl == 1:
        print(tc.BLUE, text, tc.DEFAULT)
    elif lvl == 2:
        print(tc.CYAN, text, tc.DEFAULT)
    elif lvl == 3:
        print(tc.YELLOW, text, tc.DEFAULT)
    elif lvl == 4:
        print(tc.PURPLE, text, tc.DEFAULT)
    elif lvl == 5:
        print(tc.RED, text, tc.DEFAULT)
    elif lvl == -1:
        print(tc.WHITE, text, tc.DEFAULT)
    else:
        print(tc.DEFAULT, text, tc.DEFAULT)


if __name__ == "__main__":
    a = MapEditInterface()
    a.cmdloop()
