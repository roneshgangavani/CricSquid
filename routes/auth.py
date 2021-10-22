from flask import render_template, request, redirect, url_for, flash, abort

from models.user import User
from db.db import db
from flask_login import login_user, current_user, logout_user
import bcrypt
from datetime import datetime, timedelta, date
from flask import request
from user_agents import parse
import psycopg2
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize
stop_word = stopwords.words('english')
import string
import heapq
import networkx as nx
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
    match_title=worl_cup_schedule1['match_title'].unique()[0]
    worl_cup_upcoming=worl_cup_schedule[worl_cup_schedule['date']>=str(date.today())+"T10:00:00+00:00"]
    worl_cup_upcoming=worl_cup_upcoming.head(4)
    worl_cup_upcoming=worl_cup_upcoming.loc[:,['match_title','date']]
    worl_cup_upcoming['match_title']=worl_cup_upcoming['match_title'].str.split("at")
    print(worl_cup_upcoming)
    return render_template("index.html", title="Fantastic Playing Players",match_title=match_title,worl_cup_upcoming=worl_cup_upcoming)
def match1():
    return render_template("match1.html", title="Australia vs South Africa",team1="Aus",team2="SA",playing="TOP 11")

# def covid_ask_help():
#     return render_template("ask_help.html", title="Ask Help")
# def covid_view_help():
#     return render_template("view_help.html", title="View Help")
# def covid_volunterr_help():
#     return render_template("volunteer.html", title="Volunteer Registration")