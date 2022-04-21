from __future__ import annotations
from .Element import Element
from pygame import font, Surface

class TextElement(Element):
    '''A GUI element that displays text'''
    
    font.init() # ensures font is always initiliazed before DEFAULTFONTOBJECT is created
    DEFAULTFONT = 'arial'
    DEFAULTSIZE = 20
    DEFAULTFONTOBJECT = font.SysFont('arial', 20)

    def __init__(self, coords: tuple[int], dims: tuple[int], font: font.Font, text: str, fc: tuple[int] = (0,0,0), bc: tuple[int] = None) -> None:
        super().__init__(coords, dims, c=bc)
        self.font = font
        self.text = text
        self.fc = fc
        self.bc = bc
    
    def render_to(self, surf: Surface) -> None:
        self.sprite.fill(self.c) # text gets fuzzy when not cleared
        self.sprite.blit(self.font.render(self.text, True, self.fc, self.bc), (0,0))
        surf.blit(self.sprite, self.coords)

    @classmethod
    def generate_font_text(cls, name: str, size: int, bold: bool = False, italic: bool = False) -> TextElement:
        '''A method to create a text element by describing a font. Element has no width, size, or text, but can be changed'''
        font_spot = font.match_font(name, bold, italic)
        if not font_spot: return None # font doesn't exist
        return TextElement((0,0), (0,0), font.Font(font_spot, size), '')
    
    @classmethod
    def generate_font(cls, name: str, size: int, bold: bool = False, italic: bool = False) -> font.Font:
        '''A method to create a pygame.Font object'''
        font_spot = font.match_font(name, bold, italic)
        if not font_spot: return None # font doesn't exist
        return font.Font(font_spot, size)