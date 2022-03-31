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
