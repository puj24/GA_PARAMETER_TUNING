import numpy as np
import pygad
import subprocess
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import quaternion

import warnings
warnings.filterwarnings('ignore')

# Define the target outputs
desired_outputs = np.loadtxt("D:\Avanti\SSP\Parameter_tuning\ORION\output.txt", dtype=float)
desired_outputs = desired_outputs.reshape(50, 4)

# Define the C program command
c_program_command_1 = "gcc -o D:\Avanti\SSP\Parameter_tuning\ORION\main.exe D:\Avanti\SSP\Parameter_tuning\ORION\main.c"
c_program_command_2 = "D:\Avanti\SSP\Parameter_tuning\ORION\main.exe "
# Define the genetic algorithm parameters
population_size = 50
mutation_rate = 1
max_generations = 50

# Define the number of constants (genes) to generate number of
num_constants = 3

# Define the gene bounds
gene_bounds = [
    (1e-15, 3e-15),  # epsilon stepsize e-15
    (1e-6, 1e-2),  # delta (1e-4 2e-4) stepsize
    (1e-4 , 1e-2) ,#EPSILON_SEQ_ERROR
    #(0.99999999999, 0.999999999999),  # ymax
    #(0.93, 0.95),  # ymin
    
]

# Convert gene_bounds to a np array
gene_space = np.array(gene_bounds)

def quaternion_error(q1, q2):
    """
    Calculate the error (angle) between two quaternions.

    Parameters:
        q1 (np.ndarray): The first quaternion in the format [w, x, y, z].
        q2 (np.ndarray): The second quaternion in the format [w, x, y, z].

    Returns:
        float: The error (angle) between the two quaternions in radians.
    """
    # Normalize the quaternions
    q1 = q1 / np.linalg.norm(q1)
    q2 = q2 / np.linalg.norm(q2)

    # Convert the quaternions to np-quaternion objects
    q1 = np.quaternion(*q1)
    q2 = np.quaternion(*q2)

    # Calculate the quaternion multiplication (q_diff = q2_conjugate * q1)
    q_diff = q2.conjugate() * q1

    # Extract the angle (error) from the resulting quaternion
    angle_rad = 2 * np.arccos(q_diff.w)

    # Check for invalid angles and return a valid result
    if np.isnan(angle_rad) or np.abs(angle_rad) > 1:
        return 0.0

    return angle_rad


