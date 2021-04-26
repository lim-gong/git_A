import time
import pyupbit
import datetime

access = "xMHfyvYODFxy70JlgEa1NsF4tgoc1LLXcoAt3xXL"
secret = "h7KpRORRx9j2KyOSwyrUBwCXwrC9ixdUeWtgPo8o"
import requests


def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text}
                             )
    print(response)


myToken = "xoxb-2005003311860-1998840760514-gOLn9V1q9tsVcFsuCknktkod"

post_message(myToken, "#w", "jocoding")

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
post_message(myToken,"#crypto", "autotrade start")
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-DAWN")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=30):
            target_price = get_target_price("KRW-DAWN", 0.28)
            current_price = get_current_price("KRW-DAWN")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-DAWN", krw*0.9995)
                    post_message(myToken, "#w", " buy : " + str(buy_result))
        else:
            btc = get_balance("DAWN")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-DAWN", btc*0.9995)
                post_message(myToken, "#w", " buy : " + str(sell_result))
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken, "#w", e)
        time.sleep(1)