import time
import pyupbit
import datetime
import pandas as pd
import numpy as np
import numpy
import requests

access = "xMHfyvYODFxy70JlgEa1NsF4tgoc1LLXcoAt3xXL"
secret = "h7KpRORRx9j2KyOSwyrUBwCXwrC9ixdUeWtgPo8o"
myToken = "xoxb-2005003311860-1998347017317-FAezi2ZWJhopifatXMP6k5LJ"


def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)




post_message(myToken,"#qqq", "시작")

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]



# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
post_message(myToken,"#qqq", "autotrade start")
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-VET")
        end_time = start_time + datetime.timedelta(days=1)

        url = "https://api.upbit.com/v1/candles/minutes/5"

        querystring = {"market": "KRW-VET", "count": "100"}
        response = requests.request("GET", url, params=querystring)
        data = response.json()
        df = pd.DataFrame(data)
        df = df['trade_price'].iloc[::-1]

        querystring1 = {"market": "KRW-VET", "count": "100"}
        response1 = requests.request("GET", url, params=querystring)
        data1 = response.json()
        df1 = pd.DataFrame(data)
        df1 = df1['trade_price'].iloc[::-1]

        if start_time < now < end_time - datetime.timedelta(seconds=30):
            target_price = get_target_price("KRW-VET", 0.2)
            #이동평균선
            ma5 = df.rolling(window=5).mean()
            ma20 = df.rolling(window=20).mean()

            #볼린저밴드
            unit = 2
            band1 = unit * numpy.std(df[len(df) - 20:len(df)])
            bb_center = numpy.mean(df[len(df) - 20:len(df)])
            band_high = bb_center + band1
            band_low = bb_center - band1
            ma5 = np.round(ma5.iloc[-1], 1)
            ma20 = np.round(ma20.iloc[-1], 1)
            band_high = np.round(band_high,1)
            band_low = np.round(band_low,1)
            current_price = get_current_price("KRW-VET")

            if ((current_price > target_price) & (current_price > ma5) & (current_price > ma20))\
                    | ((current_price > target_price) & (current_price > ma5) & (current_price > band_high))\
                    | ((current_price > target_price) & (current_price > ma20) & (current_price > band_high)):
                krw = get_balance("KRW")
                if krw > 5000:
                    buy_result = upbit.buy_market_order("KRW-VET", krw*0.9995)
                    post_message(myToken, "#qqq", " 구매 : " + str(buy_result))
            else:
                btc1 = get_balance("VET")


                if (btc1 > 25.0) & (((current_price < ma5) & (current_price < band_low))\
                        |((current_price < ma20) & (current_price < band_low))):
                    sell_result = upbit.sell_market_order("KRW-VET", btc1 * 0.9995)
                    post_message(myToken, "#qqq", " 판매 : " + str(sell_result))
            time.sleep(1)
        else:
            btc = get_balance("VET")

            if btc > 25.0:
                sell_result = upbit.sell_market_order("KRW-VET", btc*0.9995)
                post_message(myToken, "#qqq", " 판매 : " + str(sell_result))
        time.sleep(1)

    except Exception as e:
        print(e)
        post_message(myToken, "#qqq", e)
        time.sleep(1)