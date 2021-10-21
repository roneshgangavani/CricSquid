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

def iswindows():
    import platform
    if platform.system() == "Windows":
        return True
    else:
        return False

def iswindows():
    import platform
    if platform.system() == "Windows":
        return True
    else:
        return False

def index():
    return render_template("index.html", title="Hope Now")
# def covid_ask_help():
#     return render_template("ask_help.html", title="Ask Help")
# def covid_view_help():
#     return render_template("view_help.html", title="View Help")
# def covid_volunterr_help():
#     return render_template("volunteer.html", title="Volunteer Registration")