# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:30:51 2020
@author: Karl Roush

Constant values associated with the Riot API
"""

URL= {
      'base': 'https://{region}.api.riotgames.com/lol/{url}',
      
      #summoner API= returns id, accountId, puuid, name, profileIconId, revisionDate, summonerLevel
      'summoner_by_name':'summoner/v{version}/summoners/by-name/{names}',
      
      #ranked API by queue= returns ladder data
      'league_by_queue': 'league/v{version}/challengerleagues/by-queue/{queueType}',
      
      #expiremental ranked API= returns ladder data (leagueId, summonerId, name, LP, wins, losses, etc)
      'league_exp': 'league-exp/v{version}/entries/{queue}/{tier}/{division}?page={page}',
      
      #Match API= returns matches with champion, queue, role (queue 420= 5v5 Ranked Solo games SR)
      'match_by_account': 'match/v{version}/matchlists/by-account/{accountID}?queue={queue}&season={season}'}

API_VERSIONS= {
    'summoner_by_name': '4',
    'league_by_queue': '4',
    'league_exp': '4',
    'match_by_account': '4'}

QUEUES= {
    'SoloQ':'420',
    'Flex': '440'}

SEASONS= {
    'Preseason 2019': '12',
    'Season 2019': '13'}

REGIONS= {
    'BR': 'br1',
    'EUN': 'eun1',
    'EUW': 'euw1',
    'JP': 'jp1',
    'KR': 'kr',
    'LAN': 'la1',
    'LAS': 'la2',
    'NA': 'na1',
    'OCE': 'oc1',
    'TR': 'tr1',
    'RU': 'ru'}