# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:54:40 2020
@author: 417-DevOps
Determines the number of players by role in a given ladder
NOTE: this is broken, but used as a conceptual tool for future projects
"""

import time
from RiotAPI import RiotAPI
import collections
    
def getAPI_key():
    #reads the API key from local file
    file= open("../api_key.txt","r")
    return file.read()

def pull_ChallengerLadder(queue):
    ''' Returns the list of challenger players for a given server
    Inputs= queueType (soloQ, flex)
    Returns= list of ranked ladder data
    '''
    r= api.get_league(queue)
    return r.json()

def pull_apexLadderPage(**kwargs):
    ''' Pulls one page of the challenger ladder data
    Takes arguements listed in pull_allApex()
    Returns one page of challenger ranked ladder data in a list
    '''
    r= api.get_league_exp(**kwargs)
    return r.json()

def pull_allApex(ladder_params):
    ''' Retrieves full ladder list of the top tier players
    Takes in queue, tier, division, page
    Returns a list of full top players' ranked data
    '''
    ladder_data=[]
    while True:
        data= pull_apexLadderPage(**ladder_params)
        # print('current page=',ladder_params['page'])
        if len(data)== 0: #stop loop if there are not more challengers
            break
        
        for item in data:
            ladder_data.append(item)
        ladder_params['page']= str(int(ladder_params['page'])+1)
        
    return ladder_data
    
def summonerName2accountId(summonerName):
    '''
    Parameters
    ----------
    summonerName : String

    Returns
    -------
    JSON
        Json response of summoner data
    '''
    r= api.get_summoner_by_name(summonerName)
    return r.json()

def account_matchHistory(accountID):
    r= api.get_matchHistory(accountID)
    return r.json()

def positionList(matchHistory):
    matchList= matchHistory['matches']
    position_list=[]
    for item in matchList:
        if (item['role']=='NONE') or (item['role'] =='SOLO'):
            position_list.append(item['lane'])
        elif (item['role'] =='DUO'):
            if (item['lane'] != 'BOTTOM') or (item['lane'] != 'BOT'):
                position_list.append(item['lane'])
        else:
            position_list.append(item['role'])  
    return position_list

def role(position_list):
    # get three most common roles and the number of their occurances
    # ex. [('MID', 57), ('DUO_SUPPORT', 26), ('TOP', 6)]
    role_data= collections.Counter(position_list).most_common(3)
    # get the most common role
    main_role= role_data[0][0]
    return main_role

def saveData(output_label,role_breakdown):
    f= open('role_data.txt','a')
    f.write(output_label)
    f.write('\n')
    f.write(str(role_breakdown))
    f.write('\n')
    f.close()

#%% INITIAL
start_time= time.time()
# f= open('role_data.txt','w')
# f.close()

print('\n########################################################')
print('Queue Positional Data Tool')

api_key= getAPI_key()
'''change REGION here'''
#specify region of interest
target_region= 'EUW'
api= RiotAPI(api_key, target_region)
# rate limits= 20/s or 100/2min

#%% GET THE LADDER DATA
task_time= time.time()

'''change TIER here'''
challenger_only= False
# tier= CHALLENGER, GRANDMASTER, MASTER, DIAMOND
target_tier= 'GRANDMASTER'

print('Pulling ladder data...')
if challenger_only:
    # For challenger only
    ladder_queue='SoloQ' #SoloQ or Flex
    queueOptions= {'SoloQ': 'RANKED_SOLO_5x5',
                   'Flex': 'RANKED_FLEX_SR'}
    # ladderData= pull_ChallengerLadder(queueOptions['SoloQ'])
    ladderData= pull_ChallengerLadder(queueOptions[ladder_queue])
    ladderData= ladderData['entries'] #only care about the players on the ladder
else:    
    # Option to pull from other leagues 
    ladder_params= {'queue':'RANKED_SOLO_5x5',
                        'tier': target_tier,
                        'division': 'I',
                        'page': '1'}
    ladderData= pull_allApex(ladder_params)

# Isolate the summoner names from the ladder data
summonerName_list= []
for item in ladderData:
    summonerName_list.append(item['summonerName'])

print("--- Pulled Ladder Data in %s seconds ---" % (time.time() - task_time))  

#%% CONVERT SUMMONER NAMES TO ACCOUNT IDs
task_time= time.time()

print('Getting Account IDs...')
# see the image in folder for ladder amount breakdowns
accountId_list= []
count= 0
for item in summonerName_list:
    data= summonerName2accountId(item)
    accountId_list.append(data['accountId'])
    
    print(count)
    count+=1

print("--- Obtained Summoner IDs in %s seconds ---" % (time.time() - task_time))  

#%% GET MATCH HISTORIES USING ACCOUNT IDs
task_time= time.time()

print('Getting match histories...')
main_role_list=[]
count= 0
for item in accountId_list:
    # get the match history using the account ID
    matchHistory= account_matchHistory(item)
    # convert the match history to a list of positions played
    position_list= positionList(matchHistory)
    
    # find which role is their main role & append that to the list
    main_role= role(position_list)
    main_role_list.append(main_role)
    
    print(count)
    count+=1
    
print("--- Obtained Match Histories in %s seconds ---" % (time.time() - task_time))  

#%% DETERMINE THE ROLE BREAKDOWN
task_time= time.time()

print('Calculating role breakdown...')
role_breakdown= collections.Counter(main_role_list).most_common(5)

if challenger_only:
    output_label= '\nRegion= '+target_region+'Queue= '+ladder_queue+'Tier= Challenger'
    print(output_label)
    print(role_breakdown)
    saveData(output_label,role_breakdown)
else:
    output_label= '\nRegion= '+target_region+', Queue= '+ladder_params['queue']+', Tier= '+ladder_params['tier']
    print(output_label)
    print(role_breakdown)
    saveData(output_label,role_breakdown)
print("\n--- Calculated Role Breakdown in %s seconds ---" % (time.time() - task_time))  

#%% ENDING FOOTER
print("\n--- Completed in %s seconds ---" % (time.time() - start_time))  