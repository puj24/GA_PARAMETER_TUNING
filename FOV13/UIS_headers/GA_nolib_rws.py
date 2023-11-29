import numpy as np
import subprocess
import math
# Define the number of constants (genes) to generate number of
num_constants = 5

# Define the gene bounds
gene_bounds = [
    np.linspace(-7, 0),  # log delta
    np.linspace(-4, 3),  # TOL
    np.linspace(25, 50),  # P1
    np.linspace(70, 90),  # P2
    np.linspace(0.001, 0.01)  # EPSILON_SEQ_ERROR
]

# Define the target outputs
desired_outputs = np.loadtxt("out_ideal.txt", dtype=float)
desired_outputs = desired_outputs.reshape(5, 4)

# Define the C program command
c_program_command_1 = "gcc main.c -o exe -lm"
c_program_command_2 = "./exe"

# Convert gene_bounds to a np array
gene_space = np.array(gene_bounds)

def quaternion_to_euler(q):
    # Extract individual quaternion components
    q0, q1, q2, q3 = q

    # Calculate roll (x-axis rotation)
    roll = math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1**2 + q2**2))

    # Calculate pitch (y-axis rotation)
    sinp = 2 * (q0 * q2 - q3 * q1)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp)
    else:
        pitch = math.asin(sinp)

    # Calculate yaw (z-axis rotation)
    yaw = math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2**2 + q3**2))

    # Convert angles to degrees
    roll = math.degrees(roll)
    pitch = math.degrees(pitch)
    yaw = math.degrees(yaw)

    return roll, pitch, yaw

def cal_fitness(q1, q2):
    # Convert quaternions to Euler angles
    roll1, pitch1, yaw1 = quaternion_to_euler(q1)
    roll2, pitch2, yaw2 = quaternion_to_euler(q2)

    # Calculate angular difference in each axis
    roll_diff = abs(roll1 - roll2)
    pitch_diff = abs(pitch1 - pitch2)
    yaw_diff = abs(yaw1 - yaw2)

    # Convert angular difference to arc seconds (1 degree = 3600 arc seconds)
    roll_diff_arcsec = roll_diff * 3600
    pitch_diff_arcsec = pitch_diff * 3600
    yaw_diff_arcsec = yaw_diff * 3600
    print(max(roll_diff_arcsec, pitch_diff_arcsec, yaw_diff_arcsec)*1e5)
    return max(roll_diff_arcsec, pitch_diff_arcsec, yaw_diff_arcsec)*1e5


