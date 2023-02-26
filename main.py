import pygame, sys
import numpy as np
import random
import pygame.math
import pygame.font
from pygame import math
import matplotlib.pyplot as plt
import time

#Colours
susceptible_people_col = (211,211,211)
semi_immune_col = (144, 238, 144) #light green PKA WHITE
infected_people_col = (0, 255, 0) #infected people
dead_col = (56, 26, 20) #black
immune_col = (255, 165, 0) 
male_mosq_col = (0, 100, 255) #BLUE
susceptible_mosquito_col = (50, 150, 50) #GREEN
infected_mosquitoes_col = (255,0,0) #red
background_col = (25, 25, 34)  #Blue/grey
inner_surface_col = (33,33,45) #grey


class mosquito(pygame.sprite.Sprite):
    
    '''
    
    '''
    def __init__(self,x,y,width,height,color= dead_col,radius=2,velocity=[0, 0],randomize=False): 
        
        super().__init__()
        
        #Creates Mosquitoes
        self.image = pygame.Surface([radius * 2, radius * 2]).convert_alpha()
        self.image.fill(inner_surface_col)
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        #Mosquito location assinged used a vector
        self.rect = self.image.get_rect() #gets the position of the object on the screen.
        self.pos = np.array([x, y], dtype=np.float64) 
        self.vel = np.asarray(velocity, dtype=np.float64)
        
        
        self.fatality_on = False
        self.recovered = False
        self.dead = False
        self.randomize = randomize
        
        self.WIDTH = width
        self.HEIGHT = height
        
        self.sim_width = 800
        self.sim_height = 800
        
        self.window_xpos = 80
        self.window_ypos = 80
        
        
        
        
        
        
    
    def update(self, radius = 5):
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
            
            self.cycles_to_death -= 10

            if self.cycles_to_death <= 0:
                self.fatality_on = False
                if self.mortality_rate > random.uniform(0,1):
                    
                    self.dead = True
                    
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
        
        infected_mosquito = mosquito(x, y, self.WIDTH, self.HEIGHT, color = infected_mosquitoes_col, velocity = vel )
        
        self.infected_mosquito_container.add(infected_mosquito)
        
        self.all_container.add(infected_mosquito)
    
    def spawn_male_mosquitoes(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1
        np.random.rand(2)
        
        male_mosquito = mosquito(x, y, self.WIDTH, self.HEIGHT, color = male_mosq_col, velocity = vel )
        
        self.male_container.add(male_mosquito)
        
        self.all_container.add(male_mosquito)
        
    def spawn_susceptible_mosquitoes(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1
        np.random.rand(2)
        
        suscpetible_mosquito = mosquito(x, y, self.WIDTH, self.HEIGHT, color = susceptible_mosquito_col, velocity = vel )
        
        self.susceptible_mosquito_container.add(suscpetible_mosquito)
        
        self.all_container.add(suscpetible_mosquito)
    
    def fatality(self,cycles_to_death=1000, mortality_rate=0.2):
            self.fatality_on = True
            self.cycles_to_death = cycles_to_death
            self.mortality_rate = mortality_rate
            
    def infect_mosquito(self, color, radius = 2):
        self.kill()
        infected_mosquito = person(self.rect.x, self.rect.y, self.WIDTH, self.HEIGHT, color=color, velocity=self.vel, radius = 2)
        # infected_mosquito = mosquito(x, y, self.WIDTH, self.HEIGHT, color = infected_mosquitoes_col, velocity = vel )
        simulation = Simulation()
        # Simulation.infected_mosquito_container.add(infected_mosquito)
        simulation.all_container.add(infected_mosquito)
        
        return infected_mosquito

class person(mosquito, pygame.sprite.Sprite):
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
        
        recovered_person = person(self.rect.x, self.rect.y, self.WIDTH, self.HEIGHT, color=color, velocity=self.vel, radius = radius)
        simulation.all_container.add(recovered_person)
        simulation.immune_container.add(recovered_person)
        
        
        return recovered_person

    def kill_person(self, simulation, color, vel, radius = 5):
        self.vel = 0
        dead_person = person(self.rect.x, self.rect.y, self.WIDTH, self.HEIGHT, color=color, velocity=self.vel, radius = radius)
        simulation.all_container.add(dead_person)
        simulation.dead_container.add(dead_person)
        
        
        return dead_person


class RealTimeGraph:
    def __init__(self, figsize=(5, 4), dpi=100, fig=None):
        # set up the screen to match the Matplotlib figure size
        self.screen_width = int(figsize[0] * dpi)
        self.screen_height = int(figsize[1] * dpi)

        if fig is None:
            self.fig, self.ax = plt.subplots(figsize=figsize, dpi=dpi, facecolor="#21212D")
        else:
            self.fig = fig
            self.ax = self.fig.gca()
            plt.close(self.fig)
        # set up Matplotlib figure and axes

        # create a plot_surface array with the dimensions of the Pygame surface
        self.plot_surface = np.zeros((self.screen_height, self.screen_width, 4), dtype=np.uint8)

        # initialize data structures
        self.xdata = []
        self.ydata = []
        self.ydata_susceptible = []
        self.ydata_immune = []
        self.ydata_infected = []
        self.ydata_male = []
        self.ydata_dead = []
        self.ydata_infected_mosquitoes = []
        self.data_hash = {}  # hash table
        self.tree = None  # binary search tree
        
    def generate_data(self, n_susceptible_people, n_immune_people, n_infected_people, n_male, n_dead_people, n_infected_mosquitoes):
        # update the data structures
        plt.rcParams['figure.max_open_warning'] = 1
        self.xdata.append(len(self.xdata))
        self.ydata_susceptible.append(n_susceptible_people)
        self.ydata_immune.append(n_immune_people)
        self.ydata_infected.append(n_infected_people)
        self.ydata_male.append(n_male)
        self.ydata_dead.append(n_dead_people)
        self.ydata_infected_mosquitoes.append(n_infected_mosquitoes)

        self.data_hash[len(self.xdata) - 1] = (len(self.xdata), n_susceptible_people, n_immune_people, n_infected_people, n_male, n_dead_people, n_infected_mosquitoes)

        # update the tree
        class Node:
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.left = None
                self.right = None
        sys.setrecursionlimit(100000) 
        def insert(node, x, y):
            if node is None:
                return Node(x, y)
            if x < node.x:
                node.left = insert(node.left, x, y)
            else:
                node.right = insert(node.right, x, y)
            return node
        self.ax.clear()
        self.tree = insert(self.tree, len(self.xdata), n_susceptible_people)
        self.tree = insert(self.tree, len(self.xdata), n_immune_people)
        self.tree = insert(self.tree, len(self.xdata), n_infected_people)
        self.tree = insert(self.tree, len(self.xdata), n_male)
        self.tree = insert(self.tree, len(self.xdata), n_dead_people)
        self.tree = insert(self.tree, len(self.xdata), n_infected_mosquitoes)

    def update_graph(self):
        # update the Matplotlib figure
        self.ax.plot(self.xdata, self.ydata_susceptible, c='#d3d3d3', lw=2, label='Susceptible People')
        self.ax.plot(self.xdata, self.ydata_immune, c='#ffa500', lw=2, label='Immune People')
        self.ax.plot(self.xdata, self.ydata_infected, c='#90ee90', lw=2, label='Infected People')
        self.ax.plot(self.xdata, self.ydata_male, c='#0064ff', lw=2, label='Male')
        self.ax.plot(self.xdata, self.ydata_dead, c='#381a14', lw=2, label='Dead People')
        self.ax.plot(self.xdata, self.ydata_infected_mosquitoes, c='#ff0000', lw=2, label='Infected Mosquitoes')
        self.ax.set_title('Real-time graph', color="white")
        self.ax.set_xlim(0, len(self.xdata))
        self.ax.set_ylim(0, max(max(self.ydata_susceptible, self.ydata_immune, self.ydata_infected, self.ydata_male, self.ydata_dead, self.ydata_infected_mosquitoes)) + 10)
        self.ax.tick_params(axis='both', colors='white')
        self.ax.set_xlabel('Time', color='white')
        self.ax.set_ylabel('Number of People/Mosquitoes', color='white')
        # self.ax.legend()

        # update the Matplotlib figure
        self.fig.canvas.draw()
        # copy the Matplotlib figure onto the Pygame surface
        self.plot_surface = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
        self.plot_surface = self.plot_surface.reshape((self.screen_height, self.screen_width, 3))
        self.plot_surface = np.rot90(self.plot_surface, 1)  # rotate counterclockwise by 90 degrees
        self.plot_surface = np.flipud(self.plot_surface)  # flip the surface vertically
        # close the previous figure
        if len(plt.get_fignums()) > 1:
            plt.close(plt.gcf())


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
        
        
        #Variables
        self.n_susceptible_mosquito = 80
        self.n_infected_mosquito = 50
        self.n_male_mosquito = 15
        self.n_susceptible_people = 200
        self.n_infected_people = 100
        self.cycles_to_death = 1000
        self.mortality_rate = 0.2
        
        # # create a surface to display both the simulation and the graph
        self.graph_surface = pygame.Surface((self.WIDTH - self.sim_width - 100, self.HEIGHT - 300))
        self.graph_surface_rect = self.graph_surface.get_rect()
        self.graph_surface_rect.topleft = (self.sim_width + 100, 300)
        self.graph = RealTimeGraph(figsize=(self.graph_surface.get_width() / 100, self.graph_surface.get_height() / 100))
        
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
        
        for i in range(self.n_male_mosquito):
            mosquito.spawn_male_mosquitoes(self)
        
        for i in range(self.n_susceptible_mosquito):
            mosquito.spawn_susceptible_mosquitoes(self)
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
                if susceptible_people or infected_mosquitoes not in self.immune_container:
                    incidence = random.uniform(0,1)
                    if incidence < 10:
                        infected_people = susceptible_people.infect_person(infected_people_col, radius = 5)
                        infected_people.vel *= -1
                        infected_people.fatality(self.cycles_to_death, self.mortality_rate)
                        self.infected_people_container.add(infected_people)
                        self.all_container.add(infected_people)
            
            #Uses Collision group to make susceptible mosquitoes infected by susceptible people.
            collision_group = pygame.sprite.groupcollide(self.susceptible_mosquito_container,self.infected_people_container,False,False)
            
            for susceptible_mosquitoes, infected_people in collision_group.items():
                if susceptible_mosquitoes or infected_people in self.immune_container:
                    incidence = random.uniform(0,1)
                    if incidence < 10:
                        infected_mosquitoes = susceptible_mosquitoes.infect_mosquito(infected_mosquitoes_col, radius = 2)
                        self.infected_mosquito_container.add(infected_mosquitoes)
                        self.all_container.add(infected_mosquitoes)
            
            
            to_remove = []
            to_recover = []

            for infected_person in self.infected_people_container:
                if infected_person.recovered:
                    to_remove.append(infected_person)
                    to_recover.append(infected_person)
                elif infected_person.dead:
                    to_remove.append(infected_person)
                    dead_person = infected_person.kill_person(self, dead_col, vel=0)
                    self.dead_container.add(dead_person)

            for people in to_remove:
                self.infected_people_container.remove(people)
                self.all_container.remove(people)

            for people in to_recover:
                recovered_person = people.recover(self, immune_col)
                self.immune_container.add(recovered_person)
                self.all_container.add(recovered_person)
        
            #Draws All Objects on the Screen
            self.all_container.draw(screen)
            
            if len(to_recover) > 0:
                self.infected_mosquito_container.remove(*to_recover)
                self.all_container.remove(*to_recover)
                
            # Create font object
            font = pygame.font.SysFont(None, 30)
            
            # Create list of text surfaces
            text_surfaces = [
                font.render("Susceptible: " + str(len(self.susceptible_people_container)), True, (susceptible_people_col)),
                font.render("Immune: " + str(len(self.immune_container)), True, (immune_col)),
                font.render("Infected: " + str(len(self.infected_people_container)), True, (infected_people_col)),
                font.render("Dead: " + str(len(self.dead_container)), True, (dead_col)),
                font.render("Male Mosquitoes: " + str(len(self.male_container)), True, (male_mosq_col)),
                font.render("Susceptible Mosquitoes: " + str(len(self.dead_container)), True, (susceptible_mosquito_col)),
                font.render("Infected Mosquitoes: " + str(len(self.infected_mosquito_container)), True, (infected_mosquitoes_col)),
            ]
            text_surfaces.reverse()
            
            
            # update the real-time graph
            self.graph.generate_data(len(self.susceptible_people_container), len(self.immune_container), len(self.infected_people_container),
                                     len(self.male_container),len(self.dead_container), len(self.infected_mosquito_container))
            self.graph.update_graph()
            self.graph_surface.fill((255, 255, 255))  # clear the graph surface
            self.graph_surface.blit(pygame.surfarray.make_surface(self.graph.plot_surface), (0, 0))  # draw the graph on the graph surface
            
            # Blit text surfaces onto screen surface
            for i, text_surface in enumerate(text_surfaces):
                screen.blit(text_surface, (self.sim_width + 100, self.HEIGHT - self.sim_height + 160 - i*30))
            screen.blit(self.text, self.text_rect)

            # draw the simulation and the real-time graph on the same Pygame window
            screen.blit(self.graph_surface, self.graph_surface_rect)
            frame_rate = "Frame Rate: " + str(int(clock.get_fps()))
            frame_rate_surface = font.render(frame_rate, True, (255, 255, 255))
            screen.blit(frame_rate_surface, (10, 10))

            clock.tick(120)
            
            # self.screen.blit(self.graph_surface, self.graph_surface_rect)  # draw the graph surface on the screen
            pygame.display.flip()
        pygame.quit()
        plt.show()
            


if __name__ == "__main__":
    malaria = Simulation()
    malaria.start()
    # graph = RealTimeGraph()
    


