import time
import pyupbit
import datetime
import pandas as pd
import numpy as np
import numpy
import requests

access = "xMHfyvYODFxy70JlgEa1NsF4tgoc1LLXcoAt3xXL"
secret = "h7KpRORRx9j2KyOSwyrUBwCXwrC9ixdUeWtgPo8o"
mytoken = "xoxb-2005003311860-1998840760514-fBjrdpKU5Zd9hjVXRGOuF0wB"
A="XRP"
A1="KRW-XRP"
B="EOS"
B1="KRW-EOS"
C="VET"
C1="KRW-VET"
D="XEM"
D1="KRW-XEM"
Z=[A,B,C,D]
X=[A1,B1,C1,D1]
i=1
buy_result20 = 0
buy_result09 = 0
qwe=0
asd=1
buy=0
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)




post_message(mytoken,"#qqq", "시작")

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_target_pric(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_pric = df.iloc[0]['close'] + (df.iloc[0]['low'] - df.iloc[0]['high']) * k
    return target_pric


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

# 자동매매 시작


while True:
    try:
        krw = get_balance("KRW")
        zxc = time.strftime('%H', time.localtime(time.time()))
        if krw > 5000.0:
            i+=1
        if i == 4:
            i=0
        if zxc != qwe:
            post_message(mytoken, "#qqq", "작동중")
            qwe=zxc

        now = datetime.datetime.now()
        start_time = get_start_time(X[i])
        end_time = start_time + datetime.timedelta(days=1)

        url = "https://api.upbit.com/v1/candles/minutes/5"

        querystring = {"market": X[i], "count": "100"}
        response = requests.request("GET", url, params=querystring)
        data = response.json()
        df = pd.DataFrame(data)
        df = df['trade_price'].iloc[::-1]
        print("3")

        if start_time < now < end_time - datetime.timedelta(seconds=30):
            target_price = get_target_price(X[i], 0.4)
            taraet_pric= get_target_pric(X[i], 0.45)


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
            current_price = get_current_price(X[i])
            print("4")

            if ((current_price > target_price) & (current_price > ma5) & (current_price > ma20))\
                    | ((current_price > target_price) & (current_price > band_high))\
                    | ((current_price < taraet_pric) & (current_price < ma5))\
                    | ((current_price < taraet_pric) & (current_price < ma20)):
                if krw > 5000.0:
                    buy_result = upbit.buy_market_order(X[i], krw)
                    #구매가
                    buy = current_price
                    asd=2
                    buy_result20 = buy * 1.03
                    buy_result09 = buy * 0.985

            else:
                btc1 = get_balance(Z[i])
                print("2")

                if (btc1 > 5.0) & (((current_price < ma5) & (current_price < ma20) & (current_price < band_low))\
                                   |(current_price > buy_result20)|(current_price < buy_result09)):
                    sell_result = upbit.sell_market_order(X[i], btc1)
                    asd=1

            time.sleep(1)
        else:
            btc = get_balance(Z[i])
            print("1")

            if (btc > 5.0) & (buy<current_price):
                sell_result = upbit.sell_market_order(X[i], btc)
                asd=1

        time.sleep(1)

    except Exception as e:
        print(e)
        post_message(mytoken, "#qqq", e)
        time.sleep(1)
