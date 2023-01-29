import pygame, sys
import numpy as np
import random
import pygame.math as math


#Colours
susceptible_people_col = (211,211,211)
semi_immune_col = (144, 238, 144) #light green PKA WHITE
infected_people_col = (255, 0, 0) #infected people
dead_col = (0, 0, 0) #black
immune_col = (255, 165, 0)
male_mosq_col = (0, 100, 255) #BLUE
susceptible_mosquito_col = (50, 150, 50) #GREEN
infected_mosquitoes_col = (255,0,0) #red
background_col = (112, 74, 81)  #Blue/grey
inner_surface_col = (44, 100, 101) #grey


class mosquito(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,color= dead_col,radius=2,velocity=[0, 0],randomize=False): 
        
        super().__init__()
        
        #Creates Mosquitoes
        self.image = pygame.Surface([radius * 2, radius * 2]) 
        self.image.fill(background_col)
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        #Mosquito location assinged used a vector
        self.rect = self.image.get_rect() #gets the position of the object on the screen.
        self.pos = np.array([x, y], dtype=np.float64) 
        self.vel = np.asarray(velocity, dtype=np.float64)
        
        
        self.killswitch_on = False
        self.recovered = False
        self.randomize = randomize
        
        self.WIDTH = width
        self.HEIGHT = height
        
        self.sim_width = 800
        self.sim_height = 800
        
        self.window_xpos = 80
        self.window_ypos = 80
    
    def update(self):
        #Assigns a speed to the position vector
        self.pos += self.vel 

        dx, dy = self.pos

        # Periodic boundary conditions to prevent objects going off the screen
        # if the person goes off screen it puts them on the other side
        
        if dx < self.window_xpos:                               #left boarder
            self.pos[0] = self.window_xpos + self.sim_width
            dx = self.window_xpos + self.sim_width
        if dx > self.window_xpos + self.sim_width:              #right boarder
            self.pos[0] = self.window_xpos
            dx = self.window_xpos
        if dy < self.window_ypos:                               #top boarder
            self.pos[1] = self.window_ypos + self.sim_height
            dy = self.window_ypos + self.sim_height
        if dy > self.window_ypos + self.sim_height:             #bottom boarder
            self.pos[1] = self.window_ypos
            dy = self.window_ypos
        
        self.rect.x = dx
        self.rect.y = dy
        
    def infect(self, color, radius = 2):
        return mosquito(self.rect.x,self.rect.y,self.WIDTH,self.HEIGHT,color=color,velocity=self.vel)


class Simulation:
    def __init__(self, width = 1600, height = 900, sim_width = 800, sim_height = 800):
        self.WIDTH = width
        self.HEIGHT = height
        self.sim_width = sim_height
        self.sim_height = sim_width
        
        self.inner_surface = pygame.Surface((sim_width, sim_height))
        
        
        #A container class to hold and manage multiple Sprite objects in this case to manage each category of person and mosquito
        self.susceptible_people_container = pygame.sprite.Group()
        self.semi_immune_people_container = pygame.sprite.Group()
        self.infected_people_container = pygame.sprite.Group()
        self.dead_container = pygame.sprite.Group()
        self.immune_container = pygame.sprite.Group()
        self.male_container = pygame.sprite.Group()
        self.susceptible_mosquito_container = pygame.sprite.Group()
        self.infected_mosquito_container = pygame.sprite.Group()
        self.all_container = pygame.sprite.Group()
        
        #number of each mosquito
        self.n_susceptible_mosquito = 200
        self.n_infected_mosquito = 50
        
        
    def start(self):
        
        #calc total population
        self.total_population = self.n_susceptible_mosquito + self.n_infected_mosquito
        
        #initiliases pygame window and display
        pygame.init()
        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        
        #main loop which moves the susceptible mosquitoes on screen
        for i in range(self.n_susceptible_mosquito):
            x = np.random.randint(0, self.WIDTH + 1)
            y = np.random.randint(0, self.HEIGHT + 1)
            vel = np.random.rand(2) * 2 - 1
            np.random.rand(2)
            guy = mosquito(x, y, self.WIDTH, self.HEIGHT, color = susceptible_people_col, velocity = vel )
            
            self.susceptible_mosquito_container.add(guy)
            self.all_container.add(guy)
        
        
        #loop which moves non infected mosquitoes on screen
        for i in range(self.n_infected_mosquito):
            x = np.random.randint(0, self.WIDTH + 1)
            y = np.random.randint(0, self.HEIGHT + 1)
            vel = np.random.rand(2) * 2 - 1
            np.random.rand(2)
            
            guy = mosquito(x, y, self.WIDTH, self.HEIGHT, color = infected_mosquitoes_col, velocity = vel )
            
            self.infected_mosquito_container.add(guy)
            
            self.all_container.add(guy)
        
        clock = pygame.time.Clock()
        
        T = True
        #loop which updates all movements to the display
        while T:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    T = False
            
            
            self.all_container.update()
            
            screen.fill(background_col)
            self.inner_surface.fill(inner_surface_col)
            screen.blit(self.inner_surface, (80, 80)) # blit the inner surface to the main window surface
            
            #detects collision between infected mosq and suscpetible mosq and moves it to the infected container
            collision_group = pygame.sprite.groupcollide(self.susceptible_mosquito_container,self.infected_mosquito_container,True,False)
            
            #Uses collision_group to make susceptible mosquitoes infected.
            for guy in collision_group:
                new_mosquito = guy.infect(infected_mosquitoes_col)
                self.infected_mosquito_container.add(new_mosquito)
                self.all_container.add(new_mosquito)
                
            self.all_container.draw(screen)
            clock.tick(60)
            pygame.display.flip()

if __name__ == "__main__":
    malaria = Simulation()
    malaria.start()
    



pygame.display.update()