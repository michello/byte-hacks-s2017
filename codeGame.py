import os
import tkinter
import pygame
import random
from tkinter import messagebox
from tkinter import *

#Colors
#Pro-tip for nice colors: use www.color-hex.com
black = (0, 0, 0)
white = (255, 255, 255)
green = (86,221,86)
red = (246,84,106)
blue = (176,224,230)

#Screen dimensions
screen_width = 1000
screen_height = 700

def generateFact():
    #pop up for killing/add this at the end:
    facts = ['You can save a value to a variable using an equal sign! \n For example, x = 10',
                'Variable names are ',
                'You can print words using the print function. \n For example, by typing: \n print("Hello world!");\n You are typing, "Hello world!"',
                'A string is a collection of characters surrounded by quotes \n For example, "This is a string" is a string',
                'You can save a string to a variable using the equal sign. \n For example, string_var = "A string"',
                '']
    num = random.randrange(len(facts))
    return(messagebox.showinfo(facts[num], 'OK'))

def calc_grav(self):
    #Calculate gravity.
    if self.change_y == 0:
        self.change_y = 1
    else:
        self.change_y += 0.26

    #See if we are on the ground.
    if self.rect.y >= screen_height - self.rect.height and self.change_y >= 0:
        self.change_y = 0
        self.rect.y = screen_height - self.rect.height
'''
def move(self):
    if (self.rect.x > self.rect.x + 300):
        self.rect.change_x = 100
    self.rect.x += 100


class Monster(pygame.sprite.Sprite): # not using
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        width = 30
        height = 40

        boundary_left = 0
        boundary_right = 0


        # self.image = pygame.image.load(monsterimageURLhere).convert_alpha()

        self.image = pygame.Surface([width, height])
        self.image.fill(red)

        self.rect = self.image.get_rect()

        #Speed vector of monster
        self.change_x = 0
        self.change_y = 0

        #List of sprites we can bump against
        self.level = None

        #health
        self.health = 2

    def update(self):
        #Gravity
        calc_grav(self)

        #Move left or right
        self.rect.x += self.change_x

        
        #random monster movement
        self.direction = random.choice(('left','right'))

        if self.x_direction == 'left':
            if self.rect.x > 1:
                    self.rect.x -= 1
            else:
                    self.rect.x_direction = 'right'
                    self.rect.x += 1
        else:
            if self.rect.x < px - 1:
                    self.rect.x += 1
            else:
                    self.rect.x_direction = 'left'

        #Check for collision
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
        #If moving right, set our right side to the left side of the thing we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                #Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        #Move up/down
        self.rect.y += self.change_y

        #Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            #Reset position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            #Moves monster with the moving platform
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x
        

        #Check and see if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            #We did hit the player. REDUCE PLAYER HEALTH BY 1
            self.player.health-=1


    def lowerHealth(self):
        self.health -= 1
        if health == 0:
            self.kill()
            generateFact()
'''
class Player(pygame.sprite.Sprite):

    #Methods
    def __init__(self):
        #Constructor function

        #Calls the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        #Creates image of the player block.
        #width = 40
        #height = 60

        self.image = pygame.image.load("img/Walk 1.png").convert_alpha() #change the memon yoda to the img of protag


        #self.image = pygame.Surface([width, height])
        #self.image.fill(red)

        #Reference to the image rect.
        self.rect = self.image.get_rect()

        #Speed vector of player
        self.change_x = 0
        self.change_y = 0

        #List of sprites we can bump against
        self.level = None

        #health
        self.health = 3

    def update(self):

        #This is where the player moves.

        #Gravity
        calc_grav(self)

        #Move left or right
        self.rect.x += self.change_x

        #Check for collision
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
        #If moving right, set our right side to the left side of the thing we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                #Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        #Move up/down
        self.rect.y += self.change_y

        #Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            #Reset position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            #Stop vertical movement
            self.change_y = 0

            #Moves us with the moving platform
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x
                if (MovingPlatform.status == True):
                    generateFact()
                    MovingPlatform.status = False
                block.kill()
                MovingPlatform.status = True


    def jump(self):
        #Called when user presses up button.

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        #If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= screen_height:
            self.change_y = -10

    #Player-controlled movement:
    def left(self):
        #Called when the user hits the left arrow.
        self.change_x = -6

    def right(self):
        #Called when the user hits the right arrow.
        self.change_x = 6

    def stop(self):
        #Called when the user lets off the keyboard.
        self.change_x = 0


class Platform(pygame.sprite.Sprite):

    def __init__(self, width, height):

        pygame.sprite.Sprite.__init__(self)


        #self.image = pygame.Surface([width, height])
        #self.image.fill(green)


        self.image = pygame.image.load("img/FloatingPlatform.png").convert_alpha()
        self.rect = self.image.get_rect()

class MovingPlatform(Platform):
    def __init__(self, width, height):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("img/black.png").convert_alpha()
        self.rect = self.image.get_rect()
        
    #Platform that moves side to side or up and down.
    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    status = True

    player = None

    level = None

    def update(self):
        if isinstance(self, Player):
            self.kill()

        if self.status == False:
            self.kill()
            self.rect.x = 0
            self.rect.y = 0

        #Moves the platform.
        #If the player is in the way, it will shove the player out of the way.

        #Move left/right
        self.rect.x += self.change_x

        #See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            #We did hit the player. Move player and assume they won't hit anything else.

            #If we are moving right, set our right side to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                #Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        #Move up/down
        self.rect.y += self.change_y

        #Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            #We did hit the player. Move player and assume they won't hit anything else.

            #Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        #Check the boundaries and see if we need to reverse direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

