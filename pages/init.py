import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plagiate_labeltool.pages.label_pairs as label_pairs
PLOTLY_LOGO = "../assets/logo.png"

GLOBAL_MARGIN = {'l': 60, 'b': 60, 't': 10, 'r': 10}
GLOBAL_MARGIN_BOTTOMLARGE = {'l': 60, 'b': 100, 't': 10, 'r': 10}
GLOBAL_MARKER_SIZE = 7
GLOBAL_TEMPLATE = "plotly_white"

external_stylesheets = [dbc.themes.CERULEAN]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# dash.register_page(__name__)

list_semester = ["SoSe19", "SoSe20", "SoSe21",
                 "SoSe22", "WiSe20", "WiSe21", "WiSe22"]
dataset_names = ["raw.csv", "raw_c.csv"]

app.layout = html.Div(
    # layout = html.Div(
    [
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
                            no_gutters=True,
                        ),
                        href="/init",
                        # href="https://www.ni.tu-berlin.de/menue/members/postgraduate_students_and_doctoral_candidates/goerttler_thomas/",
                    ),
                ]
            ),
            color="primary",
            dark=True,
            id="navbar",
        ),
        dbc.Col(html.Button('starten', id='start', n_clicks=0), md=6),
        html.Div(id="page-content")
    ],
    id='page-init',
    className="h-100"
)

init_page = html.Div([
    dbc.Row([
            dbc.Col(html.Label('Wähle das jeweilige Semester aus'), md=6),
            # TODO welche HA soll gelabelt werden hinzufügen
            dbc.Col(html.Label(
                'Wähle die zu labelnden Aufgaben aus'), md=6),
            ]),
    dbc.Row([
            # html.Br(),
            dbc.Col(dcc.Dropdown(list_semester,
                    'Semesterwahl', id='semester'), md=6),
            dbc.Col(dcc.Dropdown(['Aufgabe 1', 'Aufgabe 2', 'Aufgabe 3', 'Aufgabe 4', 'Aufgabe 5', 'Aufgabe 6', 'Aufgabe 7', 'Aufgabe 8', 'Aufgabe 9', 'Aufgabe 10'],
                                    ['Aufgabe 7', 'Aufgabe 8', 'Aufgabe 9'],
                                    multi=True), md=4),
            ]),
    html.Hr(),
    html.Label('Falls du einige Paare der Hausaufgabe bereits gelabelt hast, dann füge die bisherige csv Datei hier hinzu'),
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
            html.Label('Keine bereits angefangene gelablete csv-Datei benutzen'),
            html.Div([
                dcc.RadioItems(
                    ['Keine bereits angefangene gelablete csv-Datei benutzen'],
                    None,
                    id='continue_label'
                    # ,
                    # inline=True
                ),
            ]),
            ]),
    html.Hr(),
    dbc.Row([
            html.Div([
                dbc.Col(
                    html.Div([
                        dcc.RadioItems(
                            ['Java', 'C'],
                            'C',
                            id='language'),
                    ]),
                    md=6),
            ]),
            dbc.Col(html.Button('starten', id='start', n_clicks=0), md=6),
            ]),
])


# @callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/lable_pairs':
#         return lable_pairs.layout
#     elif pathname == '/init':
#         return init.layout
#     else:
#         return '404'

@callback(
    Output("page-content", "children"),
    Input("start", "n_clicks")
)
def continue_to_label_page(clicked):
    if clicked == 0:
        return init_page
    else:
        return label_pairs.layout


if __name__ == '__main__':
    app.run_server(debug=True)
