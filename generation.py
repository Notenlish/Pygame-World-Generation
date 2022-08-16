import pygame as pg
from noise import snoise2
from PIL import Image
from sys import exit
import random
import math

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
        tt = str(self.seed)
        xseed = int(tt[:4])
        yseed = int(tt[4:])

        self.file = open(self.path, 'wt')
        self.file.write('P2\n')
        self.file.write('256 256\n')
        self.file.write('255\n')
        for y in range(self.size[1]):
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

                self.file.write("%s\n" % 
                 int((tt-1) * 127.0 + 128.0))
        self.file.close() #write and save the file in the pgm format

        im1 = Image.open(self.path)
        a = self.path
        newstring=a[:-3]+"png" #change the file format to .png
        im1.save(newstring) #write the new .png file
        self.mapsurf = pg.image.load(newstring).convert()
        self.maparray = pg.surfarray.array2d(self.mapsurf)
        print("generated new map")
        self.convert_map(island)
    


    def convert_map(self,island):
        # NOTE: since its a greyscale image i will only look at the r value since there isnt a need to look at other values
        # 0 - 255
        # 0 75 water
        # 76 85 sand
        # 86 155 land
        # 156 255 mountain

        water = 70
        sand = 136
        land = 210

        center = (self.size[0]/2,self.size[1]/2 )

        self.map = [ ]
        testmap = [ ]
        y = 0
        for line in self.maparray:
            self.map.append([])
            testmap.append([])
            x = 0
            for px in line:
                color = self.mapsurf.unmap_rgb(px)
                color = [color[0]/255,color[1]/255,color[2]/255]
                checked_channel = color[0]
                if island:
                    linear_shaping = 6.2  +  0.00001
                    nx = 2*x/self.size[0] - 1 #range from -1 to 1
                    ny = 2*y/self.size[1] - 1 #range from -1 to 1

                    d = min(1, (math.pow(nx,2) + math.pow(ny,2)) / math.sqrt(2)) #distance

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
                if checked_channel > water and color[1] <= sand:
                    smt = 1 #sand
                if checked_channel > sand and color[1] <= land:
                    smt = 2 #land
                if checked_channel > land :
                    smt = 3 #mountain
                self.map[y].append(smt)
                testmap[y].append(checked_channel)
                x += 1
            y += 1
        print("converted map")
        
        self.render_map()
        with open('log.txt','w') as file:
            file.write(str(testmap))
            print("wrote the file")

    def render_map(self):
        self.game.gamemapsurf = pg.surface.Surface((self.size[0]*self.game.tilesize,self.size[1]*self.game.tilesize))
        self.game.gamemapsurf.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        colors = ['blue','sandybrown','green','grey']

        y = 0
        for line in self.map:
            x = 0
            for tile in line: #the tile variable is 0 1 2 etc.
                rect = (x*self.game.tilesize,y*self.game.tilesize,self.game.tilesize,self.game.tilesize)
                pg.draw.rect(self.game.gamemapsurf,colors[tile],rect)
                x += 1
            y += 1
        print("rendered map")
               