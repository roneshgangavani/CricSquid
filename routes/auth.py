from flask import render_template, request, redirect, url_for, flash, abort

from models.user import User
from db.db import db
from flask_login import login_user, current_user, logout_user
import bcrypt
from datetime import datetime, timedelta, date
from flask import request
from user_agents import parse
import re

from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize
stop_word = stopwords.words('english')
import string
import heapq

from nltk.cluster.util import cosine_distance
import numpy as np
import csv
from application import app
import pandas as pd
def index():
    worl_cup_schedule=pd.read_csv("data/2021_cup_schedule.csv")
    worl_cup_schedule=worl_cup_schedule.loc[:,['id','match_title','match_subtitle','venue','date']]
    worl_cup_schedule['date']=pd.to_datetime(worl_cup_schedule['date'])
    print(date.today())
    worl_cup_schedule1=worl_cup_schedule[worl_cup_schedule['date']==str(date.today())+"T10:00:00+00:00"]
    list1=worl_cup_schedule1['match_title']
    print(list1)
    for i in list1:
        print("-------i-----------")
        teams=i.split('at')
        print(teams)
        t=teams[0].split('v')
        print(t)
        worl_cup_schedule1['team1']=t[0]
        worl_cup_schedule1['team2']=t[1]
    print(worl_cup_schedule1)
    worl_cup_upcoming=worl_cup_schedule[worl_cup_schedule['date']>str(date.today())+"T10:00:00+00:00"]
    worl_cup_upcoming=worl_cup_upcoming.head(4)
    worl_cup_upcoming=worl_cup_upcoming.loc[:,['match_title','date']]
    worl_cup_upcoming['match_title']=worl_cup_upcoming['match_title'].str.split("at")


    return render_template("index.html", title="Fantastic Playing Players",match_todays=worl_cup_schedule1,worl_cup_upcoming=worl_cup_upcoming)
def match1():
    t1 = request.args.get('t1')  
    team=t1.split('v')
    team1=str(team[0])
    team2=str(team[1])
    team1=team1.replace(' ','')
    team2=team2.replace(' ','')
    team1=pd.read_csv('data/t20_team/'+team1+'.csv')
    team2=pd.read_csv('data/t20_team/'+team2+'.csv')
    
    return render_template("match1.html", title=t1,team1=team[0],team2=team[1],playing="TOP 11",sqaud1=team1,squad2=team2)
def todays():
    t1 = request.args.get('t1')
    title=t1
     
    team=t1.split(' ')
    team1=str(team[0])
    team2=str(team[1])
    team11=team1.replace(' ','')
    team22=team2.replace(' ','')
    print(team1)
    print(team2)
    team1=pd.read_csv('data/t20_team/'+team1+'.csv')
    team2=pd.read_csv('data/t20_team/'+team2+'.csv')
    print("-------t1-----------")
    print(t1)  
    print(team)
    print(team[0])
    print(team[1])
    return render_template("match1.html", title=title,team1=team11,team2=team22,playing="TOP 11",sqaud1=team1,squad2=team2)

# def covid_ask_help():
#     return render_template("ask_help.html", title="Ask Help")
# def covid_view_help():
#     return render_template("view_help.html", title="View Help")
# def covid_volunterr_help():
#     return render_template("volunteer.html", title="Volunteer Registration")