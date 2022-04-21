from __future__ import annotations
from pygame import Surface, Rect, SRCALPHA
from pygame.event import Event as pgEvent

class Element:
    '''An object representing a GUI element'''
    def __init__(self, coords: tuple[int], dims: tuple[int], c: tuple[int] = (0,0,0)) -> None:
        if c == None: c = (0,0,0,0)
        self.coords = coords
        self.sprite = Surface(dims, SRCALPHA)
        self.sprite.fill(c)
        self.hb = self.sprite.get_rect().move(coords)
        self.c = c
        self.children = []
        self.named_children = {}
    
    def render_to(self, surf: Surface) -> None:
        '''Render object onto a surface'''
        surf.blit(self.sprite, self.coords)

    def resize(self, size: tuple[int]) -> Element:
        '''Change the size of an element'''
        self.sprite = Surface(size)
        self.sprite.fill(self.c)
        self.hb = self.sprite.get_rect().move(self.coords)
        return self
    
    def relocate(self, coords: tuple[int]) -> Element:
        '''Change the coords of an element'''
        self.coords = coords
        self.hb.move_ip(coords)
        return self

    # here are some redudant meethods for inheritance
    def on_click(self, coords: tuple[int]) -> None: pass
    def on_hover(self) -> None: pass
    def handle_events(self, ev: pgEvent) -> None: pass
    
