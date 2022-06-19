import pygame
from settings import *
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('./media/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)  # full size of the image
        self.hit_box = self.rect.inflate(0, -26)  # changing the size of the image for overlapping

        # graphics setup
        self.animations = None
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animations_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()  # by default x: 0 y: 0
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        """adding all player images in the dictionary"""
        character_path = './media/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []
        }
        for animation in self.animations.keys():  # using animation key for folder name. dict is the same as folders name
            full_path = character_path + animation  # ./media/player/up, left, down, ....
            self.animations[animation] = import_folder(
                full_path)  # filling images in the dict self.animation = {up: [up_img]....}

    def input(self):
        if not self.attacking:
            """Player movement when we press the button"""
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                """when the key is not press setting up to 0 to stop moving"""
                self.direction.x = 0

            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()  # runs once
                print('attack')

            # magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()  # runs once
                print('magic')

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

            if self.attacking:
                # while attacking can't move
                self.direction.x = 0
                self.direction.y = 0

                if not 'attack' in self.status:
                    if 'idle' in self.status:
                        # overwrite
                        self.status = self.status.replace('_idle', '_attack')
                    else:
                        self.status = self.status + '_attack'
            else:
                if 'attack' in self.status:
                    self.status = self.status.replace('_attack', '_idle')

    def move(self, speed):
        if self.direction.magnitude() != 0:
            """normalize the speed does not matter what direction is going always will be one"""
            self.direction = self.direction.normalize()

        self.hit_box.x += self.direction.x * speed
        self.collision('horizontal')
        self.hit_box.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hit_box.center
        # self.rect.center += self.direction * speed

    def collision(self, direction):
        """Collision to obstacles"""
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                """Checking collision rectangle of sprite to rectangle of the player"""
                if sprite.hit_box.colliderect(self.hit_box):
                    if self.direction.x > 0:  # moving right
                        """checking if the collision is in the right"""
                        """moving the right site of the player to the left site of the obstacle"""
                        self.hit_box.right = sprite.hit_box.left

                    if self.direction.x < 0:  # moving left
                        """checking if the collision is in the left"""
                        """moving the left site of the player to the right site of the obstacle"""
                        self.hit_box.left = sprite.hit_box.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                """Checking collision rectangle of sprite to rectangle of the player"""

                if sprite.hit_box.colliderect(self.hit_box):
                    if self.direction.y > 0:  # moving down
                        """checking if the collision is it down"""
                        """moving the down site of the player to the up site of the obstacle"""
                        self.hit_box.bottom = sprite.hit_box.top

                    if self.direction.y < 0:  # moving up
                        """checking if the collision is it up"""
                        """moving the up site of the player to the down site of the obstacle"""
                        self.hit_box.top = sprite.hit_box.bottom

    def cooldowns(self):
        """Timer"""
        current_time = pygame.time.get_ticks()  # running infantile
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        animation = self.animations[self.status]  # picking the key only that exist in dict
        # loop over the frame index
        self.frame_index += self.animations_speed  # continues give large number
        if self.frame_index >= len(animation):  # when get to end of dict will get to beginning
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hit_box.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
