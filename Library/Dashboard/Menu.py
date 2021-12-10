## Libraries
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import dash
import dash_table as dt
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State

## Importation of our databases
from Library.Recognizer import ROOT_DIR

df = pd.read_csv(r"" + ROOT_DIR + '/Outputs/dataset_serious_games.csv', sep =",")
df = df[["App Name","App Id","Category","Rating","Rating Count","Installs","Price","Developer Id","Last Updated",
         "Description","Reviews","Learning_category","Age_range"]]
df_general = df[["App Name","Category","Rating","Rating Count","Price","Developer Id","Learning_category","Age_range"]]
df2 = pd.read_csv(r"" + ROOT_DIR + '/Outputs/dataset_papers2.csv', sep =",")
validated_app = [i for i in df2["App Name"].unique()]

app = dash.Dash(__name__, suppress_callback_exceptions=True)
application = app.server

tabs_styles = {
    'height': '5em'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'color': 'rgb(0, 179, 134)',
    'fontWeight': 'bold',
    'fontSize': '1.5em',
    'vertical-align': 'center'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'rgb(0, 179, 134)',
    'color': 'white',
    'padding': '6px',
    'fontSize': '1.5em',
    'vertical-align': 'center',
    'fontWeight': 'bold'
}

# TAB n°1: Dropdown menus (for learning categories and age ranges)
dropdown = html.Div([
    html.Br(),
    html.Label('Learning categories', style={'fontSize': '1.5em'}),
    dcc.Dropdown(id='dropdown_d1', options=[{'label': i, 'value': i} for i in df["Learning_category"].unique()], value=None),
    html.Br(),
    html.Label('Age range', style={'fontSize': '1.5em'}),
    dcc.Dropdown(id='dropdown_d2', options=[{'label': i, 'value': i} for i in df["Age_range"].unique()], value=None)
])

# TAB n°2: Dropdown menus (for learning categories, age ranges and app names)
dropdown2 = html.Div([
    html.Label('Learning categories'),
    dcc.Dropdown(id='dropdown_d1_2', options=[{'label': i, 'value': i} for i in df["Learning_category"].unique()], value=None),
    html.Label('Age range'),
    dcc.Dropdown(id='dropdown_d2_2', options=[{'label': i, 'value': i} for i in df["Age_range"].unique()], value=None),
    html.Label('App names'),
    dcc.Dropdown(id='dropdown_d3_2', options=[{'label': i, 'value': i} for i in df["App Name"].unique()], value=None)
])

# TAB n°3: Dropdown menus (for app names and titles of papers)
dropdown3 = html.Div([
    html.Label('App names'),
    dcc.Dropdown(id='dropdown_d1_3', options=[{'label': i, 'value': i} for i in df2["App Name"].unique()], value=None),
    html.Label('Associated paper(s)'),
    dcc.Dropdown(id='dropdown_d2_3', options=[{'label': i, 'value': i} for i in df2["title"].unique()], value=None)
])

# Tabs
tabs = html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Field overview', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Details per app', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Papers per validated app', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Similar apps per non-validated app', value='tab-4', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

# Dash tables
final_table = html.Div(id="final_table")
final_table_2 = html.Div(id="final_table_2")
final_table_3 = html.Div(id="final_table_3")

# Layouts
layout1 = html.Div([html.H1("Overview per learning category"),
                    dcc.Graph(id="graph1",
                              figure={'data': [{'app_documented': ['counting','science','food','sport','shape','music','language'],
                                                'y': [20,14,7,5,3,2,3],
                                                'type': 'bar',
                                                'name': 'Ships'}],
                                                'layout': {'title': 'Number of applications per learning category'}})])
layout2 = html.Div([html.H1("Overview per age range"),
                    dcc.Graph(id="graph2",
                              figure={'data': [{'app_documented': ['babies', 'children', 'adults'],
                                                'y': [16, 59, 2],
                                                'type': 'bar',
                                                'name': 'Ships'}],
                                                'layout': {'title': 'Number of applications per age range'}})])
layout3 = html.Div([html.H1("Overview of the number of papers per validated application"),
                    dcc.Graph(id="graph3",
                              figure={'data': [{'values': [2,2,2,1,2,2,2,2,2,2,2],
                                      'labels': ['Baby Panda World','Little Panda Policeman', 'MentalUP - Learning Games & Brain Games',
                                                 'Halloween Makeup Me','Coloring & Learn','Tailor Kids','Animal Jam',
                                                 'Kids Educational Game 5','Bubbu School - My Cute Pets | Animal School Game',
                                                 'Animals Farm For Kids','Baby Panda World'],
                                      'type': 'pie',
                                      'name': 'Ships'}]})])

