from cProfile import label
import pandas as pd
import sys
import re
import random
from bs4 import BeautifulSoup
import argparse
import difflib
import matplotlib.pyplot as plt


def create_labled_table(df, semester, ha, tasks, prog_language):
    df_labled = pd.DataFrame(columns=['semester', 'ha', 'task', 'prog_lang',
                             'surname1', 'lastname1', 'surname2', 'lastname2', 'code1', 'code2', 'label', 'hand_labled'])
    # df_labled.index.name = 'index'
    for task in tasks:
        i = 0
        for ln1, sn1, code1 in df.loc[df[f'{task} empty'] == 0][['Nachname', 'Vorname', task]].values:
            for ln2, sn2, code2 in df.loc[(df[f'{task} empty'] == 0) & (df[task] != code1)][['Nachname', 'Vorname', task]][i:].values:
                prelabel1 = difflib.SequenceMatcher(None, code1, code2).ratio()
                prelabel2 = difflib.SequenceMatcher(None, code2, code1).ratio()
                df_labled.loc[len(df_labled)] = [
                    semester, ha, task, prog_language, sn1, ln1, sn2, ln2, code1, code2, max(prelabel1, prelabel2), 0]
            i += 1
    return df_labled


def get_given_code(file):
    try:
        with open(file) as xmlstr:
            soup = BeautifulSoup(xmlstr, 'xml')
            answerpreload = soup.find('answerpreload').text
            questiontext = soup.find('questiontext').text
            return answerpreload, questiontext
    except FileNotFoundError:
        return "Keine Vorgabedatei im Repo gefunden", "Keine Vorgabedatei im Repo gefunden"


"""
(empty- or template solution) == 1
"""


def add_valid_code_columns(df, semester, ha, tasks, prog_language):
    for task in tasks:
        # answerpreload = get_given_code(f'../../data/code_templates/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten_{task}.xml')
        answerpreload, _ = get_given_code(
            f'./data/code_templates/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten_{task}.xml')
        answerpreload = answerpreload.replace(
            '\t', '').replace('\r', '').replace('\n', '')
        # every special character beetween \Q and \E is ignored, but the inserted \S*; answers shouldnt contain \Q and \E!
        answerpreload = re.escape(answerpreload)
        # {{ cr_random.f1 }} --> \S*
        answerpreload = re.sub(
            r"\\{\\{\\\s*\S+\s*\\}\\}", r"\\S*", answerpreload)
        summe = 0
        result = 0
        df[f"{task} empty"] = 0
        # TODO wie vergleicht man leicht unterschiedliche texte auf Gleichheit miteinander??? -> bisher nur direkte gleichheit
        for j, column in enumerate(df[task]):
            # there are \\n in the student solutions because "...\n" --> "...\\n" while read_csv
            column = column.replace('\t', '').replace(
                '\r', '').replace('\n', '').replace('\\n', r'\n')
            # test if template was given or not
            if answerpreload != '':
                result = re.match(answerpreload, column)
            if column == '-' or result:
                df.loc[j, f"{task} empty"] = 1
                summe += 1
    return df


def create_labled_table_routine(semester, ha, tasks, prog_language, labled_csv=None):
    # csv_path = f'../../data/raw_data/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten.csv'
    csv_path = f'./data/raw_data/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten.csv'
    df = pd.read_csv(csv_path, delimiter=',')
    keep_columns = ['Nachname', 'Vorname'] + tasks
    drop_columns = []
    for x in df.columns:
        if x not in keep_columns:
            drop_columns.append(x)
    df = df.drop(drop_columns, axis=1)
    df = add_valid_code_columns(
        df=df, semester=semester, ha=ha, tasks=tasks, prog_language=prog_language)
    df_labled = create_labled_table(df, semester, ha, tasks, prog_language)
    return df_labled, len(df_labled)


def get_new_pair(df_labled, last_task, last_id):
    next = df_labled.iloc[last_id:].loc[df_labled['hand_labled'] == 0]
    if next.empty:
        if last_id != 0:
            return get_new_pair(df_labled, last_task, 0)
        return None
    index = next.index[0]
    next = next.values[0]
    answerpreload = None
    questiontext = None
    # return new template
    if last_task != next[2]:
        answerpreload, questiontext = get_given_code(
            f'./data/code_templates/PPR [{next[0]}]-{next[1]}. Hausaufgabe - Pflichttest {next[3]}-Antworten_{next[2]}.xml')
        if answerpreload == "":
            answerpreload = "Keine Vorgabe"
    return next[8], next[9], answerpreload, questiontext, next[10], str(index), next[2]


def set_label(df_labled, last_id, label_score, labled_pairs):
    try:
        if df_labled.loc[int(last_id), 'hand_labled'] == 0:
            df_labled.loc[int(last_id), 'label'] = label_score
            df_labled.loc[int(last_id), 'hand_labled'] = 1
            labled_pairs += 1
        return True, labled_pairs, df_labled
    except:
        print(
            f'beim Setzen des labels wurde die Reihe mit dem gegebenen index {last_id} nicht gefunden')
        return False, labled_pairs, df_labled


def count_labled(df_labled):
    return len(df_labled.loc[df_labled['hand_labled'] == 1])


if __name__ == '__main__':
    pass
