"""Instantiate a Dash app."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd

from dash.dependencies import Input, Output

from .data import dataframe
from .layout import html_layout_original

# Load DataFrame
# df = instalytics_dataframe()
df = dataframe()

def init_Dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/Dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
            'https://fonts.googleapis.com/css?family=Lato'
        ]
    )

    # Custom HTML layout
    dash_app.index_string = html_layout_original

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            dashGraph(df),
            dashTable(df),
            dcc.Interval(
                id='interval-component',
                interval=1*3000, # in milliseconds
                n_intervals=0
            )
        ],
        id='dash-container'
    )

    # Calling callback function
    graph_callbacks(dash_app)
    table_callbacks(dash_app)

    # Pass dash_app as a parameter
    return dash_app.server 

def dashTable(df):
    """Create instalytics data table"""
    tabel = dash_table.DataTable(
        id='database-table',
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode='native',
        page_size=25
    )
    return tabel

def dashGraph(df):
    graph = dcc.Graph(
            id='histogram-graph',
            figure=
            {
                'data': [{
                    'x': df['timestamp'],
                    'y': df['suhu'],
                    'name': 'Grafik suhu ruang.',
                    'type': 'line'
                }],
                'layout': {
                    'title': 'Grafik suhu ruang.',
                    'height': 500,
                    'padding': 150
                }
            }
        )
    return graph

def graph_callbacks(app):
    @app.callback(
        Output('histogram-graph', 'figure'),
        # Input('num-multi', 'value')
        Input('interval-component', 'n_intervals')

    )
    def update_output(n_intervals):
        df2 = dataframe()
        
        fig ={
                'data': [{
                    'x': df2['timestamp'],
                    'y': df2['suhu'],
                    'name': 'Grafik suhu ruang.',
                    'type': 'line'
                }],
                'layout': {
                    'title': 'Grafik suhu ruang.',
                    'height': 500,
                    'padding': 150
                }
            }

        data=df2.to_dict('records')

        return fig

def table_callbacks(app):
    @app.callback(
        Output('database-table', 'data'),
        # Input('num-multi', 'value')
        Input('interval-component', 'n_intervals')

    )
    def update_output(n_intervals):
        df2 = dataframe()
        df2 = df2.sort_values(['id'], ascending=[0])
        
        fig ={
                'data': [{
                    'x': df2['timestamp'],
                    'y': df2['suhu'],
                    'name': 'Grafik suhu ruang.',
                    'type': 'line'
                }],
                'layout': {
                    'title': 'Grafik suhu ruang.',
                    'height': 500,
                    'padding': 150
                }
            }

        data=df2.to_dict('records')

        return data