## Libraries
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import dash
import dash_table as dt
# from dash import dash_table as dt
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State

## Importation of our databases
from Library.Recognizer import ROOT_DIR

# Datasets
df = pd.read_csv(r"" + ROOT_DIR + '/Outputs/dataset_serious_games.csv', sep =",")
df = df[["App Name","App Id","Category","Rating","Rating Count","Installs","Price","Developer Id","Last Updated",
         "Description","Reviews","Learning_category","Age_range"]]
df_general = df[["App Name","Category","Rating","Rating Count","Price","Developer Id","Learning_category","Age_range"]]
# df2 = pd.read_csv(r"" + ROOT_DIR + '/Outputs/dataset_papers2.csv', sep =",")
df2 = pd.read_csv(r"" + ROOT_DIR + '/Outputs/app_name_papers_final.csv', sep =",")
df3 = pd.read_csv(r"" + ROOT_DIR + '/Outputs/similar_apps.csv', sep =",")

# # List of the names of all apps
# all_apps = [i for i in df["App Name"].unique()]

# # List of the levels of validation of all apps
# lv_val = []
# for j in all_apps:
#     dff = df2[(df2["app_name"]==j)]
#     lv_val.append(dff['validation_level'].iloc[0])
#
# # New df with 1 more column: Validation_level
# df["Validation_level"] = lv_val

# List of the names of validated apps
validated_app = []
for i in range(len(df2)):
    if df2.iloc[i]["validation_level"] >= 3:
        validated_app.append(df2.iloc[i]["app_name"])

# List of the number of papers per validated app
nb_papers_per_app = []
for i in validated_app:
    nb_papers_per_app.append(len(df2[(df2["app_name"]==i)]))

## Dashboard
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
    html.Label('App names', style={'fontSize': '1.5em'}),
    dcc.Dropdown(id='dropdown_d1_2', options=[{'label': i, 'value': i} for i in df2["app_name"].unique()], value=None)
])

# TAB n°3: Dropdown menus (for app names and titles of papers)
dropdown3 = html.Div([
    html.Label('App names', style={'fontSize': '1.5em'}),
    dcc.Dropdown(id='dropdown_d1_3', options=[{'label': i, 'value': i} for i in df2["app_name"].unique()], value=None),
    html.Label('Associated paper(s)', style={'fontSize': '1.5em'}),
    dcc.Dropdown(id='dropdown_d2_3', options=[{'label': i, 'value': i} for i in df2["title"].unique()], value=None)
])

