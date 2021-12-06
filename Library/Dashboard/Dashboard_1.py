## Libraries
import pandas as pd
import dash
import dash_table as dt
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State

## Importation of our database
df = pd.read_csv(r'Outputs/dataset_serious_games.csv', sep=",")
df = df[["App Name", "Category", "Rating", "Rating Count", "Developer Id", "Reviews", "Learning_category", "Age_range"]]

## Dashboard
app = dash.Dash()
application = app.server

# Dropdown menus (for learning categories and age ranges)
dropdown = html.Div([
    html.Label('Learning categories'),
    dcc.Dropdown(id='dropdown_d1', options=[{'label': i, 'value': i} for i in df["Learning_category"].unique()],
                 value=None),
    html.Label('Age range'),
    dcc.Dropdown(id='dropdown_d2', options=[{'label': i, 'value': i} for i in df["Age_range"].unique()], value=None)
])

# Dash tables
columns_i = [
    dict(id='learning_category', name='Learning category'),
    dict(id='counts', name='Number of App', type='numeric'),
]
data_i = [
    dict(learning_category='counting', counts=20, ),
    dict(learning_category='science', counts=14),
    dict(learning_category='food', counts=7),
    dict(learning_category='sport', counts=5),
    dict(learning_category='shape', counts=3),
    dict(learning_category='music', counts=2),
    dict(learning_category='language', counts=3),
]
final_table = html.Div(id="final_table")

app.layout = html.Div([dropdown, final_table])


# Callback to update second dropdown based on first dropdown
@app.callback(Output('dropdown_d2', 'options'),
              [Input('dropdown_d1', 'value'), ])
def update_dropdown_2(d1):
    print(d1)
    if (d1 != None):
        df_filtered = df[(df["Learning_category"] == d1)]
        return [{'label': i, 'value': i} for i in df_filtered["Age_range"].unique()]
    else:
        return []


# Callback to update the final table based on both the input dropdown values
@app.callback(Output('final_table', 'children'),
              [Input('dropdown_d1', 'value'),
               Input('dropdown_d2', 'value'), ])
def update_table(d1, d2):
    if (d1 != None and d2 != None):
        df_filtered = df[(df["Learning_category"] == d1) & (df["Age_range"] == d2)]
        return [dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
        )]
    elif (d1 != None and d2 == None):
        df_filtered = df[(df["Learning_category"] == d1)]
        return [dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
        )]
    else:
        print("none")
        return [dt.DataTable(
            columns=columns_i,
            data=data_i
        )]


if __name__ == "__main__":
    app.run_server(debug=True)
