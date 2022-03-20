# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:16:05 2022

Author: 417-DevOps
Desc: Get lane that challenger players typically play
"""

#%% ##--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher #'pip install riotwatcher' in Anaconda prompt
from dotenv import load_dotenv #'pip install python-dotenv' in Anaconda prompt
import os, time

from collections import Counter
import pandas as pd
import numpy as np

from get_matchData import *


#%% ##--------- FUNCTIONS ---------##
def setup_env():
    load_dotenv('../../config.env')
    api_key = os.environ['DEV_KEY'] 

    lol_watcher = LolWatcher(api_key) #Tell Riot Watcher to use LoL functions with the API key
    del(api_key)
    
    return lol_watcher

def get_match_history(summonerName, player_region, summoner):
    match_history= lol_watcher.match.matchlist_by_puuid(region= player_routing, puuid= summoner['puuid'],
                                                    queue= 420, 
                                                    start=0, count= 5)
    return match_history

def get_challenger_players(player_region,queue_type, lol_watcher):
    challenger_players= pd.DataFrame.from_dict(lol_watcher.league.challenger_by_queue(region= player_region, 
                                                              queue=queue_type)['entries']) 
    challenger_players= challenger_players.sort_values(by = 'leaguePoints', ascending = False) #organize into leaderboard
    challenger_players.reset_index(drop=True, inplace=True) #reset index to match order
    summoner_names= challenger_players['summonerName'].tolist()
    return summoner_names
    
def get_challenger_lane(summonerName, player_routing, lol_watcher):
    summoner= lol_watcher.summoner.by_name(player_region, summonerName) #get the summoner info
    match_history= get_match_history(summonerName, player_region, summoner)
    
    roles_played= []
    lanes_played= []
    win_loss_list= []
    for matchID in match_history:
        try:
            [lane, role,win]= get_matchData(matchID, summonerName, player_routing, lol_watcher)
            roles_played.append(role)
            
            if role=='DUO':
                lanes_played.append('BOTTOM_'+role)
            elif (role== 'SUPPORT' and lane == 'JUNGLE'):
                lanes_played.append(lane)
            elif role=='SUPPORT':
                lanes_played.append('BOTTOM_'+role)
            else:
                lanes_played.append(lane)
            win_loss_list.append(win)
            
        except:
            pass
    
    player_pref_lane= Counter(lanes_played).most_common(1)[0][0]
    player_pref_role= Counter(roles_played).most_common(1)[0][0]
    win_loss_ratio= np.mean(win_loss_list)
    
    return [player_pref_lane, player_pref_role, win_loss_ratio]
   
#%% MAIN CODE
start_time = time.time()
lol_watcher= setup_env()

# Get challenger players
player_region= 'KR'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
player_routing= 'asia'
queue_type= 'RANKED_SOLO_5x5' #RANKED_SOLO_5x5, RANKED_FLEX_SR, 

summoner_names= get_challenger_players(player_region,queue_type, lol_watcher)

col_names= ['lane','role','win_rate']
raw_data= pd.DataFrame(columns = col_names)
for summonerName in summoner_names:
    print(summonerName)
        
    # summonerName= summoner_names[i] #grab the summoner name
    try:
        res= get_challenger_lane(summonerName, player_routing, lol_watcher)
        
        row = pd.Series(res, index=raw_data.columns)
        raw_data = raw_data.append(row, ignore_index=True)
    except:
        pass
    
# print(raw_data)
raw_data['summoner names'] = summoner_names
filename= player_region+'_challenger_lanes'+'.xlsx'
raw_data.to_excel(filename, index = False)

print("\n--- %s seconds ---" % (time.time() - start_time))