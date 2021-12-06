import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import dash
import dash_table as dt
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State

## Importation of our database
df = pd.read_csv(r'Outputs/dataset_seriousgames.csv', sep =",")
df = df[["App Name","Category","Rating","Rating Count","Developer Id","Reviews","Learning_category","Age_range"]]

app = dash.Dash(__name__, suppress_callback_exceptions=True)
application = app.server

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# TAB n°1: Dropdown menus (for learning categories and age ranges)
dropdown = html.Div([
    html.Label('Learning categories'),
    dcc.Dropdown(id='dropdown_d1', options=[{'label': i, 'value': i} for i in df["Learning_category"].unique()], value=None),
    html.Label('Age range'),
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

# Tabs
tabs = html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Field overview', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Details per app', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Details per paper', value='tab-3', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

# Dash table
final_table = html.Div(id="final_table")
final_table_2 = html.Div(id="final_table_2")

app.layout = html.Div([tabs])

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([dropdown, final_table])
    elif tab == 'tab-2':
        return html.Div([dropdown2, final_table_2])
        # return html.Div([
        #     html.H3('Tab content 2')
        # ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
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
        df_filtered = df[(df["Learning_category"]==d1) & (df["Age_range"]==d2)]
        return [dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
        )]
    else:
        print("none")
        return []

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
        return [dt.DataTable(
            id='table2',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
        )]
    else:
        print("none")
        return []


if __name__ == '__main__':
    app.run_server(debug=True)