# -*- coding: utf-8 -*-
from turtle import width
import dash
from dash import no_update, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import plotly.graph_objs as go

# from helper import *
# from data import Data

from datetime import datetime, date
from sklearn.manifold import MDS
import dash_table as dt

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

code1 = """#include <stdio.h>

void factorize(long product, long *factor1, long *factor2)
{
	int i=2;


    if (product==0 || product==1 )
    {
        *factor1 = 1;
        *factor2 = product;
    }
    else if (product>2)
    {
        for (i=2; i<=product ; i++)
        {
            if (product%i==0)
            {
                *factor2=i;
                *factor1=product/i;
                break;
            }
        }
    }
}

int main(){
        long product, factor1, factor2;
	printf("Please enter an Integer: ");
        scanf("%li",&product);
        factorize(product, &factor1, &factor2);
	printf("Possible Factors of %li are %li and %li.\n",product,factor1,factor2);
	return 0;
}"""
code2 = """#include <stdio.h>

void factorize(long produkt, long *faktor1, long *faktor2)
{
	if(produkt <=1){
		*faktor1=1;
		*faktor2=produkt;
	}
	else{
		long i=2;
		while (i<=produkt){
			long temp=produkt % i;
			if(temp==0){
				*faktor1=produkt/i;
				*faktor2=i;
				break;
			}
			i++;

		}

	}
}

int main(){
	long produkt;
	long faktor1;
	long faktor2;
	printf("Please enter an Integer: ");
	scanf("%ld",&produkt);
	factorize(produkt, &faktor1, &faktor2);
	printf("Possible Factors of %ld are %ld and %ld.\n", produkt, faktor1, faktor2);
	return 0;
}"""
vorgabe = """<pre><code>#include <stdio.h>

void factorize (long resultat, long *nummer1, long *nummer2)
{
	// Your factorization
	if (resultat == 0 || resultat == 1) {
		*nummer1 = 1;
		*nummer2 = resultat;
	} else {
		int i = 0;
		while (resultat % (resultat/2 - i) != 0) {
			i++;
		}
		*nummer1 = resultat/2 - i;
		*nummer2 = resultat/(*nummer1);
	}
}

int main(){
	printf("Please enter an Integer: ");
	long resultat, nummer1, nummer2;
	scanf("%ld",&resultat);
	factorize(resultat, &nummer1, &nummer2);
	printf("Possible Factors of %ld are %ld and %ld.\n",resultat, nummer1 , nummer2);
	return 0;
}</code></pre>"""
labled_pairs = 1
all_pairs = 2
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
                            dbc.Col(html.H5('Code 1'), md=4,
                                    className="title_container"),
                            dbc.Col(html.H5('Code 2'), md=4,
                                    className="title_container"),
                            dbc.Col(html.H5('Vorgabe'), md=3,
                                    className="title_container"),
                            dbc.Col(html.H5(
                                f'{labled_pairs}/{all_pairs} Paaren'), md=0, className="title_container"),
                        ]),
                        dcc.Textarea(
                            id='textarea1',
                            value=code1,
                            style={'width': '33%', 'height': 700},
                        ),
                        dcc.Textarea(
                            id='textarea2',
                            value=code2,
                            style={'width': '33%', 'height': 700},
                            className="code",
                        ),
                        dcc.Textarea(
                            id='textarea3',
                            value=vorgabe,
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
                            dbc.Col(html.Button('Download', id='download',
                                    n_clicks=0), md=0, className="button_do"),
                            dcc.Download(id="download-text")
                        ]),
                        ],
                    className="h-100"), md=12, className="content")
            ], className="h-100"),
    ], className="h-100", id='page-lable_pairs'
    ),
], className="h-100")

# @app.callback(
#     Output("page-content", "children"),
#     Input("start", "n_clicks"))
# def start_labeling(clicks):
#     if(clicks > 1):
#         return     else:
#         return None


def find_new_samples():
    return random.randint(0, len(data)-1), random.randint(0, len(data)-1)


# @app.callback(
#     [
#         Output('answer_1', 'children'),
#         Output('answer_2', 'children'),
#     ],
#     [
#         Input('done_next', 'n_clicks'),
#     ],
#     [
#         State('score', 'value')]
#     )
# def update_dropdown(done_clicks, score):
#     if done_clicks == 0:
#         return no_update, no_update
#     else:
#         global current1
#         global current2
#         scores.append([current1, current2, score])
#         print(scores)
#         current1, current2 = find_new_samples()
#         return  data[current1], data[current2]


# @app.callback(
#     Output("download-text", "data"),
#     [Input('download', 'n_clicks')])
# def update_dropdown(n_clicks):
#     if n_clicks >= 1:
#         global scores
#         # save file (ask user where to save ...)
#         filecontet = f"{scores}"
#         scores = []
#         return dict(content=filecontet, filename="output.csv")
#     else:
#         return no_update


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
    app.run_server(debug=True)
