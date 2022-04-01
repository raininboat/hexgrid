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
from hexgrid.global_const import TERMCOLOR as COLOR

__escape_list = [
    ("&", "&#38;"),
    ("|", "&#124;")
]


def escape(txt: str):
    "use it to save map files"
    this_list = __escape_list.copy()    # shallow copy
    for i, j in this_list:
        txt = txt.replace(i, j)
    return txt


def unescape(txt: str):
    "use it to load map files"
    this_list = __escape_list.copy()    # shallow copy
    this_list.reverse()
    for i, j in this_list:
        txt = txt.replace(j, i)
    return txt


def set_color(color, text) -> str:
    "set text color for terminal output"
    return f"{color}{text}{COLOR.DEFAULT}"
