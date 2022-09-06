import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from .src import csv_stuff
from json import dumps

PLOTLY_LOGO = "../assets/logo.png"
GLOBAL_MARGIN = {'l': 60, 'b': 60, 't': 10, 'r': 10}
GLOBAL_MARGIN_BOTTOMLARGE = {'l': 60, 'b': 100, 't': 10, 'r': 10}
GLOBAL_MARKER_SIZE = 7
GLOBAL_TEMPLATE = "plotly_white"

dash.register_page(__name__, path='/', redirect_from=['/init'])

list_semester = ["SoSe19", "SoSe20", "SoSe21",
                 "SoSe22", "WiSe20", "WiSe21", "WiSe22"]
dict_tasks = {'Aufgabe 7': 'Antwort 7',
              'Aufgabe 8': 'Antwort 8',
              'Aufgabe 9': 'Antwort 9',
              'Aufgabe 10': 'Antwort 10',
              'Aufgabe 11': 'Antwort 11',
              }

list_has = [str(x) for x in range(5, 11)]

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand(
                        "PPR Hausaufgaben Labeltool", className="ml-2")),
                ],
                align="center",
                # no_gutters=True,
            ),
            # href="https://www.ni.tu-berlin.de/menue/members/postgraduate_students_and_doctoral_candidates/goerttler_thomas/",
        ),
    ],
    color="primary",
    dark=True,
    id="navbar",
)

init_content = html.Div([
    dbc.Row([
            dbc.Col(html.Label('Wähle das jeweilige Semester aus'), md=4),
            dbc.Col(html.Label('Wähle die jeweilige Hausaufgabe aus'), md=3),
            dbc.Col(dcc.RadioItems(['Java', 'C'],
                    'C', id='prog_language'), md=1),
            dbc.Col(html.Label(
                'Wähle die zu labelnden Aufgaben aus'), md=4),
            ]),
    dbc.Row([
            # html.Br(),
            dbc.Col(dcc.Dropdown(list_semester, list_semester[2],
                    id='semester'), md=4),
            dbc.Col(dcc.Dropdown(list_has, list_has[4],
                    id='ha'), md=4),
            dbc.Col(dcc.Dropdown([x for x in dict_tasks.keys()],
                                 [x for x in dict_tasks.keys()][-4:-2],
                                 id='tasks',
                                 multi=True), md=4),
            ]),
    html.Hr(),
    html.Label(
        'Falls du einige Paare der Hausaufgabe bereits gelabelt hast, dann füge die bisherige csv Datei hier hinzu:'),
    dbc.Row([
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    ["Ziehe Datei oder klicke auf das Feld (i.e. 'PPR [SoSe21]-9. Hausaufgabe - Pflichttest C-Antworten_labled.csv')"]
                ),
                style={
                    "width": "100%",
                    "height": "300px",
                    "lineHeight": "300px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
                multiple=False,
            ),
            ]),
    dbc.Row([
            html.Div([
                dcc.Checklist(
                    ['Keine bereits angefangene csv-Datei benutzen'],
                    ['Keine bereits angefangene csv-Datei benutzen'],
                    id='continue_label'
                ),
            ]),
            ]),
    html.Hr(),
    dbc.Row([
            # dbc.Col(dcc.Link(html.Button('starten', n_clicks=0), id='start', href=dash.page_registry['pages.label_pairs']['path'], refresh=False), md=6),
            # dbc.Col(dbc.Button('starten', n_clicks=0, id='start',
            #         class_name="d-grid gap-2 col-6 mx-auto"), md=12),
            dbc.Col(dbc.Button('starten', n_clicks=0,
                    href=dash.page_registry['pages.label_pairs']['path'], id='submit', class_name="d-grid gap-2 col-6 mx-auto"), md=12),
            ]),
])

layout = html.Div(
    # layout = html.Div(
    [
        navbar,
        init_content,
    ],
    id='page-init',
    className="h-100"
)


# TODO erstes Paar wird übersprungen?
# TODO csv drag and drop funktioniert noch nicht + funktionalität hinzufügen
# store values with dcc.store and change website to label_pairs --> the init function should create the table and also store it with dcc.store
@callback(
    Output('st_semester', 'data'),
    Output('st_ha', 'data'),
    Output('st_tasks', 'data'),
    Output('st_prog_language', 'data'),
    Output('st_df_labled_len', 'data'),
    Output('st_df_labled', 'data'),
    State('semester', 'value'),
    State('ha', 'value'),
    State('tasks', 'value'),
    State('prog_language', 'value'),
    State('upload-data', 'data'),
    State('continue_label', 'value'),
    Input('submit', 'n_clicks'), prevent_initial_call=True)
def start_button_pressed(semester, ha, tasks, prog_language, labled_csv, continue_label, n_clicks):
    print(f"Es Wurde eine Callback ausgeführt: {n_clicks}")
    ctx = dash.callback_context
    # 'Aufgabe 7' --> 'Antwort 7'
    tasks = [dict_tasks[x] for x in tasks]
    if labled_csv == None:
        print("ohne csv")
        df_labled, df_labled_len = csv_stuff.create_labled_table_routine(
            semester, ha, tasks, prog_language)
    else:
        print("mit csv")
        df_labled = labled_csv
        df_labled_len = len(labled_csv)
    print((semester, ha, tasks, prog_language, df_labled_len, df_labled.head(3)))
    return dumps(semester), dumps(ha), dumps(tasks), dumps(prog_language), dumps(df_labled_len), df_labled.to_json(date_format='iso', orient='split')


# @callback(
#     Output('test', 'children'),
#     Input('start', 'n_clicks'))
# def start_button_pressed(n_clicks):
#     # ctx = dash.callback_context
#     # if ctx.triggered_id != 'start':
#     #     raise dash.exceptions.PreventUpdate
#     # if n_click == None:
#     #     return dash.no_update
#     print("Es Wurde eine Callback ausgeführt: {n_clicks}")
#     return dumps(n_clicks)
