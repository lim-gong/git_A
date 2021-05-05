import time
import pyupbit
import datetime
import pandas as pd
import numpy as np
import numpy
import requests


access = "xMHfyvYODFxy70JlgEa1NsF4tgoc1LLXcoAt3xXL"
secret = "h7KpRORRx9j2KyOSwyrUBwCXwrC9ixdUeWtgPo8o"
mytoken = "xoxb-2005003311860-1998347017317-DSJlvjkGX7jCycJLEIjRErzU"

X=['KRW-MTL', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-KMD', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-EMC2', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-IGNIS', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-LOOM', 'KRW-ADX', 'KRW-BAT', 'KRW-IOST', 'KRW-DMT', 'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-THETA', 'KRW-EDR', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-SOLVE', 'KRW-MBL', 'KRW-TSHP', 'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-PXL', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-LAMB', 'KRW-HUNT', 'KRW-MARO', 'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-PCI', 'KRW-STRAX', 'KRW-AQT', 'KRW-BCHA', 'KRW-GLM', 'KRW-QTCON', 'KRW-SSX', 'KRW-META', 'KRW-OBSR', 'KRW-FCT2', 'KRW-LBC', 'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE', 'KRW-STRK', 'KRW-PUNDIX', 'KRW-FLOW', 'KRW-DAWN', 'KRW-AXS', 'KRW-STX']
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
        if krw < 5000:
            i+=1
        if i == 111:
            i=0
        if zxc != qwe:
            post_message(mytoken, "#qqq", "작동중")
            qwe=zxc
        url = "https://api.upbit.com/v1/candles/minutes/5"
        now = datetime.datetime.now()
        querystring = {"market": X[i], "count": "100"}
        response = requests.request("GET", url, params=querystring)
        data = response.json()
        df = pd.DataFrame(data)
        df = df['trade_price'].iloc[::-1]
        if True!= (start_time < now < end_time):
            target_price = get_target_price(X[i], 0.35)
            target_pric = get_target_price(X[i], 0.5)

            #이동평균선
            ma5 = df.rolling(window=9).mean()
            ma20 = df.rolling(window=26).mean()
            #볼린저밴드
            unit = 2
            band1 = unit * numpy.std(df[len(df) - 20:len(df)])
            bb_center = numpy.mean(df[len(df) - 20:len(df)])
            band_high = bb_center + band1
            band_low = bb_center - band1
            band_high = np.round(band_high,1)
            band_low = np.round(band_low,1)
            current_price = get_current_price(X[i])
            ma5 = np.round(ma5.iloc[-1], 2)
            ma20 = np.round(ma20.iloc[-1], 2)
            ma1 = get_yesterday_ma5(X[i])


            if ((current_price > target_price) & (current_price < target_pric) & (current_price > ma1) &(current_price > ma5)) & (1000.0 < current_price < 45000.0):
                if krw > 5000.0:
                    buy_result = upbit.buy_market_order(X[i],krw*0.9995)
                    #구매가
                    buy = current_price
                    buy_result20 = buy * 1.025
                    buy_result09 = buy * 0.9
                    buy_result10 = buy * 1.01
                    start_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
                    end_time = datetime.datetime.now() + datetime.timedelta(minutes=30, seconds=10)

                else:
                    btc = get_balance(Z[i])
                    if btc == None:
                        btc = 0

                    if (btc > 0.5) & (((current_price < ma5) & (current_price < ma20) & (current_price < band_low)) \
                                      | (current_price > buy_result20) | (current_price < buy_result09)):
                        sell_result = upbit.sell_market_order(X[i], btc * 1.0)
            else:
                if btc == None:
                    btc = 0

                if (btc > 0.5) & (((current_price < ma5) & (current_price < ma20) & (current_price < band_low))\
                                   |(current_price > buy_result20)|(current_price < buy_result09)):
                    sell_result = upbit.sell_market_order(X[i], btc*1.0)

            time.sleep(1)
        else:
            btc = get_balance(Z[i])
            current_price = get_current_price(X[i])
            if btc == None:
                btc = 0
            if (btc > 0.5) & (buy_result10<current_price):
                sell_result = upbit.sell_market_order(X[i], btc*1.0)
            else:
                start_time +=  datetime.timedelta(minutes=10)
                end_time += datetime.timedelta(minutes=10, seconds=10)

        time.sleep(1)

    except Exception as e:
        print(e)
        post_message(mytoken, "#qqq", e)
        time.sleep(1)
