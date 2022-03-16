# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:16:05 2022

@author: 417-DevOps

"""

#%% ========== IMPORT LIBRARIES ========== %%#
from riotwatcher import LolWatcher

from dotenv import load_dotenv
import time, os


#%% ========== DEFINE FUNCTIONS ========== %%# 
def get_matchData(match_ID, player_name, player_routing,
                  lol_watcher):
    game_data= lol_watcher.match.by_id(region= player_routing, match_id= match_ID)
    
    ##--------- GET TOP LEVEL Match & Team STATS ---------##
    participant_data= game_data['info']['participants']

    
    #teams are 0-4 and 5-9, so let's find the id of the summoner
    player_name= player_name
    for item in participant_data:
        if item['summonerName'] == player_name:
            p_id= game_data['info']['participants'].index(item)
        else:
            # print(item['summonerName'])
            pass

    ##--------- GET Individual STATS ---------##
    player_stats= participant_data[p_id]

    # Champ, Lane, win/loss
    lane= player_stats['lane']
    role= player_stats['role']
    win_loss= float(player_stats['win'])

    return lane, role, win_loss

#%% ========== TROUBLESHOOTING ========== %%#
if __name__ == '__main__':
    start_time = time.time()

    ##--------- LOAD CONFIG DATA ---------##
    load_dotenv('../../config.env')
    api_key = os.environ['DEV_KEY'] 
    lol_watcher = LolWatcher(api_key)
    del api_key

    ##--------- SET PLAYER PARAMETERS ---------##
    player_name= 'RebirthNA'
    player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
    player_routing= 'americas'
   
    
    ##--------- LOAD THE PLAYER DATA AS CLASS ---------##
    summoner= lol_watcher.summoner.by_name(player_region, player_name)
    match_history= lol_watcher.match.matchlist_by_puuid(region= player_routing, puuid= summoner['puuid'],
                                                        queue= 420, 
                                                        start=0, count= 2)
    last_match= match_history[0] #this is the most recent match ID
    # print('Match ID= ', last_match)
    
    
    ##--------- GET MATCH DATA BY MATCH ID ---------##    
    [lane, role, win_loss]= get_matchData(last_match, player_name, player_routing, lol_watcher)
    print(lane)
    print(role)
    
    print("\n--- %s seconds ---" % (time.time() - start_time))