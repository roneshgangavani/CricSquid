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
from routes.volunteer_mail import send_mail
from dash_table.Format import Format

from util.dash_layout import external_stylesheets, update_fig
import pandas as pd
import psycopg2
# from config.flask_config import DatabaseConfig
import numpy as np
from datetime import date
from datetime import datetime
from dateutil import relativedelta
import pandas as pd
pd.options.display.float_format = '{:.2f}'.format
home_url = "/covid_requirments/volunteers/"
from csv import writer
import re
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
def check_mail(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True
    else:
        return False
covid_volunteer = dash.Dash(__name__,
                          server=app,
                          url_base_pathname=home_url,
                          external_stylesheets=external_stylesheets)

df=pd.read_csv('data/state.csv')
print(df)
covid_volunteer.layout = html.Div(
    [
    html.H3(["Volunteer Registartion"
             ], className="text-center"),
    html.Div([
        html.Label("Name:"),
    dcc.Input(
            id="fullname",
            type="text",
            placeholder="Full Name",
        )
         ],
    style={'width': '25%', 'display': 'inline-block', 'marginTop': 10, 'marginBottom': 1}),
    html.Div([
        html.Label("Age:"),
    dcc.Input(
            id="age",
            type="number",
            placeholder="Age",
        )
    ],
    style={'width': '25%', 'display': 'inline-block', 'marginTop': 10, 'marginBottom': 1}),
    html.Div([
        html.Label("Contact:"),
    dcc.Input(
            id="contact",
            type="text",
            placeholder="Whatsapp Num.",
        )
         ],
    style={'width': '25%', 'display': 'inline-block', 'marginTop': 100, 'marginBottom': 1}),
      html.Div([
        html.Label("Email:"),
    dcc.Input(
            id="email",
            type="email",
            placeholder="email@email.com",
        )
         ],
    style={'width': '25%', 'display': 'inline-block', 'marginTop': 5, 'marginBottom': 20}),

    html.Div([
        html.Label("Select State :"),
        dcc.Dropdown(
                 id='demo-dropdown',
                 options=[{
                     'label': str(i).replace("_", " "), 'value': i} for i in df['state'].unique()],
                 value='Type here')
    ],
    style={'width': '25%', 'display': 'inline-block', 'marginTop': 5, 'marginBottom': 15}),
    html.Div([
        html.Label("Select District  :"),
        dcc.Dropdown(id='demo-dropdown_dis',
                 options=[{
                     'label': str(i).replace("_", " "), 'value': i} for i in df['district'].unique()],
                 value='Type here')
    ],
    style={'width': '25%', 'display': 'inline-block', 'marginTop': 5, 'marginBottom': 15}),   
    
    html.Div([
        html.Label("Gender:"),
        dcc.Dropdown(id='demo-dropdown_gen',
                 options=[
                         {
                             'label': 'MALE',
                             'value': 'M'
                         }, {
                             'label': 'FEMALE',
                             'value': 'F'
                         },
                         ],
                     value='Select')
    ],
    style={'width': '25%', 'display': 'inline-block', 'marginTop': 5, 'marginBottom': 15}),
      html.Div([
        html.Label("How you can help:"),
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
                         {
                             'label': 'Find out donors to help',
                             'value': 'Find out donors to help'
                         },
                         {
                             'label': 'other ways',
                             'value': 'other ways'
                         },

                         ],
                     value='Select')
    ],
    style={'width': '25%', 'display': 'inline-block', 'marginTop': 5, 'marginBottom': 15}),
    
    html.Div([
        html.Label("Your Message:"),
    dcc.Textarea(
        id='textarea-example',
        value='',
        style={'width': '90%', 'height': 40}
    ),
      ],
    style={'width': '30%', 'display': 'inline-block', 'marginTop': 5, 'marginBottom': 15}),
    html.Button('Registration', id='button'),
    html.Div(id='dd-output-container'),
])
@covid_volunteer.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value'),
    dash.dependencies.Input('demo-dropdown_dis', 'value'),
    dash.dependencies.Input('fullname', 'value'),
    dash.dependencies.Input('age', 'value'),
    dash.dependencies.Input('demo-dropdown_gen', 'value'),
    dash.dependencies.Input('email', 'value'),
    dash.dependencies.Input('demo-dropdown_tpye', 'value'),
     dash.dependencies.Input('contact', 'value'),
     dash.dependencies.Input('textarea-example', 'value'),
     dash.dependencies.Input('button', 'n_clicks')]
)
def update_output_once(state,district,fullname,age,gen,email,type_help,contact,msg,n_clicks):
    file = open('data/volunteers_details.csv','a')
    write = writer(file)
    today=date.today()
    if n_clicks != None:
        if state != None and district != None and fullname != None and age != None and gen != None and type_help != None and contact != None:
            if len(contact) == 10 and contact.isnumeric():
                if check_mail(email):
                    try:
                        send_mail(email)
                    except Exception as ex:
                        print(ex)
                    write.writerow([today,state,district,fullname,age,gen,type_help,contact,email,msg])
                    
                    return html.Div(
                        html.H3(["Registration Done"
                        ], style={'color': 'green','text-align': 'center'}),

                    )
                else:
                    return html.Div(
                        html.H3(["Failed: Please Enter Valid Email ID:"
                        ],style={'color': 'red','text-align': 'center'}),

                    )
            else:
                return html.Div(
                    html.H3(["Failed: Please Enter Valid Contact Number"
                    ], style={'color': 'red','text-align': 'center'}),

                )
        else:
                return html.Div(
                    html.H3(["Failed: Please Enter Valid Proper Details"
                    ], style={'color': 'red','text-align': 'center'}),

                )
    
    
