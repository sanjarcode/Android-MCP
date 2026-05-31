import re

_BOUNDS_RE = re.compile(r'\[(\d+),(\d+)]\[(\d+),(\d+)]')

def extract_cordinates(node):
    attributes = node.attrib
    bounds=attributes.get('bounds')
    match = _BOUNDS_RE.search(bounds)
    if match:
        x1, y1, x2, y2 = map(int, match.groups())
        return x1, y1, x2, y2

def get_center_cordinates(cordinates:tuple[int,int,int,int]):
    x_center,y_center = (cordinates[0]+cordinates[2])//2,(cordinates[1]+cordinates[3])//2
    return x_center,y_center