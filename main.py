import pygame
import numpy as np
import random
import pygame.math
import pygame.font

#Constant colours to identify objects on screen 
SUSCEPTIBLE_PEOPLE_COL = (211,211,211) #Off White
SEMI_IMMUNE_COL = (255,192,203) #Light Pink
INFECTED_PEOPLE_COL = (0, 255, 0) #Light Green
DEAD_COL = (56, 26, 20) #Brown
IMMUNE_COL = (255, 165, 0) #Yellow
MALE_MOSQUITO_COL = (0, 100, 255) #Blue
SUSCEPTIBLE_MOSQUITO_COL   = (50, 150, 50) #dark green
INFECTED_MOSQUITOES_COL  = (255,0,0) #Red
BACKGROUND_COL  = (25, 25, 34) #Darkish Blue/Grey
INNER_SURFACE_COL  = (33,33,45) #Blue/Grey, slightly lighter than background
CURRENT_SIMULATION  = None #Flag to detect if an Instance of Simulation is running



class Malaria(pygame.sprite.Sprite):
    """
    Manages the creation and behaviour of objects affected by Malaria in the simulation
    
        Args:
            x (float): x position
            y (float): y position_
            width (int): width of screen
            height (inr): height of screen
            color (tuple, RGB): colour of object. Defaults to DEAD_COL.
            radius (int): radius of the object on screen. Defaults to 2.
            velocity (vector): Velocity at which the objects move. Defaults to [0, 0].
        """        
    def __init__(self, x, y, width, height, color=DEAD_COL, radius=2, velocity=[0, 0]):
        
        super().__init__()
        # Creates Mosquitoes
        self.image = pygame.Surface([radius * 2, radius * 2]).convert_alpha()
        self.image.fill(INNER_SURFACE_COL)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.x = x
        self.y = y
        
        self.fatality_on = False
        self.recovered = False
        self.dead = False
        self.semi_immune = False

        self.WIDTH = width
        self.HEIGHT = height #

        self.sim_width = 800
        self.sim_height = 800

        self.window_xpos = 80
        self.window_ypos = 80

        #Objects location assigned used a vector
        self.rect = self.image.get_rect()  # gets the position of the object on the screen.
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.asarray(velocity, dtype=np.float64)
        self.vel = np.asarray(velocity, dtype=np.float64)
    
    def update(self):
        """
        Updates the position and status of an object 
        
        """
        # Add random displacement to make movement more realistic
        self.pos += self.vel
        displacement = np.random.rand(2) * 2 - 1
        self.pos += displacement * 0.1
        
        # Position vector
        dx, dy = self.pos
        
        # Periodic boundary conditions to prevent objects going off the screen
        # if something goes off screen it puts them on the other side
        if dx < self.window_xpos:                           # left boarder
            self.pos[0] = self.window_xpos + self.sim_width
            dx = self.window_xpos + self.sim_width
        if dx > self.window_xpos + self.sim_width:          #right boarder
            self.pos[0] = self.window_xpos
            dx = self.window_xpos
        if dy < self.window_ypos:                           # top boarder
            self.pos[1] = self.window_ypos + self.sim_height
            dy = self.window_ypos + self.sim_height
        if dy > self.window_ypos + self.sim_height:         # bottom boarder
            self.pos[1] = self.window_ypos
            dy = self.window_ypos
        
        self.rect.x = dx
        self.rect.y = dy

        # Handles mosquitos making a person semi immune, recovered or killing them.
        SEMI_IMMUNE_PROBABILITY = 0.2 #sets constant self immunity probability
        if self.fatality_on:
            self.cycles_to_death -= 10 #Count down for cycles to death
            if self.cycles_to_death <= 0: #Once at 0 determines whether someone dies or becomes semi immune
                self.fatality_on = False
                if self.mortality_rate > random.uniform(0, 1):
                    self.dead = True
                elif SEMI_IMMUNE_PROBABILITY > random.uniform(0, 1):
                    self.semi_immune = True
                else:
                    self.recovered = True
    
    def infect_person(self, color, radius = 5):
        """
        Called when an Infected Mosquito has blood meal on person and gets infected
        Doesnt spawn infected but rather makes a susceptible get infected

        Args:
            color (tuple): color of person
            radius (int): Radus of mosquito. Defaults to 5.
            
        Returns:
            _type_: infected person
        """
        self.kill() #Removes original object from the display to prevent memory leak
        infected_person = person(self.rect.x,self.rect.y,self.WIDTH,self.HEIGHT,color=color,velocity=self.vel, radius = radius)
        simulation = Simulation.get_instance()
        simulation.all_container.add(infected_person)
        return infected_person
    
    def spawn_infected_mosquitoes(self):
        x = np.random.randint(80, self.sim_width + 1) #assigns random x position
        y = np.random.randint(80, self.sim_height + 1) #assigns random y position
        vel = np.random.rand(2) * 2 - 1 #assigns velocity
        infected_mosquito = Malaria(x, y, self.WIDTH, self.HEIGHT, color = INFECTED_MOSQUITOES_COL , velocity = vel )
        #add the mosquito to their specified containers to control how they behave
        self.infected_mosquito_container.add(infected_mosquito)
        self.all_container.add(infected_mosquito) #all_contianer is updated on to the screen every frame
    
    def spawn_male_mosquitoes(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1 #assigns velocity
        male_mosquito = Malaria(x, y, self.WIDTH, self.HEIGHT, color = MALE_MOSQUITO_COL, velocity = vel )
        #add the mosquito to their specified containers to control how they behave
        self.male_container.add(male_mosquito)
        self.all_container.add(male_mosquito)
        
    def spawn_susceptible_mosquitoes(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1 #assigns velocity
        suscpetible_mosquito = Malaria(x, y, self.WIDTH, self.HEIGHT, color = SUSCEPTIBLE_MOSQUITO_COL , velocity = vel )
        #add the mosquito to their specified containers to control how they behave
        self.susceptible_mosquito_container.add(suscpetible_mosquito) 
        self.all_container.add(suscpetible_mosquito)
    
    def fatality(self,cycles_to_death=random.randint(500,5000), mortality_rate= 0):
        """
        Triggers the start of the death, semi immunity, recovery for infected peoeple
        
        Args:
            cycles_to_death (int): Count down till death, recoery or semi immunity. Defaults to random integer between 500 to 5000
            mortality_rate (int): Rate of which people die when cycles_to_death hits 0. Defaults to 0.
                                Can be altered using GUI.
        """
        self.fatality_on = True
        self.cycles_to_death = cycles_to_death
        self.mortality_rate = mortality_rate
    
    def infect_mosquito(self, color):
        """
        Infects mosquitoes when in contact with a human carrying the parasite
        
        Returns:
            object: infected mosquito which then gets displayed on the screen later on
        """
        self.kill() #Removes original object from the display to prevent memory leak
        infected_mosquito = person(self.rect.x, self.rect.y, self.WIDTH, self.HEIGHT, color=color, velocity=self.vel, radius = 2)
        simulation = Simulation.get_instance()
        simulation.all_container.add(infected_mosquito)
        return infected_mosquito

        

class person(Malaria, pygame.sprite.Sprite):
    """
    Inherits all the attributes from Malaria class therefore creating child class
    Handles the spawning, movement and spread of malaria between people on the display
    """
    def spawn_people(self):
        #spawns regular susceptible people
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1 #assigns velocity
        susceptible_people = person(x, y, self.sim_width, self.sim_height, color = SUSCEPTIBLE_PEOPLE_COL, velocity = vel, radius = 5)
        #add the people to their specified containers
        self.susceptible_people_container.add(susceptible_people) 
        self.all_container.add(susceptible_people)
    
    def spawn_infected_people(self):
        #spawns infected individuals
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1
        infected = person(x, y, self.sim_width, self.sim_height, color = INFECTED_PEOPLE_COL, velocity = vel, radius = 5)
        infected.fatality(self.cycles_to_death, self.mortality_rate) #Starts cycles_to_death count down
        self.infected_people_container.add(infected)
        self.all_container.add(infected)
    
    def spawn_semi_immune(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1
        semi_immmune = person(x, y, self.sim_width, self.sim_height, color = SEMI_IMMUNE_COL, velocity = vel, radius = 5)
        self.semi_immune_container.add(semi_immmune)
        self.all_container.add(semi_immmune)
    
    def make_semi_immune(self, simulation, color, radius = 5):
        self.kill() #Removes people from the display to prevent memory leaks
        semi_immune_person = person(self.rect.x, self.rect.y, self.WIDTH, self.HEIGHT, color=color, velocity=self.vel, radius = radius)
        simulation.all_container.add(semi_immune_person)
        simulation.semi_immune_container.add(semi_immune_person)
        
        
        return semi_immune_person
    
    def recover(self, simulation, color, radius = 5):
        self.kill()
        
        recovered_person = person(self.rect.x, self.rect.y, self.WIDTH, self.HEIGHT, color=color, velocity=self.vel, radius = radius)
        simulation.all_container.add(recovered_person)
        simulation.immune_container.add(recovered_person)
        
        
        return recovered_person

    def kill_person(self, simulation, color, vel, radius = 5):
        self.vel = 0 #stops  dead people from moving
        dead_person = person(self.rect.x, self.rect.y, self.WIDTH, self.HEIGHT, color=color, velocity=self.vel, radius = radius)
        simulation.dead_container.add(dead_person)
        simulation.all_container.add(dead_person)
        return dead_person
    
    def movement(self):
        #Makes movement appear more realistic
        # Add random displacement within the range [-0.5, 0.5]
        displacement = np.random.rand(2) - 0.5
        self.pos += displacement * 2  # adjust the scaling factor to control the amount of displacement
        

class MalariaModel:
    
    """
    Manages Mathematical formulaes for Malaria transmision in a periodic enviorment
    These determine the incidence which is deciding factor on what group people or mosquitoes are put into it after getting the parasite
    
    Args:
        human_population (int): number of total people in the simulation
        infected_population (int): number of total infected people in the simulation
        immune_class (int): #number of total immune people in the simulation
        TRANSMISSION_RATE (float): rate at which the disease transmits - default to 1.2 
        PROBABILITY_INFECTION (float): probability of getting malaria - default to 0.8
        BITING_RATE (float): rate at which mosqutioes bite people - default to 1.2
        SEMI_IMMUNE_PROBABILITY (float): probability of being semi immune - default to 0.2
    
    Returns:
        human_mosq (float): Incidence between Human to susceptible mosquito contact
        mosq_nonimmune (float): Incidence between mosquito to non immune person contact
        mosq_semi_immune (float): Incidence between mosquito to semi immune person contact
    """ 
    
    def __init__(self, human_population, infected_population, immune_class, TRANSMISSION_RATE, PROBABILITY_INFECTION, BITING_RATE, SEMI_IMMUNE_PROBABILITY):
        
        self.human_population = human_population
        self.infected_population = infected_population #infected_population
        self.immune_class = immune_class #Immune class
        
        self.TRANSMISSION_RATE = TRANSMISSION_RATE  # Transmission rate
        
        self.PROBABILITY_INFECTION = PROBABILITY_INFECTION # Probability of infection
        self.SEMI_IMMUNE_PROBABILITY = SEMI_IMMUNE_PROBABILITY
        self.BITING_RATE= BITING_RATE #Periodic biting Rate
        
    def human_to_mosquito(self):
        #Calculates Incidence between infected Human and susceptible mosquito 
        human_mosq = ((self.TRANSMISSION_RATE * self.BITING_RATE) * (self.infected_population / self.human_population)) + ((self.TRANSMISSION_RATE * self.BITING_RATE) * (self.infected_population / self.human_population))+ ((self.TRANSMISSION_RATE * self.BITING_RATE) * (self.immune_class / self.human_population))
        return human_mosq
    
    def mosquito_to_nonimmune(self):
        #Calculats Incidence between mosquito and nonimmune person
        mosq_nonimmune = ((self.PROBABILITY_INFECTION * self.BITING_RATE)*(self.infected_population / self.human_population))
        return mosq_nonimmune
    
    def mosquito_to_semi_immune(self):
        #Calculats Incidence between mosquito and semi immune person
        mosq_semi_immune = ((self.SEMI_IMMUNE_PROBABILITY*self.BITING_RATE)*(self.infected_population / self.human_population))
        return mosq_semi_immune

class Node:
    def __init__(self, time_step, population_data):
        self.time_step = time_step #increments each call in LineGraph.update()
        self.population_data = population_data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, time_step, population_data):
        new_node = Node(time_step, population_data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

class LineGraph:
    def __init__(self, graph_width, screen, width, height):
        """
        Initialises a graph and displays it and any changes onto the screen.
        
        Args:
            graph_width (int)
            screen (tuple): the pygame display which the objects are shown on
            width (int): the width of the screen
            height (int): height of the screen
        """ 
        self.font = pygame.font.SysFont(None, 30)
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.graph_width = graph_width
        self.data_max_length = graph_width // 6
        self.zoom = 1.0
        self.linkedlist = LinkedList()
        self.scroll = 0
        
        # Sets up the LinkedList data structure
        self.data = {}
        self.data["susceptible"] = [(50, 550)]
        self.data["semi_immune"] = [(50, 550)]
        self.data["infected"] = [(50, 550)]
        self.data["dead"] = [(50, 550)]
        self.data["male"] = [(50, 550)]
        self.data["immune"] = [(50, 550)]
        self.data["infected_mosquito"] = [(50, 550)]
        
        # Sets the position of the graph
        extra_padding = 530
        self.position = (screen.get_width() - graph_width + extra_padding, screen.get_height() - 600 - 50)
        
    def draw_axes(self):
            # Draw the y-axis
            x_axis_start = (830,850)
            x_axis_end = (1600,850)
            pygame.draw.line(self.screen, (255, 255, 255), x_axis_start, x_axis_end, 4)

            # Draw the x-axis
            y_axis_start = (900,850)
            y_axis_end = (900, 400)
            pygame.draw.line(self.screen, (255, 255, 255), y_axis_start, y_axis_end, 4)

            # Render and draw the "Population" label for the y-axis
            population_label = self.font.render("Population", True, (255, 255, 255))
            population_label_pos = (900, 380)
            self.screen.blit(population_label, population_label_pos)

            # Render and draw the "Time" label for the x-axis
            time_label = self.font.render("Time", True, (255, 255, 255))
            time_label_pos = (1200, 860)
            self.screen.blit(time_label, time_label_pos)
    
    def update(self, susceptible_count, semi_immune_count, infected_count, dead_count, male_count, immune_count, infected_mosquito_count):

        new_data = {
            "susceptible": susceptible_count,
            "semi_immune": semi_immune_count,
            "infected": infected_count,
            "dead": dead_count,
            "male": male_count,
            "immune": immune_count,
            "infected_mosquito": infected_mosquito_count
        }
        # Draw axes and labels
        self.draw_axes()
        
        # Update the graph data structure for each group
        self.linkedlist.append(self.linkedlist.length, new_data)
        
        #move the graph to prevent it going off the screen
        if self.linkedlist.length > self.data_max_length:
            self.scroll_right()

        # Draw the graph for each group
        current_node = self.linkedlist.head
        while current_node is not None and current_node.next is not None:
            next_node = current_node.next

            for group, color in [
                ("susceptible", SUSCEPTIBLE_PEOPLE_COL),
                ("semi_immune", SEMI_IMMUNE_COL),
                ("infected", INFECTED_PEOPLE_COL),
                ("dead", DEAD_COL),
                ("male", MALE_MOSQUITO_COL),
                ("immune", IMMUNE_COL),
                ("infected_mosquito", INFECTED_MOSQUITOES_COL),
            ]:
                #Marks where the graph starts
                p1 = (current_node.time_step - self.scroll*self.zoom , 650 - current_node.population_data[group]*self.zoom)
                p2 = (next_node.time_step - self.scroll*self.zoom, 650 - next_node.population_data[group]*self.zoom)

                # Adjust points based on the graph's position
                adjusted_p1 = (self.position[0] + 50 + p1[0], self.position[1] + p1[1]-  100)
                adjusted_p2 = (self.position[0] + 50 + p2[0], self.position[1] + p2[1] - 100)

                pygame.draw.line(self.screen, color, adjusted_p1, adjusted_p2, 2)

            current_node = next_node

    def scroll_right(self):
        # Scroll the graph to the right
        if self.linkedlist.length - self.scroll > self.data_max_length:
            self.scroll += 1
    
    def zoom_in(self):
        # Increase the zoom level by 0.1
        self.zoom = min(self.zoom + 0.1, 2)

    def zoom_out(self):
        # Decrease the zoom level by 0.1, but doesn't let it go below 0.1
        self.zoom = max(self.zoom - 0.1, 0.1)

class Simulation:
    
    _instance = None #detects if a instance of simulation already exists

    def __init__(self,n_susceptible_mosquito, n_infected_mosquito,n_male_mosquito,n_susceptible_people, n_infected_people,n_semi_immune, mortality_rate, width=1600, height=900, sim_width=800, sim_height=800):        
        """_summary_

        Args:
            n_susceptible_mosquito (int): number of susceptible mosquitoes
            n_infected_mosquito (int): number of infected mosuqitoes defined by user
            n_male_mosquito (int): number of male mosuqitoes defined by user
            n_susceptible_people (int): number of susceptible people defined by user
            n_infected_people (int): number of infected people defined by user
            n_semi_immune (int): number of semi immmune people  defined by user
            mortality_rate (float): mortalitlty rate defined by user
            width (int): width of screeen. Defaults to 1600.
            height (int): height of screen. Defaults to 900.
            sim_width (int): width of sim that the objects appear on. Defaults to 800.
            sim_height (int): height of sim that the objects appear on. Defaults to 800.
        """        
        self.WIDTH = width
        self.HEIGHT = height
        self.sim_height = sim_height
        self.sim_width = sim_width
        self.graph_width = self.WIDTH - self.sim_width - 100
        
        self.text_file = False
        #Surface which has the people rendered on it
        self.inner_surface = pygame.Surface((sim_width, sim_height))
        
        #Surface used to prevent the graph from showing behind the sim as it grows
        self.graph_block_surface = pygame.Surface((width - 700, height)) 
        
        
        try:
            pygame.font.init()

            font_file = "Anurati-Regular.otf"
            font = pygame.font.Font(font_file, 50)
            self.text = font.render("M O D E L L I N G  M A L A R I A", True, (255, 255, 255))
            self.text_rect = self.text.get_rect()
            self.text_rect.center = (self.WIDTH / 2, 30)
            self.text_file = True
        except FileNotFoundError:
            print("Font file not found.")

        try:
            icon = pygame.image.load("icon.png")
            pygame.display.set_icon(icon)
        except FileNotFoundError:
            print("Icon File Not Found")
        
        #A container class to hold and manage multiple Sprite objects in this case to manage each category of person and mosquito
        #pygame.sprite.Group objects act as a hashmap to all objects in the group
        self.susceptible_people_container = pygame.sprite.Group()
        self.semi_immune_container = pygame.sprite.Group()
        self.infected_people_container = pygame.sprite.Group()
        self.dead_container = pygame.sprite.Group()
        self.male_container = pygame.sprite.Group()
        self.immune_container = pygame.sprite.Group()
        self.susceptible_mosquito_container = pygame.sprite.Group()
        self.infected_mosquito_container = pygame.sprite.Group()
        self.all_container = pygame.sprite.Group()
        
        #Variables
        self.n_susceptible_mosquito = n_susceptible_mosquito
        self.n_infected_mosquito = n_infected_mosquito
        self.n_male_mosquito = n_male_mosquito
        self.n_susceptible_people = n_susceptible_people
        self.n_infected_people = n_infected_people
        self.n_semi_immune = n_semi_immune
        self.cycles_to_death = 5000
        self.mortality_rate = mortality_rate

        # Set the instance variable to the current instance
        Simulation._instance = self

    @classmethod
    def get_instance(cls):
        # Return the existing instance or create a new one
        if cls._instance is None:
            raise ValueError("Simulation instance not created")
        return cls._instance
    
    def start(self):
        
        #initiliases pygame window and display
        pygame.init()
        
        #calc total population
        self.total_population = self.n_susceptible_mosquito + self.n_infected_mosquito
        
        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        
        pygame.display.set_caption("Malaria Sim")
        
        #spawns the susceptible mosquitoes on screen
        for i in range(self.n_susceptible_people):
            person.spawn_people(self)
        
        #spawns the infected people on screen
        for i in range(self.n_infected_people):
            person.spawn_infected_people(self)
        
        #spawns infected mosquitoes on screen
        for i in range(self.n_infected_mosquito):
            Malaria.spawn_infected_mosquitoes(self)
        
        #spawns the male mosquitoes on screen
        for i in range(self.n_male_mosquito):
            Malaria.spawn_male_mosquitoes(self)
        #
        #spawns susceptible mosquitoes 
        for i in range(self.n_susceptible_mosquito):
            Malaria.spawn_susceptible_mosquitoes(self)
        
        #spawns semi immune mosquitoes
        for i in range(self.n_semi_immune):
            person.spawn_semi_immune(self)
        
        clock = pygame.time.Clock()
        self.graph = LineGraph(700, screen, self.WIDTH, self.HEIGHT) #assigns line graph a postiion

        T = True #game loop condition
        
        #loop which updates all movements to the display
        while T:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    T = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_EQUALS:
                        self.graph.zoom_in()
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        self.graph.zoom_out()

            screen.fill(BACKGROUND_COL)

            self.all_container.update()

            # Update the line graph with the counts for each group
            self.graph.update(len(self.susceptible_people_container), len(self.semi_immune_container), 
                                len(self.infected_people_container), len(self.dead_container), len(self.male_container), len(self.immune_container), len(self.infected_mosquito_container))
            
            self.graph_block_surface.fill(BACKGROUND_COL)
            screen.blit(self.graph_block_surface, (0,0))
            
            self.inner_surface.fill(INNER_SURFACE_COL )
            screen.blit(self.inner_surface, ((80, 80)))
            
            
            
            #detects collision between infected mosquitoes and suscpetible people 
            collision_group = pygame.sprite.groupcollide(self.susceptible_people_container,self.infected_mosquito_container,False,False)
            
            #initialises the MalariaModel class with all the required variables
            malaria = MalariaModel(human_population = len(self.all_container), infected_population = len(self.infected_people_container), immune_class = len(self.immune_container),
                                    TRANSMISSION_RATE = 1.2, PROBABILITY_INFECTION = 0.8, BITING_RATE = 1.2, SEMI_IMMUNE_PROBABILITY = 0.2)

            
            #Uses collision_group to make susceptible people infected
            for susceptible_people, infected_mosquitoes in collision_group.items():
                if susceptible_people or infected_mosquitoes not in self.immune_container:
                    incidence = malaria.mosquito_to_nonimmune()
                    if incidence < random.uniform(0,1): 
                        infected_people = susceptible_people.infect_person(INFECTED_PEOPLE_COL, radius = 5)
                        infected_people.vel *= -1 #makes people move away slighly as they would've felt the mosquito bit
                        infected_people.fatality(self.cycles_to_death, self.mortality_rate) #starts cycles to death count down
                        self.infected_people_container.add(infected_people)
                        self.all_container.add(infected_people) 
                        infected_people.update()
                        
            #used to detect collisions between containers in this case the susceptible mosquiton and infected people
            #and creates a dictionary with all those who've been in contact.
            collision_group = pygame.sprite.groupcollide(self.susceptible_mosquito_container,self.infected_people_container,False,False)
            
            #Determines whether a human infects a mosquito after a blood meal
            for susceptible_mosquitoes, infected_people in collision_group.items():
                if susceptible_mosquitoes or infected_people in self.immune_container:
                    incidence = malaria.human_to_mosquito() #Calculates Incidence
                    if incidence < random.uniform(0,1): 
                        #infects them if the incidence is greater than the number produced
                        infected_mosquitoes = susceptible_mosquitoes.infect_mosquito(INFECTED_MOSQUITOES_COL )
                        self.infected_mosquito_container.add(infected_mosquitoes)
                        self.all_container.add(infected_mosquitoes)
            
            
            to_remove = [] #objects are are going to be removed from their original container
            to_recover = []
            to_semi_immune = []
            
            #Loop which handles people who are going to die, recover or become semi-immune
            #by putting the people in the required list
            for infected_person in self.infected_people_container:
                if infected_person.recovered:
                    to_remove.append(infected_person)
                    to_recover.append(infected_person)
                elif infected_person.dead: 
                    to_remove.append(infected_person)
                    dead_person = infected_person.kill_person(self, DEAD_COL, vel=0)
                    self.dead_container.add(dead_person)
                elif infected_person.semi_immune:
                    to_remove.append(infected_person)
                    to_semi_immune.append(infected_person)
                    
            #Removes people from the infected container
            for people in to_remove:
                self.infected_people_container.remove(people)
                self.all_container.remove(people)
            
            #Makes people semi_immune and adds them to their specific container 
            for people in to_semi_immune:
                semi_immune_person = people.make_semi_immune(self, SEMI_IMMUNE_COL)
                self.semi_immune_container.add(semi_immune_person)
                self.all_container.add(semi_immune_person)
                
            #recovers people who've been added to the to_recover list
            for people in to_recover:
                recovered_person = people.recover(self, IMMUNE_COL)
                self.immune_container.add(recovered_person)
                self.all_container.add(recovered_person)

            #used to detect collisions between containers in this case the semi-immune and infected mosquitoes
            #and creates a dictionary with all those who've been in contact.
            collision_group = pygame.sprite.groupcollide(self.semi_immune_container,self.infected_mosquito_container,False,False)

            #Determines whether a semi_immune person gets infected again after an infected mosquito has a blood meal by looping over the dictionary
            for semi_immune_person, infected_mosquitoes in collision_group.items():
                if semi_immune_person or infected_mosquitoes not in self.immune_container:
                    incidence = malaria.mosquito_to_semi_immune() #calls the designated formulae to calc the incidence
                    if incidence < random.uniform(0,1): 
                        #infects them if the incidence is greater than the number produced
                        infected_people = semi_immune_person.infect_person(INFECTED_PEOPLE_COL, radius = 5) 
                        infected_people.vel *= -1
                        infected_people.fatality(self.cycles_to_death, self.mortality_rate) #starts cycles to death again
                        self.infected_people_container.add(infected_people)
                        self.all_container.add(infected_people)
                        infected_people.update()
            
            for i in self.all_container:
                #checks if the person is apart of an instance of the person clas
                if isinstance(i, person):
                    if i not in self.dead_container:
                        i.movement() #calls the movement funciton to simulate a realistic movement pattern
                
            if len(to_recover) > 0: #removes all the people in the recover container from other containers
                self.infected_people_container.remove(*to_recover)
                self.all_container.remove(*to_recover)
            
            
            
            

            # Create font object
            font = pygame.font.SysFont(None, 30)
            
            # Create list of text surfaces to display population counts
            text_surfaces = [
                font.render("Susceptible: " + str(len(self.susceptible_people_container)), True, (SUSCEPTIBLE_PEOPLE_COL)),
                font.render("Immune: " + str(len(self.immune_container)), True, (IMMUNE_COL)),
                font.render("Infected: " + str(len(self.infected_people_container)), True, (INFECTED_PEOPLE_COL)),
                font.render("Dead: " + str(len(self.dead_container)), True, (DEAD_COL)),
                font.render("Male Mosquitoes: " + str(len(self.male_container)), True, (MALE_MOSQUITO_COL)),
                font.render("Susceptible Mosquitoes: " + str(len(self.susceptible_mosquito_container)), True, (SUSCEPTIBLE_MOSQUITO_COL )),
                font.render("Infected Mosquitoes: " + str(len(self.infected_mosquito_container)), True, (INFECTED_MOSQUITOES_COL )),
                font.render("Semi Immune People: " + str(len(self.semi_immune_container)), True, (SEMI_IMMUNE_COL))
            ]
            text_surfaces.reverse()
            

            
            # Blit text surfaces onto screen surface
            for i, text_surface in enumerate(text_surfaces):
                screen.blit(text_surface, (self.sim_width + 100, self.HEIGHT - self.sim_height + 160 - i*30))
            
            if self.text_file == True:
                screen.blit(self.text, self.text_rect)
            
            # Draw all Objects on the Screen
            self.all_container.draw(screen)
            
            clock.tick(60)
            pygame.display.flip()

#takes in arguements from the config file and starts the simulation
def run_simulation(n_susceptible_mosquito, n_infected_mosquito, n_male_mosquito, n_susceptible_people, n_infected_people, n_semi_immune, mortality_rate):
    global CURRENT_SIMULATION 
    CURRENT_SIMULATION  = Simulation(n_susceptible_mosquito, n_infected_mosquito, n_male_mosquito, n_susceptible_people, n_infected_people, n_semi_immune, mortality_rate)
    CURRENT_SIMULATION.start()