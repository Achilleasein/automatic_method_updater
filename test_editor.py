# Useful regex for manual serching: (?<!chat.)navigate, it works with negative searching

import os
import fileinput
import re

# Directory to search for Python files
directory = input("Enter the directory you want to modify: ")
print(directory)
if not directory:
    directory = os.getcwd()

# Method we want to update
method = 'chat_with_person'

pattern = r"\.({})".format(re.escape(method))

# Class we want to concatenate with
class_to_concatenate = 'chat.'

# List to keep track of lines that need to be updated
lines_to_update = []

# Loop through all files in directory
for filename in os.listdir(directory):
    # Check if file is a Python file
    if filename.endswith('.py'):
        # Loop through each line in the file
        for line_number, line in enumerate(fileinput.input(os.path.join(directory, filename)), 1):
            # Check if the desired method is NOT preceded by its class
            if method in line and not class_to_concatenate + method in line:
                match = re.search(pattern, line)
                print(match)
                print(filename, line_number, line)
                if match:
                    print("here we are supposed to replace")
                    index = match.start(1)
                    new_line = line[:index] + class_to_concatenate + line[index:]
                    lines_to_update.append((filename, line_number, line, new_line))
                    print(new_line)

        # Update all the lines that need to be updated
        if lines_to_update:
            fileinput.close()  # Close the current file before writing to it
            with fileinput.input(os.path.join(directory, filename), inplace=True) as file:
                for line_number, line in enumerate(file, 1):
                    # Check if the current line needs to be updated
                    for filename_to_update, line_number_to_update, old_line, new_line in lines_to_update:
                        if filename_to_update == filename and line_number_to_update == line_number:
                            print(new_line.strip())  # write the updated line to the file
                            break
                    else:
                        print(line.strip())  # write the original line to the file
            fileinput.close()  # Close the file after writing to it

        # Reset the list of lines to update for the next file
        lines_to_update = []