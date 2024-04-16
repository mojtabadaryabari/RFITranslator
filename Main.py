# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 09:54:59 2023

@author: mojta
"""
import os
import json
import re
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
import sys
from pathlib import Path
import pandas as pd
import subprocess
import shutil




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
        
        if ("LDS" in code_content):       
            pattern = re.escape("della classe ") + r'(.*?)' + re.escape("\n")
            match = re.search(pattern, code_content, re.DOTALL)
            if match:
                return match.group(1)
            else:
                return ""
        elif ("LDV" in code_content):
            pattern = re.escape("della classe di vista ") + r'(.*?)' + re.escape("\n")
            match = re.search(pattern, code_content, re.DOTALL)
            if match:
                return match.group(1)
            else:
                return ""
       
        
def name_of_class_text(input_file):
    code_content = input_file
    if ("LDS" in code_content):       
        pattern = re.escape("della classe ") + r'(.*?)' + re.escape("\n")
        match = re.search(pattern, code_content, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return ""
    elif ("LDV" in code_content):
        pattern = re.escape("della classe di vista ") + r'(.*?)' + re.escape("\n")
        match = re.search(pattern, code_content, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return ""
   
        
        


def split_text(input_file):
    print(input_file)
    current_directory = os.path.dirname(os.path.abspath(__file__))

    with open(input_file, 'r') as file:
        code_content = file.read()
        code_content=code_content.replace("valore  Fal /*67,*/","valore  False /*67,*/")



    files=code_content.split("//***************************************************")
    for i in range(1, len(files)):
        split_point = files[i].find("Scheda di classe")
        
        file_name_without_extension, file_extension = os.path.splitext(input_file.name)
        
       
        filename=file_name_without_extension.replace("out\\","")
        folderpath= Path('output/'+filename)
        ldsfolder=Path('output/'+filename+'/LdS/')
        ldvfolder=Path('output/'+filename+'/LdV/')

        if (i==1):
            os.mkdir(folderpath)
            os.mkdir(ldsfolder)
            os.mkdir(ldvfolder)
            

        
        name=name_of_class_text(files[i])
        
        
        lds_output_file1_path = current_directory+"/output/"+filename+'/LdS'+"/"+name+".rfisrf_definition"
        lds_output_file2_path = current_directory+"/output/"+filename+'/LdS'+"/"+name+".rfisrf_sheet"
    
        ldv_output_file1_path = current_directory+"/output/"+filename+'/LdV'+"/"+name+".rfisrf_ldv_definition"
        ldv_output_file2_path = current_directory+"/output/"+filename+'/LdV'"/"+name+".rfisrf_ldv_sheet"
    
    
        # Split the code into two parts
        text_part1 = files[i][:split_point]
        text_part2 = files[i][split_point:]
        
        text_part2=text_part2.replace("Scheda di classe LDV_","Scheda della classe  di vista LDV_")


        if ( "LDS" in text_part1):
            with open(lds_output_file1_path, 'w') as file1:
                file1.write(text_part1)
            with open(lds_output_file2_path, 'w') as file2:
                file2.write(text_part2)
                
        else :
            with open(ldv_output_file1_path, 'w') as file3:
                file3.write(text_part1)

            with open(ldv_output_file2_path, 'w') as file4:
                file4.write(text_part2)
        
            

def remove_lds_dfile():
    Dizionariofile="D://Milan/RFI/AIDA-Product_Windows/standalone/inputFolder/Dizionario.rfisrf_dictionary"
    with open(Dizionariofile, 'r') as Dfile:
        lines = Dfile.readlines()
        start_index=0
        end_index=0
        for j, line in enumerate(lines):
            if "LdS" in line:
                start_index = j
            elif "LdV" in line:
                end_index = j-1
                break


        if start_index>0 and end_index>0:
            del lines[start_index + 1:end_index]
            
       
        
       
        with open(Dizionariofile, 'w') as Dfile:
            Dfile.writelines(lines)
       
           
    return 


def remove_ldv_dfile():

    

    Dizionariofile="D://Milan/RFI/AIDA-Product_Windows/standalone/inputFolder/Dizionario.rfisrf_dictionary"
    tempfile="D://Milan/RFI/AIDA-Product_Windows/standalone/template/Dizionario.rfisrf_dictionary"
    
    shutil.copy(tempfile, Dizionariofile)
    return 


def split_text_into_AIDA(input_file):
    remove_lds_dfile()
    remove_ldv_dfile()
    
    current_directory = os.path.dirname(os.path.abspath(__file__))

    with open(input_file, 'r') as file:
        code_content = file.read()
    
    code_content=code_content.replace("valore  Fal /*67,*/","valore  False /*67,*/")
    



    files=code_content.split("//***************************************************")
    for i in range(1, len(files)):
        split_point = files[i].find("Scheda di classe")
        
        file_name_without_extension, file_extension = os.path.splitext(file.name)
        
       
 
        
        name=name_of_class_text(files[i])
        lds_folder_path = "D://Milan/RFI/AIDA-Product_Windows/standalone/inputFolder/Sheets/Stazione/LdS/"
        ldv_folder_path = "D://Milan/RFI/AIDA-Product_Windows/standalone/inputFolder/Sheets/Stazione/LdV/"
        
        lds_output_file1_path = lds_folder_path+name+".rfisrf_definition"
        lds_output_file2_path = lds_folder_path+name+".rfisrf_sheet"
        
        ldv_output_file1_path = ldv_folder_path+name+".rfisrf_ldv_definition"
        ldv_output_file2_path = ldv_folder_path+name+".rfisrf_ldv_sheet"
    
    
    
        # Split the code into two parts
        text_part1 = files[i][:split_point]
        text_part2 = files[i][split_point:]
        text_part2=text_part2.replace("Scheda di classe LDV_","Scheda della classe  di vista LDV_")
       
        
        if ( "LDS" in text_part1):
            with open(lds_output_file1_path, 'w') as file1:
                file1.write(text_part1)

            with open(lds_output_file2_path, 'w') as file2:
                file2.write(text_part2)
        else:
            with open(ldv_output_file1_path, 'w') as file1:
                file1.write(text_part1)

            with open(ldv_output_file2_path, 'w') as file2:
                file2.write(text_part2)
        

        # add filename into Dizionario.rfisrf_dictionary file
        Dizionariofile="D://Milan/RFI/AIDA-Product_Windows/standalone/inputFolder/Dizionario.rfisrf_dictionary"
        
        if ("LDS" in name):            
            with open(Dizionariofile, 'r') as Dfile:
                lines = Dfile.readlines()
                start_index=0
                for j, line in enumerate(lines):
                    if "LdS" in line:
                        start_index = j
                        break
           
                    
        
                
                lines.insert(start_index+i, "\t"+"\t"+"\t"+name+'{'+name+'}'+"\n")
                with open(Dizionariofile, 'w') as Dfile:
                    print(lines)
                    Dfile.writelines(lines)
        
        elif ("LDV" in name):
            with open(Dizionariofile, 'r') as Dfile:
                lines = Dfile.readlines()
                start_index=0
                for j, line in enumerate(lines):
                    if "LdV" in line:
                        start_index = j
                        break
           
                    
        
                
                lines.insert(start_index+i, "\t"+"\t"+"\t"+name+'{'+name+'}'+"\n")
                with open(Dizionariofile, 'w') as Dfile:
                    print(lines)
                    Dfile.writelines(lines)
        
            
            
        
        
        


def runaida():
    
    create_LNC_Files_into_AIDAFolder()
    



    
def create_lncfiles_by_rmutt():
    for i in range(1, 6):
        os.system("rmutt Main.rm > tempout/out"+str(i)+".txt")
        chaneg_the_types()
        
        runaida()
        
def custom_metric(z, y):
    # x, y are two vectors
    # distance(.,.) calculates count of elements when both xi and yi are True
    size=len(z);
    same=0;
    for i in range(0, size-1):
        if (z[i]==y[i]):
            same=same+1;
    return pow(size-same,1);


def read_data_from_lncs():

    source_dir = Path('out/')

    files = source_dir.iterdir()
    files = source_dir.glob('*.txt')
    Data=[]
    pattern = r'/\*(.*?)\*/'
    
    for file in files:
       with file.open('r') as file:
            code_content = file.read()
            start_index = code_content.find("FoglioDefinizioni della classe")
            end_index = code_content.find("//***************************************************", start_index + 10)
            
            if start_index != -1 and end_index != -1:
               code_content = code_content[start_index:end_index-5]
            if start_index != -1 and end_index == -1:
                 code_content = code_content[start_index:len(code_content)]
           
           

            matches = re.findall(pattern, code_content)
            s = ''.join(str(x) for x in matches)
            s="["+s
            news= s.replace(",]","]")
            if news.endswith("]]]"):
                news=news
            elif news.endswith("]]"):
                news=news+"]"
            elif news.endswith("]"):
                news=news+"]]"
                

            
            
            filenumber=file.name;
            filenumber=filenumber.replace("out","")
            filenumber=filenumber.replace("\\","")
            filenumber=filenumber.replace(".txt","")
            

            my_list = json.loads(news)
            my_list[0].insert(0, int(filenumber))
            
            Data.append(my_list)
            
    return Data

def clustering_data(Data):
    
    dim1_size = len(Data)
    dim2_size = max(len(level) for level in Data)
    dim3_size = max(len(sublist) for level in Data for sublist in level)
    dim4_size = max(len(subsublist) if isinstance(subsublist, list) else 1
                    for level in Data
                    for sublist in level
                    for subsublist in sublist)

# Create a NumPy array with the determined sizes
    originalarray = np.zeros((dim1_size, dim2_size, dim3_size, dim4_size), dtype=int)

# Fill the array with your data
    for i, level in enumerate(Data):
        for j, sublist in enumerate(level):
            for k, subsublist in enumerate(sublist):
                if isinstance(subsublist, list):
                    originalarray[i, j, k, :len(subsublist)] = subsublist
                else:
                    originalarray[i, j, k, 0] = subsublist

# Create a NumPy array with the determined sizes


# Get the shape of the original array
    original_shape = originalarray.shape

# Reshape the array to 2D by flattening the last two dimensions
    new_shape = (original_shape[0] , original_shape[2] * original_shape[3]* original_shape[1])
    X = originalarray.reshape(new_shape)





    db = DBSCAN(min_samples=1, metric=custom_metric, eps=180, p=1).fit(X)


    labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)


    unique_labels = set(labels)
    core_samples_mask = np.zeros_like(labels, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True


    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
        # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = labels == k

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(
            xy[:, 0],
            xy[:, 1],
            "o",
            markerfacecolor=tuple(col),
            markeredgecolor="k",
            markersize=14,
            )

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(
            xy[:, 0],
            xy[:, 1],
            "o",
            markerfacecolor=tuple(col),
            markeredgecolor="k",
            markersize=4,
            )




    plt.title(f"Estimated number of clusters: {n_clusters_}")
    plt.show()
    representative_points = []

    for label in unique_labels:
        if label == -1:  # Noise points have label -1
            continue

        cluster_points = X[labels == label]
        representative_points.append(X[labels == label])

# Printing representative points
    for i, point in enumerate(representative_points):
        print(f"Cluster {i + 1} Representative Point: {point[0]}" )
    

def cut_and_paste(source_path, destination_folder):
    try:
        print(source_path)
        print("dest")
        print(destination_folder)
        # Ensure the destination folder exists, create it if not
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Get the filename from the source path
        file_name = os.path.basename(source_path)
        
        

        # Create the destination path by joining the destination folder and file name
        destination_path = os.path.join(destination_folder, file_name)

        # Move the file to the destination folder
        shutil.move(source_path, destination_path)
    except Exception as e:
        print(f"Error: {e}")
    
    return



def create_LNC_Files_into_AIDAFolder():
    
        
 
    
    source_dir = Path('D://Milan/RFI/ToolsForLNCGenarator/rmutt.js/LNCGram/tempout')

    files = source_dir.iterdir()
    files = source_dir.glob('*.txt') 
    for file in files:
        
        
        
        
        
        # remove previous files to be runed by aida
        
        
        lds_folder_path = 'D:/Milan/RFI/AIDA-Product_Windows/standalone/inputFolder/Sheets/Stazione/LdS'
        ldv_folder_path = 'D:/Milan/RFI/AIDA-Product_Windows/standalone/inputFolder/Sheets/Stazione/LdV'
        
        reportaddress="D:/Milan/RFI/AIDA-Product_Windows/standalone/reports/report_inputFolder.txt"
        
     #   os.remove(reportaddress)


    # List all lds files in the folder
        ldsprefiles = os.listdir(lds_folder_path)
        
        if not os.path.exists(lds_folder_path):
            os.makedirs(lds_folder_path)
      
        if not os.path.exists(ldv_folder_path):
            os.makedirs(ldv_folder_path)
         

    # Iterate through the files and remove each one
        for prefile in ldsprefiles:
            file_path = os.path.join(lds_folder_path, prefile)
            print(file_path)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print("removed")
                
    # List all ldv files in the folder
        ldvprefiles = os.listdir(ldv_folder_path)

          # Iterate through the files and remove each one
        for prefile in ldvprefiles:
            file_path = os.path.join(ldv_folder_path, prefile)
            print(file_path)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print("removed")
    
    
        # remove previous files to be runed by aida
        
        
        
        file_name_without_extension, file_extension = os.path.splitext(file.name)
     

        input_file_path =file
        
        

        split_text_into_AIDA(input_file_path)
        
        folder_path = "D://Milan/RFI/AIDA-Product_Windows/standalone/"
        os.chdir(folder_path)
        cmd=["code_generator","inputFolder"]
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        folder_path = "D:/Milan/RFI/ToolsForLNCGenarator/rmutt.js/LNCGram"
        os.chdir(folder_path)
        
        

        with open(reportaddress, 'r') as reportfile:
            report_content = reportfile.read()
  
            if ("Test Report on inputFolder: SUCCESS" in report_content):
                create_LNC_Files(input_file_path)
                cut_and_paste(input_file_path, "D:/Milan/RFI/ToolsForLNCGenarator/rmutt.js/LNCGram/out")
            else:
                cut_and_paste(input_file_path, "D:/Milan/RFI/ToolsForLNCGenarator/rmutt.js/LNCGram/outwitherror")
                destination_file = os.path.join("D:/Milan/RFI/ToolsForLNCGenarator/rmutt.js/LNCGram/outwitherror/", "Report_"+file.name)

                shutil.copy(reportaddress, destination_file)
        
          
        



def create_LNC_Files(filepath):
    
    current_directory = os.path.dirname(os.path.abspath(__file__))

    source_dir = Path('out/')

    files = source_dir.iterdir()
    files = source_dir.glob('*.txt') 
    for file in files:
        
        file_name_without_extension, file_extension = os.path.splitext(file.name)
        folderpath= Path('output/'+file_name_without_extension)
       
        input_file_path =file
        
        name=name_of_class(input_file_path)
        output_file1_path = current_directory+"/output/"+file_name_without_extension+"/"+name+".rfisrf_definition"
        output_file2_path = current_directory+"/output/"+file_name_without_extension+"/"+name+".rfisrf_sheet"
        

    split_text(filepath)

    return 
def isusedintheitherfiles(nextword,findte,currentclass): 
    for i in range(len(findte)):
        if (i!=currentclass):
            if (findte[i].find(nextword)!=-1):
                return True;
     
    return False;


def chaneg_the_types():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    source_dir = Path('tempout/')
    files = source_dir.iterdir()
    files = source_dir.glob('*.txt')
    definition_part_class=""
    newtxt=""
    for file in files:    
        newtxt=""
        with open(file, 'r') as readedfile:
            code_content = readedfile.read()
            code_content=code_content.replace("\n","*Enter*")
            
            findte = code_content.split("//***************************************************")
            for i in range(len(findte)):
                s=findte[i];
                index=s.find("macro");
                if (index>0):
                    definition_part_class=findte[i][:index];
              #      print(str(i)+":");
              #      print(definition_part_class);
                    text_words=definition_part_class.split()
                    nextword=""
                    for j in range(len(text_words) - 1):
                        nextword=""
                        if (text_words[j] in ("pubblico","privato","protetta","pubblica","privata","protetto")):
                            if (text_words[j+1]=="visibile"):
                                nextword=text_words[j+2]
                            else:
                                nextword=text_words[j+1]
                            exist=isusedintheitherfiles(nextword,findte,i);
                            if (exist==True and nextword!="stato"):
                                text_words[j]="pubblico";
                            
                    definition_part_class=text_words;
                    findte[i]="/*[*/"+"\n"+"//***************************************************"+"\n"+' '.join(definition_part_class).replace("*Enter*","\n")+findte[i][index:].replace("*Enter*","\n");
                    newtxt=newtxt+findte[i]
        
        
        
        with open(file, 'w') as writedfile:
            writedfile.write(newtxt)
        
                        
                        
                            
                            
                                
                            
                    
                
            
            # for every class , open them
            
                # if its is used in other class, change its type to public
            
            

        

    
    return

     
def createlistofrules():
    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    source_dir = Path('out/')
    files = source_dir.iterdir()
    files = source_dir.glob('*.txt')
    definition_part_class=""
    newtxt=""
    mylist=[];
    for file in files:    
        rule_list = [0] * 115
        with open(file, 'r') as readedfile:
            code_content = readedfile.read()  
            file_name_without_extension, file_extension = os.path.splitext(file.name);
            rule_list[114]=file_name_without_extension;
            for i in range(115):
                str_i = str(i)
                pattern = re.compile(r'\*' + re.escape(str_i) +","+ r'\*')
  
                if (re.search(pattern, code_content)):
                    rule_list[i]=1
            
            mylist.append(rule_list)
            file_name_without_extension, file_extension = os.path.splitext(file.name)
            
        
    
        
    
    


    df = pd.DataFrame(mylist, columns=[f'Rule{i}' for i in range(0, 115)])
    excel_file_path = 'output.xlsx'
    df.to_excel(excel_file_path, index=False)
    
def remove_strings(text, strings_to_remove):
    for string in strings_to_remove:
        text = text.replace(string, '')
    return text


def select_bug_reports():
    bug_list =[["",""]]
    source_dir = Path('outwitherror/')
    files = source_dir.iterdir()
    files = source_dir.glob('*Report*.txt')
    for file in files:
        with open(file, 'r') as readedfile:
            code_content = readedfile.read()  
            strings_to_remove = { "intero","booleano",
                                 "lds_mainclass_c","lds_subclass_c",
                                 "ldv_mainclass_c","ldv_subclass_c",
                                 "subclass_c","mainclass_c",
                                 "parametro","variabile_v","enumerator",
                                 "recordfiled","attribute_at","timer_t","contatore_co","controllo_c","macrova_m",
                                 "macroef_m","macrove_m","comando_c","comando","command_comm","lista_l",
                                  "pubblico","privato","protetta","pubblica","privata","protetto","stato",
                                 "modelsystemview","model","stazione","logica","argomento_af","argomento_ave",
                                 "recordheaderr","previousva_pv","restoreva_rv","stateenumerator",
                                 "restoreti_ti","previousco_c","subclass","::","1","2","3","4","5","6","7",
                                 "8","9","10","macro","commandcomm","mainclass_c","subclass_c","subclass_c","mainclass_c"
                                 "effectpermanencestate","effectnormalizationstatestate","guardnominalactuationstate",
                                 "guardnominalactuationstatestate","effectnormalizationstatestate","\'",
                                 "effectnominalactuationstatestate","000","effectpermanencestate","recordheaderr",
                                 "types","mainclass","lds","argomento_a","ldv","0","_"
      
                                 
                                 
                                 }
            
            index = code_content.find("Details")
            errorpart=code_content[index:]
            if ("the following errors were found" in errorpart):
            
            
                first_index = code_content.find('Exception') 
                first_enter=code_content.find('\n',first_index+2)
                second_enter=code_content.find('\n',first_enter+2)
                
    
                errortext= code_content[first_index:second_enter]
            
            else:
                first_index = code_content.find('Exception') 
                second_enter=code_content.find('\n',first_index+2)
                
    
                errortext= code_content[first_index:second_enter]
            
                
      
            errortext=errortext.lower();
            error_message=remove_strings(errortext,strings_to_remove)
            
            string_not_found = all(error_message not in row[1] for row in bug_list)
            if (string_not_found):
                bug_list.append([file.name,error_message])
    
    print("Different Bug reports are: "+"\n") 
    for row in bug_list:
            print(row[0]+"\n") 
            print(row[1]+"\n")
            
           
        
    return 


    
while True:
    print("select one option da fare \n")
    print("1: Create Random LNC files \n")
    print("2: Create Lists for every LNC file \n")
    print("3: Clustring Lnc Files \n")
    print("4: Create Definistion AND state files: \n")
    print("5: Change the accessability of the variables: \n")    
    print("6: Create a list of rules: \n")
    print("7: Run AIDA: \n")
   
    selectedo=input()
    if int(selectedo)==1 :
        create_lncfiles_by_rmutt()
        print("\n")
        print("\n")


    elif int(selectedo)==2:
        data=read_data_from_lncs()
    elif int(selectedo)==3:
        data=read_data_from_lncs()
        clustering_data(data)  
    elif int(selectedo)==4:
        source_dir = Path('D:/Milan/RFI/ToolsForLNCGenarator/rmutt.js/LNCGram/out')

        files = source_dir.iterdir()
        files = source_dir.glob('*.txt') 
        for file in files :
            create_LNC_Files(file)
    elif int(selectedo)==5:
        chaneg_the_types()
    elif int(selectedo)==6:
        createlistofrules()
        print("\n")
        print("\n")


    elif int(selectedo)==7:
        runaida()
        print("\n")
        print("\n")

    
    elif int(selectedo)==8:
        select_bug_reports()
        print("\n")
        print("\n")

    
                
        
        
    
    else:
        print("Finito")
        break
    








