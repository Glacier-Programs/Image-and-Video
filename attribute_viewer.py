from __future__ import annotations

from gui.Frame import Frame
from gui.Text import TextElement
from pyimg import Circle, Rectangle, Square, Polygon

'''
Using functional programming for this file to show it's possible
'''

SMALLERTEXT = TextElement.generate_font('arial', 15)

def create_attribute_viewer() -> Frame:
    '''Create the attribute viewer and its children'''
    header = TextElement((0,0), (200, 20), TextElement.DEFAULTFONTOBJECT, 'Attribute Viewer', fc = (0,0,0))
    object_name = TextElement((0,25), (200, 20), SMALLERTEXT, '')
    return Frame((600, 50), (200, 550), [], {'header': header, 'name': object_name}, c=(122,122,122))

def update_viewing(av: Frame, obj: Circle | Square | Rectangle | Polygon) -> None:
    '''Update the attribute being viewed in the attribute viewer'''
    if 'name' in obj.attributes: name = name
    else: name = str(obj)
    av.get_child('name').text = name
    av.flush_children()
    for count, attr in enumerate(obj.attributes.items()):
        # attr is (name, value)
        if attr[0] == 'name': continue # name shown at top
        y = count * 20 + 45 # 20 for each level + 35 for name of object and header
        av.children.append(TextElement((0,y), (200, 20), SMALLERTEXT, '{}: {}'.format(attr[0], str(attr[1]))))
    av.refresh_children() # reupdate the attribute view