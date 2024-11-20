import pygame, sys
from random import choice, randint
import obstacle
from aliens import Alien, Extra
from laser import Laser
from player import Player


class Game:
  def __init__(self):
    #Player Setup
    player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
    self.player = pygame.sprite.GroupSingle(player_sprite)

    # Health and score Setup
    self.lives = 3
    self.live_surf = pygame.image.load(r"...\graphics_sp\player.png").convert_alpha()
    self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
    self.score = 0
    self.font = pygame.font.Font(r"...\text_sp\Pixeled.ttf", 20)

    # Obstacle Set up
    self.shape = obstacle.shape
    self.block_size = 6
    self.blocks = pygame.sprite.Group()
    self.obstacle_amount = 4
    self.obstace_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
    self.create_multiple_obstacles(*self.obstace_x_positions, x_start = screen_width /15, y_start = 480)
   
    # Alien Set up
    self.aliens = pygame.sprite.Group()
    self.alien_lasers = pygame.sprite.Group()
    self.alien_setup( rows = 6, cols = 8)
    self.alien_direction = 1
    
    # Extra Alien
    self.extra = pygame.sprite.GroupSingle()
    self.extra_spawn_time = randint(40, 80)

    # Audio
    music = pygame.mixer.Sound(r"...\sounds_sp\music.wav")
    music.set_volume(0.2)
    music.play(loops = -1)
    
    # Laser Sound
    self.laser_sound = pygame.mixer.Sound(r"...\sounds_sp\audio_laser.wav")
    self.laser_sound.set_volume(0.5)
    # Explosion sound
    self.explosion_sound = pygame.mixer.Sound(r"...\sounds_sp\audio_explosion.wav")
    self.explosion_sound.set_volume(0.3)
    
  def create_obstacle(self, x_start, y_start, offset_x):
    for row_index, row in enumerate(self.shape):
      for col_index, col in enumerate(row):
        if col == 'x':
          x = x_start + col_index * self.block_size + offset_x
          y = y_start + row_index * self.block_size
          block = obstacle.Block(self.block_size,(241, 79, 80),x,y)
          self.blocks.add(block)

  def create_multiple_obstacles(self,*offset, x_start,y_start):
    for offset_x in offset:
      self.create_obstacle(x_start, y_start, offset_x)

  def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
    for row_index in range(rows):
      for col_index in range(cols):
        x = col_index * x_distance + x_offset
        y = row_index * y_distance + y_offset
        
        if row_index == 0: 
          alien_sprite = Alien('yellow', x, y)
        elif 1 <= row_index <= 2: 
          alien_sprite = Alien('green', x, y)
        else: 
          alien_sprite = Alien('red', x, y)
        self.aliens.add(alien_sprite)

  def alien_position_checker(self):
    all_aliens = self.aliens.sprites()
    for alien in all_aliens:
      if alien.rect.right >= screen_width:
        self.alien_direction = -1
        self.alien_move_down(2)
      elif alien.rect.left <= 0:
        self.alien_direction = 1
        self.alien_move_down(2)

  def alien_move_down(self, distance):
    if self.aliens:
      for alien in self.aliens.sprites():
        alien.rect.y += distance

  def alien_shoot(self):
    if self.aliens.sprites():
      random_alien = choice(self.aliens.sprites())
      laser_sprite = Laser(random_alien.rect.center,6,screen_height)
      self.alien_lasers.add(laser_sprite)
      self.laser_sound.play()

  def extra_alien_timer(self):
    self.extra_spawn_time -= 1
    if self.extra_spawn_time <= 0:
      self.extra.add(Extra(choice(['right','left']), screen_width))
      self.extra_spawn_time = randint(400, 800)

  def collision_checks(self):
    # Player Lasers
    if self.player.sprite.lasers:
      for laser in self.player.sprite.lasers:
        # Obstacle collisons
        if pygame.sprite.spritecollide(laser, self.blocks, True):
          laser.kill()

        # Alien Collisons
        aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
        if aliens_hit:
          for alien in aliens_hit:
            self.score += alien.value
          laser.kill()
          self.explosion_sound.play()

        # Extra Alien Collisons
        if pygame.sprite.spritecollide(laser, self.extra, True):
          laser.kill()
          self.score += 1000

     # Alien Lasers
    if self.alien_lasers:
      for laser in self.alien_lasers:
        # Obstacle collision
        if pygame.sprite.spritecollide(laser, self.blocks, True):
          laser.kill()
        # Player Collision
        if pygame.sprite.spritecollide(laser, self.player, False):
          laser.kill()
          self.lives -= 1
          if self.lives <= 0:
              pygame.quit()
              sys.exit()

    # Aliens
    if self.aliens:
      for alien in self.aliens:
        pygame.sprite.spritecollide(alien, self.player, True)
        

        if pygame.sprite.spritecollide(alien, self.player, False):
          pygame.quit()
          sys.exit()

  def alien_block_collision(self):
    for alien in self.aliens:
      collided_blocks = pygame.sprite.spritecollide(alien, self.blocks, True)
      if collided_blocks:
        pass 

  def display_lives(self):
    for live in range(self.lives - 1):
      x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
      screen.blit(self.live_surf,(x,8))

  def display_score(self):
    score_surf = self.font.render(f'Score: {self.score}', False, 'white')
    score_rect = score_surf.get_rect(topleft = (10, -10))
    screen.blit(score_surf, score_rect)

  def victory_message(self):
    if not self.aliens.sprites():
      victory_surf = self.font.render('You Won!', False, 'white')
      victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
      screen.blit(victory_surf, victory_rect)

  def run(self):
    self.player.update()
    self.player.sprite.lasers.draw(screen)
    self.aliens.update(self.alien_direction)
    self.extra.update()
    self.alien_lasers.update()
    self.alien_position_checker()
    self.extra_alien_timer()
    self.collision_checks()
    self.alien_block_collision()
    self.player.draw(screen)
    self.blocks.draw(screen)
    self.aliens.draw(screen)
    self.alien_lasers.draw(screen)
    self.extra.draw(screen)    
    self.display_lives()
    self.display_score()
    self.victory_message()

class CRT:
  def __init__(self):
    self.tv = pygame.image.load(r"...\graphics_sp\tv.png").convert_alpha()
    self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

  def create_crt_lines(self):
    line_height = 3
    line_amount = int(screen_height / line_height)
    for line in range(line_amount):
      y_pos = line * line_height
      pygame.draw.line(self.tv, 'black', (0, y_pos),(screen_width, y_pos), 1)

  def draw(self):
    self.tv.set_alpha(randint(75,90))
    self.create_crt_lines()
    screen.blit(self.tv,(0,0))

if __name__ == '__main__':
  # Intialize the Game
  pygame. init()
  
  # Create the screen
  screen_width = 600
  screen_height = 600
  screen = pygame.display.set_mode((screen_width,   screen_height))  
  clock = pygame.time.Clock()
  game = Game()
  crt = CRT()

  ALIENLASER = pygame.USEREVENT + 1
  pygame.time.set_timer(ALIENLASER,800)
  
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == ALIENLASER:
        game.alien_shoot()
  
    screen.fill((30, 30, 30))
    game.run()
    crt.draw()
  
    pygame.display.flip()
    clock.tick(60)
