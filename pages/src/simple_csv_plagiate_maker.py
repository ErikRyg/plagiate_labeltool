import pandas as pd
import numpy as np
import argparse
from obfuscator import comment_remover, rename_variables
from csv_stuff import create_labled_table_routine, add_valid_code_columns


def create_plagiate_table(df, semester, ha, task, prog_language, number_labled_pairs, path):
    df_labled = pd.DataFrame(columns=['semester', 'ha', 'task', 'prog_lang',
                                      'surname1', 'lastname1', 'code1', 'code2', 'label'])

    df = add_valid_code_columns(df, semester, ha, [task], prog_language)
    number_of_valid_codes = len(df.loc[df[f'{task} empty'] == 0])
    print("number_of_valid_codes: " + str(number_of_valid_codes))
    plagiate_per_solution = int(
        np.floor(number_labled_pairs/number_of_valid_codes))
    print("plagiate_per_solution: " + str(plagiate_per_solution))
    for ln, sn, code in df.loc[df[f'{task} empty'] == 0][['Nachname', 'Vorname', task]].values:
        for i in range(plagiate_per_solution):
            plagiate_code = comment_remover(code)
            plagiate_code = rename_variables(plagiate_code)
            df_labled.loc[len(df_labled)] = [
                semester, ha, task, prog_language, sn, ln, code, plagiate_code, 1]
    df_labled.to_csv(path)
    return df_labled


def create_plagiate_table_routine(semester, ha, task, prog_language):
    csv_path = f'../../data/raw_data/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten.csv'
    csv_path1 = f'../../data/labled/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten_removed_preload.csv'
    # csv_path1 = f'../../data/labled/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten_labled.csv'
    csv_path2 = f'../../data/labled/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten_plagiate.csv'
    df = pd.read_csv(csv_path, delimiter=',')
    number_labled_pairs = len(pd.read_csv(csv_path1, delimiter=','))
    df_labled = create_plagiate_table(
        df, semester, ha, task, prog_language, number_labled_pairs, csv_path2)
    return df_labled


def create_plagiate_table_from_df(df, semester, ha, task, prog_language, number_labled_pairs, path):
    df_labled = pd.DataFrame(columns=['semester', 'ha', 'task', 'prog_lang',
                                      'surname1', 'lastname1', 'code1', 'code2', 'label'])

    # get hole row of each unique student
    df = df.drop_duplicates(subset=['surname1'])

    number_of_valid_codes = len(df.loc[df[f'{task} empty'] == 0])
    print("number_of_valid_codes: " + str(number_of_valid_codes))
    plagiate_per_solution = int(
        np.floor(number_labled_pairs/number_of_valid_codes))
    print("plagiate_per_solution: " + str(plagiate_per_solution))
    for ln, sn, code in df.loc[df[f'{task} empty'] == 0][['Nachname', 'Vorname', task]].values:
        for i in range(plagiate_per_solution):
            plagiate_code = comment_remover(code)
            plagiate_code = rename_variables(plagiate_code)
            df_labled.loc[len(df_labled)] = [
                semester, ha, task, prog_language, sn, ln, code, plagiate_code, 1]
    df_labled.to_csv(path)
    return df_labled


def create_plagiate_table_routine_from_df(semester, ha, task, prog_language):
    csv_path1 = f'../../data/labled/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten_removed_preload.csv'
    # csv_path1 = f'../../data/labled/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten_labled.csv'
    csv_path2 = f'../../data/labled/PPR [{semester}]-{ha}. Hausaufgabe - Pflichttest {prog_language}-Antworten_plagiate.csv'
    df1 = pd.read_csv(csv_path1, delimiter=',')
    number_labled_pairs = len(df1)
    df_labled = create_plagiate_table_from_df(
        df1, semester, ha, task, prog_language, number_labled_pairs, csv_path2)
    return df_labled


def initialize_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-se', type=str, help='Semester of Source file', default='SoSe21')
    parser.add_argument('-ha', type=str, help='HA of Source file', default='9')
    parser.add_argument(
        '-pl', type=str, help='Programming Language of Source file', default='C')
    parser.add_argument(
        '-ta', type=str, help='Task of Source file', default='Antwort 9')
    return parser.parse_args()


if __name__ == '__main__':
    args = initialize_argparser()
    print(args._get_args)
    df_labled = create_plagiate_table_routine_from_df(
        args.se, args.ha, args.ta, args.pl)