class Level(object):

    def __init__(self, player):
        #Constructor. Pass in a handle to player. Needed for when moving platforms collide with the player.
        self.platform_list = pygame.sprite.Group()
        self.player = player
        #self.monster_list = pygame.sprite.Group()

        self.background = None

        #How far this world has been scrolled left/right
        self.world_shift = 0
        self.level_limit = -1500

        #Array with width, height, x, and y of platform
        level = [[100, 100, 100, 500],
                 [random.randint(150,200), 75, 750, 400],
                 #[random.randint(100,225), 75, 750, 350],
                 [random.randint(100,200), 75, 1500, 350],
                 #[random.randint(100,225), 75, 1825, 200],
                 [random.randint(100,225), 75, 2125, 250],
                 #[1200, 1, 0, 700],
                 #[1200, 1, 1200, 700
                 ]

        #Goes through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        #THE FOLLOWING 2 PLATFORMS MOVE LEFT AND RIGHT
        randNum = random.randint(1000,1300)

        block = MovingPlatform(70, 70)
        block.status = True
        block.rect.x = 300
        block.rect.y = 620 #random.randint(150,280)
        block.boundary_left = 100
        block.boundary_right = 500
        block.change_x = 3
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        randNum = random.randint(1000,1300)

        block1 = MovingPlatform(70, 70)
        block.status = True
        block1.rect.x = 700
        block1.rect.y = 300 #random.randint(150,280)
        block1.boundary_left = 700
        block1.boundary_right = 1000
        block1.change_x =3
        block1.player = self.player
        block1.level = self
        self.platform_list.add(block1)

        #THIS PLATFORM MOVES UP AND DOWN
        randNum = random.randint(1200,1300)

        block2 = MovingPlatform(70, 70)
        block2.status = True
        block2.rect.x = 2200
        block2.rect.y = 200 #random.randint(150,280)
        block2.boundary_left = 2100
        block2.boundary_right = 2400
        #block2.change_y = -5
        block2.change_x = 3
        block2.player = self.player
        block2.level = self
        self.platform_list.add(block2)
        '''
        #Array with monsters' locations (x and y coordinates of monsters)
        monsterList = [[200, 400],
                 [450, 300],
                 [750, 200],
                 [1000, 100],
                 [1825, 0],
                 [2125, 0]]

        #Goes through the array above and add monsters
        for monst in monsterList:
            block = Monster()
            block.rect.x = monst[0]
            block.rect.y = monst[1]
            block.boundary_left = monst[0] - 200
            block.boundary_right = monst[0] + 200
            block.player = self.player
            self.monster_list.add(block)
'''

    #Update everything on this level
    def update(self):
        self.platform_list.update()
        #self.monster_list.update()

    def draw(self, screen, bg):
        #Draw the background
        screen.blit(bg, (0,0))

        #Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        #self.monster_list.draw(screen)

    def shift_world(self, shift_y):
        #When the user moves left/right and we need to scroll everything:
        self.world_shift += shift_y

        #Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_y

def finalPopUp():
    global e
    
    root = Tk()

    root.title('Name')

    textBox=Text(root, height=3, width=50)
    textBox.pack()
    textBox.insert(INSERT, "Oh no, the door is locked!")
    textBox.insert(END, '\n')
    textBox.insert(INSERT, "Unlock the door by introducing \
    yourself with a \ngreeting and your name stored in a variable.")
    textBox.insert(END, '\n \n')
    e = Text(root, height=5, width=50)
    e.pack()
    e.focus_set()

    stat = False

    def analyze_line():
        global e
        string = e.get(1.0, 'end-1c')
        if (string == "hello" '\n' "punk"):
            messagebox.showinfo("You did it!", 'OK')
        else:
            messagebox.showinfo("Please try again.", 'OK')
        
    
    b = Button(root,text='okay',command=analyze_line)
    b.pack(side='bottom')


    root.mainloop()



def main():
    bg = pygame.image.load("img/Background.jpg")

    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pygame.init()

    #music handling
    pygame.mixer.init() #initializes the mixer
    pygame.mixer.music.set_volume(.4) #sets the volume to a little lower than half
    pygame.mixer.music.load('audio/BitQuest.mp3') #loads the song
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play(-1)
    #loops the song - set value to 0 if we want it to stop when the song ends

    pygame.display.set_caption("Code Quest")

    #Sets the height and width of the screen
    size = [screen_width, screen_height]
    screen = pygame.display.set_mode(size)

    #Creates the player
    player = Player()

    active_sprite_list = pygame.sprite.Group()

    level = Level(player)

    player.level = level

    player.rect.x = 300
    player.rect.y = screen_height - 650
    active_sprite_list.add(player)

    #Loop until the user presses ESC or until end of level is reached.
    done = False

    #Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #MAIN GAME LOOP
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.left()
                if event.key == pygame.K_RIGHT:
                    player.right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        #Update the player.
        active_sprite_list.update()

        level.platform_list.update()

        #level.monster_list.update()

        #If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            level.shift_world(-diff)

        #If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            level.shift_world(diff)

         #If the player gets near the top side, shift the world up (+y)
        if player.rect.top >= 800:
            diff = 500 - player.rect.top
            player.rect.top = 800
            level.shift_world(diff)

        #If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + level.world_shift
        if current_position < level.level_limit:
            finalPopUp()
            # *** COULD DO MORE HERE: ENDING SCREEN / REPLAY OPTION ***

        #ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

        level.draw(screen, bg)
        active_sprite_list.draw(screen)


        #ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        #Limit to 60 frames per second

        clock.tick(60)

        pygame.display.flip()
    if done == True:
        pygame.quit()

if __name__ == "__main__":
    main()
