# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:41:33 2020

Class that serves as access point for Riot API (to make calls)
NOTE: this is broken, but used as a conceptual tool for future projects
"""

import requests
import RiotConsts as Consts
import time

class RiotAPI(object):
    def __init__(self, api_key, region='NA'):
        #default region is NA
        self.api_key= api_key
        self.region= Consts.REGIONS[region]
    
    def _request(self, api_url, params={}):
        args= {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key]= value
                
        # can also add timeout= 0.05 to .get for testing        
        r = requests.get(Consts.URL['base'].format(
                region= self.region,
                url= api_url), params= args)
        if r.status_code != 200:
            print('Status code=',r.status_code)
            if r.status_code== 504 or r.status_code== 503: 
                # gateway or unavailable
                print('Retrying...')
                retry_counter=0
                while retry_counter < 5 and (r.status_code== 504 or r.status_code== 503):
                    time.sleep(0.25)
                    r= requests.get(Consts.URL['base'].format(
                            region= self.region,
                            url= api_url), params= args)
                    retry_counter+=1
                    
            elif r.status_code== 429: 
                # if rate limited 
                print('Rate limited. Waiting 2min...')
                time.sleep(120)
                r = requests.get(Consts.URL['base'].format(
                    region= self.region,
                    url= api_url), params= args)
                
            elif r.status_code == 404:
                # if cannot find page
                pass
        
        # print(r.url)
        return r
    
    def get_summoner_by_name(self, name):
        #summoner API= returns id, accountId, puuid, name, profileIconId, revisionDate, summonerLevel
        api_url= Consts.URL['summoner_by_name'].format(
            version= Consts.API_VERSIONS['summoner_by_name'],
            names= name)
        return self._request(api_url)
    
    def get_matchHistory(self, account):
        #match history by accountID
        api_url= Consts.URL['match_by_account'].format(
            version= Consts.API_VERSIONS['match_by_account'],
            queue= Consts.QUEUES['SoloQ'],
            season= Consts.SEASONS['Season 2019'],
            accountID= account)
        return self._request(api_url)
    
    def get_league(self,queue):
        #ranked API by queue= returns ladder data
        api_url= Consts.URL['league_by_queue'].format(
            version= Consts.API_VERSIONS['league_by_queue'],
            queueType= queue)
        return self._request(api_url)
    
    def get_league_exp(self, **kwargs):
        #expiremental ranked API= returns ladder data (leagueId, summonerId, name, LP, wins, losses, etc)
        api_url= Consts.URL['league_exp'].format(
            version= Consts.API_VERSIONS['league_exp'],
            queue= kwargs['queue'],
            tier= kwargs['tier'],
            division= kwargs['division'],
            page= kwargs['page'])
        return self._request(api_url)