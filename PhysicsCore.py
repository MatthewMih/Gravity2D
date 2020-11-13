import pygame
import numpy as np

#add focys mode for cam

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Body:
  def __init__(self, scene, coords = np.array([0., 0.]), velocity = np.array([0., 0.]), m = 1, force = 100, size = 10, color = (255, 255, 255)):
    self.scene = scene
    scene.bodies.append(self)
    
    self.time = 0
    self.coords = coords
    self.velocity = velocity
    self.mass = m
    self.force = force
    
    self.size = size
    self.color = color
    
    self.FEEL_GRAVITY = True
    self.TRACE = True
    self.PREDICT = True
    
    self.PREDICTION_TIME = scene.PREDICTION_TIME
    self.PREDICTION_POINTS = scene.PREDICTION_POINTS
    self.PREDICTION_POINTS_TO_DRAW = scene.PREDICTION_POINTS_TO_DRAW
    self.trace = []
    
  def __calculateBasicVelocityChanging__(self, dt, position): # how to remove position?
    #add here calculation of collision with planes and planes array in scene.
    dV = np.array([0, 0])
    if self.scene.GRAVITY and self.FEEL_GRAVITY:
      dV = np.array([dV[0], dV[1] -  self.scene.g * dt])
      dV = dV + self.scene.G * self.scene.F(self, self.scene.bodies, position) * dt
    return dV
  
  def __calculateTrajectoryPrediction__(self, dt, T):
    coordsArray = [self.coords]
    velocity = self.velocity
    
    for i in range(int(T / float(dt))):
      velocity = velocity + self.__calculateBasicVelocityChanging__(dt, coordsArray[i]) #or i+1?
      coordsArray.append(coordsArray[i] + velocity * dt)
    return coordsArray
  
  def move(self, dt):
    self.velocity = self.velocity + self.__calculateBasicVelocityChanging__(dt, self.coords)
    #add here additional velocity changing for rockets and etc.
    self.coords = self.coords + self.velocity * dt
    
    if self.TRACE:
      self.trace.append(self.coords)
  
  def draw(self):
    #drawing body shape
    pygame.draw.circle(self.scene.screen, self.color, self.scene.PhysicsCoordsToScreen(self.coords).astype(int), int(self.size * self.scene.k))
    
    #drawing body trace
    if len(self.trace) >= 2:
      pygame.draw.lines(self.scene.screen, self.color, False, self.scene.PhysicsCoordsArrayToScreenCoordsArray(np.array(self.trace)).astype(int), 5)
    
    #drawing trajectory prediction
    if self.scene.PREDICT and self.PREDICT:
      prediction =  self.__calculateTrajectoryPrediction__(float(self.PREDICTION_TIME) / self.PREDICTION_POINTS, self.PREDICTION_TIME)
      predictionToDraw=[]
      for i in range(self.PREDICTION_POINTS_TO_DRAW):
        predictionToDraw.append(prediction[self.PREDICTION_POINTS // self.PREDICTION_POINTS_TO_DRAW * i])
      
      if len(predictionToDraw) >= 2:
        pygame.draw.lines(self.scene.screen, BLUE, False, self.scene.PhysicsCoordsArrayToScreenCoordsArray(predictionToDraw), 2)
    
    #drawing velocity vector
    pygame.draw.line(self.scene.screen, RED, self.scene.PhysicsCoordsToScreen(self.coords).astype(int), self.scene.PhysicsCoordsToScreen(self.coords + self.velocity).astype(int), 2)
    


class Scene:  
  def __init__(self, screen):
    self.PREDICTION_TIME = 20
    self.PREDICTION_POINTS = 500
    self.PREDICTION_POINTS_TO_DRAW = 100
    
    self.time = 0
    
    self.screen = screen
    self.WIDTH, self.HEIGHT = pygame.display.get_surface().get_size()    
    self.center = np.array([0, 0])
    self.k = 1. #homothety coefficient
    
    self.g = 10
    self.G = 1.
    
    self.GRAVITY = True
    self.TRACE = True
    self.PAUSE = False
    self.PREDICT = True
    
    self.bodies = []
  
  def addBody(self, coords = np.array([0, 0]), velocity = np.array([0, 0]), m = 1, force = 100, size = 10, color = (255, 255, 255)):
    b = Body(self, coords, velocity, m, force, size, color)
  def distance(self, X1, X2):
    return np.sqrt((X2[0] - X1[0]) ** 2 + (X2[1] - X1[1]) ** 2)

  def f(self, r):
    return 1. / (r ** 2)

  def F(self, body, bodies, position):
    F = np.array([0,0])
    for b in bodies:
      if b != body:
        F = F + (b.coords - position) / distance(b.coords, position) * self.f(distance(b.coords, position)) * b.mass
    return F
    
  def ScreenCoordsToPhysics(self, X):
    u = self.center[0] + (X[0] - self.WIDTH / 2) / self.k
    v = self.center[1] - (X[1] - self.HEIGHT / 2) / self.k
    return np.array([u, v])
  
  def PhysicsCoordsToScreen(self, U):
    x = self.WIDTH / 2 + (U[0] - self.center[0]) * self.k
    y = self.HEIGHT / 2 - (U[1] - self.center[1]) * self.k
    return np.array([x, y])
  
  def PhysicsCoordsArrayToScreenCoordsArray(self, arr):
    newArr = []
    for i in arr:
      newArr.append(self.PhysicsCoordsToScreen(i))
    return np.array(newArr)
  
  def move(self, dt):
    for body in self.bodies:
      body.move(dt)
      
  def draw(self):
    for body in self.bodies:
      body.draw()
      
  def clearTraces(self):
    for body in self.bodies:
      body.trace = []
