from dash import Dash, html, dcc, Input, Output
import dash
import dash_bootstrap_components as dbc

GLOBAL_MARGIN = {'l': 60, 'b': 60, 't': 10, 'r': 10}
GLOBAL_MARGIN_BOTTOMLARGE = {'l': 60, 'b': 100, 't': 10, 'r': 10}
GLOBAL_MARKER_SIZE = 7
GLOBAL_TEMPLATE = "plotly_white"

external_stylesheets = [dbc.themes.CERULEAN]
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dash.page_container,
    dcc.Store(id='st_semester'),
    dcc.Store(id='st_ha'),
    dcc.Store(id='st_tasks'),
    dcc.Store(id='st_prog_language'),
    dcc.Store(id='st_df_labled_len'),
    dcc.Store(id='st_df_labled'),
    # dcc.Store(id='st_df_labled_tmp'),
    dcc.Store(id='st_given_csv'),
])


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
