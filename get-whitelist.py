from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time
from operator import mul
from itertools import starmap

#SKnight20210307
def generateWhiteListHighestVolume(exchange, stake_currency):
    #generateWhiteList with highest volume in past 24hrs - nonTradeAblePairs
    exchange_data = requests.get(f'https://coinmarketcap.com/exchanges/%s/'%(exchange))
    soup = BeautifulSoup(exchange_data.content, 'html.parser')
    # sort_keys, indent are optional and used for pretty-write
    #print(soup.prettify)

    data = soup.find('script', id="__NEXT_DATA__",type="application/json")
    
    
    pairs = {}
    coins = {}
    rank = {}
    volume = {}
    pair_data = json.loads(data.contents[0])
    if(exchange == 'kraken'):
         top_volume = pair_data['props']['initialState']['exchange']['marketPairsLatest']['data']['24']['active']['data']['market_pairs']
         market_pair = []
         volume_two4hr = []
         temp = []
         vol = []
         whitelist =[]
         count_binance =1
         count_vol_binance = 0
         for i in top_volume:
             z = volume[str(i['rank'])]=i['market_pair'],i['calculated_market_pair_volume_percentage'],count_binance
             market_pair.append(z)
             count_binance +=1
         for vol in market_pair:
             temp.append(vol[1])

         #declaring1Whole
         cum_volume_percent_total_market = sum(starmap(mul, enumerate(temp)))

         for dataList in market_pair:
             cum_volume_percent_stake_currency = ((temp[count_vol_binance]/cum_volume_percent_total_market)*10)
             #STOREDocument
             if('%s/'%(stake_currency) in dataList[0]):
                print("Rank: "+str(dataList[2])+" : " + dataList[0] +" : "+ " Volume(Entire Exchange): "+str(dataList[1]/100)+ " Volume(Stake_currency): "+str(cum_volume_percent_stake_currency))
                whitelist.append('"'+dataList[0]+'"'+',')
                count_vol_binance +=1
             elif('/%s'%(stake_currency) in dataList[0]):
                print("Rank: "+str(dataList[2])+" : " + dataList[0] +" : "+ " Volume(Entire Exchange): "+str(dataList[1]/100)+ " Volume(Stake_currency): "+str(cum_volume_percent_stake_currency))
                whitelist.append('"'+dataList[0]+'"'+',')
         for i in range(len(whitelist)):
             print(whitelist[i])

    elif(exchange == 'binance'):
         top_volume = pair_data['props']['initialState']['exchange']['marketPairsLatest']['data']['270']['active']['data']['market_pairs']
         market_pair = []
         volume_two4hr = []
         temp = []
         vol = []
         whitelist =[]
         count_binance =1
         count_vol_binance = 0
         for i in top_volume:
             z = volume[str(i['rank'])]=i['market_pair'],i['calculated_market_pair_volume_percentage'],count_binance
             market_pair.append(z)
             count_binance +=1
         for vol in market_pair:
             temp.append(vol[1])

         #declaring1Whole
         cum_volume_percent_total_market = sum(starmap(mul, enumerate(temp)))

         for dataList in market_pair:
             cum_volume_percent_stake_currency = ((temp[count_vol_binance]/cum_volume_percent_total_market)*10)
             #STOREDocument
             if('%s/'%(stake_currency) in dataList[0]):
                print("Rank: "+str(dataList[2])+" : " + dataList[0] +" : "+ " Volume(Entire Exchange): "+str(dataList[1]/100)+ " Volume(Stake_currency): "+str(cum_volume_percent_stake_currency))
                whitelist.append('"'+dataList[0]+'"'+',')
                count_vol_binance +=1
             elif('/%s'%(stake_currency) in dataList[0]):
                print("Rank: "+str(dataList[2])+" : " + dataList[0] +" : "+ " Volume(Entire Exchange): "+str(dataList[1]/100)+ " Volume(Stake_currency): "+str(cum_volume_percent_stake_currency))
                whitelist.append('"'+dataList[0]+'"'+',')
         for i in range(len(whitelist)):
             print(whitelist[i])

def cleanBinance(pairs):
     pairs.remove('"USDC/BTC",'),
     pairs.remove('"CRO/BTC",'),
     pairs.remove('"MIOTA/BTC",'),
     pairs.remove('"BUSD/BTC",')
     return pairs

def generateWhiteListTop100(exchange, stake_currency):
    #Returns top 100 - nonAvailable pairs
    cmc = requests.get('https://coinmarketcap.com/exchanges/binance/')
    soup = BeautifulSoup(cmc.content, 'html.parser')
    print(soup.prettify)

    data = soup.find('script', id="__NEXT_DATA__",type="application/json")
    coins = {}

    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listings:
        coins[str(i['id'])] = i['slug']
    market_cap = []
    volume = []
    timestamp = []
    name = []
    symbol = []
    slug = []
    temp = []
    for j in listings:
        symbol.append(j['symbol'])

    for ticker in symbol:
        temp.append('"'+"%s/%s"%(ticker, stake_currency)+'"'+',')

    if(exchange == 'binance'):
        temp.remove('"USDT/BTC",'),
        temp.remove('"USDC/BTC",'),
        temp.remove('"CRO/BTC",'),
        temp.remove('"MIOTA/BTC",'),
        temp.remove('"BUSD/BTC",'),
        return temp
    elif(exchange == 'kraken'):
        #insert incompatible pairs here
        return temp

#generateWhiteListTop100('binance', 'BTC')
generateWhiteListHighestVolume('binance', 'BTC')
