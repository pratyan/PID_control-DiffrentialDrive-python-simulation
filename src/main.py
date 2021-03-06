import pygame
import math
#import tensorflow as tf
#import keras
import matplotlib.pyplot as plt

class Envir:
    def __init__(self, dimentions):
        #color
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.red = (255,0,0)
        self.yel = (255,255,0)
        
        #map dims
        self.height = dimentions[0]
        self.width = dimentions[1]

        
        #window setting
        pygame.display.set_caption("Differential drive robot")
        self.map = pygame.display.set_mode((self.width, self.height))

class Robot:
    def __init__(self, startpos, robotImg, width):
        self.m2p=3779.52 #meter 2 pixels
        #robot dims
        self.w = width
        self.x = startpos[0]
        self.y = startpos[1]
        self.theta = 0
        self.vl = 0.01*self.m2p
        self.vr = 0.01*self.m2p
        self.maxspeed = 0.02*self.m2p
        self.minspeed = 0.02*self.m2p

        #PID values
        self.p = 0.01
        self.i = 0.0001
        self.d = 0.03

        #PID parametrs
        self.last_error = 0
        self.cum_error = 0

        #for plot
        self.data_x = []
        self.data_y = []

        #graphics
        self.img = pygame.image.load(robotImg)
        self.rotated = self.img
        self.rect=self.rotated.get_rect(center=(self.x,self.y))

    def draw(self, map):
        map.blit(self.rotated,self.rect)

    def move(self, event=None):

        '''
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP4:
                    self.vl+=0.001*self.m2p
                elif event.key == pygame.K_KP1:
                    self.vl -= 0.001*self.m2p
                elif event.key == pygame.K_KP6:
                    self.vr += 0.001*self.m2p
                elif event.key == pygame.K_KP3:
                    self.vr -= 0.001*self.m2p
        '''


        #PID update
        error = linepos[1] - self.y
        self.cum_error += error;
        self.delta_error = error - self.last_error
        self.last_error = error

        self.e_p = error
        self.e_i = self.cum_error * 0.1
        self.e_d = self.delta_error/0.1

        self.x += ((self.vl+self.vr)/2)*math.cos(self.theta)*dt
        self.data_x.append(self.x)
        #self.y -= ((self.vl+self.vr)/2)*math.sin(self.theta)*dt
        self.y += self.p*self.e_p + self.i*self.e_i + self.d*self.e_d
        self.data_y.append(self.y)
        self.theta += (self.vr-self.vl)/self.w*dt

        self.rotated = pygame.transform.rotozoom(self.img, math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x, self.y))


    def get_value(self):
        return (self.data_x, self.data_y)


    
    # def model(self):
    #     input = tf.keras.Input()
    #     hd1 = tf.keras.layers.Dense(3,activation='relu',kernel_initializer='he_normal')(data)
    #     output = tf.keras.layers.Dense(1,activation='linear',kernel_initializer='he_normal')(hd1)
    #     Model = tf.keras.Model(input=data,output=output)
    #     loss = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
    #     Model.compile(loss=loss,optimizer='Adam',metrics=['accuracy'])
    #     return Model

    # def train_model(self):
    #     input_data = tf.Variable([self.last_error,self.cum_error,self.delta_error])
    #     m = self.model(input_data,linepos[1]-self.y)
    #     m.fit()

#initialisation
pygame.init() 

#start position 
start = (100,100)

#dimentions
dims = (800,1200)

#running or not
running = True

# the envir
environment = Envir(dims)

#the robot
robot = Robot(start, "E:\differential drive\AGV.png", 0.01*3779.52)


#line position
linepos = (0,650)

# #pid values
# p = 0.1
# i = 0.01
# d = 0.1


#dt variable
dt = 0
lasttime = pygame.time.get_ticks()

#simulation loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #robot.move(event)
            
    
    dt=(pygame.time.get_ticks()-lasttime)/1000
    lasttime = pygame.time.get_ticks()
    pygame.display.update()
    environment.map.fill(environment.black)
    pygame.draw.line(environment.map, (255,0,0), linepos, (1500, linepos[1]))
    robot.move()
    robot.draw(environment.map)


#for ploting            
(x, y) = robot.get_value()
plt.plot(x,y)

plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('graph')

plt.show()
