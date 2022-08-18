import pygame as pg
from noise import snoise2
from PIL import Image
from sys import exit
import random
import math
import time
#from numba import jit 

#@jit(nopython=True,fastmath=True) 
def fastconv(x,y,size,px,water,sand,land,island,sqrt2):
    checked_channel = px/255
    if island:
        linear_shaping = 6.2  +  0.00001
        nx = 2*x/size[0] - 1 #range from -1 to 1
        ny = 2*y/size[1] - 1 #range from -1 to 1

        d = min(1, (math.pow(nx,2) + math.pow(ny,2)) / sqrt2) #distance

        checked_channel = (checked_channel + (1-d)) / linear_shaping
        checked_channel *= 255*1.1
        if checked_channel <= water: 
            checked_channel = math.pow(checked_channel,1.01)
        elif checked_channel > water:
            checked_channel = math.pow(checked_channel,1.15)
        if checked_channel > sand:
            checked_channel = math.pow(checked_channel,1.055)
        
    
    else:
        checked_channel *= 255
    
        

    smt = 0
    if checked_channel <= water:
        smt = 0 #water
    if checked_channel > water and checked_channel <= sand:
        smt = 1 #sand
    if checked_channel > sand and checked_channel <= land:
        smt = 2 #land
    if checked_channel > land :
        smt = 3 #mountain

    return smt,checked_channel



class Generator:
    def __init__(self,game) -> None:
        self.path = 'testmap.png' #input("enter the name of map:")
        self.size = (256,256)
        self.octaves = 1
        self.freq = 70.0 * self.octaves
        self.file = open(self.path, 'wt')
        self.screen = pg.display.set_mode((700,400))
        self.calcbut = pg.rect.Rect(350,210,200,80)
        self.slider = pg.rect.Rect(350,100,200,25)
        self.seed = 25349862
        self.game = game

    def new_seed(self,mp):
        # How a seed works:
        # the first 4 values are for x
        # the last 4 values are for y
        # calc_new_map() function takes these x and y values and uses them
        self.seed = int((99999999/self.slider.width) * (255/self.slider.width)*(mp[0]- self.slider.x))
        a = str(self.seed)
        if len(a) < 8:
            print("length is smaller than 8")
            self.seed = random.randint(11111111,99999999)
        if len(a) > 9:
            print("length is bigger than 8")
            self.seed = random.randint(11111111,99999999)

    def generate_map(self,island=False):
        self.st = time.time()
        tt = str(self.seed)
        t = time.time()
        xseed = int(tt[:4])
        yseed = int(tt[4:])

        #self.file = open(self.path, 'wt')
        #self.file.write('P2\n')
        #self.file.write('256 256\n')
        #self.file.write('255\n')

        self.maparray = []
        for y in range(self.size[1]):
            self.maparray.append([])
            for x in range(self.size[0]): 
                var1 = x / self.freq +xseed
                var1 += (x / self.freq*0.25 +xseed)*0.5
                var2 = y / self.freq +yseed
                var2 += (y / self.freq*0.25 +yseed)*0.5
                var3 = self.octaves

                tt = snoise2(var1, var2,var3)
                tt += 1
                tt = math.pow(tt,1.2)
                if tt > 2:
                    tt = 2

                self.maparray[y].append(int((tt-1) * 127.0 + 128.0))

                #self.file.write("%s\n" % 
                # int((tt-1) * 127.0 + 128.0) )
        #self.file.close() #write and save the file in the pgm format

        print("it took {} seconds to generate map".format(time.time()-t))
        self.convert_map(island)


    def convert_map(self,island):
        water = 70
        sand = 136
        land = 210

        self.map = [ ]
        testmap = [ ]
        y = 0
        t = time.time()
        sqrt2 = math.sqrt(2) #precalculate
        for line in self.maparray:
            self.map.append([])
            testmap.append([])
            x = 0
            for px in line:
                
                smt,checked_channel = fastconv(x,y,self.size,px,water,sand,land,island,sqrt2)
                self.map[y].append(smt)
                testmap[y].append(checked_channel)
                x += 1
            y += 1
        print("it took {} seconds to convert".format(time.time()-t))
        
        
        self.render_map()
        with open('log.txt','w') as file:
            file.write(str(testmap))
            print("wrote the file")

    def render_map(self):
        self.game.gamemapsurf = pg.surface.Surface((self.size[0]*self.game.tilesize,self.size[1]*self.game.tilesize))
        self.game.gamemapsurf.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        colors = ['blue','sandybrown','green','grey']


        t = time.time()
        y = 0
        for line in self.map:
            x = 0
            for tile in line: #the tile variable is 0 1 2 etc.
                rect = (x*self.game.tilesize,y*self.game.tilesize,self.game.tilesize,self.game.tilesize)
                pg.draw.rect(self.game.gamemapsurf,colors[tile],rect)
                x += 1
            y += 1
        print("it took {} to render the map".format(time.time()-t))
        print("it took a total of {} seconds to make a map".format(time.time()-self.st))
               