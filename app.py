from dash import html, dcc
import dash
import dash_bootstrap_components as dbc

GLOBAL_MARGIN = {'l': 60, 'b': 60, 't': 10, 'r': 10}
GLOBAL_MARGIN_BOTTOMLARGE = {'l': 60, 'b': 100, 't': 10, 'r': 10}
GLOBAL_MARKER_SIZE = 7
GLOBAL_TEMPLATE = "plotly_white"

external_stylesheets = [dbc.themes.CERULEAN]
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets)
server = app.server

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


if __name__ == '__main__':
    app.run_server(debug=True)
