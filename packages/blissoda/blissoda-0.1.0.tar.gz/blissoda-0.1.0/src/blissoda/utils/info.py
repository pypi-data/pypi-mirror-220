from pprint import pformat
from typing import Dict

import numpy


def format_info(info: Dict) -> str:
    if not info:
        return ""
    rows = [
        (str(name), pformat(value, width=60).split("\n"))
        for name, value in info.items()
    ]
    lengths = numpy.array(
        [[len(name), max(len(s) for s in value)] for name, value in rows]
    )
    fmt = "   ".join(["{{:<{}}}".format(n) for n in lengths.max(axis=0)])
    lines = list()
    for name, value in rows:
        for i, s in enumerate(value):
            if i == 0:
                lines.append(fmt.format(name, s))
            else:
                lines.append(fmt.format("", s))
    return "\n ".join(lines)
