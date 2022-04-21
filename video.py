from pygame.image import save
from pygame import Surface
import ffmpeg
from os import system as cmd

from pyimg import PyImg

'''
ffmpeg cheat sheet
| -i   Determines input file. No output file, that is just the last listed thing
| -c   Determine how to convert files. ex -c:a libvorbis converts the audio to vorbis
| -b   Determines the bit rate of the output file. use same :a / :v as -c
| -s   Determines the output dimensions
'''

VOLATILE_PATH = 'volatile/'

# this prompt to combine images. Change -i '{}.png' to be images 
cmd_prompt = "ffmpeg -framerate 30 -pattern_type glob -i '{}.png' \  -c:v libx264 -pix_fmt yuv420p out.mp4 "

def generate_empty(t: int, output: str) -> None:
    '''Create an empty video of t second at a selected location'''
    surf = Surface((800,600))
    save(surf, output + '.png')
    cmd_prompt = "ffmpeg -r 1/5 -i {}.png -c:v libx264 -r 30 -pix_fmt yuv420p {}.mp4".format(output, output)
    cmd(cmd_prompt)

def generate_sunset(output: str) -> None:
    surf = PyImg('images/setting_sun.pyimg').image
    save(surf, output + '.png')
    cmd_prompt = "ffmpeg -r 1/5 -i {}.png -c:v libx264 -r 30 -pix_fmt yuv420p {}.mp4".format(output, output)
    cmd(cmd_prompt)

if __name__ == '__main__':
    generate_empty(20, 'videos/empty')
    generate_sunset('videos/sun')