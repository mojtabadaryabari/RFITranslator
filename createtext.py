import os
import json
import re
import matplotlib.pyplot as plt

import numpy as np


from sklearn.cluster import DBSCAN

Data=[]


dirList = os.listdir("./") # current directory


# Define a regular expression pattern to capture the text between */ and /*
pattern = r'/\*(.*?)\*/'

# Use re.findall to find all matches of the pattern in the text

input_file = "./out.txt"



with open(input_file, 'r') as file:
    code_content = file.read()

# Use re.findall to find all matches of the pattern in the text
matches = re.findall(pattern, code_content)


s = ''.join(str(x) for x in matches)   


# my_list = json.loads(s)

print(s.replace(",]","]"))





