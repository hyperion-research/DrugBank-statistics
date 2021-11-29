#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import xml.etree.ElementTree as ET
import time
import io
from tqdm import tqdm
import pandas as pd
tree = ET.parse("full database.xml")
root = tree.getroot()
with open("ddi-5.1.8-edges-atc.csv", 'r') as fs:
    reader_e = csv.reader(fs)
    my_edge_list = list(reader_e)
group_focus = "approved"
drugs = list(root)
with io.open('ddi-5.1.8-edges-atc-filtered.csv', "w", encoding="utf-8", newline='') as csv_file3:
    results_writer_cd = csv.writer(csv_file3, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    valid_link = True
    for j in range(0,len(my_edge_list)):
        med_1 = my_edge_list[j][0]
        med_2 = my_edge_list[j][1]
        for i in tqdm(range(len(drugs))):
            drug = drugs[i]
            idDB = drug[0].text
            for idx,feature in enumerate(drug):
                if 'name' in str(feature): # drug name
                    drug_name = drug[idx].text
                    #print(drug_name)
                if 'groups' in str(feature): #type of drug
                    group_name = list(drug[idx])[0].text
                    #print(group_name)
                if 'atc-codes' in str(feature): #atc-codes
                    atc_names = list(drug[idx])
                    #print(group_name)
            if ((drug_name == med_1) or (drug_name == med_2)) and ((group_focus not in group_name) or (len(atc_names)<1)):
                valid_link = False
        if (valid_link == True):
            print(med_1, med_2)
            results_writer_cd.writerow([med_1, med_2])

