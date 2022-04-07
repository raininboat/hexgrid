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
from . import global_const

# from .global_const import TERMCOLOR as COLOR

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
    return f"{color}{text}{global_const.TERMCOLOR.DEFAULT}"


class LogCls:
    "the local diagnose api cls"

    def __init__(self, fmt=None, setlevel=0) -> None:
        if fmt is None:
            fmt = "{color}[{lvl}]: {message}{default_color}"
        self._fmt = fmt
        self._setlevel = setlevel

    @classmethod
    def log(cls, *args, level, msg, fmt=None, setlevel=0, **kwargs):
        "print the log"
        if fmt is None:
            fmt = "{color}[{lvl}]: {message}{default_color}"
        if level < setlevel:
            return
        if level >= 50:
            lvl = "CRITICAL"
            color = global_const.TERMCOLOR.RED
        elif level >= 40:
            lvl = "WARNING"
            color = global_const.TERMCOLOR.PURPLE
        elif level >= 30:
            lvl = "ERROR"
            color = global_const.TERMCOLOR.YELLOW
        elif level >= 20:
            lvl = "INFO"
            color = global_const.TERMCOLOR.CYAN
        elif level >= 10:
            lvl = "DEBUG"
            color = global_const.TERMCOLOR.GREEN
        else:
            lvl = "UNKNOWN"
            color = global_const.TERMCOLOR.DEFAULT

        # print(msg, args, )
        text = str(msg).format(*args, **kwargs)
        output_string = fmt.format(
            color=color, lvl=lvl, message=text,
            default_color=global_const.TERMCOLOR.DEFAULT
        )
        print(output_string)

    def debug(self, msg, *args, **kwargs):
        "print log in debug lvl"
        self.log(
            level=10, msg=msg, fmt=self._fmt,
            setlevel=self._setlevel, *args, **kwargs
        )

    def info(self, msg, *args, **kwargs):
        "print log in info lvl"
        self.log(
            level=20, msg=msg, fmt=self._fmt,
            setlevel=self._setlevel, *args, **kwargs
        )

    def error(self, msg, *args, **kwargs):
        "print log in error lvl"
        self.log(
            level=30, msg=msg, fmt=self._fmt,
            setlevel=self._setlevel, *args, **kwargs
        )

    def warning(self, msg, *args, **kwargs):
        "print log in warning lvl"
        self.log(
            level=40, msg=msg, fmt=self._fmt,
            setlevel=self._setlevel, *args, **kwargs
        )

    def critical(self, msg, *args, **kwargs):
        "print log in critical lvl"
        self.log(
            level=50, msg=msg, fmt=self._fmt,
            setlevel=self._setlevel, *args, **kwargs
        )
