from .Element import Element
from pygame import Surface

class Frame(Element):
    '''A GUI element that can hold other elements'''
    def __init__(self, coords: tuple[int], dims: tuple[int], children: list[Element], named_children: dict[str], c: tuple[int] = (0,0,0)) -> None:
        # children and named_children can't be defaulted since they are mutable objects
        super().__init__(coords, dims, c)
        self.children = children
        self.named_children = named_children
        self.refresh_children()

    def get_child(self, name: str) -> Element:
        '''A more clear way of accesing a named child'''
        return self.named_children[name]

    def flush_children(self) -> None:
        '''A function to remove all unnamed children at once'''
        self.children = []

    def on_click(self, coords: tuple[int]) -> None:
        coords = [coords[0]-self.coords[0], coords[1]-self.coords[1]]
        for child in self.children:
            if not child.hb.collidepoint(coords): continue
            return child.on_click(coords) 
        for child in self.named_children:
            if not self.named_children[child].hb.collidepoint(coords): continue
            return self.named_children[child].on_click(coords) 
    
    def refresh_children(self) -> None:
        '''Method to reload children onto self.sprite'''
        self.sprite.fill(self.c)
        for child in self.children: child.render_to(self.sprite)
        for child in self.named_children: 
            self.named_children[child].render_to(self.sprite)
    
    def render_to(self, surf: Surface) -> None:
        return super().render_to(surf)