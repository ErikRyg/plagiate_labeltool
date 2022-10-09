import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from json import loads, dumps
from .src import csv_stuff

PLOTLY_LOGO = "../assets/logo.png"
dash.register_page(__name__)

layout = html.Div([
    html.Div([
        dbc.Navbar(
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.A(
                                    html.Img(src=PLOTLY_LOGO, height="30px"),
                                    href="https://www.ni.tu-berlin.de/menue/neural_information_processing_group/")
                            ),
                            dbc.Col(dbc.NavbarBrand(
                                "PPR Hausaufgaben Labeltool", className="ml-2", href="/")
                            ),
                        ],
                        align="center",
                    ),
                    # href="https://www.ni.tu-berlin.de/menue/members/postgraduate_students_and_doctoral_candidates/goerttler_thomas/",
                ]
            ),
            color="primary",
            dark=True,
            id="navbar",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([
                        dbc.Row([
                            dbc.Col(html.H5(id='retry_message'), md=12,
                                    className="title_container")
                        ]),
                        dbc.Row([
                            dbc.Col(html.H5(html.Details(children=[
                                html.Summary('Aufgabenstellung'),
                                dcc.Loading(
                                    children=html.Iframe(
                                        id='aufgabenstellung',
                                        style={'width': '100%', 'height': 300}
                                    ),
                                    type="circle"
                                )])), md=6),
                            dbc.Col(html.H5(html.Details(children=[
                                html.Summary('Vorgabe'),
                                dcc.Loading(
                                    children=dcc.Textarea(
                                        id='textarea3',
                                        style={'width': '100%', 'height': 300}
                                    ),
                                    type="circle",
                                )])), md=6),
                        ]),
                        dbc.Row([
                            dbc.Col(html.H5('Code 1'), md=6,
                                    className="title_container"),
                            dbc.Col(html.H5('Code 2'), md=5,
                                    className="title_container"),
                            dbc.Col(html.H5(
                                id='labled_pairs_string'), md=1, className="title_container"),
                        ]),
                        # TODO use prettify
                        dbc.Row([
                            dbc.Col(dcc.Loading(
                                children=dcc.Textarea(
                                    id='textarea1',
                                    style={
                                        'width': '100%', 'height': 600, 'fonz-size': '32px'},
                                ),
                                type="circle",
                            )),
                            dbc.Col(dcc.Loading(
                                children=dcc.Textarea(
                                    id='textarea2',
                                    style={'width': '100%',
                                           'height': 600},
                                ),
                                type="circle",
                            )),
                        ]),
                        dbc.Row([
                            dbc.Col(html.Div(id='answer_1'), md=6,
                                    className="graph_container"),
                            dbc.Col(html.Div(id='answer_2'), md=6,
                                    className="graph_container"),
                        ]),
                        dbc.Row([
                            html.Div(children='Eine Skala zum Labeln von Plagiaten. Eine 1 bedeutet Plagiat und eine 0 kein Plagiat', style={
                                'textAlign': 'center'
                            }),
                        ]),
                        dbc.Row([
                            dbc.Col(dcc.Slider(0, 1, 0.01, value=0.5, marks={0: "0", 0.25: "0.25", 0.5: "0.5", 0.75: "0.75", 1: "1"}, id='score',
                                tooltip={"placement": "bottom", "always_visible": True}), md=12, className="graph_container"),
                        ]),
                        dbc.Row([
                            # dbc.Col(html.Button('vorheriges Paar', id='previous',
                            #         n_clicks=0), md=4, className="button", width={"offset": 1}),
                            dbc.Col(dbc.Button('Download [...]_labled.csv', id='download',
                                    n_clicks=0), md=4, className="button_do", width={"offset": 1}),
                            dcc.Download(id="download-text"),
                            dbc.Col(dbc.Button(
                                'bewerten und weiter', id='done_next', n_clicks=0), md=4, className="button"),
                            dbc.Col(dbc.Button('überspringen', id='next',
                                    n_clicks=0), md=3, className="button"),
                        ]),
                        ],
                    className="h-100"), md=12, className="content")
            ], className="h-100"),
    ], className="h-100", id='page-lable_pairs'
    ),
    dcc.Store(id='st_labled_pairs'),
    dcc.Store(id='st_last_id'),
    dcc.Store(id='st_last_task'),
    # dcc.Store(id='st_last_ids_list'),
], className="h-100")


