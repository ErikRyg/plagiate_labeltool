import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from json import loads, dumps
from .src import csv_stuff

PLOTLY_LOGO = "../assets/logo.png"
# semester = 'SoSe21'
# ha = '9'
# # tasks = ['Antwort 9']
# tasks = ['Antwort 8', 'Antwort 9', 'Antwort 10']
# prog_language = 'C'
# last_task = 0
# last_id = -1
# labled_pairs = 0
# df_labled, df_labled_len = csv_stuff.create_labled_table_routine(
#     semester, ha, tasks, prog_language)
# df_labled_len = df_labled_len

dash.register_page(__name__)

layout = html.Div([
    # content will be rendered in this element
    html.Div([
        dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Img(src=PLOTLY_LOGO, height="30px")),
                                dbc.Col(dbc.NavbarBrand(
                                    "PPR Hausaufgaben Labeltool", className="ml-2")),
                            ],
                            align="center",
                        ),
                        href="/init"
                        # href="https://www.ni.tu-berlin.de/menue/members/postgraduate_students_and_doctoral_candidates/goerttler_thomas/",
                    ),
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
                            dbc.Col(html.H5('Code 1', id='caption1'), md=4,
                                    className="title_container"),
                            dbc.Col(html.H5('Code 2', id='caption2'), md=4,
                                    className="title_container"),
                            dbc.Col(html.H5('Vorgabe'), md=3,
                                    className="title_container"),
                            dbc.Col(html.H5(
                                id='labled_pairs_string'), md=0, className="title_container"),
                        ]),
                        # TODO use prettify
                        dcc.Textarea(
                            id='textarea1',
                            wrap='<pre>',
                            style={'width': '33%', 'height': 600},
                        ),
                        dcc.Textarea(
                            id='textarea2',
                            style={'width': '33%', 'height': 600},
                            className="code",
                        ),
                        dcc.Textarea(
                            id='textarea3',
                            style={'width': '33%', 'height': 600},
                        ),
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
                            # dbc.Col(dcc.Slider(min=0, max=1, step=0.05, value=0.5, id='score'), md=6, className="graph_container"),
                            dbc.Col(dcc.Slider(0, 1, 0.01, value=0.5, marks={0: "0", 0.25: "0.25", 0.5: "0.5", 0.75: "0.75", 1: "1"}, id='score',
                                tooltip={"placement": "bottom", "always_visible": True}), md=12, className="graph_container"),
                        ]),
                        dbc.Row([
                            dbc.Col(html.Button('vorheriges Paar', id='previous',
                                    n_clicks=0), md=4, className="button", width={"offset": 1}),
                            dbc.Col(html.Button(
                                'bewerten und weiter', id='done_next', n_clicks=0), md=4, className="button"),
                            dbc.Col(html.Button('überspringen', id='next',
                                    n_clicks=0), md=2, className="button"),
                            dbc.Col(html.Button('Download [...]_labled.csv', id='download',
                                    n_clicks=0), md=0, className="button_do"),
                            dcc.Download(id="download-text")
                        ]),
                        ],
                    className="h-100"), md=12, className="content")
            ], className="h-100"),
    ], className="h-100", id='page-lable_pairs'
    ),
    dcc.Store(id='st_labled_pairs'),
    dcc.Store(id='st_last_id'),
    dcc.Store(id='st_last_task'),
], className="h-100")


# @app.callback(
#     Output('semester', 'data'),
#     Output('ha', 'data'),
#     Output('tasks', 'data'),
#     Output('prog_language', 'data'),
#     Output('df_labled_len', 'data'),
#     Output('df_labled', 'data'))
# def init_call(semester, ha, tasks, prog_language):
#     # print('button pressed ' + str(n_clicks))
#     df_labled, df_labled_len = csv_stuff.create_labled_table_routine(semester, ha, tasks, prog_language)
#     return dumps(semester), dumps(ha), dumps(tasks), dumps(prog_language), dumps(df_labled_len), df_labled.to_json(date_format='iso', orient='split')


