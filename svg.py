from collections import namedtuple
from math import cos, sin, pi
from numbers import Real


ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IIII', 5: 'V', 6: 'VI', 7: 'VII',
         8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'}


def get_shape(prms):
    fun_name = f'get_{prms.shape.name}'
    fun = globals()[fun_name]
    return fun(prms)


def get_border(prms):
    """namedtuple('ObjParams', ['shape', 'r', 'fi', 'args', 'color'])"""
    height = prms.args[0]
    range = prms.args[1] * 2*pi / 2
    d = describeArc(0, 0, prms.r-height/2, prms.fi - range, prms.fi + range, height)

    return f'<g stroke="{prms.color}" fill="none" stroke-width="{height}">' \
        f'<path d="{d}"/></g>'


def describeArc(x, y, r, start_fi, end_fi, height):
    r_b = r - height
    start = polarToCartesian(x, y, r, end_fi)
    end = polarToCartesian(x, y, r, start_fi)
    start_b = polarToCartesian(x, y, r_b, start_fi)
    end_b = polarToCartesian(x, y, r_b, end_fi)
    arcSweep = 1  # 0 if end_fi - start_fi <= 180 else 1
    d = [
        'M', start.x, start.y,
        'A', r, r, 0, arcSweep, 0, end.x, end.y
    ]
    return ' '.join(str(a) for a in d)


def polarToCartesian(center_x, center_y, radius, fi):
    Point = namedtuple('Point', list('xy'))
    x = center_x + (radius * cos(fi))
    y = center_y + (radius * sin(fi))
    return Point(x, y)


def get_line(prms):
    """namedtuple('ObjParams', ['shape', 'r', 'fi', 'args'])"""
    height, width = prms.args
    x1 = cos(prms.fi) * prms.r
    x2 = cos(prms.fi) * (prms.r - height)
    y1 = sin(prms.fi) * prms.r
    y2 = sin(prms.fi) * (prms.r - height)
    return _get_line(x1, y1, x2, y2, width)


def get_date(prms):
    """namedtuple('ObjParams', ['shape', 'r', 'fi', 'args', 'color'])"""
    bckg = get_line(prms)
    height, width = prms.args
    txt_size = width - 3
    Prms = namedtuple('Prms', ['shape', 'r', 'fi', 'args', 'color'])
    prms = Prms(prms.shape, prms.r - height/2 + txt_size/2, prms.fi, [txt_size, 31, "horizontal"],
                "white")
    txt = get_number(prms)
    return bckg + txt


def get_rounded_line(prms):
    """namedtuple('ObjParams', ['shape', 'r', 'fi', 'args'])"""
    height, width = prms.args
    rot = (prms.fi - pi / 2) / pi * 180
    return f'<rect rx="{width/2}" y="{prms.r-height}" x="-{width/2}" ry="{width/2}" ' \
           f'transform="rotate({rot})" height="{abs(height)}" width="{width}">' \
           '</rect>'


def get_two_lines(prms):
    """namedtuple('ObjParams', ['shape', 'r', 'fi', 'args'])"""
    height, width, sep = prms.args
    x1 = cos(prms.fi) * (prms.r - height)
    x2 = cos(prms.fi) * prms.r
    y1 = sin(prms.fi) * (prms.r - height)
    y2 = sin(prms.fi) * prms.r
    factor = width / 2 * (1 + sep)
    dx = sin(prms.fi) * factor
    dy = cos(prms.fi) * factor
    return _get_line(x1 + dx, y1 + dy, x2 + dx, y2 + dy, width) + \
        _get_line(x1 - dx, y1 - dy, x2 - dx, y2 - dy, width)


def get_circle(prms):
    diameter = prms.args[0]
    cx = cos(prms.fi) * (prms.r - diameter / 2)
    cy = sin(prms.fi) * (prms.r - diameter / 2)
    return f'<circle cx={cx} cy={cy} r={abs(diameter) / 2} style="stroke-width: 0;' \
           ' fill: rgb(0, 0, 0);"></circle>'


