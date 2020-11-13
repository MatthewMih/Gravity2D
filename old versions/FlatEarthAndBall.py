import pygame
import numpy as np

#for new version (rebuild)
# - Array of bodies
# - coords in array

print("\n\n\n    ***CONTROL KEYS***\n\n")
print("Space -- pause")
print("Arrows -- for acceleration")
print("F -- to focus camera on ball")
print("RMB -- to move camera, scroll to zoom")
print("G -- gravity switch")
print("T -- trace switch")
print("P - trajectory prediction switch\n")
print("https://github.com/MatthewMih/Gravity2D\n\n")
WIDTH = 1080
HEIGHT = 1080
FPS = 30
PREDICTION_TIME = 20
PREDICTION_POINTS = 1000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class ModelParams:
  pass
p = ModelParams()
p.u0 = 0
p.v0 = 0
p.k = 1.
p.g = 10.
p.GRAVITY = True
p.TRACE = True
p.PAUSE = False
p.PREDICT = True # TO DO and focuse mode for cam, pause, help window, text info, razvyazat dt i FPS, images, changable prediction time
p.FOCUS_MODE = False
def XYtoUV(x, y):
  u = p.u0 + (x - WIDTH / 2) / p.k
  v = p.v0 - (y - HEIGHT / 2) / p.k
  return [u, v]

def UVtoXY(u, v):
  x = WIDTH / 2 + (u - p.u0) * p.k
  y = HEIGHT / 2 - (v - p.v0) * p.k
  return [x, y] 
def UVtoXYinArr(arr):
  newArr = []
  for i in arr:
    newArr.append(UVtoXY(i[0], i[1]))
  return newArr
def TrajectoryVanga(body, T, dt): #add bodies array here    
  vu = body.vu
  vv = body.vv
  u = body.u
  v = body.v
  arr = []
  arr.append([u,v])
  for i in range(int(T / dt)):
    if p.GRAVITY:
      vv -= p.g * float(dt)
    if v < body.d:
      vv = np.abs(vv)
    u += vu * float(dt)
    v += vv * float(dt)  
    arr.append([u,v])
  return arr





class BodyRect:
  def __init__(self):
    self.mass = 1
    self.force = 100
    self.d = 10
    self.u = 0
    self.v = 0
    self.vu = 0
    self.vv = 0
    self.trace = []
  def getXY(self):
    return UVtoXY(self.u, self.v)
  def move(self):
    if p.GRAVITY:
      self.vv -= p.g / float(FPS)
    if self.v < self.d:
      self.vv = np.abs(self.vv)
    self.u += self.vu / float(FPS)
    self.v += self.vv / float(FPS)
    if p.TRACE:
      self.trace.append([self.u, self.v])
  def draw(self, sc):
    #pygame.draw.rect(sc, WHITE, (b1.getXY()[0] - self.d * p.k / 2, b1.getXY()[1] - self.d * p.k / 2, self.d * p.k, self.d * p.k))
    pygame.draw.circle(sc, WHITE, (int(self.getXY()[0]), int(self.getXY()[1])), int(self.d * p.k))
    if len(self.trace) >= 2:
      pygame.draw.lines(sc, WHITE, False, UVtoXYinArr(self.trace), 5)
    if p.PREDICT:
      prediction = TrajectoryVanga(self, PREDICTION_TIME, PREDICTION_TIME / float(PREDICTION_POINTS))
      if len(prediction) >= 2:
        pygame.draw.lines(sc, BLUE, False, UVtoXYinArr(prediction), 2)
    pygame.draw.line(sc, RED, self.getXY(), UVtoXY(self.u + self.vu, self.v + self.vv), 2)
class Floor:
  def __init__(self):
    self.v = 0
  def getY(self):
    return UVtoXY(0, self.v)[1]
  def draw(self, sc):
    pygame.draw.rect(sc, GREEN, (0, int(self.getY()), HEIGHT, WIDTH))
#def evaluate(bodies)





b1 = BodyRect()
grass = Floor()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flat Earth and ball")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_g:
          if p.GRAVITY:
            p.GRAVITY = False
            print("GRAVITATION DISABLED")
          else:
            p.GRAVITY = True
            print("GRAVITATION ENABLED")
        if event.key == pygame.K_t:
          if p.TRACE:
            p.TRACE = False
            b1.trace = []
          else:
            p.TRACE = True
          print("TRACE: %s"%p.TRACE)
        if event.key == pygame.K_SPACE:
          if p.PAUSE:
            print("SIMULATION STARTED")
            p.PAUSE = False
          else:
            print("SIMULATION PAUSED")
            p.PAUSE = True
        if event.key == pygame.K_p:
          if p.PREDICT:
            print("PREDICTION STOPPED")
            p.PREDICT = False
          else:
            print("PREDICTION STARTED")
            p.PREDICT = True
        if event.key == pygame.K_f:
          if p.FOCUS_MODE:
            print("FOCUS MODE DISABLED")
            p.FOCUS_MODE = False
          else:
            print("FOCUS MODE DISABLED")
            p.FOCUS_MODE = True
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
          p.k = p.k * 1.03
        elif event.button == 5:
          p.k = p.k / 1.03
        if event.button == 3:
          prevPosition = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[2]:
      p.u0 -= XYtoUV(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[0] - XYtoUV(prevPosition[0], prevPosition[1])[0]
      p.v0 -= XYtoUV(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[1] - XYtoUV(prevPosition[0], prevPosition[1])[1]
      prevPosition = pygame.mouse.get_pos()
    if p.FOCUS_MODE:
      p.u0 = b1.u
      p.v0 = b1.v    


    if p.PAUSE == False:
      if pygame.key.get_pressed()[pygame.K_RIGHT]:
        b1.vu += float(b1.force) / b1.mass / float(FPS)
      if pygame.key.get_pressed()[pygame.K_LEFT]:
        b1.vu -= float(b1.force) / b1.mass / float(FPS)
      if pygame.key.get_pressed()[pygame.K_UP]:
        b1.vv += float(b1.force) / b1.mass / float(FPS)
      if pygame.key.get_pressed()[pygame.K_DOWN]:
        b1.vv -= float(b1.force) / b1.mass / float(FPS)
    
      b1.move()



    screen.fill(BLACK)
    grass.draw(screen)
    b1.draw(screen)    

    pygame.display.flip()

pygame.quit()
