# gui stuffs
from gui.Frame import Frame
from gui.Button import Button
from gui.Text import TextElement
from canvas import Canvas

# file handling
import attribute_viewer as av
from pyimg import PyImg

# other stuff
from typing import NoReturn
import pygame as pg
pg.init()

def close() -> NoReturn:
    pg.quit()
    quit()

def create_toolbar(canvas: Canvas) -> Frame:
    # changing modes
    select_btn = Button( (0,0), (50,100), onClick= lambda mc: canvas.set_active(canvas.select), c= (255,0,0) )
    edit_btn = Button( (50,0), (50,100), onClick= lambda mc: canvas.set_active(canvas.edit), c= (0,255,0) )
    make_btn = Button( (100,0), (50,100), onClick= lambda mc: canvas.set_active(canvas.make), c= (0,0,255) )
    return Frame((0,0), (800, 50), [select_btn, edit_btn, make_btn], {}, (255,255,255))

def main():
    win = pg.display.set_mode((800, 600))
    pg.display.set_caption('Image Editor')

    attribute_viewer = av.create_attribute_viewer()
    canvas = Canvas((0, 50), (600, 550), PyImg('images/setting_sun.pyimg'), attribute_viewer)
    tb = create_toolbar(canvas)

    # attribue viewer variables
    selected_object = None

    # misc.
    scoped = Element((0,0), (0,0)) # null element
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if canvas.hb.collidepoint(event.pos):
                    canvas.on_click(event.pos)
                    scoped = canvas
                elif tb.hb.collidepoint(event.pos):
                    tb.on_click(event.pos)
                    scoped = tb
                else:
                    scoped.handle_events(event)
        win.fill((255,255,255))
        canvas.render_to(win)
        attribute_viewer.render_to(win)
        tb.render_to(win)
        pg.display.flip()

if __name__ == '__main__': main()
