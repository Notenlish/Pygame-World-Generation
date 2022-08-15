import pygame as pg
import noise 
from noise import snoise2
from PIL import Image
from sys import exit

class Generator:
    def __init__(self) -> None:
        self.path = 'testmap.png' #input("enter the name of map:")
        self.size = (256,256)
        self.octaves = 1
        self.freq = 70.0 * self.octaves
        self.file = open(self.path, 'wt')
        self.tilesize = 1
        self.screen = pg.display.set_mode((700,400))
        self.calcbut = pg.rect.Rect(350,210,200,80)
        self.slider = pg.rect.Rect(350,100,200,25)
        self.seed = 25349862

    def calc_new_map(self):
        # ilk 4 sayı x, son 4 sayı y
        
        

        tt = str(self.seed)
        xseed = int(tt[:4])
        yseed = int(tt[4:])

        self.file = open(self.path, 'wt')
        self.file.write('P2\n')
        self.file.write('256 256\n')
        self.file.write('255\n')
        for y in range(self.size[1]):
            for x in range(self.size[0]): 
                self.file.write("%s\n" % int(snoise2(x / self.freq +xseed, y / self.freq +yseed, self.octaves) * 127.0 + 128.0))
        self.file.close() #write and save the file in the pgm format

        im1 = Image.open(self.path)
        a = self.path
        newstring=a[:-3]+"png" #change the file format to .png
        im1.save(newstring) #write the new .png file
        self.mapsurf = pg.image.load(newstring).convert()
        self.maparray = pg.surfarray.array2d(self.mapsurf)
        print("generated new map")
        self.convert_map()
        

    def convert_map(self):
        # NOTE: since its a greyscale image i will only look at the r value since there isnt a need to look at other values
        # 0 - 255
        # 0 75 water
        # 76 85 sand
        # 86 155 land
        # 156 255 mountain

        water = 105
        sand = 160
        land = 240

        self.map = [ ]
        y = 0
        for line in self.maparray:
            self.map.append([])
            for px in line:
                color = self.mapsurf.unmap_rgb(px)
                smt = 0
                if color[0] <= water:
                    smt = 0 #water
                if color[1] > water and color[1] <= sand:
                    smt = 1 #sand
                if color[1] > sand and color[1] <= land:
                    smt = 2 #land
                if color[1] > land :
                    smt = 3 #mountain
                self.map[y].append(smt)
            y += 1
        
        self.render_map()

    def render_map(self):
        self.gamemapsurf = pg.surface.Surface((self.size[0]*self.tilesize,self.size[1]*self.tilesize))
        colors = ['blue','sandybrown','green','grey']
        y = 0
        for line in self.map:
            x = 0
            for tile in line: #the tile variable is 0 1 2 etc.
                rect = (x*self.tilesize,y*self.tilesize,self.tilesize,self.tilesize)
                pg.draw.rect(self.gamemapsurf,colors[tile],rect)
                x += 1
            y += 1
        
        

    def run(self):
        self.calc_new_map()


        
        while True:
            self.screen.fill('black')
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.calc_new_map()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mp = pg.mouse.get_pos()
                    if pg.mouse.get_pressed()[0] and self.calcbut.collidepoint(mp):
                        self.calc_new_map()
                    if pg.mouse.get_pressed()[0] and self.slider.collidepoint(mp):
                        # How a seed works:
                        # the first 4 values are for x
                        # the last 4 values are for y
                        # calc_new_map() function takes these x and y values and uses them
                        self.seed = int((99999999/self.slider.width) * (255/self.slider.width)*(mp[0]- self.slider.x))
                        a = str(self.seed)
                        while len(a) < 8:
                            a = str(self.seed)
                            a = a+'1'
                            self.seed = int(a)
                        self.seed = int(a)
                            
                        #int(99999*3 * (255/self.slider.width)*(mp[0]- self.slider.x))
                        print(self.seed)
                        self.calc_new_map()
            
            

            self.screen.blit(self.mapsurf,(0,0))
            self.screen.blit(self.gamemapsurf,(10,10))
            
            pg.draw.rect(self.screen,'green',self.calcbut)
            pg.draw.rect(self.screen,'white',self.slider)

            pg.display.update()
                


if __name__ == '__main__':
    gen = Generator()
    gen.run()
