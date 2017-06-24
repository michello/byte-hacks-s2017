#Intro to CS Game Design Project

from __future__ import print_function, division
import pygame
import random
import math

width = 800

height = 600

#colors defined below

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class player(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLUE)
        self.speed = 20 #how fast the user is able to move
        self.rect = self.image.get_rect() #self.rect = reference to the image
        self.moveX = 0
        self.moveY = 0

    def move(self):
        self.rect.x += self.change_x #move left or right
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.moveX > 0:
                self.rect.right = block.rect.left
            elif self.moveX < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        self.rect.y += self.moveY #move up or down
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.moveY > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0

    def jump(self):
    #call this when the user presses UP
    #incorporate gravity???
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10


    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.moveX = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.moveX = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.moveX = 0

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()


def game():
    
    pygame.init()

    screen = pygame.display.set_mode((width, height)) #sets the screen size of the game

    background = pygame.Surface(screen.get_size()) #Create empty pygame surface

    background.fill((255,255,255)) #Fill the background white color (red,green,blue)

    background = background.convert() # Convert Surface to make blitting faster

    screen.blit(background, (0, 0)) #blit the surface background to position (0, 0)

    FPS = 30

    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
    playtime += seconds 

    player = player()

    active_sprite_list = pygame.sprite.Group()

    player.rect.x = 340
    player.rect.y = height - player.rect.height
    active_sprite_list.add(player)

    ingame = True

    while ingame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ingame = False
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.moveX < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.moveX > 0:
                    player.stop()
        active_sprite_list.move()
        


    pygame.quit()
    

if __name__ == "__main__":
    game()











                
