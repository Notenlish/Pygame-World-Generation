import pygame as pg
import json

with open('log.txt','r') as file:
    file = json.load(file)
    map = file.copy()


clock = pg.time.Clock()
screen = pg.display.set_mode((1000,600))
mapsurf = pg.surface.Surface((1000,600))

def visualize():
    mapsurf.fill((255,255,255))
    y = 0
    for line in map:
        x = 0
        for tile in line: #the tile variable is 0 1 2 etc.
            rect = (x,y,1,1)
            tile = int(tile)
            if tile > 255:
                col = tuple((255,255,255))
            else:
                col = (tile,tile,tile)
            #col = pg.color.Color(1,2,3,255)
            pg.draw.rect(mapsurf,col,rect)
            x += 1
        y += 1
    y = 0

    
    size = [len(map[0]),len(map)]
    center = [size[0]//2,size[1]//2]
    offset = [ 400,100]
    center[0] += offset[0]
    center[1] += offset[1]

    list = [x for x in range(1,len(map))]
    y = 0
    for radius in reversed(list):
        color = (radius,radius,radius)
        if color[0] > 255:
            color = (255,255,255)
        pg.draw.circle(mapsurf,color,center,radius)
    y = 0

visualize()

while True:
    clock.tick(60)
    screen.fill('black')
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    
    screen.blit(mapsurf,(10,10))
    pg.display.update()

