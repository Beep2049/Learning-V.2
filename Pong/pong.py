import pygame

pygame.init()

# Font
font = pygame.font.Font('freesansbold.ttf', 20)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen Parameters
WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock() 
FPS = 30

#The Paddles
class Paddle:
  def __init__(self, posx, posy, width, height, speed, color):
    self.posx = posx
    self.posy = posy
    self.width = width
    self.height = height
    self.speed = speed
    self.color = color
    # Rect that is used to control the position and collision of the object
    self.block_Rect = pygame.Rect(posx, posy, width, height)
    # Object that is blit on the screen
    self.block = pygame.draw.rect(screen, self.color, self.block_Rect)

  #Displays the object on the screen
  def display(self):
    self.block = pygame.draw.rect(screen, self.color, self.block_Rect)

  def update(self, yFac):
    self.posy = self.posy + self.speed*yFac

    # Restricting the Paddle to be below the top surface of the screen
    if self.posy <= 0:
      self.posy = 0
    # Restricting the Paddle to be above the bottom surface of the screen
    elif self.posy + self.height >= HEIGHT:
      self.posy = HEIGHT-self.height

    # Updating the rect with the new values
    self.block_Rect = (self.posx, self.posy, self.width, self.height)
    
    # Display the Score
  def displayScore(self, text, score, x, y, color):
    text = font.render(text+str(score), True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)

    screen.blit(text, textRect)

  # Function to call the Block
  def getRect(self):
    return self.block_Rect

#The Ball
class Ball:
  def __init__(self, posx, posy, radius, speed, color):
    self.posx = posx
    self.posy = posy
    self.radius = radius
    self.speed = speed
    self.color = color
    self.xFac = 1
    self.yFac = -1
    self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
    self.firstTime = 1

  def display(self):
    self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

  def update(self):
    self.posx += self.speed*self.xFac
    self.posy += self.speed*self.yFac

    # If the ball hits the top or bottom surfaces, it bounces
    if self.posy <= 0 or self.posy >= HEIGHT:
      self.yFac *= -1

    if self.posx <= 0 and self.firstTime:
      self.firstTime = 0
      return 1
    
    elif self.posx >= WIDTH and self.firstTime:
      self.firstTime = 0
      return -1
    
    else:
      return 0

  def reset(self):
    self.posx = WIDTH//2
    self.posy = HEIGHT//2
    self.xFac *= -1
    self.firstTime = 1
    self.speed = 5

  # Used to reflect the ball along the X-axis
  def hit(self):
    self.xFac *= -1

  def getRect(self):
    return self.ball

#Game Loop
def main():
  running = True

  # Defining the objects
  Player_1 = Paddle(20, 0, 10, 100, 10, WHITE)
  Player_2 = Paddle(WIDTH-30, 0, 10, 100, 10, WHITE)
  ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)

  list_of_players = [Player_1,Player_2]

  # Initial parameters of the players
  P1_Score, P2_Score = 0, 0
  P1_YFac, P2_YFac = 0, 0

  while running:
    screen.fill(BLACK)

    #Key Strokes
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          P2_YFac = -1
        if event.key == pygame.K_DOWN:
          P2_YFac = 1
        if event.key == pygame.K_w:
          P1_YFac = -1
        if event.key == pygame.K_s:
          P1_YFac = 1
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
          P2_YFac = 0
        if event.key == pygame.K_w or event.key == pygame.K_s:
          P1_YFac = 0

    # Collision detection
    for player in list_of_players:
      if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
        ball.hit()
    for player in list_of_players:
      if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
        ball.speed += 1

    # Updating the objects
    Player_1.update(P1_YFac)
    Player_2.update(P2_YFac)
    point = ball.update()

    # Updating the score
    if point == -1:
      P1_Score += 1
    elif point == 1:
      P2_Score += 1

  
    if point: 
      ball.reset()

    # Displaying the objects on the screen
    Player_1.display()
    Player_2.display()
    ball.display()

    # Displaying the scores of the players
    Player_1.displayScore("Player 1 : ", 
            P1_Score, 100, 20, WHITE)
    Player_2.displayScore("Player 2 : ", 
            P2_Score, WIDTH-100, 20, WHITE)
    

    pygame.display.update()
    clock.tick(FPS)	 


if __name__ == "__main__":
  main()
  pygame.quit()