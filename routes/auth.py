from flask import render_template, request, redirect, url_for, flash, abort

from models.user import User
from db.db import db
from flask_login import login_user, current_user, logout_user
import bcrypt
from datetime import datetime, timedelta, date
from flask import request
from user_agents import parse
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

from nltk.cluster.util import cosine_distance
import numpy as np
import csv
from application import app
import pandas as pd
def index():
    worl_cup_schedule=pd.read_csv("data/2021_cup_schedule.csv")
    worl_cup_schedule=worl_cup_schedule.loc[:,['id','match_title','match_subtitle','venue','date']]
    worl_cup_schedule['date']=pd.to_datetime(worl_cup_schedule['date'])
    worl_cup_schedule['date'] =pd.to_datetime( worl_cup_schedule['date']).dt.date
    worl_cup_schedule1=worl_cup_schedule[worl_cup_schedule['date']==date.today()]
    print(worl_cup_schedule1)
    todays_match=pd.DataFrame()
    for i in worl_cup_schedule1['match_title']:
        print("-------i-----------")
        teams=i.split('at')
        print(teams)
        t=teams[0].split('v')
        print(t)
        worl_cup_schedule1['team1']=t[0]
        worl_cup_schedule1['team2']=t[1]
        todays_match=todays_match.append(worl_cup_schedule1)
    todays_match=todays_match.drop_duplicates(subset=['team1','team2'])
    worl_cup_upcoming=worl_cup_schedule[worl_cup_schedule['date']>date.today()]
    worl_cup_upcoming['date'] =pd.to_datetime( worl_cup_upcoming['date']).dt.date
    worl_cup_upcoming=worl_cup_upcoming.head(8)
    worl_cup_upcoming=worl_cup_upcoming.loc[:,['match_title','date']]
    worl_cup_upcoming['match_title']=worl_cup_upcoming['match_title'].str.split("at")


    return render_template("index.html", title="Fantastic Playing Players",match_todays=todays_match,worl_cup_upcoming=worl_cup_upcoming)
