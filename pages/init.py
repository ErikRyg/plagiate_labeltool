import base64
import io
import pandas as pd
import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from .src import csv_stuff
from json import dumps, loads

PLOTLY_LOGO = "../assets/logo.png"
GLOBAL_MARGIN = {'l': 60, 'b': 60, 't': 10, 'r': 10}
GLOBAL_MARGIN_BOTTOMLARGE = {'l': 60, 'b': 100, 't': 10, 'r': 10}
GLOBAL_MARKER_SIZE = 7
GLOBAL_TEMPLATE = "plotly_white"

dash.register_page(__name__, path='/', redirect_from=['/init'])

list_semester = ["SoSe20", "SoSe21",
                 "SoSe22", "WS2021", "WS2122"]  # SoSe19 & WS1920 händisch hinzufügen?
dict_tasks = {'Aufgabe 7': 'Antwort 7',
              'Aufgabe 8': 'Antwort 8',
              'Aufgabe 9': 'Antwort 9',
              'Aufgabe 10': 'Antwort 10',
              'Aufgabe 11': 'Antwort 11',
              }
list_has = [str(x) for x in range(6, 11)]

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand(
                        "PPR Hausaufgaben Labeltool", className="ml-2")),
                ],
                align="center",
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
                    'C', id='prog_language', persistence=True), md=1),
            dbc.Col(html.Label(
                'Wähle die zu labelnden Aufgaben aus'), md=4),
            ]),
    dbc.Row([
            # html.Br(),
            dbc.Col(dcc.Dropdown(list_semester, list_semester[2],
                    id='semester', persistence=True), md=4),
            dbc.Col(dcc.Dropdown(list_has, list_has[4],
                    id='ha', persistence=True), md=4),
            dbc.Col(dcc.Dropdown([x for x in dict_tasks.keys()],
                                 [x for x in dict_tasks.keys()][-4:-2],
                                 id='tasks',
                                 persistence=True,
                                 multi=True), md=4),
            ]),
    html.Hr(),
    html.Label([
        html.B('Falls'), ' Sie einige Paare der Hausaufgabe bereits gelabelt haben, dann fügen Sie die bisherige csv Datei hier hinzu:']),
    dbc.Row([
        dcc.Loading(
            dcc.Upload(
                id="upload_data",
                children=html.Div(
                    [html.B("Ziehe Datei"), " (i.e. 'PPR [SoSe21]-9. Hausaufgabe - Pflichttest C-Antworten_labled.csv')", html.B(" oder klicke"), " auf das Feld"], id='upload_text'
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
            type="default",
        ),
    ]),
    html.Hr(),
    dbc.Row([
            dbc.Col(dbc.Button('starten', n_clicks=0,
                    href=dash.page_registry['pages.label_pairs']['path'], id='submit', class_name="d-grid gap-2 col-6 mx-auto"), md=12),
            ]),
])

layout = html.Div(
    [
        navbar,
        init_content,
    ],
    id='page-init',
    className="h-100"
)


# TODO csv drag and drop funktioniert noch nicht + funktionalität hinzufügen
@callback(
    Output('st_semester', 'data'),
    Output('st_ha', 'data'),
    Output('st_tasks', 'data'),
    Output('st_prog_language', 'data'),
    Output('st_given_csv', 'data'),
    Input('submit', 'n_clicks'),
    State('semester', 'value'),
    State('ha', 'value'),
    State('tasks', 'value'),
    State('prog_language', 'value'),
    State('upload_data', 'contents'),
    State('upload_data', 'filename'), prevent_initial_call=True)
def start_button_pressed(n_clicks, semester, ha, tasks, prog_language, labled_csv, filename):
    # print(
    #     f"Es Wurde eine Callback auf der init-seite ausgeführt: {n_clicks}")
    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate
    # 'Aufgabe 7' --> 'Antwort 7'
    tasks = [dict_tasks[x] for x in tasks]
    if labled_csv is not None:
        _, content_string = labled_csv.split(',')
        labled_csv = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                labled_csv = pd.read_csv(
                    io.StringIO(labled_csv.decode('utf-8')))
                # print(type(labled_csv.head(3)))
                # print(labled_csv.head(3))
                # print((dumps(semester), dumps(ha), dumps(tasks),
                #       dumps(prog_language), labled_csv.head(3)))
                return dumps(semester), dumps(ha), dumps(tasks), dumps(prog_language), labled_csv.to_json(date_format='iso', orient='split')
        except Exception as e:
            print(e)
            return dash.exceptions.PreventUpdate
    # print((dumps(semester), dumps(ha), dumps(tasks), dumps(
    #     prog_language), dumps(labled_csv)))
    return dumps(semester), dumps(ha), dumps(tasks), dumps(prog_language), dumps(labled_csv)


@callback(
    Output('upload_text', 'children'),
    Input('upload_data', 'filename'), prevent_initial_call=True)
def react_on_uploaded_data(filename):
    if 'csv' in filename:
        return ['Es wurde die Datei "', html.B(filename), '" hochgeladen. ', html.B('Achten Sie darauf'), ', dass die gewählten Optionen mit der Datei übereinstimmen!']
    else:
        return ['Die Datei "', html.B(filename), '" ist ', html.B('keine'), ' csv Datei. Bitte lade eine bereits erstellte csv Datei hoch!']