# TAB n°4: Dropdown menus (for app names)
dropdown4 = html.Div([
    html.Label('App names', style={'fontSize': '1.5em'}),
    dcc.Dropdown(id='dropdown_d1_4', options=[{'label': i, 'value': i} for i in df3["app_name"].unique()], value=None),
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
final_table_4 = html.Div(id="final_table_4")

# Layouts
layout1 = html.Div([html.H1("Overview per learning category"),
                    dcc.Graph(id="graph1",
                              figure={'data': [{'x': ['counting','science','food','sport','shape','music','language'],
                                                'y': [len(df[(df["Learning_category"]=="counting")]),len(df[(df["Learning_category"]=="science")]),len(df[(df["Learning_category"]=="food")]),len(df[(df["Learning_category"]=="sport")]),len(df[(df["Learning_category"]=="shape")]),len(df[(df["Learning_category"]=="music")]),len(df[(df["Learning_category"]=="language")])],
                                                'type': 'bar',
                                                'name': 'Ships'}],
                                        'layout': {'title': 'Number of applications per learning category'}})])
layout2 = html.Div([html.H1("Overview per age range"),
                    dcc.Graph(id="graph2",
                              figure={'data': [{'x': ['babies', 'children', 'adolescents','adults'],
                                                'y': [len(df[(df["Age_range"]=="babies")]), len(df[(df["Age_range"]=="children")]), len(df[(df["Age_range"]=="adolescents")]), len(df[(df["Age_range"]=="adults")])],
                                                'type': 'bar',
                                                'name': 'Ships'}],
                                        'layout': {'title': 'Number of applications per age range'}})])
layout3 = html.Div([html.H1("Overview of the number of papers per validated application"),
                    dcc.Graph(id="graph3",
                              figure={'data': [{'values': nb_papers_per_app,
                                      'labels': validated_app,
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
        return html.Div([dropdown4, final_table_4])


# TAB n°1: Callback to update second dropdown based on first dropdown
@app.callback(Output('dropdown_d2', 'options'),
             [Input('dropdown_d1', 'value'),])

def update_dropdown_2(d1):
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
            # style_data={'color': 'black',
            #             'backgroundColor': 'white',
            #             'whiteSpace': 'normal',
            #             'height': 'auto',
            #             },
            style_cell={'textAlign': 'left',
                            'maxWidth': '0',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            },
            tooltip_data=[
                    {
                        column: {'value': str(value), 'type': 'markdown'}
                        for column, value in row.items()
                    } for row in df_filtered.to_dict('records')
                ],
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
            # style_data={
            #             'whiteSpace': 'normal',
            #             'height': 'auto',
            #         },
            data=df_filtered.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_cell={'textAlign': 'left',
                                'maxWidth': '0',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                },
            tooltip_data=[
                        {
                            column: {'value': str(value), 'type': 'markdown'}
                            for column, value in row.items()
                        } for row in df_filtered.to_dict('records')]

                )]
    else:
        return [html.Div([dbc.Col([
                          dbc.Row([dbc.Col(layout1, width=True),
                                   dbc.Col(layout2, width=True)])])])]


# TAB n°2: Callback to update second dropdown based on first dropdown
# @app.callback(Output('dropdown_d2_2', 'options'),
#              [Input('dropdown_d1_2', 'value'),])
#
# def update_dropdown_2_2(d1):
#     print(d1)
#     if(d1 != None):
#         df_filtered = df[(df["Learning_category"]==d1)]
#         return [{'label': i, 'value': i} for i in df_filtered["Age_range"].unique()]
#     else:
#         return []

# TAB n°2: Callback to update third dropdown based on second dropdown
# @app.callback(Output('dropdown_d3_2', 'options'),
#              [Input('dropdown_d1_2', 'value'),
#               Input('dropdown_d2_2', 'value'),])
#
# def update_dropdown_3_2(d1,d2):
#     print(d1)
#     print(d2)
#     if(d1 != None and d2 != None):
#         df_filtered = df[(df["Learning_category"]==d1) & (df["Age_range"]==d2)]
#         return [{'label': i, 'value': i} for i in df_filtered["App Name"].unique()]
#     else:
#         return []

# TAB n°2: Callback to update the final table based on both the input dropdown value
@app.callback(Output('final_table_2', 'children'),
             [Input('dropdown_d1_2', 'value')])

def update_table_2(d1):
    if d1 != None:
        df2_filtered = df2[(df2["app_name"]==d1)]
        if d1 in validated_app:
            df2_filtered2 = df2_filtered["validation_level"]
            return [html.Div([html.H2('More specific information about the selected app:')],
                              style={'textAlign': 'left'}),
                    dt.DataTable(id='table2',
                                columns=[{"name": i, "id": i} for i in df2_filtered.columns],
                                # style_data={
                                #      'whiteSpace': 'normal',
                                #      'height': 'auto',
                                #  },
                                data=df2_filtered.to_dict('records'),
                                style_header={'color': 'white',
                                               'backgroundColor': 'rgb(45, 89, 134)',
                                               'fontWeight': 'bold'},
                                 style_cell={'textAlign': 'left',
                                             'maxWidth': '0',
                                             'overflow': 'hidden',
                                             'textOverflow': 'ellipsis',
                                             },
                                 tooltip_data=[
                                     {
                                         column: {'value': str(value), 'type': 'markdown'}
                                         for column, value in row.items()
                                     } for row in df2_filtered.to_dict('records')
                                 ],
                                ),
                    html.Br(),
                    html.Ul([
                    html.Li([
                        dbc.Button(["Level of validation: ",
                                    dbc.Badge(df2_filtered2.iloc[0], color="white", text_color="blue", className="ms-1"), ],
                                   style={'color': 'white', 'backgroundColor': 'green'},
                                   color="white")]),
                    html.Li([
                        dbc.Button(["Number of associated paper(s): ",
                                    dbc.Badge(len(df2_filtered), color="white", text_color="blue", className="ms-1"), ],
                                   style={'color': 'white', 'backgroundColor': 'rgb(0, 179, 134)'},
                                   color="white")])]),
                    html.Div([html.H3('For more detailed information on these papers, search them in tab n°3.')]),
                    ]
        else:
            return [html.Div([html.H2('More specific information about the selected app:')],
                              style={'textAlign': 'left'}),
                    dt.DataTable(id='table2',
                                columns=[{"name": i, "id": i} for i in df2_filtered.columns],
                                # style_data={
                                #      'whiteSpace': 'normal',
                                #      'height': 'auto',
                                #  },
                                data=df2_filtered.to_dict('records'),
                                style_header={'color': 'white',
                                              'backgroundColor': 'rgb(45, 89, 134)',
                                              'fontWeight': 'bold'},
                                 style_cell={'textAlign': 'left',
                                             'maxWidth': '0',
                                             'overflow': 'hidden',
                                             'textOverflow': 'ellipsis',
                                             },
                                 tooltip_data=[
                                     {
                                         column: {'value': str(value), 'type': 'markdown'}
                                         for column, value in row.items()
                                     } for row in df2_filtered.to_dict('records')]
                                 ),
                    html.Br(),
                    html.Ul([
                        html.Li([
                            dbc.Button(["Level of validation: ",
                                        dbc.Badge(0, color="white", text_color="blue",
                                                  className="ms-1"), ],
                                       style={'color': 'white', 'backgroundColor': 'red'},
                                       color="white")]),
                        html.Li([
                            dbc.Button(["Number of associated paper(s): ",
                                        dbc.Badge(len(df2_filtered), color="white", text_color="blue",
                                                  className="ms-1"), ],
                                       style={'color': 'white', 'backgroundColor': 'rgb(0, 179, 134)'},
                                       color="white")])]),
                    html.Div([html.H3('For more detailed information on the potential papers, search them in tab n°3. Otherwise, check similar validated apps in tab n°4.')]),
                    ]
    else:
        return [html.Div([html.H2('General details:')],
                          style={'textAlign': 'left'}),
                dbc.Button(["Number of apps found: ",
                            dbc.Badge(len(df), color="white", text_color="blue", className="ms-1"), ],
                           style={'color': 'white', 'backgroundColor': 'rgb(0, 179, 134)'},
                           color="white"),
            dt.DataTable(
            id='table2',
            columns=[{"name": i, "id": i} for i in df.columns],
            # style_data={
            #         'whiteSpace': 'normal',
            #         'height': 'auto',
            #     },
            data=df.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_cell={'textAlign': 'left',
                        'maxWidth': '0',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        },
            tooltip_data=[
                    {
                        column: {'value': str(value), 'type': 'markdown'}
                        for column, value in row.items()
                    } for row in df.to_dict('records')
                ],
                tooltip_duration=None
        )]


# TAB n°3: Callback to update second dropdown based on first dropdown
@app.callback(Output('dropdown_d2_3', 'options'),
              [Input('dropdown_d1_3', 'value'), ])
def update_dropdown_2_3(d1):
    if (d1 != None):
        df2_filtered = df2[(df2["app_name"] == d1)]
        return [{'label': i, 'value': i} for i in df2_filtered["title"].unique()]
    else:
        return []


# TAB n°3: Callback to update the final table based on both the input dropdown values
@app.callback(Output('final_table_3', 'children'),
              [Input('dropdown_d1_3', 'value'),
               Input('dropdown_d2_3', 'value'), ])
def update_table_3(d1, d2):
    if (d1 != None and d2 != None):
        df2_filtered = df2[(df2["app_name"] == d1) & (df2["title"] == d2)]
        return [html.Div([html.H2('More specific information about the selected paper:')],
                          style={'textAlign': 'left'}),
            dt.DataTable(
            id='table3',
            columns=[{"name": i, "id": i} for i in df2_filtered.columns],
            style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
            data=df2_filtered.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        )]
    elif (d1 != None and d2 == None):
        df2_filtered = df2[(df2["app_name"] == d1)]
        return [html.Div([html.H2('More specific information about the paper(s) of the selected app:')],
                          style={'textAlign': 'left'}),
                dbc.Button(["Number of papers found: ",
                            dbc.Badge(len(df2_filtered), color="white", text_color="blue", className="ms-1"), ],
                           style={'color': 'white', 'backgroundColor': 'rgb(0, 179, 134)'}),
            dt.DataTable(
            id='table3',
            columns=[{"name": i, "id": i} for i in df2_filtered.columns],
            style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
            data=df2_filtered.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        )]
    else:
        return [html.Div([dbc.Col([dbc.Row([dbc.Col(layout3, width=True)])])])]

# TAB n°4: Callback to update the final table based on both the input dropdown values
@app.callback(Output('final_table_4', 'children'),
              [Input('dropdown_d1_4', 'value'),])
def update_table_4(d1):
    if d1 != None:
        df3_filtered = df3[(df3["app_name"] == d1)]
        return [html.Div([html.H2('Related similar apps:')],
                          style={'textAlign': 'left'}),
            dt.DataTable(
            id='table4',
            columns=[{"name": i, "id": i} for i in df3_filtered.columns],
            style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
            data=df3_filtered.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        )]
    else:
        return [html.Div([html.H2('Similar applications per non-validated app:')],
                          style={'textAlign': 'left'}),
            dt.DataTable(
            id='table4',
            columns=[{"name": i, "id": i} for i in df3.columns],
            style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
            data=df3.to_dict('records'),
            style_header={'color': 'white',
                          'backgroundColor': 'rgb(45, 89, 134)',
                          'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        )]

if __name__ == '__main__':
    app.run_server(debug=True)