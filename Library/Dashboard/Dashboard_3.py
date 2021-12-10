## Libraries
import pandas as pd
import dash
import dash_table as dt
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State

## Importation of our database
df2 = pd.read_csv(r'C:/Users/Gilles FACCIN/PycharmProjects/e-HealthProject/Outputs/dataset_papers2.csv', sep =",")


app = dash.Dash()
application = app.server

# Dropdown menus (for learning categories and age ranges)
dropdown = html.Div([
    html.Label('App names'),
    dcc.Dropdown(id='dropdown_d1', options=[{'label': i, 'value': i} for i in df2["App Name"].unique()],
                 value=None),
    html.Label('Associated paper(s)'),
    dcc.Dropdown(id='dropdown_d2', options=[{'label': i, 'value': i} for i in df2["title"].unique()], value=None)
])

# Dash tables
columns_i = [
    dict(id='app_name', name='App Name'),
    dict(id='counts', name='Number of Papers', type='numeric'),
]
data_i = [
    dict(app_name='Baby Panda World', counts=2, ),
    dict(app_name='Little Panda Policeman', counts=2, ),
    dict(app_name='MentalUP - Learning Games & Brain Games', counts=2, ),
    dict(app_name='Halloween Makeup Me', counts=1, ),
    dict(app_name='Coloring & Learn', counts=2, ),
    dict(app_name='Tailor Kids', counts=2, ),
    dict(app_name='Animal Jam', counts=2, ),
    dict(app_name='Kids Educational Game 5', counts=2, ),
    dict(app_name='Bubbu School - My Cute Pets | Animal School Game', counts=2, ),
    dict(app_name='Animals Farm For Kids', counts=2, ),
    dict(app_name='Baby Panda World', counts=2, )
]
final_table = html.Div(id="final_table")

app.layout = html.Div([dropdown, final_table])


# Callback to update second dropdown based on first dropdown
@app.callback(Output('dropdown_d2', 'options'),
              [Input('dropdown_d1', 'value'), ])
def update_dropdown_2(d1):
    print(d1)
    if (d1 != None):
        df2_filtered = df2[(df2["App Name"] == d1)]
        return [{'label': i, 'value': i} for i in df2_filtered["title"].unique()]
    else:
        return []


# Callback to update the final table based on both the input dropdown values
@app.callback(Output('final_table', 'children'),
              [Input('dropdown_d1', 'value'),
               Input('dropdown_d2', 'value'), ])
def update_table(d1, d2):
    if (d1 != None and d2 != None):
        df2_filtered = df2[(df2["App Name"] == d1) & (df2["title"] == d2)]
        # abs = df2_filtered[1,3]
        return [html.Div([html.H5("Abstract"),
                          html.Br([]),
                          html.P(df2_filtered['abstract'],
                                style={"color": "#ffffff"}),]),
            dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df2_filtered.columns],
            data=df2_filtered.to_dict('records'),
        )]
    elif (d1 != None and d2 == None):
        df2_filtered = df2[(df2["App Name"] == d1)]
        return [dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df2_filtered.columns],
            data=df2_filtered.to_dict('records'),
        )]
    else:
        print("none")
        return [dt.DataTable(
            columns=columns_i,
            data=data_i
        )]


if __name__ == "__main__":
    app.run_server(debug=True)
