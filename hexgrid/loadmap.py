import re
import hexgrid

Node = hexgrid.gridcls.Node
unescape = hexgrid.misc.unescape


class MapSaveClsTamplate(object):
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
        return self.MapSave_row(this_line_list)

    def get_line_save(self):
        return self.MapSave_iter(self, needTag=True)

    def __iter__(self):
        return self.MapSave_iter(self, needTag=False)

    class MapSave_row(hexgrid.gridcls.MapGridElement_tamplate):
        "basic_tamplate"

    class MapSave_iter(object):
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


class MapSave_color(MapSaveClsTamplate):
    def __init__(self):
        super().__init__("<color>")

    def has_color(self, strrgb):
        if strrgb in self.data:
            return True
        else:
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
        else:
            self.feed_line(strrgb)
            return self.index(strrgb)

    def index(self, strrgb):
        if self.has_color(strrgb):
            return self.data.index(strrgb)
        else:
            return None

    class MapSave_row(Node.color):
        def __init__(self, row_data_list):
            self.color = row_data_list[0]


class MapSave_floor(MapSaveClsTamplate):
    def __init__(self):
        super().__init__("<floor>")

    class MapSave_row(Node.floor):
        def __init__(self, row_data_list):
            self.pos = hexgrid.gridcls.Pos(row_data_list[0])
            self.color = row_data_list[1]


class MapSave_set(MapSaveClsTamplate):
    def __init__(self):
        super().__init__("<set>")

    class MapSave_row(Node.set):
        def __init__(self, row_data_list):
            self.x_max = int(row_data_list[0])
            self.y_max = int(row_data_list[1])
            self.r = int(row_data_list[2])      # TODO: 存档六角格半径可变
            self.name = row_data_list[3]


class MapSave_item(MapSaveClsTamplate):
    def __init__(self):
        super().__init__(tag="<item>")

    class MapSave_row(Node.item):
        def __init__(self, row_data_list):
            self.id = row_data_list[0]
            self.name = row_data_list[1]
            self.color = int(row_data_list[2])
            self.type = int(row_data_list[3])
            self.pos = hexgrid.gridcls.Pos(pos=row_data_list[4])


class MapSave_user(MapSaveClsTamplate):
    def __init__(self):
        super().__init__(tag="<user>")

    class MapSave_row(Node.user):
        def __init__(self, row_data_list):
            self.uid = row_data_list[0]
            self.hash = row_data_list[1]


class MapSave_player(MapSaveClsTamplate):
    def __init__(self):
        super().__init__(tag="<player>")

    class MapSave_row(Node.player):
        def __init__(self, row_data_list):
            self.id = row_data_list[0]
            self.name = row_data_list[1]
            self.uid = row_data_list[2]
            self.color = int(row_data_list[3])
            self.type = int(row_data_list[4])
            self.pos = hexgrid.gridcls.Pos(pos=row_data_list[5])


__tag_class = {
    "<unknown>": MapSaveClsTamplate,
    "<set>": MapSave_set,
    "<item>": MapSave_item,
    "<user>": MapSave_user,
    "<player>": MapSave_player,
    "<color>": MapSave_color,
    "<floor>": MapSave_floor
}


def load_file(path, encode="utf-8"):
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
    grid = hexgrid.gridcls.Grid(ret)
    return grid


if __name__ == "__main__":
    path = "./sample/save.hgdata"
    file = load_file(path)
    print(file)
    # print("\n".join(file["<set>"].get_line_save()))
