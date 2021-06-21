import scrapy
import json
import pymongo
from pymongo import MongoClient

import os 
import sys
import threading
import datetime
import logging

logging.basicConfig(filename = 'kthulu.log', level=logging.DEBUG)
class KthuluSpider(scrapy.Spider):

    name = 'kthulu_volume'
    allowed_domains = ['https://coinmarketcap.com/exchanges/kraken/']
    start_urls = ['https://coinmarketcap.com/exchanges/kraken/']

    def __init__(self):
        logging.info('Starting Kthulu v0.01' + str(datetime.datetime.now()))
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['exchange_information']
        self.now = datetime.datetime.today().replace(microsecond=0)

    def parse(self, response):
        threading.Timer(30, self.parse).start()
        coin_info = {}
        export_dict = {}
        coin_ranking_volume = response.xpath('//table/tbody/tr[@class="cmc-table-row"]')
        collection_kraken_volume_history = self.db['kraken_volume_history']

        try:
            for coin in coin_ranking_volume:
                rank = coin.xpath('//td[@class="cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__rank"]/div[@class=""]/text()').getall()
                pair = coin.xpath('//table/tbody/tr[@class="cmc-table-row"]/td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__market-pair"]/div[@class=""]/div[@class="hmd6df-0 kCRNNr"]/a/text()').getall()
                price = coin.xpath('//table/tbody/tr[@class="cmc-table-row"]/td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price"]/div[@class="price___3rj7O "]/text()').getall()
                volume_24hr = coin.xpath('//table/tbody/tr[@class="cmc-table-row"]/td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__volume-24-h"]/div[@class="cmc-table__column-market-pair-volume-24h"]/text()').getall()
                volume_percent = coin.xpath('//table/tbody/tr[@class="cmc-table-row"]/td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__calculated-market-pair-volume-percentage"]/div[@class="cmc-table__column-market-pair-volume-percent"]/text()').getall()
                volume_percent = volume_percent[::2]

            for i in range(20):
                coin_info.update({
                    "%s"%(rank[i]): {
                        "%s"%(pair[i]): {
                            "price": price[i],
                            "volume_24hr" : volume_24hr[i],
                            "volume_percent": volume_percent[i]
                        }
                    }
                })

            export_dict = {
                "Timestamp_%s"%(self.now) : {
                    "kraken_exchange_volume": coin_info
                }
            }
            collection_kraken_volume_history.insert_one(export_dict)
            
        except Exception as e:
            pass

