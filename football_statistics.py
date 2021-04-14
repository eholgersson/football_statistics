#!/bin/python3

import pandas as pd
import numpy as np 
import requests
import json
import api_config as cfg
import os
import time
from tqdm import tqdm

print(os.getcwd())

global url, api_key

url = cfg.api_config['url']
api_key = cfg.api_config['api_key']

# %%
league = {"id": 39, "name": "Premier League"}
l = "".join(league['name'].split(" "))
l

print(api_key)

def config():
    global headers
    api_key = cfg.api_config['api_key']
    headers = {
        "x-apisports-key" : api_key
    }

# get teams from league and year
def get_response(league, year):
    url = f"https://v3.football.api-sports.io/teams?league={league}&season={year}"
    payload={}
    api_key = cfg.api_config['api_key']
    headers = {
        "x-apisports-key" : api_key
    }

    resp = requests.get(url=url, headers=headers, data=payload)
    print(resp)

    return resp

def write_to_json(resp, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(resp, f, ensure_ascii=False, indent=4)

def load_json(filename):

    with open(filename) as json_file:
        data = json.load(json_file)
    
    return data

def teams_endpoint(resp):

    df = pd.json_normalize(resp['response'])

    print(df.head())

    return df


def save_to_csv(df, filename):

    filename = filename.split('/')[-1].split('.')[0]
    filename = os.getcwd()+'/'+filename
    df.to_csv(filename+'.csv', encoding='utf-8', index=False)
    print(os.getcwd())
    print("saved to: " + filename)


# get team statistics
def get_team_statistics(team, league, year):
    config()
    
    url = cfg.api_config['url']

    url += f"teams/statistics?season={year}&team={team}&league={league}"
    #print('in config: ', headers)
    #print(url)
    payload={}

    resp = requests.get(url, headers=headers, data=payload)

    resp = resp.json()

    #print(resp)

    try:
        # team statistic: json to df
        team = resp['response']['team']
        fixtures = resp['response']['fixtures']
        df_team = pd.json_normalize(team)
        df_fixtures = pd.json_normalize(fixtures)
        df = pd.json_normalize(resp['response'])
        #print(df.columns)
        #print(df_team.head())
        #print(df_fixtures.head())

        # Adds fixtures and team for the specified team
        df = pd.concat([df_fixtures,df_team], axis=1)
    except TypeError:
        print(resp)
    

    return df
        

def main_statistics(league_id, year):
    # from api
    resp = get_response(league_id, year)
    resp = resp.json()

    df = pd.json_normalize(resp['response'])
    print(df.head())
    print(df.columns)

    # team to loop through via team id
    team_id = df['team.id']
    columns = ["played.home", "played.away", "played.total", "wins.home", "wins.away", "wins.total", "draws.home", "draws.away", "draws.total", "loses.home", "loses.away" ,"loses.total","id","name","logo"]
    df_stats = pd.DataFrame(columns=columns)
    excluded = [10]
    for t_id in tqdm(team_id):
        if t_id in excluded:
            continue
        df = get_team_statistics(t_id,league_id, year)
        df_stats = df_stats.append(df, ignore_index=True)
        time.sleep(6.1)
    print(df_stats.head())

    l = "".join(league['name'].split(" "))
    filename= f"teams_statistics_{l}_{year}.csv"
    save_to_csv(df_stats, filename)




def main():
    

    # get teams and team statistics for a specific league and year 
    main_statistics(league['id'], 2019)


    if 0:

        print(os.getcwd())
        #save response
        version = 4
        filename = '/Users/emanuel.holgersson/Documents/Python/REST_APIs/football_statistics_teams_'+str(version)+'.json'
        
        #write_to_json(resp, filename)

    #go_through(filename)

    # from file
    #resp = load_json(filename)
    

    # df = teams_endpoint(resp)

    #save_to_csv(df, filename)

    
    #print(type(resp['response']))


    #df = pd.DataFrame(resp['response'])

    #df1 = pd.DataFrame(resp['response']['league'])

    

    #print(df.league.apply(pd.Series).head())
    #df.seasons = df.seasons.map(eval)
    # print(df.seasons.apply(lambda x: x[0]))
    # df.seasons = df.seasons.apply(lambda x: x[0])
    # print(df.seasons.apply(pd.Series).head())
    #print(resp.json())


if __name__ == '__main__':
    main()


# %%
import pandas
import json

people = {1: {'name': 'John', 'age': '27', 'sex': 'Male'}}

print(people[1]['name'])

# %%

import pandas as pd

df1 = pd.DataFrame([1,2,3], columns=['a'])
df1
df2 = pd.DataFrame([1,2,3], columns=['b'])
df2

# %%
pd.concat([df1, df2], axis=1)
# %%
