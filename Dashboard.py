import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash import html
import pandas as pd

df_sg = pd.read_csv(r'Outputs/dataset_seriousgames.csv', sep =",")

app = dash.Dash(__name__)

layout1 = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Science', 'value': 'science'},
            {'label': 'Counting', 'value': 'counting'},
            {'label': 'Language', 'value': 'language'},
            {'label': 'Creativity', 'value': 'creativity'},
            {'label': 'Shape', 'value': 'shape'},
            {'label': 'Food', 'value': 'food'},
            {'label': 'Music', 'value': 'music'},
            {'label': 'Sport', 'value': 'sport'}
        ],
        # Default value
        value='None'
    ),
    html.Div(id='dd-output-container')
])

layout2 = html.Div([
    dcc.Dropdown(
        id='demo-dropdown2',
        options=[
            {'label': 'Babies', 'value': 'babies'},
            {'label': 'Children', 'value': 'children'},
            {'label': 'Adolescents', 'value': 'adolescents'},
            {'label': 'Adults', 'value': 'adults'}
        ],
        # Default value
        value='None'
    ),
    html.Div(id='dd-output-container2')
])

app.layout = html.Div([
    layout1,
    layout2
])

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)

# The function that displays the number and list of apps for each category and subcategory
def update_output(value, df_sg):
    df = df_sg[((df_sg["Learning_category"] == value))]
    return df["App Name"]



@app.callback(
    Output('dd-output-container2', 'children'),
    Input('demo-dropdown2', 'value')
)

# The function that displays the number and list of apps for each category and subcategory
def update_output(value, df_sg):
    df = df_sg[((df_sg["Learning_category"] == value))]
    return df["App Name"]

if __name__ == '__main__':
    app.run_server(debug=True)