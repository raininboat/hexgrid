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

# all the global constants
# the global default config of single hexagon
PX_RATIO = 0.866    # sqrt(3)/2     y/x
PX_R = 28           # hexagon radius

# the sesource stamp file path
RESOURCE_STAMP_TYPE = [
    "./res/stamp/add_{color:d}.png",
    "./res/stamp/circle_{color:d}.png",
    "./res/stamp/crosscircle_{color:d}.png",
    "./res/stamp/heart_{color:d}.png",
    "./res/stamp/multiply_{color:d}.png",
    "./res/stamp/square_{color:d}.png",
    "./res/stamp/star_{color:d}.png",
    "./res/stamp/triangle_{color:d}.png"
]

# the font in the map
FONT_TITLE_PATH = r"./res/font/Ubuntu-B.ttf"
FONT_DESC_PATH = r"./res/font/Ubuntu-L.ttf"


# the unix terminal word color
class TERMCOLOR:
    "terminal color"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    DEFAULT = "\033[0m"