# Evaluate the fitness for each test case
def fitness_func(solution):
    # Create a header file with the current solution's parameters
    with open("constants.h", "w") as file:
        file.write("#include <stdio.h>\n")
        # Write constants based on the solution
        for i, param_range in enumerate(gene_bounds):
            file.write("#include <stdio.h>\n")
            file.write("#include <stdlib.h>\n")
            file.write("#include <math.h>\n")
            file.write("#include <string.h>\n")
            # Generate multiple constants based on the solution's genes
            #file.write("#define THRESHOLD 3\n")
            file.write("#define STAR_MIN_PIXEL 3\n")
            file.write("#define STAR_MAX_PIXEL 150\n")
            file.write("#define MAX_STARS 100\n")
            file.write("#define SKIP_PIXELS 2\n")
            file.write("#define LENGTH 1820\n")
            file.write("#define BREADTH 1820\n")     
            file.write("#define PIXEL_WIDTH 1.55e-6\n")
            file.write("#define NUM_MAX_STARS 13\n")
            file.write("//SM constants\n")
            file.write("#define FOCAL_LENGTH 0.0175\n")
            #file.write("#define EPSILON 2.2e-15\n")
            file.write("#define EPSILON 2.22e-15\n")
            file.write("#define DELTA {}\n".format(10**solution[0]))
            file.write("#define ANG_DIST_TOLERANCE 1.2\n")
            file.write("#define N_GC 8876\n")
            file.write("#define N_KVEC_PAIRS 625957\n")
            file.write("#define Y_MAX 0.999999999992621\n")
            file.write("#define Y_MIN 0.971731093094223\n")
            file.write("#define TOL {}\n".format(10**solution[1]))
            file.write("#define P1 {}\n".format(solution[2]))
            file.write("#define P2 {} \n".format(solution[3]))
            file.write("#define EPSILON_SEQ_ERROR {} \n".format(solution[4])) 
            file.write("#define EPSILON_EST 0.001 \n")
    
    subprocess.run(c_program_command_1, shell=True)

    # Run the C program and collect the output
    process = subprocess.Popen(c_program_command_2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode().strip()
    output = list(filter(None, output.split('\n')))
    print(output)

    # Calculate the fitness based on the differences between desired and obtained coordinates
    output_coordinates = np.array([list(map(float, line.split())) for line in output])

    fitness =[]
    for i in range(desired_outputs.shape[0]):
        desired_row = desired_outputs[i, :]
        obtained_row = output_coordinates[i, :]
        fitness.append(cal_fitness(desired_row, obtained_row))

    least_fitness=min(fitness)
    return least_fitness

# Define uniform crossover function
def uniform_crossover(parent1, parent2):
    child = np.empty(len(parent1))
    for i in range(len(parent1)):
        if np.random.rand() < 0.5:
            child[i] = parent1[i]
        else:
            child[i] = parent2[i]
    return child


def probabilistic_selection(population, fitness_values, num_parents):

    fitness_values=[-item for item in fitness_values]
    # Calculate the sum of fitness values

    total_fitness = sum(fitness_values)

    # Calculate the probability of selecting each chromosome
    probabilities = [total_fitness / f for f in fitness_values]

    # Scale the probabilities to be between 0 and 1
    max_probability = max(probabilities)
    scaled_probabilities = [prob / max_probability for prob in probabilities]
    # Adjust the scaled probabilities to sum to 1
    scaled_probabilities = [prob / sum(scaled_probabilities) for prob in scaled_probabilities]

    # Select parents using roulette wheel selection with inverted probabilities
    selected_indices = np.random.choice(len(population), size=num_parents, p=scaled_probabilities)
    selected_parents = [population[i] for i in selected_indices]
    selected_fitness = [fitness_values[i] for i in selected_indices]
    selected_fitness= [-item for item in selected_fitness]
    return selected_parents, selected_fitness




# Define gene-wise mutation function
def mutate_adaptive(solution, mutation_rate, parent_fitness):
    mutated_solution = solution.copy()
    for i in range(len(solution)):
        if np.random.rand() < mutation_rate:
            mutation_range = max(parent_fitness) - min(parent_fitness)
            if mutation_range==0: mutation_range=1
            mutation_factor = (parent_fitness[i] - min(parent_fitness)) / mutation_range
            gene_mutation = mutation_factor * 0.1  # Adjust this factor as needed
            mutated_solution[i] += gene_mutation * (np.random.rand() - 0.5)
            # Ensure the mutated gene is within the bounds
            mutated_solution[i] = np.clip(mutated_solution[i], gene_bounds[i][0], gene_bounds[i][-1])
    return mutated_solution

# Hyperparameters
population_size = 10
num_generations = 10
initial_mutation_rate = 0.1
final_mutation_rate = 0.01
#mutation_rate=[final_mutation_rate,initial_mutation_rate]
# Initialize the population with random solutions within the gene bounds
population = np.random.rand(population_size, num_constants)
for i in range(population_size):
    for j in range(num_constants):
        population[i, j] = np.random.choice(gene_bounds[j])
mutation_rate=initial_mutation_rate
# Main genetic algorithm loop
for generation in range(num_generations):
    # Evaluate the fitness of the current population
    fitness_values = [fitness_func(solution) for solution in population]

    # Rank-based selection of parents
    num_parents = int(population_size / 2)
    parents, parent_fitness = probabilistic_selection(population, fitness_values, num_parents)

    # Create the next generation through crossover and adaptive mutation
    offspring = np.empty((population_size, num_constants))
    for i in range(num_parents):
        parent1 = parents[i]
        parent2 = parents[(i + 1) % num_parents]  # Circular selection of parents
        child = uniform_crossover(parent1, parent2)
        child = mutate_adaptive(child, mutation_rate,parent_fitness)
        offspring[i] = child
    population[num_parents:, :] = offspring[:population_size - num_parents]

    # Report the best fitness in this generation    
    best_fitness_idx = np.argmin(fitness_values)
    best_solution = population[best_fitness_idx]
    best_fitness = fitness_values[best_fitness_idx]
    print(f"Generation {generation+1}: Best Fitness = {best_fitness}")

   

# Print the best solution found
print("Best Solution:")
print(best_solution)
print("Best Fitness:", best_fitness)
