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
    def __init__(self, x, y, width, height, color=dead_col, radius=2, velocity=[0, 0]):
        super().__init__()
        # Creates Mosquitoes
        self.image = pygame.Surface([radius * 2, radius * 2]).convert_alpha()
        self.image.fill(inner_surface_col)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.x = x
        self.y = y

        # Mosquito location assigned used a vector
        self.rect = self.image.get_rect()  # gets the position of the object on the screen.
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.asarray(velocity, dtype=np.float64)

        self.fatality_on = False
        self.recovered = False
        self.dead = False

        self.WIDTH = width
        self.HEIGHT = height

        self.sim_width = 800
        self.sim_height = 800

        self.window_xpos = 80
        self.window_ypos = 80
        
        self.move = 2

    def update(self, radius=5):
        # Assigns a speed to the position vector
        self.pos += self.vel

        # Add random displacement within the range [-1, 1]
        displacement = np.random.rand(2) * 2 - 1
        self.pos += displacement * 0.1

        # Position vector
        dx, dy = self.pos

        # Periodic boundary conditions to prevent objects going off the screen
        # if the person goes off screen it puts them on the other side
        if dx < self.window_xpos:  # left boarder
            self.pos[0] = self.window_xpos + self.sim_width
            dx = self.window_xpos + self.sim_width
        if dx > self.window_xpos + self.sim_width:  # right boarder
            self.pos[0] = self.window_xpos
            dx = self.window_xpos
        if dy < self.window_ypos:  # top boarder
            self.pos[1] = self.window_ypos + self.sim_height
            dy = self.window_ypos + self.sim_height
        if dy > self.window_ypos + self.sim_height:  # bottom boarder
            self.pos[1] = self.window_ypos
            dy = self.window_ypos

        self.rect.x = dx
        self.rect.y = dy

        if self.fatality_on:
            self.cycles_to_death -= 10
            if self.cycles_to_death <= 0:
                self.fatality_on = False
                if self.mortality_rate > random.uniform(0, 1):
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
    
    def insecticide(self):
        displacement = np.random.rand(2) - 0.5
        self.pos += displacement * 2  # adjust the scaling factor to control the amount of displacement
        # insectid

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
        simulation.dead_container.add(dead_person)
        simulation.all_container.add(dead_person)
        
        
        return dead_person
    
    def movement(self):
            # Add random displacement within the range [-0.5, 0.5]
            displacement = np.random.rand(2) - 0.5
            self.pos += displacement * 2  # adjust the scaling factor to control the amount of displacement

class MalariaModel:
    def __init__(self, human_population, infected_population, immune_class, transmission_rate, probability_infection, biting_rate):
        self.human_population = human_population
        self.infected_population = infected_population #infected_population
        self.immune_class = immune_class #Immune class
        
        self.transmission_rate = transmission_rate  # Transmission rate
        
        self.probability_infection = probability_infection # Probability of infection
        self.biting_rate= biting_rate #Periodic biting Rate
        

    def human_to_mosquito(self):
        
        human_mosq = ((self.transmission_rate * self.biting_rate) * (self.infected_population / self.human_population)) + ((self.transmission_rate * self.biting_rate) * (self.infected_population / self.human_population))+ ((self.transmission_rate * self.biting_rate) * (self.immune_class / self.human_population))
        print('Human to Mosquito',human_mosq)
        return human_mosq
    
    def mosquito_to_nonimmune(self):
        mosq_nonimmune = ((self.probability_infection * self.biting_rate)*(self.infected_population / self.human_population))
        print('Mosquito to Human', mosq_nonimmune)
        return mosq_nonimmune
    
    def mosquito_to_semi_immune(self):
        pass


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
        self.screen.fill(inner_surface_col, (self.position[0], self.position[1], self.graph_width, 600))

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
                        color = susceptible_people_col
                    elif group == "semi_immune":
                        color = semi_immune_col
                    elif group == "infected":
                        color = infected_people_col
                    elif group == "dead":
                        color = dead_col
                    elif group == "male":
                        color = male_mosq_col
                    elif group == "immune":
                        color = immune_col
                    elif group == "infected_mosquito":
                        color = infected_mosquitoes_col
                    pygame.draw.lines(self.screen, color, False, scaled_points, 2)


    def zoom_in(self):
        # Increase the zoom level by 0.1
        self.zoom = min(self.zoom + 0.1, 1)

    def zoom_out(self):
        # Decrease the zoom level by 0.1, but don't let it go below 0.1
        self.zoom = max(self.zoom - 0.1, 0.1)

