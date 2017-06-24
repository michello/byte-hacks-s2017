'''
Intro to Computer Science
Game Design Project
Randomized Single Level Platformer
'''
import pygame
import random

#Colors
#Pro-tip for nice colors: use www.color-hex.com
black = (0, 0, 0)
white = (255, 255, 255)
green = (86,221,86)
red = (246,84,106)
blue = (176,224,230)
 
#Screen dimensions
screen_width = 1000
screen_height = 900

class Player(pygame.sprite.Sprite):
 
    #Methods
    def __init__(self):
        #Constructor function
 
        #Calls the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        #Creates image of the player block.
        width = 40
        height = 60
        self.image = pygame.image.load("memon yoda2.png").convert() # ellie's platform
        
        #Reference to the image rect.
        self.rect = self.image.get_rect()
 
        #Speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        #List of sprites we can bump against
        self.level = None
 
    def update(self):
        #This is where the player moves.
        #Gravity
        self.calc_grav()
 
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
 
    def calc_grav(self):
        #Calculate gravity.
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35
 
        #See if we are on the ground.
        if self.rect.y >= screen_height - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = screen_height - self.rect.height
 
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
        # self.image = pygame.image.load("bg-image-url").convert()

        

        rand = random.randint(0,3)
        if rand == 0:
            self.image = pygame.image.load("nasir memon.jpg").convert()
        elif rand == 1:
            self.image = pygame.image.load("other memon.jpg").convert()
        elif rand == 2:
            self.image = pygame.image.load("donald trump.png").convert()
        elif rand == 3:
            self.image = pygame.image.load("nic cage.jpg").convert()

        self.rect = self.image.get_rect()

class MovingPlatform(Platform):
    #Platform that moves side to side or up and down.
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
 
    player = None
 
    level = None
 
    def update(self):
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
         
        #Background image
        self.background = None
     
        #How far this world has been scrolled left/right
        self.world_shift = 0
        self.level_limit = -1500        
 
        # Array with width, height, x, and y of platform
        level = [[random.randint(150,250), random.randint(50,75), 200, 550],
                 [random.randint(150,200), random.randint(50,75), 450, 425],
                 [random.randint(100,225), random.randint(50,75), 750, 350],
                 [random.randint(100,200), random.randint(50,75), 1000, 400],
                 [random.randint(100,225), random.randint(50,75), 1825, 200],
                 [random.randint(100,225), random.randint(50,75), 2125, 100]
                 ]
        # Goes through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
        #THE FOLLOWING 2 PLATFORMS MOVE LEFT AND RIGHT
        randNum = random.randint(1000,1300)
        
        block = MovingPlatform(70, 70)
        block.rect.x = randNum
        block.rect.y = random.randint(150,280)
        block.boundary_left = randNum
        block.boundary_right = random.randint(1300,1500)
        block.change_x = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        randNum = random.randint(1350,1500)
        
        block1 = MovingPlatform(70, 70)
        block1.rect.x = randNum
        block1.rect.y = random.randint(150,280)
        block1.boundary_left = randNum
        block1.boundary_right = random.randint(1550,1850)
        block1.change_x = 5
        block1.player = self.player
        block1.level = self
        self.platform_list.add(block1)

        #THIS PLATFORM MOVES UP AND DOWN
        randNum = random.randint(1200,1300)
        
        block1 = MovingPlatform(70, 70)
        block1.rect.x = randNum
        block1.rect.y = random.randint(150,280)
        block1.boundary_top = 200
        block1.boundary_bottom = 500
        block1.change_y = -5
        block1.player = self.player
        block1.level = self
        self.platform_list.add(block1)
 
    #Update everything on this level
    def update(self):
        self.platform_list.update()
 
    def draw(self, screen):
        #Draw the background
        screen.fill(blue)
 
        #Draw all the sprite lists that we have
        self.platform_list.draw(screen)
 
    def shift_world(self, shift_y):
        #When the user moves left/right and we need to scroll everything:
        self.world_shift += shift_y
 
        #Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_y

def main():
    pygame.init()

    pygame.mixer.music.load('otherSong.mp3')
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()

    pygame.display.set_caption("Random Platformer")

    #Sets the height and width of the screen
    size = [screen_width, screen_height]
    screen = pygame.display.set_mode(size)

    #Creates the player
    player = Player()

    active_sprite_list = pygame.sprite.Group()

    level = Level(player)

    player.level = level

    player.rect.x = 300
    player.rect.y = screen_height - 300
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
            done = True
            # *** COULD DO MORE HERE: ENDING SCREEN / REPLAY OPTION ***
 
        #ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    
        level.draw(screen)
        active_sprite_list.draw(screen)
           
        #ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        
        #Limit to 60 frames per second
        clock.tick(60)
 
        pygame.display.flip()
 
    pygame.quit()
 
if __name__ == "__main__":
    main()
