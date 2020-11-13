import pygame
import numpy as np
import PhysicsCore as phys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 1080
HEIGHT = 1080
FPS = 30
SCROLLSPEED = 1.03

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity2D")
clock = pygame.time.Clock()

model = phys.Scene(screen)
model.addBody()

running = True
while running:
  clock.tick(FPS)
  
  #events block:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
    #keys events:
    if event.type == pygame.KEYDOWN:
      
      if event.key == pygame.K_g:
        model.GRAVITY = not model.GRAVITY
        print("GRAVITY: %s"%model.GRAVITY)
        
      if event.key == pygame.K_t:
        if model.TRACE:
          model.clearTraces()
        model.TRACE = not model.TRACE
        print("TRACE: %s"%model.TRACE)
        
      if event.key == pygame.K_SPACE:
        model.PAUSE = not model.PAUSE
        print("SIMULATION: %s"%model.PAUSE)
        
      if event.key == pygame.K_p:
        model.PREDICT = not model.PREDICT
        print("PREDICTION: %s"%model.PREDICT)
        
      #if event.key == pygame.K_f: -- FOCUS MODE!
    
    #mouse events:
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 4:
        model.k = model.k * SCROLLSPEED
      elif event.button == 5:
        model.k = model.k / SCROLLSPEED
      if event.button == 3:
        prevPosition = np.array(pygame.mouse.get_pos())
      
  #keys pushes:
  if not model.PAUSE:
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
      model.bodies[0].velocity[0] += float(model.bodies[0].force) / model.bodies[0].mass / float(FPS)
    if pygame.key.get_pressed()[pygame.K_LEFT]:
      model.bodies[0].velocity[0] -= float(model.bodies[0].force) / model.bodies[0].mass / float(FPS)
    if pygame.key.get_pressed()[pygame.K_UP]:
      model.bodies[0].velocity[1] += float(model.bodies[0].force) / model.bodies[0].mass / float(FPS)
    if pygame.key.get_pressed()[pygame.K_DOWN]:
      model.bodies[0].velocity[1] -= float(model.bodies[0].force) / model.bodies[0].mass / float(FPS)
  
  #mouse pushes:
  if pygame.mouse.get_pressed()[2]:
    model.center = model.center -  model.ScreenCoordsToPhysics(np.array(pygame.mouse.get_pos())) + model.ScreenCoordsToPhysics(prevPosition)
    prevPosition = np.array(pygame.mouse.get_pos())
  
  #calculations:
  model.move(1./FPS)
  
  #drawing:
  screen.fill(BLACK)
  model.draw()
  pygame.display.flip()
pygame.quit()
  