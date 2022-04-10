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

import math

import numpy

""" NOTE:
reference: https://www.redblobgames.com/grids/hexagons


1、将六角格地图从便于人类阅读的 offset coordinate（A1） 转化为向量坐标
    坐标均根据六角格中心计算
    对于原点坐标 当 x 为奇数时
    u = x
    v = 

2、向量坐标系定义
    basis vector u, v 分别为 4点钟方向和 6点钟方向 1格
    则于正交坐标系(y轴正方向朝下方，由于图片原点在左上)的转化为
    u = (sqrt(3)/2, -1/2)
    v = (0, -1)

3、和笛卡尔坐标系的映射关系
"""

class OffsetCoordinate:
    def __init__(self, offset_x, offset_y):
        self.offset_x = offset_x
        self.offset_y = offset_y

    def str_x(self):
        "the text version of _x coordinate"
        if self.offset_x <= 0:
            return ""
        x_lst = []
        tmp_x = self.offset_x
        for _ in range(int(math.log(self.offset_x, 26))+1):
            # calculate the text for offset_x (>ABC< 9)
            # a 26 based interger
            tmp_x, this = divmod(tmp_x, 26)
            x_lst.append(this + 0x40)   # 1 => A 0x41
        x_lst.reverse()         # list in long devide is from lowest to highest
        x_ascii = bytes(x_lst.__iter__())
        return x_ascii.decode(encoding="utf-8")

class MapRowAbs:
    def __init__(self):
        self.data = []


class MapAllContainer:
    """the container of all the hexagon grids, can use
        self[col][row] to get the target data
        also can use self.get_offset(), self.get_axis() to get the node
    """
    def __init__(self, max_x, max_y):
        "create a rectangle map grids"
        self.max_x = max_x
        self.max_y = max_y
        self.data = []

    def init_map(self):
        for i in range(self.max_y):
            
            self.data.append()



if __name__ == "__main__":
    print(OffsetCoordinate(28,1).str_x())
