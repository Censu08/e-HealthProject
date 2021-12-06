## Libraries
import pandas as pd
import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
from dash_table import DataTable, FormatTemplate
## Importation of our database
df = pd.read_csv(r'C:\Users\sribhuvaneshsudan\PycharmProjects\e-HealthProjec\Outputs\dataset_seriousgames.csv', sep =",")
df = df[["App Name","Category","Rating","Rating Count","Developer Id","Reviews","Description","Learning_category","Age_range"]]


## Dashboard
app = dash.Dash()
application = app.server
columns = [
    dict(id='learing_category', name='Learing category'),
    dict(id='counts', name='Number of App', type='numeric'),
]
data = [
    dict(learing_category='counting', counts=20),
    dict(learing_category='science', counts=14),
    dict(learing_category='food', counts=7),
    dict(learing_category='sport', counts=5),
     dict(learing_category='shape', counts=3),
     dict(learing_category='music', counts=2),
    dict(learing_category='language', counts=3),
]
# Dropdown menus (for learning categories, age ranges and app names)
dropdown = html.Div([
    html.H1(children="Google Play Store Serious games",style= {'font-size':'1.5em','text-align':'center'}),
#'width':'10%'
#text-align: center
#'font-style': 'italic'
#'color':'blue'
#'font-size':'small'

    html.Label('Learning_Categories',style= {'font-style': 'italic','color':'blue'}),
    dcc.Dropdown(id='dropdown_d1', options=[{'label': i, 'value': i,} for i in df["Learning_category"].unique()], value=None,),
    html.Label('Age range',style= {'font-style': 'italic','color':'blue'}),
    dcc.Dropdown(id='dropdown_d2', options=[{'label': i, 'value': i} for i in df["Age_range"].unique()], value=None),
    html.Label('App names',style= {'font-style': 'italic','color':'blue'}),
    dcc.Dropdown(id='dropdown_d3', options=[{'label': i, 'value': i} for i in df["App Name"].unique()], value=None),
])

# Dash table
final_table = html.Div(id="final_table")

app.layout = html.Div([dropdown, final_table])
app.layout1 = DataTable(columns=columns, data=data)
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
        df_filtered = df[(df["Learning_category"]==d1) & (df["Age_range"]==d2) & (df["App Name"]==d3)],
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

#counting learning category
s= df['Learning_category'].value_counts()