@callback(
    Output('textarea1', 'value'),
    Output('textarea2', 'value'),
    Output('textarea3', 'value'),
    Output('caption1', 'children'),
    Output('caption2', 'children'),
    Output('labled_pairs_string', 'children'),
    Output('st_labled_pairs', 'data'),
    Output('st_df_labled_len', 'data'),
    Output('st_df_labled', 'data'),
    Output('st_last_id', 'data'),
    Output('st_last_task', 'data'),
    Input('previous', 'n_clicks'),
    Input('done_next', 'n_clicks'),
    Input('next', 'n_clicks'),
    Input('score', 'value'),
    State('st_df_labled_len', 'data'),
    State('st_df_labled', 'data'),
    State('st_labled_pairs', 'data'),
    State('st_last_id', 'data'),
    State('st_last_task', 'data'),
    State('st_given_csv', 'data'),
    State('st_semester', 'data'),
    State('st_ha', 'data'),
    State('st_tasks', 'data'),
    State('st_prog_language', 'data'))  # , prevent_initial_call=True
def button_pressed(prev_clicks, done_clicks, next_clicks, label, st_df_labled_len, st_df_labled, st_labled_pairs, st_last_id, st_last_task, st_given_csv, st_semester, st_ha, st_tasks, st_prog_language):
    # print('button pressed ' + str(n_clicks))
    ctx = dash.callback_context
    if st_df_labled == None:
        print('initial call triggered this callback')
        given_csv = st_given_csv
        labled_pairs = 0
        print((st_semester, st_ha, st_tasks, st_prog_language))
        # print((loads(st_semester), loads(st_ha), loads(
        # st_tasks), loads(st_prog_language)))
        if given_csv == None or given_csv == 'null':
            print("ohne csv")
            df_labled, df_labled_len = csv_stuff.create_labled_table_routine(
                loads(st_semester), loads(st_ha), loads(st_tasks), loads(st_prog_language))
        else:
            print("mit csv")
            print(type(given_csv))
            print(given_csv)
            df_labled = loads(given_csv)
            df_labled_len = len(given_csv)
            labled_pairs = csv_stuff.count_labled(df_labled)
        rt = get_new_pair_routine(df_labled, 0, "")
        return rt[0], rt[1], rt[2], rt[3], rt[4], f'{labled_pairs}/{df_labled_len} Paaren', dumps(labled_pairs), dumps(df_labled_len), df_labled.to_json(date_format='iso', orient='split'), dumps(rt[5]), dumps(rt[6])
    print(ctx.triggered_id)
    df_labled = pd.read_json(st_df_labled, orient='split')
    last_id = int(loads(st_last_id))
    last_task = loads(st_last_task)
    # if ctx.triggered_id == None:
    #     rt = get_new_pair_routine(df_labled, last_id, last_task)
    #     return rt[0], rt[1], rt[2], rt[3], rt[4], dash.no_update, dash.no_update, dash.no_update, dumps(rt[5]), dumps(rt[6])
    if ctx.triggered_id == 'done_next':
        print((last_id, last_id+1))
        df_labled_len = loads(st_df_labled_len)
        labled_pairs = loads(st_labled_pairs)
        print('label_button_pressed ' + str(done_clicks))
        valid_set, labled_pairs, df_labled = csv_stuff.set_label(
            df_labled, last_id, label, labled_pairs)
        if not valid_set:
            raise dash.exceptions.PreventUpdate
        rt = get_new_pair_routine(df_labled, last_id+1, last_task)
        return rt[0], rt[1], rt[2], rt[3], rt[4], f'{labled_pairs}/{df_labled_len} Paaren', dumps(labled_pairs), dash.no_update, df_labled.to_json(date_format='iso', orient='split'), dumps(rt[5]), dumps(rt[6])
    elif ctx.triggered_id == 'next':
        rt = get_new_pair_routine(df_labled, last_id+1, last_task)
        return rt[0], rt[1], rt[2], rt[3], rt[4], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dumps(rt[5]), dumps(rt[6])
    # elif ctx.triggered_id == 'previous':
    #     return get_new_pair_routine(df_labled)
    else:
        raise dash.exceptions.PreventUpdate


def get_new_pair_routine(df_labled, last_id, last_task):
    # print(f'last id in get_new_pair_routine: {last_id}')
    next = csv_stuff.get_new_pair(df_labled, last_task, last_id)
    print(f'last id in get_new_pair_routine: {last_id}')
    if next == None:
        return '', '', '', 'Niemandes Code', 'Niemandes Code', last_id, last_task
    last_id = next[5]
    if next[2] == None:
        return next[0], next[1], dash.no_update, next[3], next[4], last_id, last_task
    last_task = next[6]
    return next[0], next[1], next[2], next[3], next[4], last_id, last_task


