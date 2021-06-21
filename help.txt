python3 -m venv env

pip install requirements.txt
scrapy shell https://coinmarketcap.com/exchanges/kraken/

scrapy startproject squid
scrapy genspider kthulu coinmarketcap.com/exchanges/kraken/
