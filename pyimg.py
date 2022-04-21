from pygame import Rect, Surface, SRCALPHA, draw
from pygame.gfxdraw import aacircle

class Circle:
    def __init__(self, coords: list[int], rad: int, attributes: list[any]) -> None:
        self.coords = coords
        self.rad = rad
        self.attributes = attributes

    def render_to(self, surf: Surface) -> Rect:
        '''Render object to a specific surface'''
        # if the color is defined, use it. Else, use black
        if 'c' in self.attributes: color = self.attributes['c']
        else: color = (0,0,0)
        aacircle(surf, self.coords[0], self.coords[1], self.rad-1, color)
        return draw.circle(surf, color, self.coords, self.rad)

class Rectangle:
    def __init__(self, coords: list[int], attributes: list[any]) -> None:
        self.coords = coords
        self.attributes = attributes

    def render_to(self, surf: Surface) -> Rect:
        '''Render object to a specific surface'''
        # if the color is defined, use it. Else, use black
        if 'c' in self.attributes: color = self.attributes['c']
        else: color = (0,0,0)
        return draw.polygon(surf, color, self.get_points())

    def get_points(self) -> list[tuple[int]]:
        '''Get the points that make up the shape'''
        return [(self.coords[0], self.coords[1]), (self.coords[0]+self.attributes['x-size'], self.coords[1]), 
                (self.coords[0]+self.attributes['x-size'], self.coords[1]+self.attributes['y-size']), 
                (self.coords[0], self.coords[1]+self.attributes['y-size']) ]

class Square:
    def __init__(self, coords: list[int], size: int , attributes: list[any]) -> None:
        self.coords = coords
        self.size = size
        self.attributes = attributes
    
    def render_to(self, surf: Surface) -> None:
        '''Render object to a specific surface'''
        # if the color is defined, use it. Else, use black
        if 'c' in self.attributes: color = self.attributes['c']
        else: color = (0,0,0)
        return draw.polygon(surf, color, self.get_points())

    def get_points(self) -> list[tuple[int]]:
        '''Get the points that make up the shape'''
        return [ (self.coords[0], self.coords[1]), (self.coords[0]+self.size, self.coords[1]), 
                 (self.coords[0]+self.size, self.coords[1]+self.size), (self.coords[0], self.coords[1]+self.size)]

class Polygon:
    def __init__(self, attributes: list[any]) -> None:
        self.attributes = attributes
        self.points = []
        for pt in range(int(len(self.attributes['points'])/2)): # only go over half the list
            self.points.append( (self.attributes['points'][pt*2], self.attributes['points'][pt*2+1]) ) # attributs['points'] will jsut be a series of numbers
    
    def render_to(self, surf: Surface) -> None:
        '''Render object to a specific surface'''
        # if the color is defined, use it. Else, use black
        if 'c' in self.attributes: color = self.attributes['c']
        else: color = (0,0,0)
        return draw.polygon(surf, color, self.points)
    
    def get_points(self) -> list[tuple[int]]:
        '''Get the points that make up the shape'''
        return self.points

class PyImg:
    '''
    A class representing a pyimg file and image
    '''
    def __init__(self, fileName: str) -> None:
        self.name = fileName
        self.named_objects = {}
        self.image = Surface((100, 100))
        self.shape_hb = []
        self.shape_order = [] # shapes added here in order of how they are rendered
        with open(fileName, 'r') as f:
            data = f.read().split('\n')
            count = 0 # count lines
            for line in data: # go through each line and register the shapes
                count += 1
                line_data = line.split(' ')
                if count == 1:
                    size = data[0].split('x')
                    self.image = Surface( ( int(size[0]), int(size[0]) ) )
                    continue
                shape = line_data[0]
                x, y, rad = int(line_data[1]), int(line_data[2]), int(line_data[3])
                # look for attributes
                in_attribute_definition = False
                attributes = {'c': []} # c: color, '': stand in for nothing
                current_attribute = ''
                attribute_values = []
                for part in line_data:
                    start = False
                    if '/' in part: # either defining or ending an attribute
                        in_attribute_definition = not in_attribute_definition
                        if len(part) == 1: 
                            attributes[current_attribute] = attribute_values
                            attribute_values = []
                        current_attribute = part[0:-1]
                        continue
                    if in_attribute_definition: # just add attribute value for now, change it out of str later
                        attribute_values.append(part)
                attributes = _fix_attribute_list(attributes)
                
                # match shape to it's proper object
                if shape == 'c': obj = Circle([x,y], rad, attributes)
                elif shape == 's': obj = Square([x,y], rad, attributes)
                elif shape == 'r': obj = Rectangle([x,y], attributes)
                elif shape == 'p': obj = Polygon(attributes)

                hb = obj.render_to(self.image)
                self.shape_hb.append(hb)
                self.shape_order.append(obj)
                if 'name' in attributes: # object is named
                    self.named_objects[attributes['name']] = obj

    def render_to(self, surf: Surface, spot: tuple[int]) -> list[Rect]:
        '''Put the image onto something so it can be seen'''
        surf.blit(self.image, spot)

def _fix_attribute_list(attributes: dict[str:str]) -> dict[str:any]:
    '''
    Fix the values in 'attributes' during file reading
    '''
    list_attributes = ['c', 'points'] # attributes that form lists
    type_mapping = { # map attributes to their appropriate typing
        'c'    :  int,
        'name' :  str,
        'x-size' : int,
        'y-size' : int,
        'points' : int,
        ''     : str
    }
    for atr in attributes:
        if atr in list_attributes:
            count = 0
            for thing in attributes[atr]:
                # for each thing in the attribute that's a list
                # correct its typing
                attributes[atr][count] = type_mapping[atr](thing)
                count += 1
            continue
        attributes[atr] = type_mapping[atr](attributes[atr][0]) # use 0 index since it will be in a list
    return attributes


if __name__ == '__main__':
    import pygame as pg
    image_path = 'images/'
    circle_image = PyImg(image_path+'setting_sun.pyimg')

    win = pg.display.set_mode((400,400))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

        circle_image.render_to(win, (0,0))
        pg.display.flip()