from typing import Callable

from pygame import Surface, SRCALPHA
from pygame.draw import polygon, circle
from pygame import KEYDOWN, MOUSEBUTTONUP, MOUSEMOTION

from pyimg import PyImg, Circle, Rectangle, Square, Polygon
from gui.Element import Element
import attribute_viewer as av

class Canvas(Element):
    '''A canvas that can be drawn on. Drawings can be saved as .pyimg'''
    def __init__(self, coords: tuple[int], dims: tuple[int], img: PyImg, av: str) -> None:
        super().__init__(coords, dims)
        '''
        Scope:
         - Object: Work on parts of img as a whole
         - Attribute: Work on specific attributes of an image
         - 
        '''
        self.scope = 0
        self.scopes = ['object', 'attribute']
        self.effects = Surface(dims, SRCALPHA)
        self.img = img
        self.av = av
        # mode info
        self.mode = self.select
        self.selected = None
        self.make_object = Polygon
        self.make_points = []
        self.is_selected = False
        self.held_down = False

    def on_click(self, coords: tuple[int]) -> None:
        coords = [coords[0] - self.coords[0], coords[1] - self.coords[1]]
        self.mode(coords)
    
    def hightlight_outline(self, obj: any) -> None: 
        ''' Color the edges and vertices of a shape '''
        if obj.attributes['c'][0:3] == [0,0,0]: col = (255,255,255) # only sample first 3 items so the highlight color is regardless of translucency
        else: col = (0,0,0)
        if type(obj) == Circle:
            circle(self.effects, col, obj.coords, obj.rad, 2)
        elif type(obj) == Rectangle or type(obj) == Square or type(obj) == Polygon:
            pts = obj.get_points()
            polygon(self.effects, col, pts, 2)
            for pt in pts:
                circle(self.effects, col, pt, 10)
    
    def unhighlight_outline(self, obj: any = False) -> None:
        if not obj: return self.effects.fill((0,0,0,0))
    
    def render_to(self, surf: Surface) -> None:
        self.sprite.fill((0,0,0))
        self.img.render_to(self.sprite, (0,0))
        self.sprite.blit(self.effects, (0,0))
        return super().render_to(surf)
    
    def update_check(self, ev: any) -> None:
        '''A way to track events other than MOUSEBUTTONDOWN'''
        if ev.type == MOUSEBUTTONUP: self.held_down = False
        elif ev.type == MOUSEMOTION: self.held_down = True
        elif ev.type == KEYDOWN:
            if ev.unicode == 'o': self.scope = 0
            elif ev.unicode == 'a': self.scope = 1

    ''' Mode Methods '''
    def set_active(self, onClickFunc: Callable) -> None:
        '''Method to set the canvas mode'''
        self.mode = onClickFunc

    def select(self, coords: tuple[int]) -> None:
        '''Logic to use when on_click() is used in select mode'''
        self.unhighlight_outline()
        shape_count = len(self.img.shape_hb)
        for i in range(shape_count):
            # use shape_count - i - 1 for index so that list is gone through in reverse
            if not self.img.shape_hb[shape_count-i-1].collidepoint(coords): continue # not clicked
            self.selected = self.img.shape_order[shape_count-i-1]
            self.hightlight_outline(self.selected)
            av.update_viewing(self.av, self.selected)
            break # only highlight one shape
        return super().on_click(coords)
    
    def edit(self, coords: tuple[int]) -> None:
        '''Logic to use when on_click() is used in edit mode'''
        print('edit')
        if self.selected == None or not self.img.shape_hb[ self.img.shape_hb.index(self.selected) ].collidepoint(coords) : 
            # if nothing is selected or u click on something unselected
            return self.select(coords)
        # getter here means that the currently selected object has been clicked
        if self.scopes[self.scope] == 'object':
            # this means that the object was clicked
            pass
        elif self.scopes[self.scope] == 'attribute':
            pass
    
    def make(self, coords: tuple[int]) -> None:
        '''Logic to use when on_click() is used in make mode'''