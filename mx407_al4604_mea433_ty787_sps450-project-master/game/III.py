'''
Intro to Computer Science
Game Design Project
Randomized Single Level Platformer
'''
import pygame
import random
 
# Colors
# Pro-tip: use www.color-hex.com
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (86,221,86)
RED = (246,84,106)
BLUE = (176,224,230)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 
 
class Player(pygame.sprite.Sprite):
 
    # Methods
    def __init__(self):
        # Constructor function
 
        # Calls the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Creates an image of the block, and fill it with a color.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
 
        # Referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):
        # Move the player. 
        # Gravity
        self.calc_grav()
 
        # Move left or right
        self.rect.x += self.change_x
 
        # Check for collision
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0

            # Moves us with the moving platform 
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x
 
    def calc_grav(self):
        # Calculate effect of gravity.
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        # Called when user hits 'jump' button. 
 
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        # Called when the user hits the left arrow.
        self.change_x = -6
 
    def go_right(self):
        # Called when the user hits the right arrow. 
        self.change_x = 6
 
    def stop(self):
        # Called when the user lets off the keyboard. 
        self.change_x = 0
 
 
class Platform(pygame.sprite.Sprite): 
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
        an array of 5 numbers like what's defined at the top of this code. """
        pygame.sprite.Sprite.__init__(self)
 
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()
 
 
class MovingPlatform(Platform):
    # Platform that moves side to side.
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
 
    player = None
 
    level = None
 
    def update(self):
        # Moves the platform.
        # If the player is in the way, it will shove the player out of the way.
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
 
        # Check the boundaries and see if we need to reverse direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
 
 
class Level(object):
    # This is a generic super-class used to define a level.
    # Create a child class for each level with level-specific info.
 
 
    def __init__(self, player):
        # Constructor. Pass in a handle to player. Needed for when moving
        # platforms collide with the player.
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
     
        # How far this world has been scrolled left/right
        self.world_shift = 0
        self.level_limit = -1000
 
    # Update everythign on this level
    def update(self):
        # Update everything in this level.
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        # Draw everything on this level. 
 
        # Draw the background
        screen.fill(BLUE)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_y):
        # When the user moves left/right and we need to scroll everything:
 
        # Keep track of the shift amount
        self.world_shift += shift_y
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_y
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_y
 
 
# Create platforms for the level
class Level_01(Level):
    # Definition for level 1. 
 
    def __init__(self, player):
        # Creates level 1. 
 
        # Calls the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1500        
 
        # Array with width, height, x, and y of platform
        level = [[random.randint(150,250), random.randint(50,75), 200, 550],
                 [random.randint(150,200), random.randint(50,75), 450, 425],
                 [random.randint(100,225), random.randint(50,75), 750, 350],
                 [random.randint(100,200), random.randint(50,75), 1000, 275],
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
 
        # Adds a random moving platform
        randNum = random.randint(1000,1350)
        
        block = MovingPlatform(70, 70)
        block.rect.x = randNum
        block.rect.y = random.randint(150,280)
        block.boundary_left = randNum
        block.boundary_right = random.randint(1300,1600)
        block.change_x = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        randNum = random.randint(1350,1600)
        
        block1 = MovingPlatform(70, 70)
        block1.rect.x = randNum
        block1.rect.y = random.randint(150,280)
        block1.boundary_left = randNum
        block1.boundary_right = random.randint(1500,1800)
        block1.change_x = 5
        block1.player = self.player
        block1.level = self
        self.platform_list.add(block1)
 
 
def main():
    pygame.init()

    pygame.mixer.music.load('song.mp3')
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()
 
    # Sets the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Random Platformer")
 
    # Creates the player
    player = Player()
 
    # Creates all the levels
    level_list = []
    level_list.append(Level_01(player))
 
    # Sets the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 300
    player.rect.y = SCREEN_HEIGHT - 300
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                    pygame.mixer.music.load('Jumping sound.mp3')
                    pygame.mixer.music.play(0)
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                pygame.mixer.music.load('Jumping sound.mp3')
                pygame.mixer.music.play(0)
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
                pygame.mixer.music.load('Jumping sound.mp3')
                pygame.mixer.music.play(0)
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)

         # If the player gets near the right side, shift the world up (+y)
        if player.rect.top >= 800:
            diff = 500 - player.rect.top
            player.rect.top = 800
            current_level.shift_world(diff)
 
        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            if current_level_no < len(level_list)-1:
                player.rect.x = 120
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                # Out of levels. This just exits the program.
                # You'll want to do something better.
                done = True
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    
        current_level.draw(screen)
        active_sprite_list.draw(screen)
           
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    pygame.quit()
 
if __name__ == "__main__":
    main()