app.layout = html.Div([
                html.H1(children="Google PlayStore Serious Games",
                        style= {'color': 'rgb(0, 179, 134)', 'backgroundColor': 'white',
                                'font-size':'5em','text-align':'center'}),
                tabs])

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([dropdown, final_table])
    elif tab == 'tab-2':
        return html.Div([dropdown2, final_table_2])
    elif tab == 'tab-3':
        return html.Div([dropdown3, final_table_3])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])

# TAB n°1: Callback to update second dropdown based on first dropdown
@app.callback(Output('dropdown_d2', 'options'),
             [Input('dropdown_d1', 'value'),])

def update_dropdown_2(d1):
    print(d1)
    if(d1 != None):
        df_filtered = df[(df["Learning_category"]==d1)]
        return [{'label': i, 'value': i} for i in df_filtered["Age_range"].unique()]
    else:
        return []

# TAB n°1: Callback to update the final table based on both the input dropdown values
@app.callback(Output('final_table', 'children'),
              [Input('dropdown_d1', 'value'),
              Input('dropdown_d2', 'value'),])

def update_table(d1, d2):
    if(d1 != None and d2 != None):
        df_filtered = df_general[(df_general["Learning_category"]==d1) & (df_general["Age_range"]==d2)]
        return [html.Div([html.H2('General information about the apps in the selected field:')],
                     style={'textAlign': 'left'}),
                dbc.Button(["Number of apps found: ",
                            dbc.Badge(len(df_filtered), color="white", text_color="blue", className="ms-1"), ],
            style={'color': 'white', 'backgroundColor': 'rgb(0, 179, 134)'},
                           color="white"),
            dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_data={'color': 'black',
                        'backgroundColor': 'white'},
            style_cell={'textAlign': 'left'}
        )]
    elif (d1 != None and d2 == None):
        df_filtered = df_general[(df_general["Learning_category"] == d1)]
        return [html.Div([html.H2('General information about the apps in the selected field:')],
                     style={'textAlign': 'left'}),
                dbc.Button(["Number of apps found: ",
                            dbc.Badge(len(df_filtered), color="white", text_color="blue", className="ms-1"),],
                           style={'color': 'white', 'backgroundColor': 'rgb(0, 179, 134)'},
                            color="white"),
                dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'})
        ]
    else:
        return [html.Div([dbc.Col([
                          dbc.Row([dbc.Col(layout1, width=True),
                                   dbc.Col(layout2, width=True)])])])]


# TAB n°2: Callback to update second dropdown based on first dropdown
@app.callback(Output('dropdown_d2_2', 'options'),
             [Input('dropdown_d1_2', 'value'),])

def update_dropdown_2_2(d1):
    print(d1)
    if(d1 != None):
        df_filtered = df[(df["Learning_category"]==d1)]
        return [{'label': i, 'value': i} for i in df_filtered["Age_range"].unique()]
    else:
        return []

# TAB n°2: Callback to update third dropdown based on second dropdown
@app.callback(Output('dropdown_d3_2', 'options'),
             [Input('dropdown_d1_2', 'value'),
              Input('dropdown_d2_2', 'value'),])

def update_dropdown_3_2(d1,d2):
    print(d1)
    print(d2)
    if(d1 != None and d2 != None):
        df_filtered = df[(df["Learning_category"]==d1) & (df["Age_range"]==d2)]
        return [{'label': i, 'value': i} for i in df_filtered["App Name"].unique()]
    else:
        return []

# TAB n°2: Callback to update the final table based on both the input dropdown values
@app.callback(Output('final_table_2', 'children'),
             [Input('dropdown_d1_2', 'value'),
              Input('dropdown_d2_2', 'value'),
              Input('dropdown_d3_2', 'value'),])

