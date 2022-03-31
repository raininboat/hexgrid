import cmd
from tkinter import filedialog, Tk, colorchooser
import hexgrid
from objprint import op
import time

class MapEditInterface(cmd.Cmd):
    intro = """\
Welcome to Map Editor of hexgrid V0.1(DEMO Version)
This is a terminal based interface of map editor
Use '.help' to see help ...
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
        if len(arg) == 0 or arg == "tk":
            rt = Tk()
            rt.withdraw()
            # rt.
            rt.wm_attributes('-topmost', 1)
            path = filedialog.askopenfilename(initialdir=".", filetypes=[(
                "hexgrid save file", ".hgdata"), ("all files", ".*")],
                parent=rt, title="select hex grid save file")
            rt.destroy()
        else:
            path = arg
        if path == "":
            color_print("cancelled", lvl=1)
            return False
        color_print("- start -",lvl=2)
        t = time.time()
        self.data = hexgrid.loadmap.load_file(path)
        self.mapcanvas = hexgrid.create_grid_pic.MapCanvas(self.data)
        self.mapcanvas.craete_map()
        color_print("time used - {0}".format(time.time()-t),lvl=2)
        return False

    def do_status(self, arg: str):
        op(self.data)

    def do_show(self, arg: str):
        pass

    def do_preview(self, arg: str):
        if self.mapcanvas is not None:
            color_print("- start -",lvl=2)
            t = time.time()
            preview = self.mapcanvas.image.copy()
            size = self.mapcanvas.image.size
            preview.resize((int(size[0]/1.5), int(size[1]/1.5)),1)
            preview.show()
            color_print("time used - {0}".format(time.time()-t),lvl=2)

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
                return False
            pos = hexgrid.gridcls.Pos(pos=arg[1])
            color_raw = arg[2]
            color_id = None
            if color_raw.startswith("#"):
                if color_raw in self.data.color:
                    color_id = self.data.color.index(color_raw)
                else:
                    color_id = self.data.color.add_color(color_raw)
            elif color_raw.isalnum():
                color_id = int(color_raw)
            a = hexgrid.loadmap.MapSave_floor.MapSave_row()
            self.data.map_dict["<floor>"][pos]
            # self.data.color.append(hexgrid.loadmap.MapSave_color.MapSave_row([color_raw]))

    def do_save(self, arg: str):
        arg_lst = arg.split()
        if len(arg_lst) == 0 or arg_lst[0] == "tk":
            rt = Tk()
            rt.withdraw()
            # rt.
            rt.wm_attributes('-topmost', 1)
            path = filedialog.asksaveasfilename(initialdir=".", filetypes=[(
                "hexgrid data file", ".hgdata"), ("all files", ".*")],
                parent=rt, title="select hex grid save file",
                defaultextension='.hgdata')
            print(path)
            rt.destroy()

    def do_render(self, arg: str):
        arg_lst = arg.split()
        if len(arg_lst) == 0 or arg_lst[0] == "tk":
            rt = Tk()
            rt.withdraw()
            # rt.
            rt.wm_attributes('-topmost', 1)
            path = filedialog.asksaveasfilename(initialdir=".", filetypes=[(
                "png file", ".png"), ("all files", ".*")],
                parent=rt, title="select hex grid save file",
                defaultextension=".png")
            print(path)
            rt.destroy()
        else:
            pass
        pass
        color_print("- start -",lvl=2)
        t = time.time()
        self.mapcanvas.image.save(path)
        color_print("time used - {0}".format(time.time()-t),lvl=2)

    def do_exit(self, arg: str):
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
    tc = hexgrid.global_const.TERMCOLOR
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
