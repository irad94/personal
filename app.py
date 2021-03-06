import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from numpy import arange, array, ones
import numpy as np
from scipy import stats
import plotly.io as pio
import pandas as pd
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_spss("C:/Users/IOR_C/Downloads/Base de datos FGF21 final.sav")

df = df.select_dtypes(include=np.number)\
    .dropna(axis=1, how='all')

available_indicators = df.columns

app.layout = html.Div([

    html.H1("Plataforma de análisis"),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='FGF21_OFICIAL'
            )
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='ACTANTIOX_OFICIAL'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),
    html.P(""),
    html.P("Introduzca el nombre del eje de las ordenadas"),
    dcc.Input(id='input-1-state', type='text', value='FGF21_OFICIAL', size='50'),
    html.P("Introduzca el nombre del eje de las abscisas"),
    dcc.Input(id='input-2-state', type='text', value='ACTANTIOX_OFICIAL', size='50'),
    html.Hr(style={'width': '35%', 'margin': '0', 'margin-top': '15px', 'margin-bottom': '15px'}),
    html.Button(id='btn-1', children='ACTUALIZAR EJES')
])


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('btn-1', 'n_clicks'),
     Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value')],
     [State('input-1-state', 'value'),
     State('input-2-state', 'value')])
def update_graph(n_clicks1, xaxis_column_name, yaxis_column_name, input_1, input_2):
    dff = df.dropna(subset=[xaxis_column_name, yaxis_column_name])
    # Construcción del modelo
    slope, intercept, r_value, p_value, std_err = stats.linregress(dff[xaxis_column_name], dff[yaxis_column_name])
    line = slope * dff[xaxis_column_name] + intercept
    return {
        'data': [dict(
            x=dff[xaxis_column_name],
            y=dff[yaxis_column_name],
            mode='markers',
            marker={
                'size': 7,
                'opacity': 0.6,
                'color': 'black'
            },
            hoverinfo='x+y'
        ),dict(
            x=dff[xaxis_column_name],
            y=line,mode='lines',
            marker={
                'size': 9,
                'opacity': 0.8,
                'color': 'grey'},
            hoverinfo="x+y+text")],
        'layout': dict(
            xaxis={
                'title': input_2
            },
            yaxis={
                'title': input_1
            },
            margin={'l': 60, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest',
            annotations=[dict(
                x=dff[xaxis_column_name].max()-(dff[xaxis_column_name].max()*0.1),
                y=dff[yaxis_column_name].max()-(dff[yaxis_column_name].max()*0.1),
                text='<b>R^2 = '+str(round(r_value**2,4))+', p-value = '+str(round(p_value,4))+'<b>',
                showarrow=False,
                font_size=10,
                font_color="grey"
            ),dict(
                x=dff[xaxis_column_name].max()-(dff[xaxis_column_name].max()*0.12),
                y=dff[yaxis_column_name].max()-(dff[yaxis_column_name].max()*0.15),
                text='<b>Y = ' + str(round(intercept, 4)) + ' + ' + str(round(slope, 4)) + 'X<b>',
                showarrow=False,
                font_size=16,
                font_color="grey"
            )],
            showlegend=False
        )
    }



if __name__ == '__main__':
    app.run_server(debug=True)
