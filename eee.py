import time
import pyupbit
import datetime
import pandas as pd
import numpy as np
import numpy
import requests


access = "xMHfyvYODFxy70JlgEa1NsF4tgoc1LLXcoAt3xXL"
secret = "h7KpRORRx9j2KyOSwyrUBwCXwrC9ixdUeWtgPo8o"
mytoken = "xoxb-2005003311860-1998347017317-NWGIXjFBViDuW91twCOlcIHe"

X=['KRW-REP','KRW-ADA','KRW-BCH','KRW-BTC','KRW-LINK','KRW-XRP','KRW-ETH','KRW-MTL','KRW-BSV','KRW-ETC','KRW-HUNT','KRW-MED']
Z=[]
for i in X:
    Y=i.replace("KRW-","")
    Z.append(Y)

i=0
buy_result20 = 0
buy_result09 = 0
buy_result10 = 0
qwe=0
buy=0
btc=0

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)




post_message(mytoken,"#qqq", "시작")

def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]

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



start_time = get_start_time(X[i])
end_time = start_time + datetime.timedelta(seconds=10)

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작


while True:
    try:
        krw = get_balance("KRW")
        zxc = time.strftime('%H', time.localtime(time.time()))
        now = datetime.datetime.now()
        rrr = get_start_time("KRW-BTC")
        end_rrr = rrr + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            X = ['KRW-REP','KRW-ADA','KRW-BCH','KRW-APIX','KRW-BTC','KRW-LINK','KRW-TMTG','KRW-XRP','KRW-ETH','KRW-MTL']

        if krw > 5000:
            i+=1
        if i == 12:
            i=0
        if zxc != qwe:
            post_message(mytoken, "#qqq", "작동중")
            qwe=zxc
        url = "https://api.upbit.com/v1/candles/minutes/5"
        querystring = {"market": X[i], "count": "100"}
        response = requests.request("GET", url, params=querystring)
        data = response.json()
        df = pd.DataFrame(data)
        df = df['trade_price'].iloc[::-1]
        if True!= (start_time < now < end_time):
            target_price = get_target_price(X[i], 0.35)
            target_pric = get_target_price(X[i], 0.9)

            #이동평균선
            ma5 = df.rolling(window=9).mean()
            ma20 = df.rolling(window=26).mean()
            current_price = get_current_price(X[i])
            ma5 = np.round(ma5.iloc[-1], 2)
            ma20 = np.round(ma20.iloc[-1], 2)
            ma1 = get_yesterday_ma5(X[i])

            print(X[i])
            print(current_price)
            print(target_price)
            print(target_pric)
            print(ma1 , ma5)
            print("----------------")


            if (target_price < current_price < target_pric) & (current_price > ma1) & (current_price > ma5):
                if krw > 5000.0:
                    buy_result = upbit.buy_market_order(X[i],krw*0.9995)
                    #구매가
                    buy = current_price
                    buy_result20 = buy * 1.02
                    buy_result09 = buy * 0.97
                    buy_result10 = buy * 1.01
                    start_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
                    end_time = datetime.datetime.now() + datetime.timedelta(minutes=30, seconds=10)
                    post_message(mytoken, "#qqq", X[i])
                    post_message(mytoken, "#qqq", "구매가 : "+str(current_price))
                    post_message(mytoken, "#qqq", "변동성 전략가격 : "+str(target_price))
                    post_message(mytoken, "#qqq", "변동성 전략제한가격 : "+str(target_pric))
                    post_message(mytoken, "#qqq", "5일 평균가격 : " +str(ma1))
                    post_message(mytoken, "#qqq", "5분봉 가격 : " +str(ma5))

                else:
                    btc = get_balance(Z[i])
                    if btc == None:
                        btc = 0

                    if (btc > 0.0005) & ((current_price > buy_result20) | (current_price < buy_result09)):
                        sell_result = upbit.sell_market_order(X[i], btc * 1.0)
                        if current_price < buy_result09:
                            del A[i]
            else:
                if btc == None:
                    btc = 0

                if (btc > 0.0005) & ((current_price > buy_result20)|(current_price < buy_result09)):
                    sell_result = upbit.sell_market_order(X[i], btc*1.0)
                    if current_price < buy_result09:
                        del A[i]

            time.sleep(1)
        else:
            btc = get_balance(Z[i])
            current_price = get_current_price(X[i])
            if btc == None:
                btc = 0
            if (btc > 0.0005) & (buy_result10<current_price):
                sell_result = upbit.sell_market_order(X[i], btc*1.0)
            else:
                start_time +=  datetime.timedelta(minutes=5)
                end_time += datetime.timedelta(minutes=5, seconds=10)

        time.sleep(1)

    except Exception as e:
        print(e)
        post_message(mytoken, "#qqq", e)
        time.sleep(1)