# Define the fitness function
def fitness_func(ga_instance, solution, solution_idx):
    individual = solution[:num_constants]

    # Generate random values for each gene within the bounds
    individual = np.random.uniform(low=gene_bounds[0][0], high=gene_bounds[0][1])
    for i in range(1, num_constants):
        individual = np.append(individual, np.random.uniform(low=gene_bounds[i][0], high=gene_bounds[i][1]))


    # Save the individual's genes in a header file as constants
    with open("D:/Avanti/SSP/Parameter_tuning/ORION/constants.h", "w") as file:
        file.write("#include <stdio.h>\n")
        file.write("#include <stdlib.h>\n")
        file.write("#include <math.h>\n")
        file.write("#include <string.h>\n")
        # Generate multiple constants based on the individual's genes
        file.write("#define THRESHOLD 3\n")
        file.write("#define STAR_MIN_PIXEL 3\n")
        file.write("#define STAR_MAX_PIXEL 150\n")
        file.write("#define MAX_STARS 100\n")
        file.write("#define SKIP_PIXELS 2\n")
        file.write("#define LENGTH 808\n")
        file.write("#define BREADTH 608\n")
        file.write("#define PIXEL_WIDTH 0.0000048\n")
        file.write("#define NUM_MAX_STARS 13\n")
        file.write("//SM constants\n")
        file.write("#define FOCAL_LENGTH 0.036\n")
        file.write("#define EPSILON {}\n".format(individual[0]))
        file.write("#define DELTA {}\n".format(individual[1]))
        file.write("#define ANG_DIST_TOLERANCE 1.2\n")
        file.write("#define N_GC 8876\n")
        file.write("#define N_KVEC_PAIRS 224792\n")
        file.write("#define Y_MAX 0.9999999999926209\n")
        file.write("#define Y_MIN 0.9900261208247870\n")
        file.write("#define TOL 0.5\n")
        file.write("#define P1 35 \n")
        file.write("#define P2 80 \n")
        file.write("#define EPSILON_SEQ_ERROR {} \n".format(individual[2])) # 1e-4 to 1e-2
        file.write("#define EPSILON_EST 0.001 \n")

  # Evaluate the fitness for each test case
    # Run the C program and collect the output
    result = subprocess.run(c_program_command_1, shell=True, capture_output=True, text=True)
    process = subprocess.Popen(c_program_command_2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #process = subprocess.Popen(c_program_command_2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode().strip()
    #print("EPSILON:", individual[0]," DELTA:", individual[1], " y_max:" , individual[2], "y-min", individual[3])
    print("Output:", output)
    output = list(filter(None, output.split('\r\n')))
# Calculate the fitness based on the differences between desired and obtained coordinates
    output_coordinates = np.array([list(map(float, line.split())) for line in output])

    # Check the shapes of the arrays
    if desired_outputs.shape != output_coordinates.shape:
        raise ValueError("Shape mismatch between desired_outputs and output_coordinates")

    # Calculate the fitness based on the differences between desired and obtained coordinates
   # fitness = np.sum(np.abs(desired_outputs - output_coordinates))
    #fitness=np.abs(sim_error(desired_outputs,output_coordinates))
    fitness=0
    for i in range(desired_outputs.shape[0]):
        desired_row = desired_outputs[i, :]
        obtained_row = output_coordinates[i, :]
        fitness += quaternion_error(desired_row, obtained_row)
    print(fitness)
    
    return fitness

# Convert gene_bounds to a list
gene_space = gene_space.tolist()
initial_mutation_percent = 0.0001
final_mutation_percent = 0.05
mutation_percent_genes = [initial_mutation_percent, final_mutation_percent]

# Create an instance of the pygad.GA class
ga_instance = pygad.GA(num_generations=max_generations,
                       num_parents_mating=population_size,
                       fitness_func=fitness_func,
                       sol_per_pop=population_size,
                       num_genes=num_constants,
                       gene_type=float,
                       gene_space=gene_space,
                       mutation_type="adaptive",
                       mutation_percent_genes=mutation_percent_genes,  
                       crossover_type="single_point",
                       parent_selection_type="rws",
                       stop_criteria=["reach_0.001"])

# Run the genetic algorithm
ga_instance.run()

# Get the best solution and its fitness
best_solution, best_fitness = ga_instance.best_solution(), ga_instance.best_fitness()

# Print the best solution and its fitness
print("Best solution:", best_solution[:num_constants])
print("Fitness:", best_fitness)
# plot the error on test sample

def plot_error(best_solution):
    individual = best_solution[:num_constants]

    #
    

    # Save the  best genes in a header file as constants
    with open("D:/Avanti/SSP/Parameter_tuning/ORION/constants.h", "w") as file:
        file.write("#include <stdio.h>\n")
        file.write("#include <stdlib.h>\n")
        file.write("#include <math.h>\n")
        file.write("#include <string.h>\n")
        # Generate multiple constants based on the individual's genes
        file.write("#define THRESHOLD 3\n")
        file.write("#define STAR_MIN_PIXEL 3\n")
        file.write("#define STAR_MAX_PIXEL 150\n")
        file.write("#define MAX_STARS 100\n")
        file.write("#define SKIP_PIXELS 2\n")
        file.write("#define LENGTH 808\n")
        file.write("#define BREADTH 608\n")
        file.write("#define PIXEL_WIDTH 0.0000048\n")
        file.write("#define NUM_MAX_STARS 13\n")
        file.write("//SM constants\n")
        file.write("#define FOCAL_LENGTH 0.036\n")
        file.write("#define EPSILON {}\n".format(individual[0]))
        file.write("#define DELTA {}\n".format(individual[1]))
        file.write("#define ANG_DIST_TOLERANCE 1.2\n")
        file.write("#define N_GC 8876\n")
        file.write("#define N_KVEC_PAIRS 224792\n")
        file.write("#define Y_MAX 0.9999999999926209\n")
        file.write("#define Y_MIN 0.9900261208247870\n")
        file.write("#define TOL 0.5\n")
        file.write("#define P1 35 \n")
        file.write("#define P2 80 \n")
        file.write("#define EPSILON_SEQ_ERROR {} \n".format(individual[1])) #0.001
        file.write("#define EPSILON_EST 0.001 \n")

  # Evaluate the fitness for each test case
    # Run the C program and collect the output
    result = subprocess.run(c_program_command_3, shell=True, capture_output=True, text=True)
    process = subprocess.Popen(c_program_command_4, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #process = subprocess.Popen(c_program_command_2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode().strip()
    #print("EPSILON:", individual[0]," DELTA:", individual[1], " y_max:" , individual[2], "y-min", individual[3])
    #print("Output:", output)
    output = list(filter(None, output.split('\r\n')))
# Calculate the fitness based on the differences between desired and obtained coordinates
    output_coordinates = np.array([list(map(float, line.split())) for line in output])

    # Check the shapes of the arrays
    if desired_outputs.shape != output_coordinates.shape:
        raise ValueError("Shape mismatch between desired_outputs and output_coordinates")

    fitness = np.sum(np.abs(desired_outputs - output_coordinates), axis=1)  # Sum along axis 1 (rows)

    # Plot the difference between desired and obtained coordinates for each test case
    
    fig, axes = plt.subplots(nrows=desired_outputs.shape[0], ncols=1, figsize=(8, 2 * desired_outputs.shape[0]))

    for i in range(desired_outputs.shape[0]):
        axes[i].plot(desired_outputs[i], label='Desired')
        axes[i].plot(output_coordinates[i], label='Obtained')
        axes[i].set_title(f'Test Case {i+1}')
        axes[i].legend()

    plt.tight_layout()
    plt.show()