def get_triangle(prms):
    height, width = prms.args
    x1 = (cos(prms.fi) * prms.r) - (sin(prms.fi) * width / 2)
    y1 = (sin(prms.fi) * prms.r) + (cos(prms.fi) * width / 2)
    x2 = (cos(prms.fi) * prms.r) + (sin(prms.fi) * width / 2)
    y2 = (sin(prms.fi) * prms.r) - (cos(prms.fi) * width / 2)
    x3 = cos(prms.fi) * (prms.r - height)
    y3 = sin(prms.fi) * (prms.r - height)
    return f'<polygon points="{x1},{y1} {x2},{y2} {x3},{y3}" />'


def get_upside_triangle(prms):
    height, width = prms.args
    x1 = cos(prms.fi) * prms.r
    y1 = sin(prms.fi) * prms.r
    r2 = prms.r - height
    x2 = (cos(prms.fi) * r2) - (sin(prms.fi) * width / 2)
    y2 = (sin(prms.fi) * r2) + (cos(prms.fi) * width / 2)
    x3 = (cos(prms.fi) * r2) + (sin(prms.fi) * width / 2)
    y3 = (sin(prms.fi) * r2) - (cos(prms.fi) * width / 2)
    return f'<polygon points="{x1},{y1} {x2},{y2} {x3},{y3}" />'


def get_number(prms):
    """namedtuple('ObjParams', ['shape', 'r', 'fi', 'args'])"""
    orient = ''
    font = 'arial'
    weight = ''
    if len(prms.args) == 2:
        size, kind = prms.args
    elif len(prms.args) == 3:
        size, kind, orient = prms.args
    elif len(prms.args) == 4:
        size, kind, orient, font = prms.args
    else:
        size, kind, orient, font, weight = prms.args
    #size_r = size * 2/3
    x = cos(prms.fi) * (prms.r - size / 2)
    y = sin(prms.fi) * (prms.r - size / 2)
    i = get_num_str(kind, prms.fi)
    rot = get_num_rotation(orient, prms.fi)
    fact = 6
    return f'<g transform="translate({x}, {y})"><text transform="rotate({rot}' \
           f'), translate(0, {size/fact})" class="title" fill="{prms.color}" fill-opacity="1" font-size=' \
           f'"{size*(1+1.0/fact*2)}" font-weight="{weight}" font-family="{font}" ' \
           f'alignment-baseline="middle" text-anchor="middle">{i}</text></g>'


def get_square(prms):
    """namedtuple('ObjParams', ['shape', 'r', 'fi', 'args'])"""
    height = prms.args[0]
    ObjParams = namedtuple('ObjParams', ['shape', 'r', 'fi', 'args'])
    prms = ObjParams(prms.shape, prms.r, prms.fi, [height, height])
    return get_line(prms)


def get_octagon(prms):
    height, width, sides_factor = prms.args


def get_arrow(prms):
    height, width, angle = prms.args


def get_rhombus(prms):
    height, width = prms.args


def get_trapeze(prms):
    height, width, width_2 = prms.args


def get_tear(prms):
    height, width = prms.args


def get_spear(prms):
    height, width, center = prms.args


###
##  UTIL
#

def _get_line(x1, y1, x2, y2, width):
    return f'<line x1={x1} y1={y1} x2={x2} y2={y2} style="stroke-width:' \
           f'{width}; stroke:#000000"></line>'


def get_num_str(kind, deg):
    if isinstance(kind, Real):
        return deg_to_time(deg, kind)
    if isinstance(kind, list):
        i = deg_to_time(deg, len(kind))
        return kind[i-1]
    if kind == 'minute':
        return get_minute(deg)
    if kind == 'roman':
        hour = get_hour(deg)
        return ROMAN[hour]
    else:
        return get_hour(deg)


def get_num_rotation(orient, deg):
    if orient == "horizontal":
        return 0
    elif orient == "rotating":
        return (deg + pi / 2) / pi * 180
    else:
        delta = pi if 0 < deg < pi else 0
        return (deg + pi / 2 + delta) / pi * 180


def get_hour(deg):
    return deg_to_time(deg, 12)


def get_minute(deg):
    return deg_to_time(deg, 60)


def deg_to_time(deg, factor):
    i = (deg + pi / 2) / (2 * pi) * factor
    if factor < 0:
        i = abs(factor) + i
    i = round(i)
    if i == 0:
        i = factor
    return i
