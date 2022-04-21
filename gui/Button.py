from typing import Callable
from .Element import Element

class Button(Element):
    '''
    A Gui Element that does something when pressed
    An Element object with on_click defined could also be used
    '''
    def __init__(self, coords: tuple[int], dims: tuple[int], onClick: Callable[..., None], c: tuple[int] = (0,0,0)) -> None:
        super().__init__(coords, dims, c)
        self.on_click = onClick