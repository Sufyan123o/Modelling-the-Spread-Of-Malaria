import pygame
import numpy as np
import random
import pygame.math
import pygame.font
import math

#Constant colours to identify objects on screen 
SUSCEPTIBLE_PEOPLE_COL = (211,211,211)
SEMI_IMMUNE_COL = (255,192,203) #pink
INFECTED_PEOPLE_COL = (0, 255, 0) #infected people
DEAD_COL = (56, 26, 20) #black
IMMUNE_COL = (255, 165, 0) 
MALE_MOSQUITO_COL = (0, 100, 255) #BLUE
SUSCEPTIBLE_MOSQUITO_COL   = (50, 150, 50) #GREEN
INFECTED_MOSQUITOES_COL  = (255,0,0) #red
BACKGROUND_COL  = (25, 25, 34)  #Blue/grey
INNER_SURFACE_COL  = (33,33,45) #grey
CURRENT_SIMULATION  = None



class Malaria(pygame.sprite.Sprite):
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
        self.HEIGHT = height

        self.sim_width = 800
        self.sim_height = 800

        self.window_xpos = 80
        self.window_ypos = 80

        # Mosquito location assigned used a vector
        self.rect = self.image.get_rect()  # gets the position of the object on the screen.
        self.rect.x = random.randint(1, self.sim_width)
        self.rect.y = random.randint(1, self.sim_height)
        self.pos = self.rect.x, self.rect.y
        self.vel = np.asarray(velocity, dtype=np.float64)

        self.move = 2
        self.inside = None
        self.stay_time = 100
        self.line_to_dest = None

    def route(self, dest: tuple[int, int], set_home: bool) -> None:

<<<<<<< HEAD
        # Set a home which can be returned to
        if set_home:
            self.home = self.pos

        self.inside = dest

        x1, y1 = self.pos
        x2, y2 = self.inside

        i, j = x2 - x1, y2 - y1

        magnitude = math.sqrt(i**2 + j**2)
        

        try:
            # Vector on which mosquito should move to the destination
            self.vector = (i * self.vel) / magnitude, (j * self.vel) / magnitude
            self.line_to_dest = (self.pos, self.inside)
        except ZeroDivisionError:
            # Occurs when magnitude is so small float rounds to zero
            # This means mosquito is already next to the destination, so do not create route
            self.inside = None

    
    def update(self, inner_surface):
        # Add random displacement within the range [-1, 1]
=======
        #Movment model for Humans and Mosquitoes that adjusts the
        #way they behave whilsts moving around to make it more realistic
