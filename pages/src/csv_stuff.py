import pandas as pd
import sys
import re
import random
from bs4 import BeautifulSoup
import argparse
import matplotlib.pyplot as plt


def create_pair_routine(semester, ha, tasks, prog_language, labled_csv=None):
    csv_path = f'../data/raw_data/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten.csv'
    df = pd.read_csv(csv_path, delimiter=',')



# def read_and_store_from_csv(file):
    # df = pd.read_csv(f'{file}.csv', delimiter=',')
    # semester = re.search("\[(\S+)\]", file).group(1)
    # ha_number = re.search("-(\d{1,2})", file).group(1)
    # for i, row in enumerate(df.values):
    #     #TODO always 3 programming tasks?
    #     for j in range(0, 3):
    #         # "unlabled/SoSe21/PPR [SoSe21]-9. Hausaufgabe - Pflichttest C-Antworten"
    #         with open(f'unlabled/{semester}/HA{ha_number}C-{j}_{i}.c', 'w') as file:
    #             #TODO is task 16. in every homework first programming task?
    #             file.write(row[15+j])
