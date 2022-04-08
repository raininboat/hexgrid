# HEXGRID - A hexagon map editor on command line
[![Pylint](https://github.com/raininboat/hexgrid/actions/workflows/pylint.yml/badge.svg?branch=master)](https://github.com/raininboat/hexgrid/actions/workflows/pylint.yml)
========

This is a test version of `hexgrid` with a lot of features unfinished

![hexagon map preview](./sample/sample_grid.jpg)

# CURRENT STATUS
this map editor is based on command line, and can be used on both `Windows` and `Linux`.

commands are listed as follows:

| command | description |
| ------- | ----------- |
| `new` | create a new map |
| `load` | load a `*.hgdata` [map save file](./sample/save.hgdata) |
| `show` | list the data of the current map |
| `add` | add something on the map |
| `preview` | show the current preview (require gui) |
| `save` | save the map data file `*.hgdata` |
| `render` | render the map, export `*.jpg` or `*.png` |
| `clear` | clear all the data loaded |

*use `help <command>` in termianl to see syntax*

# LICENSE
Licensed under Apache License
~~~
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
~~~