@ callback(
    Output('textarea1', 'value'),
    Output('textarea2', 'value'),
    Output('textarea3', 'value'),
    Output('aufgabenstellung', 'srcDoc'),
    Output('labled_pairs_string', 'children'),
    Output('score', 'value'),
    Output('st_labled_pairs', 'data'),
    Output('st_df_labled_len', 'data'),
    Output('st_df_labled', 'data'),
    Output('st_last_id', 'data'),
    Output('st_last_task', 'data'),
    # Input('previous', 'n_clicks'),
    Input('done_next', 'n_clicks'),
    Input('next', 'n_clicks'),
    State('score', 'value'),
    State('st_df_labled_len', 'data'),
    State('st_df_labled', 'data'),
    State('st_labled_pairs', 'data'),
    State('st_last_id', 'data'),
    State('st_last_task', 'data'),
    State('st_given_csv', 'data'),
    State('st_semester', 'data'),
    State('st_ha', 'data'),
    State('st_tasks', 'data'),
    State('st_prog_language', 'data'))
def button_pressed(done_clicks, next_clicks, label, st_df_labled_len, st_df_labled, st_labled_pairs, st_last_id, st_last_task, st_given_csv, st_semester, st_ha, st_tasks, st_prog_language):
    ctx = dash.callback_context
    if st_df_labled == None or st_last_id == None:
        # print('initial call triggered this callback')
        labled_pairs = 0
        # print((st_semester, st_ha, st_tasks, st_prog_language))
        if st_given_csv == None or st_given_csv == 'null':
            # print("ohne csv")
            try:
                df_labled, df_labled_len = csv_stuff.create_labled_table_routine(
                    loads(st_semester), loads(st_ha), loads(st_tasks), loads(st_prog_language))
                # print(type(df_labled.head(3)))
                # print(df_labled.head(3))
            except TypeError:
                raise dash.exceptions.PreventUpdate
        else:
            print("mit csv")
            # print(type(st_given_csv))
            df_labled = loads(st_given_csv)
            df_labled_len = len(st_given_csv)
            labled_pairs = csv_stuff.count_labled(df_labled)
        rt = get_new_pair_routine(df_labled, 0, "")
        return rt[0], rt[1], rt[2], rt[3], f'{labled_pairs}/{df_labled_len} Paaren', rt[4], dumps(labled_pairs), dumps(df_labled_len), df_labled.to_json(date_format='iso', orient='split'), dumps(rt[5]), dumps(rt[6])
    df_labled = pd.read_json(st_df_labled, orient='split')
    # print(df_labled.head(3))
    # print((st_semester, st_ha, st_tasks, st_prog_language))
    # print((st_last_id, st_last_task, len(st_df_labled)))
    last_id = int(loads(st_last_id))
    last_task = loads(st_last_task)
    if ctx.triggered_id == 'done_next':
        df_labled_len = loads(st_df_labled_len)
        labled_pairs = loads(st_labled_pairs)
        # print((last_id, last_task, label, labled_pairs))
        # print('label_button_pressed ' + str(done_clicks))
        valid_set, labled_pairs, df_labled = csv_stuff.set_label(
            df_labled, last_id, label, labled_pairs)
        if not valid_set:
            raise dash.exceptions.PreventUpdate
        rt = get_new_pair_routine(df_labled, last_id+1, last_task)
        return rt[0], rt[1], rt[2], rt[3], f'{labled_pairs}/{df_labled_len} Paaren', rt[4], dumps(labled_pairs), dash.no_update, df_labled.to_json(date_format='iso', orient='split'), dumps(rt[5]), dumps(rt[6])
    elif ctx.triggered_id == 'next':
        rt = get_new_pair_routine(df_labled, last_id+1, last_task)
        return rt[0], rt[1], rt[2], rt[3], dash.no_update, rt[4], dash.no_update, dash.no_update, dash.no_update, dumps(rt[5]), dumps(rt[6])
    # elif ctx.triggered_id == 'previous':
    #     return get_new_pair_routine(df_labled)
    else:
        raise dash.exceptions.PreventUpdate


