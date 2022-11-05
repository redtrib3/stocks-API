#!/usr/bin/python3

# uvicorn main:app --reload

from urllib.request import urlopen, Request     # urllib To request Html
from bs4 import BeautifulSoup                   # Bs4 to parse html
from fastapi import FastAPI



app = FastAPI(
        title="⚡ Real-time stocks/Crypto API 🗠",
        description="`GET real time stocks/Cryptocurrency info for a specific stock or a crpytocurrency`",
        version='0.0.1'
        )

def fetch_info(company):
    url = f"https://finance.yahoo.com/quote/{company}/"

    #headers cause we're scraping
    page = urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36"}))
    page = page.read().decode('utf-8')
    
    # The parser obj    
    soup = BeautifulSoup(page, "html.parser")


    try:
        co_title = soup.find_all('h1',{'class':'D(ib) Fz(18px)'})[0].string
        curr_price = soup.find_all('fin-streamer',{'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)'})
        curr_price = curr_price[0].string

        stata = soup.find_all('td',{'class':'Ta(end) Fw(600) Lh(14px)'})


        data = {
                "Company":co_title,
                "Current-Price":curr_price,
                "Net Assets":stata[8].string,
                "prevClose":stata[0].string,
                "openPrice":stata[1].string,
                "52 week-avg":stata[5].string
               }
    
        return data   
        
    except:
       return {"Error":f"abbreviation \'{company}\' NOT Found"} 
    
    
@app.get('/')
def index_page():
    return {"Description":"GET real time stock/crypto information using this API","documentation":"visit /docs"}
    
# stocks page

@app.get('/stock/{company}')
def stocks_data(company: str):
    
    # prevent crypto stuff from showing up in stocks stuff.
    if '-' in company:
        return {"Error":f"abbreviations \'{company}\' NOT Found. Check /docs for Usage."} 
    data = fetch_info(company)
    return data



@app.get('/crypto/{coin}')
def crypto_data(coin: str):
    
    #prevent stocks stuff from showing up in crypto stuff plus format is key.
    if '-' not in coin:
        return {"ERROR":'Wrong Input Format',"FORMAT":'/crypto/[coin]-[currency]',"Example":'/crypto/BTC-USD , /crypto/ETH-INR'}
    
    else:
        data1 = fetch_info(coin)
        return data1












