# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 18:22:08 2018

@author: k
"""
import sys    
import pandas as pd    


if len(sys.argv) != 3:
	print ("Usage: python 주식.py [stock_name] [page_range]")
	print ("you can get 10*[page_range] stock data")
	exit()
stock_name, page_range = sys.argv[1] , int(sys.argv[2])


code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]  #상장법인목록
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format) 
code_df = code_df[['회사명', '종목코드']]
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

#일별
def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code) 
    print("요청 URL = {}".format(url)) 
    return url # 신라젠의 일자데이터 url 가져오기 item_name='신라젠' url = get_url(item_name, code_df)

def Refine(url):
    df = pd.DataFrame()
    for page in range(1, page_range): #페이지별로 데이터 불러오기
        pg_url = '{url}&page={page}'.format(url=url, page=page) 
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
        df = df.dropna() #NA제거

    df = df.rename(columns= {'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'}) #이름 변경
    df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)#데이터 타입 변경
    df['date'] = pd.to_datetime(df['date'])  #데이터 타입 변경
    df = df.sort_values(by=['date'], ascending=True) #날짜 오름차순 정렬
    df['MA5'] = df.close.rolling(window=5).mean()    
    df['MA20'] = df.close.rolling(window=20).mean()
    df['MA60'] = df.close.rolling(window=60).mean()
    
    return df

#플롯
import matplotlib.pyplot as plt
import matplotlib.finance as matfin
import matplotlib.ticker as ticker    
df = Refine(get_url(stock_name,code_df))

day_list = range(len(df['date'])) #날짜 길이
name_list = [] #x축에 표시할 데이터 모음

#이동평균선
MA5=[]
MA20=[]
MA60=[]

for i in reversed(df.MA5):
    MA5.append(i)
for i in reversed(df.MA20):
    MA20.append(i)
for i in reversed(df.MA60):
    MA60.append(i)


#그리기
for day in df['date']:
    name_list.append(day.strftime("%d"))
    
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))
matfin.candlestick2_ohlc(ax, df['open'], df['high'], df['low'], df['close'], width=0.5, colorup='r', colordown='b')
plt.plot(MA5,'r')
plt.plot(MA20,'g')
plt.plot(MA60,'b')
plt.grid()
plt.show()



#일별데이터는 R-샤이니로   
"""
def Time_get_url(item_name, code_df,thistime=""):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    time_url = 'http://finance.naver.com/item/sise_time.nhn?code={code}'.format(code=code) + '&thistime={thistime}'.format(thistime=thistime)
    print("요청 URL = {}".format(time_url)) 
    return time_url # 신라젠의 일자데이터 url 가져오기 item_name='신라젠' url = get_url(item_name, code_df)

def Time_Refine():
    time_df = pd.DataFrame()
    for page in range(1, 30): #페이지별로 데이터 불러오기
        pg_url = '{url}&page={page}'.format(url=time_url, page=page) 
        time_df = time_df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
        time_df = time_df.dropna() #NA제거

    time_df = time_df.rename(columns= {'체결시각': 'time', '체결가': 'price', '전일비': 'diff', '매도': 'sell', '매수': 'buy', '거래량': 'volume', '변동량': 'offage'}) #이름 변경
    time_df[[ 'price', 'diff', 'sell', 'buy', 'volume','offage']] = time_df[[ 'price', 'diff', 'sell', 'buy', 'volume','offage']].astype(int)#데이터 타입 변경
    time_df['time'] = pd.to_datetime(time_df['time'])  #데이터 타입 변경
    time_df = time_df.sort_values(by=['time'], ascending=True) #날짜 오름차순 정렬
"""
"""

day_list = range(len(time_df['time'])) #날짜 길이
name_list = [] #x축에 표시할 데이터 모음

for day in time_df['time']:
    name_list.append(day.strftime("%d"))
    
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))

plt.plot(time_df['price'])



"""
