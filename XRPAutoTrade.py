import time
import pyupbit
import datetime
import numpy as np

access = "RIIiGAKxfIMfxyGzmGunXdpxDp1Dmolxrz6IErbx"
secret = "9ZSwV65ufwl7R7bDTOS63wKCEqZlGOc4BC2wEeK0"

def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-XRP")
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0032
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    
    return ror

def want(i=0):
    want_k=0
    arry=0
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(k)
        if ror>arry:
            arry=ror
            want_k=k

    return want_k 

def get_target_price(ticker, k):
   
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price




def get_start_time(ticker):
  
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
   
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):

    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
   
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
want_a=want(0)
print(want_a)

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-XRP")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-XRP", want_a)
            ma15 = get_ma15("KRW-XRP")
            current_price = get_current_price("KRW-XRP")
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-XRP", krw*0.9995)
        else:
            btc = get_balance("XRP")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-XRP", btc*0.9995-228)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
