## Libraries
import pandas as pd
import dash
import dash_table as dt
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State

## Importation of our database
df = pd.read_csv(r'../../Outputs/dataset_serious_games.csv', sep =",")
df = df[["App Name","Category","Rating","Rating Count","Developer Id","Reviews","Description","Learning_category","Age_range"]]
df2 = pd.read_csv(r'C:/Users/Gilles FACCIN/PycharmProjects/e-HealthProject/Outputs/dataset_papers2.csv', sep =",")
validated_app = [i for i in df2["App Name"].unique()]

## Dashboard
app = dash.Dash()
application = app.server

# Dropdown menus (for learning categories, age ranges and app names)
dropdown = html.Div([
    html.Label('Learning categories'),
    dcc.Dropdown(id='dropdown_d1', options=[{'label': i, 'value': i} for i in df["Learning_category"].unique()], value=None),
    html.Label('Age range'),
    dcc.Dropdown(id='dropdown_d2', options=[{'label': i, 'value': i} for i in df["Age_range"].unique()], value=None),
    html.Label('App names'),
    dcc.Dropdown(id='dropdown_d3', options=[{'label': i, 'value': i} for i in df["App Name"].unique()], value=None)
])

# Dash table
final_table = html.Div(id="final_table")

app.layout = html.Div([dropdown, final_table])

# Callback to update second dropdown based on first dropdown
@app.callback(Output('dropdown_d2', 'options'),
             [Input('dropdown_d1', 'value'),])

def update_dropdown_2(d1):
    print(d1)
    if(d1 != None):
        df_filtered = df[(df["Learning_category"]==d1)]
        return [{'label': i, 'value': i} for i in df_filtered["Age_range"].unique()]
    else:
        return []

# Callback to update third dropdown based on second dropdown
@app.callback(Output('dropdown_d3', 'options'),
             [Input('dropdown_d1', 'value'),
              Input('dropdown_d2', 'value'),])

def update_dropdown_3(d1,d2):
    print(d1)
    print(d2)
    if(d1 != None and d2 != None):
        df_filtered = df[(df["Learning_category"]==d1) & (df["Age_range"]==d2)]
        return [{'label': i, 'value': i} for i in df_filtered["App Name"].unique()]
    else:
        return []

# Callback to update the final table based on both the input dropdown values
@app.callback(Output('final_table', 'children'),
             [Input('dropdown_d1', 'value'),
              Input('dropdown_d2', 'value'),
              Input('dropdown_d3', 'value'),])

def update_table(d1, d2, d3):
    if(d1 != None and d2 != None and d3 != None):
        df_filtered = df[(df["Learning_category"]==d1) & (df["Age_range"]==d2) & (df["App Name"]==d3)]
        if d3 in validated_app:
            df2_filtered = df2[(df2["App Name"] == d3)]
            return [html.Div([html.H3('Associated papers:')],
                     style={'textAlign': 'center'}),
                html.Div([len(df2_filtered)],
                     style={'textAlign': 'center'}),
                dt.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_filtered.columns],
                data=df_filtered.to_dict('records'),
            )]
        else:
            return [dt.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_filtered.columns],
                data=df_filtered.to_dict('records'),
            )]
    else:
        print("none")
        return []

if __name__ == "__main__":
    app.run_server(debug=True)