class Simulation:
    def __init__(self, width=1600, height=900, sim_width=800, sim_height=800):
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
            mosquito.spawn_mosquitoes(self)
        
        for i in range(self.n_male_mosquito):
            mosquito.spawn_male_mosquitoes(self)
        
        for i in range(self.n_susceptible_mosquito):
            mosquito.spawn_susceptible_mosquitoes(self)
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

            screen.fill(background_col)
            
            

            self.all_container.update()
            
            
            self.inner_surface.fill(inner_surface_col)
            screen.blit(self.inner_surface, ((80, 80)))
            
            #detects collision between infected mosq and suscpetible person and moves it to the infected container
            collision_group = pygame.sprite.groupcollide(self.susceptible_people_container,self.infected_mosquito_container,False,False)
            
            malaria = MalariaModel(human_population = len(self.all_container), infected_population = len(self.infected_people_container), immune_class = len(self.immune_container),
                                   transmission_rate = 1.2, probability_infection = 0.8, biting_rate = 1.2)

            
            #Uses collision_group to make susceptible people infected by mosquitoes
            for susceptible_people, infected_mosquitoes in collision_group.items():
                if susceptible_people or infected_mosquitoes not in self.immune_container:
                    incidence = malaria.mosquito_to_nonimmune()
                    if incidence < 10:
                        infected_people = susceptible_people.infect_person(infected_people_col, radius = 5)
                        infected_people.vel *= -1
                        infected_people.fatality(self.cycles_to_death, self.mortality_rate)
                        self.infected_people_container.add(infected_people)
                        self.all_container.add(infected_people)
                        infected_people.update()

            
            #Uses Collision group to make susceptible mosquitoes infected by susceptible people.
            collision_group = pygame.sprite.groupcollide(self.susceptible_mosquito_container,self.infected_people_container,False,False)
            
            for susceptible_mosquitoes, infected_people in collision_group.items():
                if susceptible_mosquitoes or infected_people in self.immune_container:
                    incidence = malaria.human_to_mosquito()
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

            for i in self.all_container:
                if isinstance(i, person):
                    if i not in self.dead_container:
                        i.movement()
                
            # Draw all Objects on the Screen
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
                font.render("Susceptible Mosquitoes: " + str(len(self.susceptible_mosquito_container)), True, (susceptible_mosquito_col)),
                font.render("Infected Mosquitoes: " + str(len(self.infected_mosquito_container)), True, (infected_mosquitoes_col)),
            ]
            text_surfaces.reverse()
            

            
            # Blit text surfaces onto screen surface
            for i, text_surface in enumerate(text_surfaces):
                screen.blit(text_surface, (self.sim_width + 100, self.HEIGHT - self.sim_height + 160 - i*30))
            screen.blit(self.text, self.text_rect)
            
            # Update the graph with the counts for each group
            self.graph.update(len(self.susceptible_people_container), len(self.semi_immune_people_container), 
                              len(self.infected_people_container), len(self.dead_container), len(self.male_container), len(self.immune_container), len(self.infected_mosquito_container))
            
            # draw the simulation and the real-time graph on the same Pygame window
            frame_rate = "Frame Rate: " + str(int(clock.get_fps()))
            frame_rate_surface = font.render(frame_rate, True, (255, 255, 255))
            screen.blit(frame_rate_surface, (10, 10))
            clock.tick(60)
            pygame.display.flip()


if __name__ == "__main__":
    malaria = Simulation()
    malaria.start()



