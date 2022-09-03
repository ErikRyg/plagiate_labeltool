# -*- coding: utf-8 -*-
from turtle import width
import dash
from dash import no_update, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import plotly.graph_objs as go

from datetime import datetime, date
from sklearn.manifold import MDS
# import js2py for highlight code, but dont know how to use it

import pandas as pd
import base64
import io
import numpy as np
import random
from src import csv_stuff

#TODO logo funktioniert nicht
PLOTLY_LOGO = "./src/logo.png"

GLOBAL_MARGIN = {'l': 60, 'b': 60, 't': 10, 'r': 10}
GLOBAL_MARGIN_BOTTOMLARGE = {'l': 60, 'b': 100, 't': 10, 'r': 10}
GLOBAL_MARKER_SIZE = 7
GLOBAL_TEMPLATE = "plotly_white"

# only needed if running single page dash app instead
external_stylesheets = [dbc.themes.CERULEAN]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# dash.register_page(__name__)
last_task = 0
last_id = -1
labled_pairs = 0
all_pairs = csv_stuff.df_labled_len
data = ["Text1", "Text2", "Text3", "Text4", "Text5"]
current1 = 0
current2 = 1
scores = []

# remove app when using index.py
# layout = html.Div([
app.layout = html.Div([
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
                            # no_gutters=True,
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
                                f'{labled_pairs}/{all_pairs} Paaren', id='number_labled'), md=0, className="title_container"),
                        ]),
                        #TODO use prettify
                        dcc.Textarea(
                            id='textarea1',
                            wrap='<pre>',
                            style={'width': '33%', 'height': 700},
                        ),
                        dcc.Textarea(
                            id='textarea2',
                            style={'width': '33%', 'height': 700},
                            className="code",
                        ),
                        dcc.Textarea(
                            id='textarea3',
                            style={'width': '33%', 'height': 700},
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
], className="h-100")



@app.callback(
    Output('textarea1', 'value'),
    Output('textarea2', 'value'),
    Output('textarea3', 'value'),
    Output('caption1', 'children'),
    Output('caption2', 'children'),
    Output('number_labled', 'children'),
    Input('previous', 'n_clicks'),
    Input('done_next', 'n_clicks'),
    Input('next', 'n_clicks'),
    Input('score', 'value'))
def button_pressed(prev_clicks, done_clicks, next_clicks, label):
    # print('button pressed ' + str(n_clicks))
    ctx = dash.callback_context
    if ctx.triggered_id == None:
        rt = get_new_pair_routine(csv_stuff.df_labled)
        return  rt[0], rt[1], rt[2], rt[3], rt[4], dash.no_update
    elif ctx.triggered_id == 'done_next':
        # global last_id
        global last_task
        global labled_pairs
        global all_pairs
        print('label_button_pressed ' + str(done_clicks))
        valid_set, labled_pairs = csv_stuff.set_label(csv_stuff.df_labled, last_id, label, labled_pairs)
        if not valid_set:
            raise dash.exceptions.PreventUpdate
        rt = get_new_pair_routine(csv_stuff.df_labled)
        return rt[0], rt[1], rt[2], rt[3], rt[4], f'{labled_pairs}/{all_pairs} Paaren'
    elif ctx.triggered_id == 'next':
        rt = get_new_pair_routine(csv_stuff.df_labled)
        return rt[0], rt[1], rt[2], rt[3], rt[4], dash.no_update
    # elif ctx.triggered_id == 'previous':
    #     return get_new_pair_routine(csv_stuff.df_labled)
    else:
        raise dash.exceptions.PreventUpdate


def get_new_pair_routine(df_labled):
    global last_id
    global last_task
    # print(f'last id in get_new_pair_routine: {last_id}')
    next = csv_stuff.get_new_pair(df_labled, last_task, last_id)
    print(f'last id in get_new_pair_routine: {last_id}')
    if next == None:
        return '', '', '', 'Niemandes Code', 'Niemandes Code'
    last_id = next[5]
    if next[2] == None:
        return next[0], next[1], dash.no_update, next[3], next[4]
    last_task = next[6]
    return next[0], next[1], next[2], next[3], next[4]



#TODO
# @app.callback(
#     Output('textarea1', 'value'),
#     Output('textarea2', 'value'),
#     Output('textarea3', 'value'),
#     Output('caption1', 'children'),
#     Output('caption2', 'children'),
#     Input('previous', 'n_clicks'), prevent_initial_call=True)
# def prev_button_pressed(n_clicks, value):
#     global last_id
#     global last_task
#     print('button pressed ' + str(n_clicks))
#     next = csv_stuff.get_new_pair(csv_stuff.df_labled, last_task, last_id)
#     if next == None:
#         return '', '', '', 'Niemandes Code', 'Niemandes Code'
#     last_id = next[5]
#     if next[2] == None:
#         return next[0], next[1], dash.no_update, next[3], next[4]
#     last_task = next[6]
#     return next[0], next[1], next[2], next[3], next[4]


@app.callback(
    Output('download-text', 'data'),
    Input('download', 'n_clicks'), prevent_initial_call=True)
def download_button_pressed(n_clicks):
    file_name = f'PPR [{csv_stuff.semester}]-{csv_stuff.ha}. Hausaufgabe - Pflichttest {csv_stuff.prog_language}-Antworten_labled.csv'
    return dcc.send_data_frame(csv_stuff.df_labled.to_csv, file_name)



#TODO how does the initial start works; every input sensitive callback starts??
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
# only needed if running single page dash app instead
if __name__ == '__main__':
    # print((csv_stuff.df_labled, type(csv_stuff.df_labled)))
    app.run_server(debug=True)
