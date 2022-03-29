import re
import hexgrid

__escape_list = [
    ("&", "&#38;"),
    ("|", "&#124;")
]


def escape(txt: str):
    this_list = __escape_list.copy()    # shallow copy
    for i, v in this_list:
        txt = txt.replace(i, v)
    return txt


def unescape(txt: str):
    this_list = __escape_list.copy()    # shallow copy
    this_list.reverse()
    for i, v in this_list:
        txt = txt.replace(v, i)
    return txt


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

    def _data_line(self, this_line_list):
        "override this to set data class"
        return self.MapSave_row(this_line_list)

    def get_line_save(self):
        return self.MapSave_iter(self, needTag=True)

    def __iter__(self):
        return self.MapSave_iter(self, needTag=False)

    class MapSave_row(object):
        def __init__(self, row_data_list):
            self.data = row_data_list

        def __iter__(self):
            return self.row_iter(self.data)

        class row_iter(object):
            def __init__(self, data_list):
                self.data = data_list
                self.index = 0

            def __iter__(self):
                return self

            def __next__(self):
                if self.index >= len(self.data):
                    raise StopIteration()
                tmp_data = str(self.data[self.index])
                self.index += 1
                return escape(tmp_data)

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

    class MapSave_row(MapSaveClsTamplate.MapSave_row):
        def __init__(self, row_data_list):
            self.id = int(row_data_list[0])
            self.color = row_data_list[1]

        def __iter__(self):
            return self.row_iter(
                [self.id, self.color]
            )


class MapSave_floor(MapSaveClsTamplate):
    def __init__(self):
        super().__init__("<floor>")

    class MapSave_row(MapSaveClsTamplate.MapSave_row):
        def __init__(self, row_data_list):
            self.pos = hexgrid.gridcls.Pos(row_data_list[0])
            self.color = row_data_list[1]

        def __iter__(self):
            return self.row_iter(
                [self.pos, self.color]
            )


class MapSave_set(MapSaveClsTamplate):
    def __init__(self):
        super().__init__("<set>")

    class MapSave_row(MapSaveClsTamplate.MapSave_row):
        def __init__(self, row_data_list):
            self.x_max = int(row_data_list[0])
            self.y_max = int(row_data_list[1])
            self.r = int(row_data_list[2])
            self.name = row_data_list[3]

        @property
        def size(self):
            x = hexgrid.global_const.PX_R * 1.5 * (self.x_max + 0.7)
            y = (hexgrid.global_const.PX_R * hexgrid.global_const.PX_RATIO
                 * self.y_max * 2
                 )
            return (int(x), int(y))

        def __iter__(self):
            return self.row_iter([self.x_max, self.y_max,
                                  self.r, self.name])


class MapSave_item(MapSaveClsTamplate):
    def __init__(self):
        super().__init__(tag="<item>")

    class MapSave_row(MapSaveClsTamplate.MapSave_row):
        def __init__(self, row_data_list):
            self.id = row_data_list[0]
            self.name = row_data_list[1]
            self.color = int(row_data_list[2])
            self.type = int(row_data_list[3])
            self.pos = hexgrid.gridcls.Pos(pos=row_data_list[4])

        @property
        def stamp_file_name(self):
            t = hexgrid.stamp_load.RESOURCE_STAMP_TYPE[self.type]
            c = self.color
            return t.format_map(color=c)

        def __iter__(self):
            return self.row_iter(
                [str(x) for x in (
                    self.id, self.name, self.color,
                    self.type, self.pos
                )]
            )


class MapSave_user(MapSaveClsTamplate):
    def __init__(self):
        super().__init__(tag="<user>")

    class MapSave_row(MapSaveClsTamplate.MapSave_row):
        def __init__(self, row_data_list):
            self.uid = row_data_list[0]
            self.hash = row_data_list[1]

        def __iter__(self):
            return self.row_iter([self.uid, self.hash])


class MapSave_player(MapSaveClsTamplate):
    def __init__(self):
        super().__init__(tag="<player>")

    class MapSave_row(MapSaveClsTamplate.MapSave_row):
        def __init__(self, row_data_list):
            self.id = row_data_list[0]
            self.name = row_data_list[1]
            self.uid = row_data_list[2]
            self.color = int(row_data_list[3])
            self.type = int(row_data_list[4])
            self.pos = hexgrid.gridcls.Pos(pos=row_data_list[5])

        @property
        def stamp_file_name(self):
            t = hexgrid.stamp_load.RESOURCE_STAMP_TYPE[self.type]
            c = self.color
            return t.format_map(color=c)

        def __iter__(self):
            return self.row_iter(
                [str(x) for x in (
                    self.id, self.name, self.uid,
                    self.color, self.type, self.pos
                )]
            )


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