def update_table_2(d1, d2, d3):
    if(d1 != None and d2 != None and d3 != None):
        df_filtered = df[(df["Learning_category"]==d1) & (df["Age_range"]==d2) & (df["App Name"]==d3)]
        if d3 in validated_app:
            df2_filtered = df2[(df2["App Name"] == d3)]
            df2_filtered = df2_filtered[["title"]]
            return [html.Div([html.H2('More specific information about the selected app:')],
                              style={'textAlign': 'left'}),
                    dt.DataTable(id='table',
                                columns=[{"name": i, "id": i} for i in df_filtered.columns],
                                data=df_filtered.to_dict('records'),),
                    dbc.Button(["Number of associated paper(s): ",
                                dbc.Badge(len(df2_filtered), color="white", text_color="blue", className="ms-1"), ],
                               style={'color': 'white', 'backgroundColor': 'rgb(0, 179, 134)'},
                               color="white"),
                    html.Div([html.H3('These papers are the followings:')]),
                    dt.DataTable(id='table2',
                                 columns=[{"name": i, "id": i} for i in df2_filtered.columns],
                                 data=df2_filtered.to_dict('records'),
                                 style_header={'color': 'white',
                                               'backgroundColor': 'rgb(45, 89, 134)',
                                               'fontWeight': 'bold'},
                                 style_cell={'textAlign': 'left'}),
                    html.Div([html.H3('For more detailed information on these papers, search them in tab n°3.')])
                    ]
        else:
            return [html.Div([html.H2('More specific information about the selected app:')],
                              style={'textAlign': 'left'}),
                    dt.DataTable(id='table2',
                                columns=[{"name": i, "id": i} for i in df_filtered.columns],
                                data=df_filtered.to_dict('records'),
                                style_header={'color': 'white',
                                              'backgroundColor': 'rgb(45, 89, 134)',
                                              'fontWeight': 'bold'},
                                style_cell={'textAlign': 'left'}),
                    html.Div([html.H3('This app is associated with 0 paper.')]),
                    html.Div([html.H3('For more detailed information on the similar and potentially validated apps, search this app in tab n°4.')]),
                    ]
    elif (d1 != None and d2 != None and d3 == None):
        df_filtered = df[(df["Learning_category"] == d1) & (df["Age_range"] == d2)]
        return [html.Div([html.H2('More specific information about the apps in the selected field:')],
                          style={'textAlign': 'left'}),
                dbc.Button(["Number of apps found: ",
                            dbc.Badge(len(df_filtered), color="white", text_color="blue", className="ms-1"), ],
                           style={'color': 'white', 'backgroundColor': 'rgb(0, 179, 134)'},
                           color="white"),
            dt.DataTable(
            id='table2',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        )]
    elif (d1 != None and d2 == None and d3 == None):
        df_filtered = df[(df["Learning_category"] == d1)]
        return [html.Div([html.H2('More specific information about the apps in the selected field:')],
                          style={'textAlign': 'left'}),
                dbc.Button(["Number of apps found: ",
                            dbc.Badge(len(df_filtered), color="white", text_color="blue", className="ms-1"), ],
                           style={'color': 'white', 'backgroundColor': 'rgb(0, 179, 134)'},
                           color="white"),
            dt.DataTable(
            id='table2',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        )]
    else:
        return []


# TAB n°3: Callback to update second dropdown based on first dropdown
@app.callback(Output('dropdown_d2_3', 'options'),
              [Input('dropdown_d1_3', 'value'), ])
def update_dropdown_2_3(d1):
    print(d1)
    if (d1 != None):
        df2_filtered = df2[(df2["App Name"] == d1)]
        return [{'label': i, 'value': i} for i in df2_filtered["title"].unique()]
    else:
        return []


# TAB n°3: Callback to update the final table based on both the input dropdown values
@app.callback(Output('final_table_3', 'children'),
              [Input('dropdown_d1_3', 'value'),
               Input('dropdown_d2_3', 'value'), ])
def update_table_3(d1, d2):
    if (d1 != None and d2 != None):
        df2_filtered = df2[(df2["App Name"] == d1) & (df2["title"] == d2)]
        print(df2_filtered["abstract"])
        return [html.Div([html.H2('More specific information about the selected paper:')],
                          style={'textAlign': 'left'}),
            dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df2_filtered.columns],
            data=df2_filtered.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        )]
    elif (d1 != None and d2 == None):
        df2_filtered = df2[(df2["App Name"] == d1)]
        return [html.Div([html.H2('More specific information about the paper(s) of the selected app:')],
                          style={'textAlign': 'left'}),
                dbc.Button(["Number of papers found: ",
                            dbc.Badge(len(df2_filtered), color="white", text_color="blue", className="ms-1"), ],
                           style={'color': 'white', 'backgroundColor': 'rgb(0, 179, 134)'}),
            dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df2_filtered.columns],
            data=df2_filtered.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        )]
    else:
        return [html.Div([dbc.Col([dbc.Row([dbc.Col(layout3, width=True)])])])]

if __name__ == '__main__':
    app.run_server(debug=True)