>>>>>>> 70d68d7e5ebfb76487a6575782dcdf9c8751d4d4
        displacement = np.random.rand(2) * 2 - 1
        self.pos += displacement * 1

        if self.inside is not None:
            inside_x, inside_x = self.inside
            dx, dy = self.pos
            dist = math.sqrt((inside_x - dx) ** 2 + (inside_x - dy) ** 2)
            
            delta_x = (inside_x - dx)
            delta_y = (inside_x - dy)
            new_pos = np.array([dx + delta_x, dy + delta_y], dtype=np.float64)

            # Draw line to show path
            pygame.draw.line(inner_surface, (255,255,255), self.pos, new_pos)

            # Update position of rect on surface
            self.rect.x = round(new_pos[0])
            self.rect.y = round(new_pos[1])
            self.pos = new_pos

            # Check if mosquito has reached its destination
            if dist < self.vel:
                self.inside = None
            pygame.draw.line(inner_surface, (255,255,255), self.pos, new_pos)
            
        else:
            # Randomly move mosquito
            self.pos += self.vel
            dx, dy = self.pos
            if dx < self.window_xpos:  # left boarder
                self.pos[0] = self.window_xpos + self.sim_width
            if dx > self.window_xpos + self.sim_width:  # right boarder
                self.pos[0] = self.window_xpos
            if dy < self.window_ypos:  # top boarder
                self.pos[1] = self.window_ypos + self.sim_height
            if dy > self.window_ypos + self.sim_height:  # bottom boarder
                self.pos[1] = self.window_ypos
            self.rect.x = round(self.pos[0])
            self.rect.y = round(self.pos[1])

            # Handles mosquitos making a person semi immune, recovered or killing them.
            semi_immune_probability = 0.2
            if self.fatality_on:
                self.cycles_to_death -= 10
                if self.cycles_to_death <= 0:
                    self.fatality_on = False
                    if self.mortality_rate > random.uniform(0, 1):
                        self.dead = True
                    elif semi_immune_probability > random.uniform(0, 1):
                        self.semi_immune = True
                    else:
                        self.recovered = True

        return False


    
    def infect_person(self, color, radius = 5):
        self.kill()
        infected_person = person(self.rect.x,self.rect.y,self.WIDTH,self.HEIGHT,color=color,velocity=self.vel, radius = radius)
        simulation = Simulation.get_instance()
        simulation.all_container.add(infected_person)
        return infected_person
    
    
    def spawn_mosquitoes(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1
        
        infected_mosquito = Malaria(x, y, self.WIDTH, self.HEIGHT, color = INFECTED_MOSQUITOES_COL , velocity = vel )
        
        self.infected_mosquito_container.add(infected_mosquito)
        
        self.all_container.add(infected_mosquito)
    
    def spawn_male_mosquitoes(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1
        np.random.rand(2)
        
        male_mosquito = Malaria(x, y, self.WIDTH, self.HEIGHT, color = MALE_MOSQUITO_COL, velocity = vel )
        
        self.male_container.add(male_mosquito)
        
        self.all_container.add(male_mosquito)
        
    def spawn_susceptible_mosquitoes(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1
        np.random.rand(2)
        
        suscpetible_mosquito = Malaria(x, y, self.WIDTH, self.HEIGHT, color = SUSCEPTIBLE_MOSQUITO_COL , velocity = vel )
        
        self.susceptible_mosquito_container.add(suscpetible_mosquito)
        
        self.all_container.add(suscpetible_mosquito)
    
    def fatality(self,cycles_to_death=1000, mortality_rate=0.2):
            self.fatality_on = True
            self.cycles_to_death = cycles_to_death
            self.mortality_rate = mortality_rate
            
    def infect_mosquito(self, color):
        self.kill()
        infected_mosquito = person(self.rect.x, self.rect.y, self.WIDTH, self.HEIGHT, color=color, velocity=self.vel, radius = 2)
        # infected_mosquito = Malaria(x, y, self.WIDTH, self.HEIGHT, color = INFECTED_MOSQUITOES_COL , velocity = vel )
        simulation = Simulation.get_instance()
        # Simulation.infected_mosquito_container.add(infected_mosquito)
        simulation.all_container.add(infected_mosquito)
        
        return infected_mosquito
    
    def insecticide(self):
        displacement = np.random.rand(2) - 0.5
        self.pos += displacement * 2  # adjust the scaling factor to control the amount of displacement
        # insectid

class person(Malaria, pygame.sprite.Sprite):
    def spawn_people(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1
        np.random.rand(2)
        susceptible_people = person(x, y, self.sim_width, self.sim_height, color = SUSCEPTIBLE_PEOPLE_COL, velocity = vel, radius = 5)
        
        self.susceptible_people_container.add(susceptible_people)
        self.all_container.add(susceptible_people)
        
    def spawn_semi_immune(self):
        x = np.random.randint(80, self.sim_width + 1)
        y = np.random.randint(80, self.sim_height + 1)
        vel = np.random.rand(2) * 2 - 1
        np.random.rand(2)
        semi_immmune = person(x, y, self.sim_width, self.sim_height, color = SEMI_IMMUNE_COL, velocity = vel, radius = 5)
        
        self.semi_immune_container.add(semi_immmune)
        self.all_container.add(semi_immmune)
    
    def make_semi_immune(self, simulation, color, radius = 5):
        self.kill()
        
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
        self.vel = 0
        dead_person = person(self.rect.x, self.rect.y, self.WIDTH, self.HEIGHT, color=color, velocity=self.vel, radius = radius)
        simulation.dead_container.add(dead_person)
        simulation.all_container.add(dead_person)
        return dead_person
    
    def movement(self):
            # Add random displacement within the range [-0.5, 0.5]
            displacement = np.random.rand(2) - 0.5
            self.pos += displacement * 2  # adjust the scaling factor to control the amount of displacement
            
    
    def simulate_gathering(self, group, num_people=5, duration=3000):
        # randomly select a small number of people
        selected_people = np.random.choice(group.sprites(), num_people, replace=False)

        # set their velocity to 0
        original_velocities = []
        for person in selected_people:
            original_velocities.append(person.vel)
            person.vel = np.array([0, 0])

        # pre-calculate the step size for all selected people
        step_sizes = []
        for person in selected_people:
            new_x = np.random.randint(80, self.sim_width + 1)
            new_y = np.random.randint(80, self.sim_height + 1)
            target_pos = np.array([new_x, new_y])
            displacement = target_pos - np.array([person.rect.x, person.rect.y])
            displacement_norm = np.linalg.norm(displacement)
            step_size = displacement / displacement_norm if displacement_norm > 0 else np.array([0, 0])
            step_sizes.append(step_size * 4)

        # start the countdown
        start_time = pygame.time.get_ticks()
        time_remaining = duration

        # loop until the duration has elapsed
        while time_remaining > 0:
            # update the positions of the selected people based on their new velocity
            for i, person in enumerate(selected_people):
                person.rect.x += step_sizes[i][0]
                person.rect.y += step_sizes[i][1]

            # update the remaining time
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            time_remaining = max(duration - elapsed_time, 0)

        # return their velocities back to the original values
        for i in range(len(selected_people)):
            selected_people[i].vel = original_velocities[i]

        # # update the display
        # self.inner_surface.fill(INNER_SURFACE_COL)
        # group.draw(self.inner_surface)





class IncidenceFormulae:
    def __init__(self, human_population, infected_population, immune_class, transmission_rate, probability_infection, biting_rate, semi_immune_probability):
        self.human_population = human_population
        self.infected_population = infected_population #infected_population
        self.immune_class = immune_class #Immune class
        
        self.transmission_rate = transmission_rate  # Transmission rate
        
        self.probability_infection = probability_infection # Probability of infection
        self.semi_immune_probability = semi_immune_probability
        self.biting_rate= biting_rate #Periodic biting Rate
        

    def human_to_mosquito(self):
        
        human_mosq = ((self.transmission_rate * self.biting_rate) * (self.infected_population / self.human_population)) + ((self.transmission_rate * self.biting_rate) * (self.infected_population / self.human_population))+ ((self.transmission_rate * self.biting_rate) * (self.immune_class / self.human_population))
        # print('human to mosquito: ',human_mosq)
        return human_mosq
    
    def mosquito_to_nonimmune(self):
        mosq_nonimmune = ((self.probability_infection * self.biting_rate)*(self.infected_population / self.human_population))
        # print('mosqutio to non immune: ',mosq_nonimmune)
        
        return mosq_nonimmune
    
    def mosquito_to_semi_immune(self):
        mosq_semi_immune = ((self.semi_immune_probability*self.biting_rate)*(self.infected_population / self.human_population))
        # print('mosquito to semi immune: ',mosq_semi_immune)
        return mosq_semi_immune


class Graph:
    def __init__(self, graph_width, screen, width, height):
        self.font = pygame.font.SysFont(None, 30)
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.graph_width = graph_width
        self.data_max_length = graph_width // 6
        self.zoom = 1.0
        self.last_update_time = 0
        
        # Set up the graph data structure
        self.data = {}
        self.data["susceptible"] = [(50, 550)]
        self.data["semi_immune"] = [(50, 550)]
        self.data["infected"] = [(50, 550)]
        self.data["dead"] = [(50, 550)]
        self.data["male"] = [(50, 550)]
        self.data["immune"] = [(50, 550)]
        self.data["infected_mosquito"] = [(50, 550)]
        
        # Set the position of the graph to the bottom right corner of the screen
        self.position = (screen.get_width() - graph_width, screen.get_height() - 600 - 50)


    def update(self, susceptible_count, semi_immune_count, infected_count, dead_count, male_count, immune_count, infected_mosquito_count):
        # Clear the graph surface for the graph display
        self.screen.fill(INNER_SURFACE_COL , (self.position[0], self.position[1], self.graph_width, 600))

        # Draw the x-axis and y-axis
        pygame.draw.line(self.screen, (255, 255, 255), (self.position[0] + 50, self.position[1] + 550), (self.position[0] + 750, self.position[1] + 550), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (self.position[0] + 50, self.position[1] + 550), (self.position[0] + 50, self.position[1] + 50), 2)

        text = self.font.render('Time', True, (255, 255, 255))
        self.screen.blit(text, (self.position[0] + 200, self.position[1] + 570))

        text = self.font.render('Population', True, (255, 255, 255))
        text = pygame.transform.rotate(text, 90)
        self.screen.blit(text, (self.position[0] + 20, self.position[1] + 300))

        # Generate new data points for each group
        new_data = {}
        new_data["susceptible"] = susceptible_count
        new_data["semi_immune"] = semi_immune_count
        new_data["infected"] = infected_count
        new_data["dead"] = dead_count
        new_data["male"] = male_count
        new_data["immune"] = immune_count
        new_data["infected_mosquito"] = infected_mosquito_count

        # Update the graph data structure for each group
        for group, count in new_data.items():
            self.data[group].append((self.data[group][-1][0] + 6, 550 - count))
            if len(self.data[group]) > self.data_max_length:
                self.data[group].pop(0)

            # Draw the graph for each group
            if len(self.data[group]) > 1:
                # Scale the points to fit within the graph width and height
                x_min = self.data[group][0][0]
                x_max = self.data[group][-1][0]
                y_min = min(p[1] for p in self.data[group])
                y_max = max(p[1] for p in self.data[group])
                x_range = x_max - x_min
                y_range = y_max - y_min
                if x_range > 0 and y_range > 0:
                    # Scale the x and y values by the current zoom level
                    x_scale = ((750 - 50) / x_range) * self.zoom
                    y_scale = ((550 - 50) / y_range) * self.zoom
                    scaled_points = [(self.position[0] + 50 + int((p[0] - x_min) * x_scale), self.position[1] + 550 - int((p[1] - y_min) * y_scale)) for p in self.data[group]]

                    # Draw the scaled points as a line for each group
                    if group == "susceptible":
                        color = SUSCEPTIBLE_PEOPLE_COL
                    elif group == "semi_immune":
                        color = SEMI_IMMUNE_COL
                    elif group == "infected":
                        color = INFECTED_PEOPLE_COL
                    elif group == "dead":
                        color = DEAD_COL
                    elif group == "male":
                        color = MALE_MOSQUITO_COL
                    elif group == "immune":
                        color = IMMUNE_COL
                    elif group == "infected_mosquito":
                        color = INFECTED_MOSQUITOES_COL 
                    pygame.draw.lines(self.screen, color, False, scaled_points, 2)


    def zoom_in(self):
        # Increase the zoom level by 0.1
        self.zoom = min(self.zoom + 0.1, 1)

    def zoom_out(self):
        # Decrease the zoom level by 0.1, but don't let it go below 0.1
        self.zoom = max(self.zoom - 0.1, 0.1)

class Simulation:
    
    _instance = None

    def __init__(self,n_susceptible_mosquito, n_infected_mosquito,n_male_mosquito,n_susceptible_people, n_infected_people,n_semi_immune, mortality_rate, width=1600, height=900, sim_width=800, sim_height=800):
        self.WIDTH = width
        self.HEIGHT = height
        self.sim_height = sim_height
        self.sim_width = sim_width
        self.graph_width = self.WIDTH - self.sim_width - 100
        
        
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
        self.semi_immune_container = pygame.sprite.Group()
        self.infected_people_container = pygame.sprite.Group()
        self.dead_container = pygame.sprite.Group()
        self.male_container = pygame.sprite.Group()
        self.immune_container = pygame.sprite.Group()
        self.susceptible_mosquito_container = pygame.sprite.Group()
        self.infected_mosquito_container = pygame.sprite.Group()
        self.all_container = pygame.sprite.Group()
        
        # config = open("config.py", "r")

        
        #Variables
        self.n_susceptible_mosquito = n_susceptible_mosquito
        self.n_infected_mosquito = n_infected_mosquito
        self.n_male_mosquito = n_male_mosquito
        self.n_susceptible_people = n_susceptible_people
        self.n_infected_people = n_infected_people
        self.n_semi_immune = n_semi_immune
        self.cycles_to_death = 1000
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

        
        
        #loop which moves the susceptible mosquitoes on screen
        for i in range(self.n_susceptible_people):
            person.spawn_people(self)
        
        #loop which moves non infected mosquitoes on screen
        for i in range(self.n_infected_mosquito):
            Malaria.spawn_mosquitoes(self)
        
        for i in range(self.n_male_mosquito):
            Malaria.spawn_male_mosquitoes(self)
        
        for i in range(self.n_susceptible_mosquito):
            Malaria.spawn_susceptible_mosquitoes(self)
            
        for i in range(self.n_semi_immune):
            person.spawn_semi_immune(self)
        
        clock = pygame.time.Clock()
        self.graph = Graph(700, screen, self.WIDTH, self.HEIGHT)

        T = True
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

            self.all_container.update(inner_surface=self.inner_surface)

            
            self.inner_surface.fill(INNER_SURFACE_COL )
            screen.blit(self.inner_surface, ((80, 80)))
            
            #detects collision between infected mosq and suscpetible person and moves it to the infected container
            collision_group = pygame.sprite.groupcollide(self.susceptible_people_container,self.infected_mosquito_container,False,False)
            
            malaria = IncidenceFormulae(human_population = len(self.all_container), infected_population = len(self.infected_people_container), immune_class = len(self.immune_container),
                                   transmission_rate = 1.2, probability_infection = 0.8, biting_rate = 1.2, semi_immune_probability = 10)

            
            #Uses collision_group to make susceptible people infected by mosquitoes
            for susceptible_people, infected_mosquitoes in collision_group.items():
                if susceptible_people or infected_mosquitoes not in self.immune_container:
                    incidence = malaria.mosquito_to_nonimmune()
                    if incidence < random.uniform(0,1):
                        infected_people = susceptible_people.infect_person(INFECTED_PEOPLE_COL, radius = 5)
                        infected_people.vel *= -1
                        infected_people.fatality(self.cycles_to_death, self.mortality_rate)
                        self.infected_people_container.add(infected_people)
                        self.all_container.add(infected_people)
                        infected_people.update(inner_surface=self.inner_surface)

            
            
            
            
            #Uses Collision group to make susceptible mosquitoes infected by susceptible people.
            collision_group = pygame.sprite.groupcollide(self.susceptible_mosquito_container,self.infected_people_container,False,False)
            
            #Determines whether a human infects a mosquito after a blood meal
            for susceptible_mosquitoes, infected_people in collision_group.items():
                if susceptible_mosquitoes or infected_people in self.immune_container:
                    incidence = malaria.human_to_mosquito() #Calculates Incidence
                    if incidence < random.uniform(0,1):
                        infected_mosquitoes = susceptible_mosquitoes.infect_mosquito(INFECTED_MOSQUITOES_COL )
                        self.infected_mosquito_container.add(infected_mosquitoes)
                        self.all_container.add(infected_mosquitoes)
            
            
            # Select the first 5 people in the susceptible_people_container group
            selected_group = pygame.sprite.Group(list(self.susceptible_people_container)[:5])
            # person_instance = person()

            for i in selected_group:
                person.simulate_gathering(self, selected_group)

            
            
            to_remove = []
            to_recover = []
            to_semi_immune = []
            
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
                    

            for people in to_remove:
                self.infected_people_container.remove(people)
                self.all_container.remove(people)

            for people in to_semi_immune:
                semi_immune_person = people.make_semi_immune(self, SEMI_IMMUNE_COL)
                self.semi_immune_container.add(semi_immune_person)
                self.all_container.add(semi_immune_person)
                
                
            for people in to_recover:
                recovered_person = people.recover(self, IMMUNE_COL)
                self.immune_container.add(recovered_person)
                self.all_container.add(recovered_person)

            collision_group = pygame.sprite.groupcollide(self.semi_immune_container,self.infected_mosquito_container,False,False)

            #Determines whether a semi_immune person gets infected again after an infected mosquito has a blood meal
            for semi_immune_person, infected_mosquitoes in collision_group.items():
                if semi_immune_person or infected_mosquitoes not in self.immune_container:
                    incidence = malaria.mosquito_to_semi_immune()
                    if incidence < random.uniform(0,1):
                        infected_people = semi_immune_person.infect_person(INFECTED_PEOPLE_COL, radius = 5)
                        infected_people.vel *= -1
                        infected_people.fatality(self.cycles_to_death, self.mortality_rate)
                        self.infected_people_container.add(infected_people)
                        self.all_container.add(infected_people)
                        infected_people.update(inner_surface=self.inner_surface)
            
            for i in self.all_container:
                if isinstance(i, person):
                    if i not in self.dead_container:
                        i.movement()
                
            
            
                
            if len(to_recover) > 0:
                self.infected_mosquito_container.remove(*to_recover)
                self.all_container.remove(*to_recover)
            
            
            # Update the graph with the counts for each group
            self.graph.update(len(self.susceptible_people_container), len(self.semi_immune_container), 
                                len(self.infected_people_container), len(self.dead_container), len(self.male_container), len(self.immune_container), len(self.infected_mosquito_container))
                
            # Create font object
            font = pygame.font.SysFont(None, 30)
            
            # Create list of text surfaces
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
            screen.blit(self.text, self.text_rect)
            

            
            # draw the simulation and the real-time graph on the same Pygame window
            frame_rate = "Frame Rate: " + str(int(clock.get_fps()))
            frame_rate_surface = font.render(frame_rate, True, (255, 255, 255))
            screen.blit(frame_rate_surface, (10, 10))
            
            # Draw all Objects on the Screen
            self.all_container.draw(screen)
            
            clock.tick(60)
            pygame.display.flip()


def run_simulation(n_susceptible_mosquito, n_infected_mosquito, n_male_mosquito, n_susceptible_people, n_infected_people, n_semi_immune, mortality_rate):
    global CURRENT_SIMULATION 
    CURRENT_SIMULATION  = Simulation(n_susceptible_mosquito, n_infected_mosquito, n_male_mosquito, n_susceptible_people, n_infected_people, n_semi_immune, mortality_rate)
    CURRENT_SIMULATION.start()



# if __name__ == "__main__":
#     malaria = Simulation()
#     malaria.start()



