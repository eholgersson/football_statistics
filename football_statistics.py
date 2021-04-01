#!/bin/python3

import pandas as pd
import numpy as np 
import requests
import json
import api_config as cfg
import os
print(os.getcwd())

def config():
    global headers
    api_key = cfg.api_key['key']
    headers = {
        "x-apisports-key" : api_key
    }

def get_response():
    url = "https://v3.football.api-sports.io/teams/statistics"
    payload={}
    api_key = cfg.api_key['key']
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

    
def get_team_statistics(team, league, year):
    config()
    
    url = ""
    resp = requests.get(url, headers=headers)

def main():
    
    # from api
    resp = get_response()
    
    resp = resp.json()

    print(os.getcwd())
    #save response
    version = 1
    filename = '/Users/emanuel.holgersson/Documents/Python/REST_APIs/football_statistics_teams_statistics'+str(version)+'.json'
    write_to_json(resp, filename)

    # from file
    #resp = load_json(filename)
    

    df = teams_endpoint(resp)

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

