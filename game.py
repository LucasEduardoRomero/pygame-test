from random import randint
import pygame

from pygame import font
from pygame import display
from pygame.image import load
from pygame.transform import scale
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame import event
from pygame.locals import QUIT, KEYUP, K_SPACE
from pygame.time import Clock

ALIVE = True
pygame.init()

tamanho = (1280, 720)
fonte = font.SysFont('comicsans', 50)
superficie = display.set_mode(tamanho, display=0)
display.set_caption('O Jogo')

fundo = scale(load('assets/space.jpg'), tamanho)

superficie.blit(
    fundo,
    (0,0)
)

class Torrada(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = load('assets/toast_small.png')
        self.rect = self.image.get_rect(
            center=(x,y)
        )

    def update(self):
        self.rect.x += 3
        if self.rect.x > tamanho[0]:
           self.kill()

class Dunofausto(Sprite):
    def __init__(self, torradas):
        super().__init__()

        self.image = load('assets/dunofausto_small.png')
        self.rect = self.image.get_rect()
        self.torradas = torradas
        self.velocidade = 2.5
    
    def tacar_torradas(self):       
        if len(self.torradas) < 15: 
            self.torradas.add(
                Torrada(*self.rect.center)
            )

    def update(self):
        keys = pygame.key.get_pressed()

        torradas_fonte = fonte.render(
            f'Torradas: {15 - len(self.torradas)}',
            True,
            (255, 255, 255)
        )
        superficie.blit(torradas_fonte, (20, 20))


        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade

class Spacebug(Sprite):
    def __init__(self):        
        super().__init__()

        self.image = load('assets/inimigo_1.png')
        self.rect = self.image.get_rect(
            center=(1500, randint(20, 380))
        )
        
    
    def update(self):        
        self.rect.x -= 3

        if self.rect.x <= 0:            
            self.kill()
            global ALIVE
            ALIVE = False



grupo_torradas = Group()
grupo_inimigos = Group()
dunofausto = Dunofausto(grupo_torradas)
grupo_duno = GroupSingle(dunofausto)
grupo_inimigos.add(Spacebug())

clock = Clock()
rounds = 0
mortes = 0

while True:
    if(not(ALIVE)):
        fonte_lost = fonte.render(
            'Você perdeu',
            True,
            (255, 255, 255)
        )
        superficie.blit(fonte_lost, (int(tamanho[0] * 0.4) , int(tamanho[1]/2)))        
        display.update()
        while True:
            for evento in event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    break

    rounds += 1
    clock.tick(120)


    if rounds % 120 == 0:
        if mortes < 20:
            grupo_inimigos.add(Spacebug())
        for _ in range(int(mortes / 10)):
            grupo_inimigos.add(Spacebug())

    for evento in event.get():
        if evento.type == QUIT:
            pygame.quit() 
            break

        if evento.type == KEYUP:
            if evento.key == K_SPACE:

                dunofausto.tacar_torradas()

    if groupcollide(dunofausto.torradas, grupo_inimigos, True, True):
        mortes += 1

    if groupcollide(grupo_duno, grupo_inimigos, False, False):
        ALIVE = False 

    
    superficie.blit(fundo, (0,0))
    

    fonte_mortes = fonte.render(
        f'Mortes: {mortes}',
        True,
        (255, 255, 255)
    )
    superficie.blit(fonte_mortes, (20, 70))

    grupo_duno.draw(superficie)
    grupo_torradas.draw(superficie)
    grupo_inimigos.draw(superficie)

    grupo_duno.update()
    grupo_torradas.update()
    grupo_inimigos.update()

    display.update()