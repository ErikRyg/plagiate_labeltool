from cProfile import label
import pandas as pd
import sys
import re
import random
from bs4 import BeautifulSoup
import argparse
import matplotlib.pyplot as plt

semester='SoSe21'
ha='9'
# tasks = ['Antwort 9']
tasks = ['Antwort 8', 'Antwort 9', 'Antwort 10']
prog_language='C'


def create_labled_table(df, semester, ha, tasks, prog_language):
    df_labled = pd.DataFrame(columns=['id', 'semester', 'ha', 'task', 'prog_lang', 'surname1', 'lastname1', 'surname2', 'lastname2', 'code1', 'code2', 'label'])
    i = 0
    for task in tasks:
        for ln1, sn1, code1 in df.loc[df[f'{task} empty']==0][['Nachname', 'Vorname', task]].values:
            for ln2, sn2, code2 in df.loc[(df[f'{task} empty']==0) & (df[task] != code1)][['Nachname', 'Vorname', task]].values:
                df_labled.loc[len(df_labled)] = [i, semester, ha, task, prog_language, sn1, ln1, sn2, ln2, code1, code2, -1]
                i += 1
    return df_labled


def get_given_code(file):
    with open(file) as xmlstr:
        soup = BeautifulSoup(xmlstr, 'xml')
        answerpreload = soup.find('answerpreload').text
        return answerpreload


"""
(empty- or template solution) == 1
"""
def add_valid_code_columns(df, semester, ha, tasks, prog_language):
    for task in tasks:
        # answerpreload = get_given_code(f'../../data/code_templates/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten_{task}.xml')
        answerpreload = get_given_code(f'./data/code_templates/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten_{task}.xml')
        answerpreload = answerpreload.replace('\t', '').replace('\r', '').replace('\n', '')
        #every special character beetween \Q and \E is ignored, but the inserted \S*; answers shouldnt contain \Q and \E!
        answerpreload = re.escape(answerpreload)
        #{{ cr_random.f1 }} --> \S*
        answerpreload = re.sub(r"\\{\\{\\\s*\S+\s*\\}\\}", r"\\S*", answerpreload)
        summe=0
        result = 0
        df[f"{task} empty"] = 0
        #TODO wie vergleicht man leicht unterschiedliche texte auf Gleichheit miteinander??? -> bisher nur direkte gleichheit
        for j,column in enumerate(df[task]):
            #there are \\n in the student solutions because "...\n" --> "...\\n" while read_csv
            column = column.replace('\t', '').replace('\r', '').replace('\n', '').replace('\\n', r'\n')
            # test if template was given or not
            if answerpreload != '':
                result = re.match(answerpreload, column)
            if column == '-' or result:
                df.loc[j, f"{task} empty"] = 1
                summe+=1
        # print(summe)
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
    df = add_valid_code_columns(df=df, semester=semester, ha=ha, tasks=tasks, prog_language=prog_language)
    df_labled = create_labled_table(df, semester, ha, tasks, prog_language)
    return df_labled[0:3], len(df_labled[0:3])


df_labled, df_labled_len = create_labled_table_routine(semester, ha, tasks, prog_language)



def get_new_pair(df_labled, last_task, last_id):
    next = df_labled.loc[(df_labled['label']==-1) & (df_labled['id'] > last_id)]
    if next.empty:
        if last_id != -1:
            return get_new_pair(df_labled, last_task, -1)
        print('no unlabled pair')
        return None
    next = next.values[0]
    answerpreload = None
    #return new template
    if last_task != next[3]:
        answerpreload = get_given_code(f'./data/code_templates/PPR [{next[1]}]-{next[2]}. Hausaufgabe - Pflichttest {next[4]}-Antworten_{next[3]}.xml')
    return next[9], next[10], answerpreload, next[5], next[7], next[0], next[3]


def set_label(df_labled, last_id, label_score, labled_pairs):
    try:
        already_labled = (df_labled.loc[last_id]['label']!=-1)
        df_labled.loc[last_id]['label'] = label_score
        # print(already_labled)
        if not already_labled:
            labled_pairs += 1
        # print(last_id)
        print(df_labled[['id', 'surname1', 'surname2', 'label']])
        return True, labled_pairs
    except:
        print('beim Setzen des labels wurde die Reihe mit der gegebene id nicht gefunden')
        # print(f'id: {last_id}')
        return False, labled_pairs


#checked
#TODO 1. erfolgreichen match hinbekommen        *check*
#TODO 2. empty_solution_matrix richtig setzen   *check*
#TODO 3. dann daraus ein paar ableiten          *check*
#TODO 4. dann daraus eine tabellenreihe für ...labled.csv machen *check*
#TODO 5. dann eine ganze tabelle draus machen   *check*
#TODO! 6. wo wird tabelle zwischengespeichert?
#TODO 7. funktion schreiben die die erste Routine macht mit #aller paar und #aller bereits gelableten und die 3 texte ausgibt  *check*
#TODO 7.1 funktion schreiben, die ein lable übergeben bekommt, in tabelle einträgt und ein neues paar zurückgibt (ggf. auch neue vorgabe)    *check*
#TODO gibt es ein Download fenster? --> ja, da dynos in heroku nicht global speichern können
#TODO 7.2 set_label zum laufen bringen      *check*
#TODO 8. Download button realisieren        *check*

#unchecked
#TODO 8.1 temporäre speicherung des df_labels
#TODO (9. neuen knopf für previous labled hinzufügen)
#TODO (10. liste für gelabelte ids hinzufügen)
#TODO (11. liste für nicht gelabelte ids hinzufügen)
#TODO 12. beide pages gleichzeitig zum laufen bringen
#TODO 13. callbacks für init page schreiben
#TODO 14. back end für halbgelabelte csv im drag&drop realisieren
#TODO checken weshalb nur 12/13 leere abgaben bei antwort 10 gefunden wurden
#TODO double linked list, für die id schreiben, um prev und next button zu realisieren
if __name__ == '__main__':
    pass