import pandas as pd
from helper import *

import time
from datetime import datetime, date


class Data(object):
    
    def __init__(self, filecontent):

        self.col_names = []
        self.names = []
        
        # print(f"Dataset {filename} is loaded.")

        self.submissions = pd.read_csv(filecontent)
        self.similarities = dict()
        
        self.names = [str(a) + ", " + str(b) for a, b in zip(self.submissions["Nachname"].values, self.submissions["Vorname"].values)]
        
        
        self.submissions['Name'] = self.names
        self.submissions = self.submissions.set_index('Name')
        
        
        for colname, coldata in self.submissions.iteritems():
        
            if colname.startswith("Antwort"):
                
                print(colname)
                      
                new_colname = colname.replace("Antwort", "Aufgabe")
                #print("Vorher", self.submissions.head())
                self.submissions = self.submissions.rename(columns={colname: new_colname})
                #print("Nachher", self.submissions.head())
                colname = new_colname
                
                self.col_names.append(colname)
    
                similarity_matrix = np.ones((len(coldata.values), len(coldata.values)))
            
                for i, val in enumerate(coldata.values):
                    maximum = 0
                    person = ""

                    for j, val_other in enumerate(coldata.values):
            
                        if i == j:
                            continue
            
                        similarity = get_similarity(str(val), str(val_other))
            
                        if similarity > maximum:
                            maximum = similarity
                            person = self.names[j]
                        similarity_matrix[i,j] = similarity_matrix[j,i] = similarity
                
                self.similarities[colname] = pd.DataFrame(similarity_matrix, index=self.names, columns=self.names)
                
                
    def get_not_empty_indices(self, colname):
        
        return self.submissions.index[self.submissions[colname] != "-"]
                
    def get_non_similar_to_template(self, colname):
        

        return self.similarities[colname].index[self.similarities[colname]["Vorlage, Die"] < 0.9]
    
    
        
    
    
    