def match1():
    t1 = request.args.get('t1')  
    team=t1.split('v')
    team1=str(team[0])
    team2=str(team[1])
    team1=team1.replace(' ','')
    team2=team2.replace(' ','')
    team1=pd.read_csv('data/t20_team/'+team1+'.csv')
    team2=pd.read_csv('data/t20_team/'+team2+'.csv')
    t20=pd.read_csv('data/t20_player_stat.csv')
    print(t20)
    player_record1=pd.DataFrame()

    for player_name1,player_name2 in zip(team1['Player Name'],team1['Player Name 2']):
        t20m=t20.copy()
        t20m.loc[t20m.player_name==player_name2,"player_name"]=player_name1
        player=t20m[t20m['player_name']==player_name1]
        
        player=player.sort_values('date')
        player['date']=pd.to_datetime(player['date'])  
        player_info=pd.DataFrame()
        player_info['player_name']=player['player_name']
        player_info['data_since']=player['date'].min()
        player_info['Runs']=player['runs'].sum().round(0)
        intl_record=player[player['tournament']=="T20_INT"]
        ipl_record=player[player['tournament']=="IPL"]
        player_info['Intl_Runs']=intl_record['runs'].sum().round(0)
        player_info['League_Runs']=ipl_record['runs'].sum().round(0)
        player_info['matches']=player['runs'].count()
       
        player_info['Intl_matches']=intl_record['runs'].count()
        player_info['League_matches']=ipl_record['runs'].count()
        player_info['Intl_avg']=player_info['Intl_Runs'].mean()
        player_info['avg']=player['runs'].mean()
        player['strike_rate']=player['strike_rate'].str.replace("-","0")
        intl_record['strike_rate']=intl_record['strike_rate'].str.replace("-","0")
        ipl_record['strike_rate']=ipl_record['strike_rate'].str.replace("-","0")
        player_info['Strike_rate']=player['strike_rate'].astype('float').mean()
        player_info['Intl_SR']=intl_record['strike_rate'].astype('float').mean()
        player_info['League_SR']=ipl_record['strike_rate'].astype('float').mean()
        player_last5=player.tail(5) 
        player_info['last_five_runs']=player_last5['runs'].sum()
        player_info['last_five_avg']=(player_last5['runs'].sum())/5
        player['economy']=player['economy'].str.replace("-","0")
        player['economy']=player['economy'].astype('float')
        player_last5['economy']=player_last5['economy'].astype('float')
        intl_record['economy']=intl_record['economy'].str.replace("-","0")
        intl_record['economy']=intl_record['economy'].astype('float')
        player_info['wickets']=player['wickets'].sum()
        player_info['economy']=player['economy'].mean()
        player_info['last_five_wickets']=player_last5['wickets'].sum()
        player_info['last_five_eco']=(player_last5['economy'].sum())/5
        player_info['Intl_wickets']=intl_record['wickets'].sum().round(0)
        player_info['League_eco']=intl_record['economy'].mean()

        # player_venue=player[player['venue']=="Dubai International Cricket Stadium"]
        # player_info['venues_runs']=player_venue['runs'].sum().round(0)
        # player_info['venues_matchs']=player_venue['runs'].count()
            
        player_record1=player_record1.append(player_info,ignore_index=True)
    player_record1=player_record1.drop_duplicates('player_name')
    player_record1
    
    player_record1['data_since'] =pd.to_datetime( player_record1['data_since']).dt.date
    player_record1['Runs']=player_record1['Runs'].astype('int')
    player_record1['last_five_runs']=player_record1['last_five_runs'].astype('int')
    player_record1['wickets']=player_record1['wickets'].astype('int')
    player_record1['last_five_wickets']=player_record1['last_five_wickets'].astype('int')
    player_record1['Intl_Runs']=player_record1['Intl_Runs'].astype('int')
    player_record1=player_record1.round(0)
    print(player_record1)

    player_record2=pd.DataFrame()

    for player_name1,player_name2 in zip(team2['Player Name'],team2['Player Name 2']):
        t20m=t20.copy()
        t20m.loc[t20m.player_name==player_name2,"player_name"]=player_name1
        player=t20m[t20m['player_name']==player_name1]
        player=player.sort_values('date')
        player['date']=pd.to_datetime(player['date'])  
        player=player.replace('-','0')
        player_info=pd.DataFrame()
        player_info['player_name']=player['player_name']
        player_info['data_since']=player['date'].min()
        player_info['Runs']=player['runs'].sum().round(0)
        intl_record=player[player['tournament']=="T20_INT"]
        ipl_record=player[player['tournament']=="IPL"]
        player_info['Intl_Runs']=intl_record['runs'].sum().round(0)
        player_info['League_Runs']=ipl_record['runs'].sum().round(0)
        player_info['matches']=player['runs'].count()
        player_info['Intl_matches']=intl_record['runs'].count()
        player_info['League_matches']=ipl_record['runs'].count()
        player_info['Intl_avg']=player_info['Intl_Runs'].mean()
        player_info['avg']=player['runs'].mean()
        player['strike_rate']=player['strike_rate'].str.replace("-","0")
        intl_record['strike_rate']=intl_record['strike_rate'].str.replace("-","0")
        ipl_record['strike_rate']=ipl_record['strike_rate'].str.replace("-","0")
        player_info['Strike_rate']=player['strike_rate'].astype('float').mean()
        player_info['Intl_SR']=intl_record['strike_rate'].astype('float').mean()
        player_info['League_SR']=ipl_record['strike_rate'].astype('float').mean()
        player_last5=player.tail(5) 
        player_info['last_five_runs']=player_last5['runs'].sum()
        player_info['last_five_avg']=(player_last5['runs'].sum())/5
        player['economy']=player['economy'].astype('float')
        player_last5['economy']=player_last5['economy'].astype('float')
        intl_record['economy']=intl_record['economy'].astype('float')
        player_info['wickets']=player['wickets'].sum()
        player_info['economy']=player['economy'].mean()
        player_info['last_five_wickets']=player_last5['wickets'].sum()
        player_info['last_five_eco']=(player_last5['economy'].sum())/5
        player_info['Intl_wickets']=intl_record['wickets'].sum().round(0)
        player_info['League_eco']=intl_record['economy'].mean()
        # player_venue=player[player['venue']=="Dubai International Cricket Stadium"]
        # player_info['venues_runs']=player_venue['runs'].sum().round(0)
        # player_info['venues_matchs']=player_venue['runs'].count()
            
        player_record2=player_record2.append(player_info)
    player_record2=player_record2.drop_duplicates('player_name')
    player_record2
    
    player_record2['data_since'] =pd.to_datetime( player_record2['data_since']).dt.date
    player_record2['Runs']=player_record2['Runs'].astype('int')
    player_record2['last_five_runs']=player_record2['last_five_runs'].astype('int')
    player_record2['wickets']=player_record2['wickets'].astype('int')
    player_record2['last_five_wickets']=player_record2['last_five_wickets'].astype('int')
    player_record2['Intl_Runs']=player_record2['Intl_Runs'].astype('int')
    player_record2=player_record2.copy()
    
    player_record=player_record1.append(player_record2)
    player_record=player_record.nlargest(11,['Strike_rate','Intl_SR','Intl_Runs','last_five_avg','wickets','economy','Intl_wickets','last_five_wickets','last_five_runs','last_five_runs'])
    player_record=player_record.reset_index()
    del player_record['index']
    player_record.index = np.arange(2, len(player_record)+2)
    print(player_record)
    
    print(player_record2)

    return render_template("match1.html", title=t1,team1=team[0],team2=team[1],playing="TOP 11",sqaud1=player_record1,squad2=player_record2,top=player_record)
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
    print(team1)
    t20=pd.read_csv('data/t20_player_stat.csv')
    print(t20)
    player_record1=pd.DataFrame()

    for player_name1,player_name2 in zip(team1['Player Name'],team1['Player Name 2']):
        t20m=t20.copy()
        t20m.loc[t20m.player_name==player_name2,"player_name"]=player_name1
        player=t20m[t20m['player_name']==player_name1]
        
        player=player.sort_values('date')
        player['date']=pd.to_datetime(player['date'])  
        player_info=pd.DataFrame()
        player_info['player_name']=player['player_name']
        player_info['data_since']=player['date'].min()
        player_info['Runs']=player['runs'].sum().round(0)
        intl_record=player[player['tournament']=="T20_INT"]
        ipl_record=player[player['tournament']=="IPL"]
        player_info['Intl_Runs']=intl_record['runs'].sum().round(0)
        player_info['League_Runs']=ipl_record['runs'].sum().round(0)
        player_info['matches']=player['runs'].count()
       
        player_info['Intl_matches']=intl_record['runs'].count()
        player_info['League_matches']=ipl_record['runs'].count()
        player_info['Intl_avg']=player_info['Intl_Runs'].mean()
        player_info['avg']=player['runs'].mean()
        player['strike_rate']=player['strike_rate'].str.replace("-","0")
        intl_record['strike_rate']=intl_record['strike_rate'].str.replace("-","0")
        ipl_record['strike_rate']=ipl_record['strike_rate'].str.replace("-","0")
        player_info['Strike_rate']=player['strike_rate'].astype('float').mean()
        player_info['Intl_SR']=intl_record['strike_rate'].astype('float').mean()
        player_info['League_SR']=ipl_record['strike_rate'].astype('float').mean()
        player_last5=player.tail(5) 
        player_info['last_five_runs']=player_last5['runs'].sum()
        player_info['last_five_avg']=(player_last5['runs'].sum())/5
        player['economy']=player['economy'].astype('float')
        player_last5['economy']=player_last5['economy'].astype('float')
        intl_record['economy']=intl_record['economy'].astype('float')
        player_info['wickets']=player['wickets'].sum()
        player_info['economy']=player['economy'].mean()
        player_info['last_five_wickets']=player_last5['wickets'].sum()
        player_info['last_five_eco']=(player_last5['economy'].sum())/5
        player_info['Intl_wickets']=intl_record['wickets'].sum().round(0)
        player_info['League_eco']=intl_record['economy'].mean()

        # player_venue=player[player['venue']=="Dubai International Cricket Stadium"]
        # player_info['venues_runs']=player_venue['runs'].sum().round(0)
        # player_info['venues_matchs']=player_venue['runs'].count()
            
        player_record1=player_record1.append(player_info,ignore_index=True)
    player_record1=player_record1.drop_duplicates('player_name')
    player_record1
    
    player_record1['data_since'] =pd.to_datetime( player_record1['data_since']).dt.date
    player_record1['Runs']=player_record1['Runs'].astype('int')
    player_record1['last_five_runs']=player_record1['last_five_runs'].astype('int')
    player_record1['wickets']=player_record1['wickets'].astype('int')
    player_record1['last_five_wickets']=player_record1['last_five_wickets'].astype('int')
    player_record1['Intl_Runs']=player_record1['Intl_Runs'].astype('int')
    player_record1=player_record1.round(0)
    print(player_record1)

    player_record2=pd.DataFrame()

    for player_name1,player_name2 in zip(team2['Player Name'],team2['Player Name 2']):
        t20m=t20.copy()
        t20m.loc[t20m.player_name==player_name2,"player_name"]=player_name1
        player=t20m[t20m['player_name']==player_name1]
        player=player.sort_values('date')
        player['date']=pd.to_datetime(player['date'])  
        player=player.replace('-','0')
        player_info=pd.DataFrame()
        player_info['player_name']=player['player_name']
        player_info['data_since']=player['date'].min()
        player_info['Runs']=player['runs'].sum().round(0)
        intl_record=player[player['tournament']=="T20_INT"]
        ipl_record=player[player['tournament']=="IPL"]
        player_info['Intl_Runs']=intl_record['runs'].sum().round(0)
        player_info['League_Runs']=ipl_record['runs'].sum().round(0)
        player_info['matches']=player['runs'].count()
        player_info['Intl_matches']=intl_record['runs'].count()
        player_info['League_matches']=ipl_record['runs'].count()
        player_info['Intl_avg']=player_info['Intl_Runs'].mean()
        player_info['avg']=player['runs'].mean()
        player['strike_rate']=player['strike_rate'].str.replace("-","0")
        intl_record['strike_rate']=intl_record['strike_rate'].str.replace("-","0")
        ipl_record['strike_rate']=ipl_record['strike_rate'].str.replace("-","0")
        player_info['Strike_rate']=player['strike_rate'].astype('float').mean()
        player_info['Intl_SR']=intl_record['strike_rate'].astype('float').mean()
        player_info['League_SR']=ipl_record['strike_rate'].astype('float').mean()
        player_last5=player.tail(5) 
        player_info['last_five_runs']=player_last5['runs'].sum()
        player_info['last_five_avg']=(player_last5['runs'].sum())/5
        player['economy']=player['economy'].astype('float')
        player_last5['economy']=player_last5['economy'].astype('float')
        intl_record['economy']=intl_record['economy'].astype('float')
        player_info['wickets']=player['wickets'].sum()
        player_info['economy']=player['economy'].mean()
        player_info['last_five_wickets']=player_last5['wickets'].sum()
        player_info['last_five_eco']=(player_last5['economy'].sum())/5
        player_info['Intl_wickets']=intl_record['wickets'].sum().round(0)
        player_info['League_eco']=intl_record['economy'].mean()
        # player_venue=player[player['venue']=="Dubai International Cricket Stadium"]
        # player_info['venues_runs']=player_venue['runs'].sum().round(0)
        # player_info['venues_matchs']=player_venue['runs'].count()
            
        player_record2=player_record2.append(player_info)
    player_record2=player_record2.drop_duplicates('player_name')
    player_record2
    
    player_record2['data_since'] =pd.to_datetime( player_record2['data_since']).dt.date
    player_record2['Runs']=player_record2['Runs'].astype('int')
    player_record2['last_five_runs']=player_record2['last_five_runs'].astype('int')
    player_record2['wickets']=player_record2['wickets'].astype('int')
    player_record2['last_five_wickets']=player_record2['last_five_wickets'].astype('int')
    player_record2['Intl_Runs']=player_record2['Intl_Runs'].astype('int')
    player_record2=player_record2.round(0)
    print(player_record2)
    player_record=player_record1.append(player_record2)
    player_record=player_record.nlargest(11,['Strike_rate','Intl_SR','Intl_Runs','last_five_avg','wickets','economy','Intl_wickets','last_five_wickets','last_five_runs'])
    player_record=player_record.reset_index()
    del player_record['index']
    # print(player_record)
    player_record.index = np.arange(2, len(player_record)+2)
    return render_template("match1.html", title=title,team1=team11,team2=team22,playing="TOP 11",sqaud1=player_record1,squad2=player_record2,top=player_record)

# def covid_ask_help():
#     return render_template("ask_help.html", title="Ask Help")
# def covid_view_help():
#     return render_template("view_help.html", title="View Help")
# def covid_volunterr_help():
#     return render_template("volunteer.html", title="Volunteer Registration")