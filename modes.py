'''
Descriptions of modes used on a canvas object
'''

from typing import Any

from pygame.event import Event as pgEvent
from pygame import MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN

from canvas import Canvas
from misc import cycle

class Mode:
    '''A base class used to define how a canvas should handle interactions'''
    def __init__(self, can: Canvas) -> None:
        # variables that might need to be accessed outside of the mode object
        # defined by vars[NAME] = VALUE
        self.public_vars : dict[str:Any] = {}

    # behaviour for when the canvas is clicked on
    def on_click(self, mcoords: tuple[int]) -> None: pass

    # behaviour for none click events
    # when creating a custom mode, using super().handle_events is only needed
    # if its behaviour is wanted
    def handle_events(self, ev: pgEvent) -> None: 
        if ev.type == KEYDOWN and ev.keycode == 39: # right arrow pressed
            pass
        elif ev.type == KEYDOWN and ev.keycode == 37: # left arrow pressed
            pass

class Select(Mode):
    '''A canvas mode that allows for certain objects to be selected'''
    def __init__(self, can: Canvas) -> None:
        super().__init__(can)
    
    def on_click(self, coords: tuple[int]) -> None:
        can = self.can
        can.unhighlight_outline() # remove already existing highlights
        shape_count = len(can.img.shape_hb)
        for i in range(shape_count):
            # use shape_count - i - 1 for index so that list is gone through in reverse
            if not can.img.shape_hb[shape_count-i-1].collidepoint(coords): continue # not clicked
            can.selected = can.img.shape_order[shape_count-i-1]
            can.hightlight_outline(can.selected)
            can.av.update_viewing(can.av, can.selected)
            break # only highlight one shape
        return super().on_click(coords)