def get_new_pair_routine(df_labled, last_id, last_task):
    next = csv_stuff.get_new_pair(df_labled, last_task, last_id)
    # print(f'last id in get_new_pair_routine: {last_id}')
    if next == None:
        return '', '', '', '', 0.5, last_id, last_task
    last_id = next[5]
    if next[2] == None:
        return next[0], next[1], dash.no_update, dash.no_update, next[4], last_id, last_task
    last_task = next[6]
    return next[0], next[1], next[2], next[3], next[4], last_id, last_task


@ callback(
    Output('download-text', 'data'),
    Input('download', 'n_clicks'),
    State('st_semester', 'data'),
    State('st_ha', 'data'),
    State('st_prog_language', 'data'),
    State('st_df_labled', 'data'), prevent_initial_call=True)
def download_button_pressed(_, st_semester, st_ha, st_prog_language, st_df_labled):
    ctx = dash.callback_context
    if ctx.triggered_id != 'download':
        raise dash.exceptions.PreventUpdate
    file_name = f'PPR [{loads(st_semester)}]-{loads(st_ha)}. Hausaufgabe - Pflichttest {loads(st_prog_language)}-Antworten_labled.csv'
    return dcc.send_data_frame(pd.read_json(st_df_labled, orient='split').to_csv, file_name)


@ callback(
    Output('retry_message', 'children'),
    Input('st_semester', 'data'),
    Input('st_ha', 'data'),
    Input('st_tasks', 'data'),
    Input('st_prog_language', 'data'))
def print_retry_message(st_semester, st_ha, st_tasks, st_prog_language):
    if st_semester == None and st_ha == None and st_tasks == None and st_prog_language == None:
        return [html.B('Drücken Sie auf "PPR Hausaufgaben Labeltool"'), " um eine neue Sesssion zu starten!"]
    else:
        return dash.no_update


# checked
# 1. erfolgreichen match hinbekommen
# 2. empty_solution_matrix richtig setzen
# 3. dann daraus ein paar ableiten
# 4. dann daraus eine tabellenreihe für ...labled.csv machen
# 5. dann eine ganze tabelle draus machen
# 6. wo wird tabelle zwischengespeichert? --> aktuelle Session des users (dcc.store)
# 7. funktion schreiben die die erste Routine macht mit #aller paar und #aller bereits gelableten und die 3 texte ausgibt
# 7.1 funktion schreiben, die ein lable übergeben bekommt, in tabelle einträgt und ein neues paar zurückgibt (ggf. auch neue vorgabe)
# gibt es ein Download fenster? --> ja, da dynos in heroku nicht global speichern können
# 7.2 set_label zum laufen bringen
# 8. Download button realisieren
# 8.1 temporäre speicherung des df_labels
# 12. beide pages gleichzeitig zum laufen bringen
# 13. callbacks für init page schreiben
# 15. loading state für page lable_pairs hinzufügen
# 16. ausklappbares Feld für die Aufgabenstellung hinzufügen hinzufügen
# 16.1 vorgabe in ausklappbares Feld umwandeln --> code1 und 2 in 50% große felder ändern

# unchecked
# TODO (9. neuen knopf für previous labled hinzufügen)
# TODO (10. liste für gelabelte ids hinzufügen)
# TODO (11. liste für nicht gelabelte ids hinzufügen)
# TODO 14. back end für halbgelabelte csv im drag&drop realisieren
# TODO 17. gespiegeltes paar gleichzeitig labeln / keine gespiegelten Paare + difflib von max(difflib(a,b), difflib(b,a))
# TODO 18. mithilfe von difflib oder anderem plagiates checker die paare prelabeln
# TODO 19. font size von code anpassen
# TODO 20. website scrollable machen
# TODO 21. csv_stuff in class umschreiben, damit übergabeparameter sich wegkürzen
# TODO 22. google how to manage multiple return values + consistenc
# TODO 23. code mithilfe von bibliotheken highlighten
# TODO checken weshalb nur 12/13 leere abgaben bei antwort 10 gefunden wurden
# TODO double linked list, für die id schreiben, um prev und next button zu realisieren
# only needed if running single page dash app instead
if __name__ == '__main__':
    app.run_server(debug=True)