# # TODO
# # @app.callback(
# #     Output('textarea1', 'value'),
# #     Output('textarea2', 'value'),
# #     Output('textarea3', 'value'),
# #     Output('caption1', 'children'),
# #     Output('caption2', 'children'),
# #     Input('previous', 'n_clicks'), prevent_initial_call=True)
# # def prev_button_pressed(n_clicks, value):
# #     global last_id
# #     global last_task
# #     print('button pressed ' + str(n_clicks))
# #     next = csv_stuff.get_new_pair(df_labled, last_task, last_id)
# #     if next == None:
# #         return '', '', '', 'Niemandes Code', 'Niemandes Code'
# #     last_id = next[5]
# #     if next[2] == None:
# #         return next[0], next[1], dash.no_update, next[3], next[4]
# #     last_task = next[6]
# #     return next[0], next[1], next[2], next[3], next[4]


# @app.callback(
@callback(
    Output('download-text', 'data'),
    Input('download', 'n_clicks'),
    State('st_semester', 'data'),
    State('st_ha', 'data'),
    State('st_prog_language', 'data'),
    State('st_df_labled', 'data'), prevent_initial_call=True)
def download_button_pressed(n_clicks, st_semester, st_ha, st_prog_language, st_df_labled):
    ctx = dash.callback_context
    if ctx.triggered_id != 'download':
        raise dash.exceptions.PreventUpdate
    file_name = f'PPR [{loads(st_semester)}]-{loads(st_ha)}. Hausaufgabe - Pflichttest {loads(st_prog_language)}-Antworten_labled.csv'
    return dcc.send_data_frame(pd.read_json(st_df_labled, orient='split').to_csv, file_name)


# TODO how does the initial start works; every input sensitive callback starts??
# --> if clicked == None: raise dash.exceptions.PreventUpdate or
# --> prevent_initial_call=True
"""
- download text in csv umwandeln
- globale variablen ersetzen, da gefährlich (https://dash.plotly.com/sharing-data-between-callbacks)
- Datenanbindung an richtige Daten
- vermutlich die textviews noch scorralbe machen für lange aufgaben
- code muss schön aussehen (tabs etc angezeigt werden)
(- syntax highliting wäre natürlich super, aber evtl. Doch sehr schwierig und zeitaufwändig)
- auf bspw. Heroku deployen, sodass andere Personen (Tobias, Paula, ..) direkt darauf zugreifen können
"""
# checked
# TODO 1. erfolgreichen match hinbekommen        *check*
# TODO 2. empty_solution_matrix richtig setzen   *check*
# TODO 3. dann daraus ein paar ableiten          *check*
# TODO 4. dann daraus eine tabellenreihe für ...labled.csv machen *check*
# TODO 5. dann eine ganze tabelle draus machen   *check*
# TODO! 6. wo wird tabelle zwischengespeichert?
# TODO 7. funktion schreiben die die erste Routine macht mit #aller paar und #aller bereits gelableten und die 3 texte ausgibt  *check*
# TODO 7.1 funktion schreiben, die ein lable übergeben bekommt, in tabelle einträgt und ein neues paar zurückgibt (ggf. auch neue vorgabe)    *check*
# TODO gibt es ein Download fenster? --> ja, da dynos in heroku nicht global speichern können       *check*
# TODO 7.2 set_label zum laufen bringen      *check*
# TODO 8. Download button realisieren        *check*

# unchecked
# TODO 8.1 temporäre speicherung des df_labels
# TODO (9. neuen knopf für previous labled hinzufügen)
# TODO (10. liste für gelabelte ids hinzufügen)
# TODO (11. liste für nicht gelabelte ids hinzufügen)
# TODO 12. beide pages gleichzeitig zum laufen bringen
# TODO 13. callbacks für init page schreiben
# TODO 14. back end für halbgelabelte csv im drag&drop realisieren
# TODO checken weshalb nur 12/13 leere abgaben bei antwort 10 gefunden wurden
# TODO double linked list, für die id schreiben, um prev und next button zu realisieren
# only needed if running single page dash app instead
if __name__ == '__main__':
    # print((df_labled, type(df_labled)))
    app.run_server(debug=True)
