import numpy as np
import csv
import math
from Levenshtein import distance

def distance_percentage(string1, string2):
    return distance(string1, string2) / np.max([len(string1), len(string2)])


def get_similarity(string1, string2):
    
    
    distance1 = distance_percentage(string1, string2)
    
    string1_p = string1
    string1 = string1.split()
    string1_w = "".join(string1)
    string1_s = "".join(sorted(string1_w))
    
    string2_p = string2
    string2 = string2.split()
    string2_w = "".join(string2)
    string2_s = "".join(sorted(string2_w))
    
    distance2 = distance_percentage(string1_w, string2_w)
    distance3 = distance_percentage(string1_s, string2_s)
        
    
    return np.max([1 - distance1, 1 - distance2, 1 - distance3])