import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# must add this line in order for the app to be deployed successfully on Heroku
# from app import app
# from app import server
# import all pages in the app
from pages import init
from plagiate_labeltool.pages import label_pairs

PLOTLY_LOGO = "./assets/logo.png"

GLOBAL_MARGIN = {'l': 60, 'b': 60, 't': 10, 'r': 10}
GLOBAL_MARGIN_BOTTOMLARGE = {'l': 60, 'b': 100, 't': 10, 'r': 10}
GLOBAL_MARKER_SIZE = 7
GLOBAL_TEMPLATE = "plotly_white"

# bootstrap theme
# https://bootswatch.com/lux/
# external_stylesheets = [dbc.themes.LUX]

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
external_stylesheets = [dbc.themes.CERULEAN]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)
server = app.server
app.config.suppress_callback_exceptions = True

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("PPR Hausaufgaben Labeltool", className="ml-2")),
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
)

app.layout = html.Div([
    dcc.Location(pathname="/init", id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
    # dash.page_container
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/lable_pairs':
        return label_pairs.layout
    elif pathname == '/init':
        return init.layout
    else:
        return '404'

"""
0.1 index datei löschen und nur noch mit app.py arbeiten *check*
0.2 knopf für sprache und knopf zum von vorne anfangen hinzufügen *okay*
1. start knopf drücken und seite wechseln
2. gesetzte parameter der neuen seite übergeben
3. parameter erhalten
4. dateien einlesen
5. nur gewünschte tabelle lesen
6. paare zählen
(7. leere dateien komplett weglassen)
8. ein paar anzeigen lassen
9. label knopf implementieren
10. gelabeltes paar in ein dataframe hinzufügen
11. knopf zum pausieren und downloaden hinzufügen und implementieren
"""
if __name__ == '__main__':
    app.run_server(debug=True)
