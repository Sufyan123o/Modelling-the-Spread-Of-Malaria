import pygame, sys
import numpy as np
import random
import pygame.math as math
import pygame.font

#Colours
susceptible_people_col = (211,211,211)
semi_immune_col = (144, 238, 144) #light green PKA WHITE
infected_people_col = (0, 255, 0) #infected people
dead_col = (0, 0, 0) #black
immune_col = (255, 165, 0)
male_mosq_col = (0, 100, 255) #BLUE
susceptible_mosquito_col = (50, 150, 50) #GREEN
infected_mosquitoes_col = (255,0,0) #red
background_col = (25, 25, 34)  #Blue/grey
inner_surface_col = (33, 33, 45	) #grey


class mosquito(pygame.sprite.Sprite):
    
    '''
    
    '''
    def __init__(self,x,y,width,height,color= dead_col,radius=2,velocity=[0, 0],randomize=False): 
        
        super().__init__()
        
        #Creates Mosquitoes
        self.image = pygame.Surface([radius * 2, radius * 2]) 
        self.image.fill(inner_surface_col)
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        #Mosquito location assinged used a vector
        self.rect = self.image.get_rect() #gets the position of the object on the screen.
        self.pos = np.array([x, y], dtype=np.float64) 
        self.vel = np.asarray(velocity, dtype=np.float64)
        
        
        self.fatality_on = False
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

        #Position vector
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
        
        if self.fatality_on:
            
            self.cycles_to_death -= 5

            if self.cycles_to_death <= 0:
                self.fatality_on = False
                if self.mortality_rate > random.uniform(0,1):
                    self.kill()
                else:
                    self.recovered = True
        
    def infect_person(self, color, radius = 5):
        self.kill()
        infected_person = person(self.rect.x,self.rect.y,self.WIDTH,self.HEIGHT,color=color,velocity=self.vel, radius = radius)
        simulation = Simulation()
        simulation.all_container.add(infected_person)
        return infected_person
    
    
    
        
    
    def spawn_mosquitoes(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1
        np.random.rand(2)
        
        infected_mosquito = mosquito(x, y, self.WIDTH, self.HEIGHT, color = infected_mosquitoes_col, velocity = vel )
        
        self.infected_mosquito_container.add(infected_mosquito)
        
        self.all_container.add(infected_mosquito)
    def fatality(self,cycles_to_death=20, mortality_rate=0.0001):
            self.fatality_on = True
            self.cycles_to_death = cycles_to_death
            self.mortality_rate = mortality_rate

class person(mosquito, pygame.sprite.Sprite):
    def infect_mosquito(self, color, radius = 2):
        return mosquito(self.rect.x,self.rect.y,self.WIDTH,self.HEIGHT,color=color,velocity=self.vel,radius = radius)
    
    def spawn_people(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1
        np.random.rand(2)
        susceptible_people = person(x, y, self.sim_width, self.sim_height, color = susceptible_people_col, velocity = vel, radius = 5)
        
        self.susceptible_people_container.add(susceptible_people)
        self.all_container.add(susceptible_people)
        
    def recover(self, simulation, color, radius = 5):
        self.kill()
        
        x = np.random.randint(0, self.sim_width)
        y = np.random.randint(0, self.sim_height)

        recovered_person = person(self.rect.x, self.rect.y, self.WIDTH, self.HEIGHT, color=color, velocity=self.vel, radius = radius)
        simulation.all_container.add(recovered_person)
        simulation.immune_container.add(recovered_person)
        
        # self.infected_people_container.remove(self)
        
        return recovered_person

        




class Simulation:
    def __init__(self, width = 1600, height = 900, sim_width = 800, sim_height = 800):
        self.WIDTH = width
        self.HEIGHT = height
        self.sim_width = sim_height
        self.sim_height = sim_width
        
        self.inner_surface = pygame.Surface((sim_width, sim_height))
        
        
        pygame.font.init()
        
        font_file = "Anurati-Regular.otf"
        
        font = pygame.font.Font(font_file, 50)
        # Render the text
        self.text = font.render("M O D E L L I N G  M A L A R I A", True, (255, 255, 255))
        # Get the rectangle of the text
        self.text_rect = self.text.get_rect()
        # Center the text in the window
        self.text_rect.center = (self.WIDTH / 2, 30)
        
        # load the icon image
        icon = pygame.image.load("icon.png")

        # set the icon for the game window
        pygame.display.set_icon(icon)
        
        
        
        #A container class to hold and manage multiple Sprite objects in this case to manage each category of person and mosquito
        #pygame.sprite.Group objects act as a hashmap to all objects in the group
        self.susceptible_people_container = pygame.sprite.Group()
        self.semi_immune_people_container = pygame.sprite.Group()
        self.infected_people_container = pygame.sprite.Group()
        self.dead_container = pygame.sprite.Group()
        self.male_container = pygame.sprite.Group()
        self.immune_container = pygame.sprite.Group()
        self.susceptible_mosquito_container = pygame.sprite.Group()
        self.infected_mosquito_container = pygame.sprite.Group()
        self.all_container = pygame.sprite.Group()
        
        all_container = self.all_container
        
        #Variables bro
        self.n_susceptible_mosquito = 200
        self.n_infected_mosquito = 50
        self.n_susceptible_people = 200
        self.n_infected_people = 100
        self.cycles_to_death = 1000
        self.mortality_rate = 0.2
        
        
    def start(self):
        
        #calc total population
        self.total_population = self.n_susceptible_mosquito + self.n_infected_mosquito
        
        #initiliases pygame window and display
        pygame.init()
        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption("Malaria Sim")

        #loop which moves the susceptible mosquitoes on screen
        for i in range(self.n_susceptible_people):
            person.spawn_people(self)
        
        #loop which moves non infected mosquitoes on screen
        for i in range(self.n_infected_mosquito):
            mosquito.spawn_mosquitoes(self)
        
        
        
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
            
            #detects collision between infected mosq and suscpetible person and moves it to the infected container
            collision_group = pygame.sprite.groupcollide(self.susceptible_people_container,self.infected_mosquito_container,False,False)
            
            #Uses collision_group to make susceptible people infected by mosquitoes
            for susceptible_people, infected_mosquitoes in collision_group.items():
                
                
                if susceptible_people or infected_mosquitoes in self.immune_container:
                    incidence = random.uniform(0,1)
                    if incidence < 0.15:
                        infected_people = susceptible_people.infect_person(infected_people_col, radius = 5)
                        infected_people.vel *= -1
                        infected_people.fatality(self.cycles_to_death, self.mortality_rate)
                        self.infected_people_container.add(infected_people)
                        self.all_container.add(infected_people)
            
            recovered = []
            
            # for susceptible_people in self.susceptible_people_container:
                # self.all_container.remove(susceptible_people)
            
            for infected_person in self.infected_people_container:
                if infected_person.recovered:
                    
                    self.infected_people_container.remove(infected_person)
                    self.all_container.remove(infected_people)
                    
                    recovered_person = infected_person.recover(self, immune_col)
                    self.immune_container.add(recovered_person)
                    self.all_container.add(recovered_person)
                    
                    # self.immune_container.draw(screen)
                
            self.all_container.draw(screen)
            
            
            if len(recovered) > 0:
                self.infected_mosquito_container.remove(*recovered)
                self.all_container.remove(*recovered)
                
            
            screen.blit(self.text, self.text_rect)
            
            clock.tick(60)
            pygame.display.flip()

if __name__ == "__main__":
    malaria = Simulation()
    malaria.start()
    



pygame.display.update()
