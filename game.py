
import random
from generation import Generator
import pygame as pg
#import opensimplex 

RES = WIDTH,HEIGHT = 700,500

class Game:
    def __init__(self) -> None:
        self.tilesize = 1
        self.screen = pg.display.set_mode(RES)
        self.calcbut = pg.rect.Rect(350,210,200,80)
        self.slider = pg.rect.Rect(350,100,200,25)
        self.generator = Generator(self)
        self.gamemapsurf = pg.surface.Surface((10,10))
        self.clock = pg.time.Clock()


    def run(self):
        self.generator.generate_map(False)
        
        while True:
            self.clock.tick(60)
            pg.display.set_caption(str(self.clock.get_fps()))
            self.screen.fill('black')
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.generator.generate_map()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mp = pg.mouse.get_pos() #mouse pos
                    if pg.mouse.get_pressed()[0] and self.calcbut.collidepoint(mp):
                        self.generator.generate_map(True)
                    if pg.mouse.get_pressed()[0] and self.slider.collidepoint(mp):
                        self.generator.new_seed(mp)
                        print(self.generator.seed)
                        self.generator.generate_map()
            

            self.screen.blit(self.gamemapsurf,(10,10))
            
            pg.draw.rect(self.screen,'green',self.calcbut)
            pg.draw.rect(self.screen,'white',self.slider)

            pg.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()