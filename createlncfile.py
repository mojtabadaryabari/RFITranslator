
import os

import re

def find_text_between_strings(input_string, start_string, end_string):
    pattern = re.escape(start_string) + r'(.*?)' + re.escape(end_string)
    match = re.search(pattern, input_string, re.DOTALL)

    if match:
        return match.group(1)
    else:
        return None

def name_of_class(input_file):
    with open(input_file, 'r') as file:
        code_content = file.read()
        pattern = re.escape("della classe ") + r'(.*?)' + re.escape("\n")
        match = re.search(pattern, code_content, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return None



def split_text(input_file, output_file1, output_file2):
    with open(input_file, 'r') as file:
        code_content = file.read()



    split_point = code_content.find("Scheda di classe")
    # Split the code into two parts
    text_part1 = code_content[:split_point]
    text_part2 = code_content[split_point:]

    # Write the code parts to separate output files
    with open(output_file1, 'w') as file1:
        file1.write(text_part1)

    with open(output_file2, 'w') as file2:
        file2.write(text_part2)


current_directory = os.path.dirname(os.path.abspath(__file__))



if __name__ == "__main__":
    
    
    input_file_path = current_directory+'/out1.txt'
    name=name_of_class(input_file_path)
    output_file1_path = current_directory+"/output/"+name+".rfisrf_definition"
    output_file2_path = current_directory+"/output/"+name+".rfisrf_sheet"
    

    split_text(input_file_path, output_file1_path, output_file2_path)
