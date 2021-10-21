import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from application import app
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash_table
from dash.dependencies import Input, Output
from datetime import datetime, timedelta, date
import boto3

from dash_table.Format import Format

from util.dash_layout import external_stylesheets, update_fig
import pandas as pd
import psycopg2
# from config.flask_config import DatabaseConfig
import numpy as np
from datetime import datetime,date
import calendar

pd.options.display.float_format = '{:.2f}'.format
global final
from datetime import datetime

home_url = "/hopecenter/view_help/"
df=pd.read_csv('data/state.csv')

view_help = dash.Dash(__name__,
                          server=app,
                          url_base_pathname=home_url,
                          external_stylesheets=external_stylesheets)    
view_help.layout = html.Div(
    [
    
    html.H3(["Please Become Helping Hand - Search Here and Contact to Them", html.Em(
        className="icon ni ni-question ml-1",
        id="tooltip-target",
    )], className="text-center"),
    dbc.Tooltip(
        "Thank you for helping to needed one. This will be your decision to help them so you should contact properly and get clear to situaltion. we just provide to platform to find which other, we own nothing! ",
        target="tooltip-target",
        className="tool-tip-width"
    ),
    html.Div([
        html.Label("Select District  :"),
        dcc.Dropdown(id='demo-dropdown_dis',
                 options=[{
                     'label': str(i).replace("_", " "), 'value': i} for i in df['district'].unique()],
                 value='Type here')
    ],
    style={'width': '50%', 'display': 'inline-block', 'marginTop': 5, 'marginBottom': 15}),   
    html.Div([
        html.Label("Type of Help:"),
        dcc.Dropdown(id='demo-dropdown_tpye',
                  options=[
                         {
                             'label': 'Hospital Beds',
                             'value': 'Hospital Beds'
                         }, {
                             'label': 'Blood Plasma',
                             'value': 'Blood Plasma'
                         },
                         {
                             'label': 'Oxygen Cylinders',
                             'value': 'Oxygen Cylinders'
                         },
                          {
                             'label': 'Remdesivir',
                             'value': 'Remdesivir'
                         },
                          {
                             'label': 'Toclizumab',
                             'value': 'Toclizumab'
                         },

                         ],
                     value='Select')
    ],
    style={'width': '50%', 'display': 'inline-block', 'marginTop': 5, 'marginBottom': 15}),
    html.Button('Search', id='button'),
    html.Div(id='dd-output-container'),
])
@view_help.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [
    dash.dependencies.Input('demo-dropdown_dis', 'value'),
    dash.dependencies.Input('demo-dropdown_tpye', 'value'),
     dash.dependencies.Input('button', 'n_clicks')]
)
def update_output(district,type_help,n_clicks):
    df_user=pd.read_csv("data/user_verify.csv")
    print(df_user)
    del df_user['email']
    df_user.columns=['Date','State','District','Want Needed','Contact No.','Message','Status']
    df_user.drop_duplicates(inplace=True)
    df_user=df_user.iloc[::-1]
    print(df_user)

    if n_clicks != None:
        if district != None and type_help != None :
            df_user=df_user[df_user['District']==district]
            df_user=df_user[df_user['Want Needed']==type_help]
            return html.Div(
               dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_user.columns],
                data=df_user.to_dict('records'),
                    )
            )
        else:
            return html.Div(
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_user.columns],
                data=df_user.to_dict('records'),
                    )

            )
    return html.Div(
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_user.columns],
                data=df_user.to_dict('records'),
                    )

            )
    