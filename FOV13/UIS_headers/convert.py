def generate_header_files(input_filename):
    with open(input_filename, 'r') as input_file:
        lines = input_file.readlines()

        current_data = []
        iteration_number = None

        for line in lines:
            line_elements = line.strip().split()

            if len(line_elements) > 0 and line_elements[0].startswith("SIS_iter_"):
                if current_data:
                    # Process the collected data for the previous iteration
                    write_header_file(iteration_number, current_data)

                # Start collecting data for a new iteration
                iteration_number = line_elements[0].split('_')[-1]
                current_data = []

            if len(line_elements) >= 3 and line_elements[0].isdigit():
                current_data.append(line_elements)

        # Process the last set of collected data
        if current_data:
            write_header_file(iteration_number, current_data)


def write_header_file(iteration_number, data):
    header_filename = f'UIS_{iteration_number}.h'

    header_content = f'''#include <stdio.h>
//N_i_{iteration_number} - Number of input centroids
#define N_i_{iteration_number} {len(data)}
double arr_out_UIS_{iteration_number}[N_i_{iteration_number}][3]={{'''

    for line_elements in data:
        header_content += f'{{{line_elements[0]}, {line_elements[1]}, {line_elements[2]}}},\n'

    header_content += '};'

    # Writing to the output header file
    with open(header_filename, 'w') as output_file:
        output_file.write(header_content)


# Replace 'input_filename.txt' with your actual input file name
input_file_name = 'out.txt'
generate_header_files(input_file_name)
