import tkinter as tk
from tkinter import END, Text
import math
import main
import sys

class SimulationInputs:
    def __init__(self, susceptible_mosquito, infected_mosquito, male_mosquito,
                    susceptible_people, infected_people, semi_immune, mortality_rate):
        self.susceptible_mosquito = susceptible_mosquito
        self.infected_mosquito = infected_mosquito
        self.male_mosquito = male_mosquito
        self.susceptible_people = susceptible_people
        self.infected_people = infected_people
        self.semi_immune = semi_immune
        self.mortality_rate = mortality_rate
        
    def set_inputs(self, susceptible_mosquito, infected_mosquito, male_mosquito,
                   susceptible_people, infected_people, semi_immune, mortality_rate):
        self.susceptible_mosquito = susceptible_mosquito
        self.infected_mosquito = infected_mosquito
        self.male_mosquito = male_mosquito
        self.susceptible_people = susceptible_people
        self.infected_people = infected_people
        self.semi_immune = semi_immune
        self.mortality_rate = mortality_rate
        
class MosquitoSimulationInputs(SimulationInputs):
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0, 0, 0.0)

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mosquito Simulation Inputs")
        self.geometry("400x900")
        self.text_primes = Text(self)

        self.label_mosquito_susceptible = tk.Label(self, text="Number of susceptible mosquitoes:")
        self.label_mosquito_infected = tk.Label(self, text="Number of infected mosquitoes:")
        self.label_mosquito_male = tk.Label(self, text="Number of male mosquitoes:")
        self.label_people_susceptible = tk.Label(self, text="Number of susceptible people:")
        self.label_people_infected = tk.Label(self, text="Number of infected people:")
        self.label_semi_immune = tk.Label(self, text="Number of semi-immune people:")
        self.label_mortality_rate = tk.Label(self, text="Mortality rate:")
        self.label_factorial = tk.Label(self, text="Factorial:")
        self.label_fibonacci = tk.Label(self, text="Fibonacci sequence:")
        self.label_primes = tk.Label(self, text="Prime numbers up to:")

        self.scale_mosquito_susceptible = tk.Scale(self, from_=0, to=250, orient=tk.HORIZONTAL)
        self.scale_mosquito_infected = tk.Scale(self, from_=100, to=250, orient=tk.HORIZONTAL)
        self.scale_mosquito_male = tk.Scale(self, from_=0, to=250, orient=tk.HORIZONTAL)
        self.scale_people_susceptible = tk.Scale(self, from_=0, to=250, orient=tk.HORIZONTAL)
        self.scale_people_infected = tk.Scale(self, from_=0, to=250, orient=tk.HORIZONTAL)
        self.scale_semi_immune = tk.Scale(self, from_=100, to=250, orient=tk.HORIZONTAL)
        self.scale_mortality_rate = tk.Scale(self, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
        self.scale_factorial = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.scale_fibonacci = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.scale_primes = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)

        self.button_submit = tk.Button(self, text="Submit", command=self.submit_inputs_callback)
        self.button_factorial = tk.Button(self, text="Calculate factorial", command=self.calculate_factorial)
        self.button_fibonacci = tk.Button(self, text="Generate Fibonacci sequence", command=self.generate_fibonacci)
        self.button_primes = tk.Button(self, text="Generate prime numbers", command=self.generate_primes)

        self.label_mosquito_susceptible.pack()
        self.scale_mosquito_susceptible.pack()
        self.label_mosquito_infected.pack()
        self.scale_mosquito_infected.pack()
        self.label_mosquito_male.pack()
        self.scale_mosquito_male.pack()
        self.label_people_susceptible.pack()
        self.scale_people_susceptible.pack()
        self.label_people_infected.pack()
        self.scale_people_infected.pack()
        self.label_semi_immune.pack()
        self.scale_semi_immune.pack()
        self.label_mortality_rate.pack()
        self.scale_mortality_rate.pack()
        self.label_factorial.pack()
        self.scale_factorial.pack()
        self.button_factorial.pack()
        self.label_fibonacci.pack()
        self.scale_fibonacci.pack()
        self.button_fibonacci.pack()
        self.label_primes.pack()
        self.scale_primes.pack()
        self.button_primes.pack()
        self.button_submit.pack()

        self.inputs = MosquitoSimulationInputs()
        
    def submit_inputs_callback(self):
        self.submit_inputs()
    


    def submit_inputs(self):
        n_susceptible_mosquito = self.scale_mosquito_susceptible.get()
        n_infected_mosquito = self.scale_mosquito_infected.get()
        n_male_mosquito = self.scale_mosquito_male.get()
        n_susceptible_people = self.scale_people_susceptible.get()
        n_infected_people = self.scale_people_infected.get()
        n_semi_immune = self.scale_semi_immune.get()
        mortality_rate = self.scale_mortality_rate.get()
        
        # Call function to run simulation with input values
        
        main.run_simulation(n_susceptible_mosquito, n_infected_mosquito, n_male_mosquito, n_susceptible_people, n_infected_people, n_semi_immune, mortality_rate)

        Window.destroy(self)
        sys.exit(Window)

    def calculate_factorial(self):
        n = self.scale_factorial.get()
        result = math.factorial(n)
        # Delete any existing text in the text widget.
        self.text_primes.delete("1.0", END)
        
        # Insert the factorial into the text widget.
        self.text_primes.insert(END, f"{n}! = {result}")
        
        # Pack the text widget into the window.
        self.text_primes.pack()


    def generate_fibonacci(self):
        n = self.scale_fibonacci.get()
        sequence = [0, 1]
        for i in range(2, n+1):
            sequence.append(sequence[i-1] + sequence[i-2])
        # print(f"Fibonacci sequence up to {n}: {sequence}")
        
        # Convert the list of primes to a string.
        sequence_str = ", ".join(str(p) for p in sequence)
        # Delete any existing text in the text widget.
        self.text_primes.delete("1.0", END)
        # Insert the list of primes into the text widget.
        self.text_primes.insert(END, f"Fibonacci sequence up to  {n}: {sequence_str}")
        self.text_primes.pack()
    
    def generate_primes(self):
        # Get the maximum value of n from the GUI.
        n = self.scale_primes.get()
        
        # Create an empty list to store the prime numbers.
        primes = []
        
        # Iterate over all numbers from 2 to n.
        for i in range(2, n+1):
            # Assume that i is a prime number until proven otherwise.
            is_prime = True
            
            # Check all numbers from 2 to sqrt(i) to see if they divide i.
            for j in range(2, int(math.sqrt(i))+1):
                if i % j == 0:
                    # If j divides i, then i is not a prime number.
                    is_prime = False
                    
                    # We don't need to check any more factors since we know it's not a prime.
                    # Commenting out the following line since it is no longer needed:
                    # break
            
            # If i is prime, add it to the list of primes.
            if is_prime:
                primes.append(i)
        
        # Convert the list of primes to a string.
        primes_str = ", ".join(str(p) for p in primes)
        
        # Delete any existing text in the text widget.
        self.text_primes.delete("1.0", END)
            
        # Insert the list of primes into the text widget.
        self.text_primes.insert(END, f"Prime numbers up to {n}: {primes_str}")
        
        self.text_primes.pack()




if __name__  == "__main__":
    window = Window()
    window.mainloop()
    
#     The three new buttons and scales added in the modified code are not directly related to the simulation of malaria spread in a pygame visualization.
# However, they can be used to generate input parameters for the simulation.

# For example, the generate_primes() method can be used to generate a list of possible values for the number of susceptible mosquitoes, 
# infected mosquitoes, susceptible people, and infected people. The generate_fibonacci() method can be used to generate a list of possible
# values for the mortality rate parameter.

## These generated values can be used as input parameters for your malaria spread simulation in pygame. By changing the values of the scales
# and clicking the buttons to generate different input values, you can explore how different values of input parameters can affect the spread of
# malaria in your simulation. This allows you to explore the behavior of your simulation under different scenarios and make informed decisions about
# which input parameters to use to accurately model the spread of malaria.