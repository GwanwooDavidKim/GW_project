import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# 폴더 선택 창 열기
Tk().withdraw()  # to hide the small tkinter window
file_path = askopenfilename(title='Select CSV File', filetypes=[('CSV Files', '*.csv')])

# 데이터 불러오기
df = pd.read_csv(file_path)

# 이동평균선 계산
def moving_average(df, window_size, column):
    ma = df[column].rolling(window=window_size).mean()
    return ma

# 단기 이동평균선 계산 (5일 이동평균선)
df['MA5'] = moving_average(df, 5, '종가')

# 장기 이동평균선 계산 (20일 이동평균선)
df['MA20'] = moving_average(df, 20, '종가')

# 매매 조건 계산
def buy_sell_signal(df):
    buy_signal = []
    sell_signal = []
    flag = -1

    for i in range(len(df)):
        if df['MA5'][i] > df['MA20'][i]:
            if flag != 1:
                buy_signal.append(df['종가'][i])
                sell_signal.append(None)
                flag = 1
            else:
                buy_signal.append(None)
                sell_signal.append(None)
        elif df['MA5'][i] < df['MA20'][i]:
            if flag != 0:
                buy_signal.append(None)
                sell_signal.append(df['종가'][i])
                flag = 0
            else:
                buy_signal.append(None)
                sell_signal.append(None)
        else:
            buy_signal.append(None)
            sell_signal.append(None)

    return buy_signal, sell_signal

# 매매 신호 계산
df['Buy'] = buy_sell_signal(df)[0]
df['Sell'] = buy_sell_signal(df)[1]

# 봉차트 데이터 생성
ohlc = df[['시가', '고가', '저가', '종가']]
ohlc.columns = ['Open', 'High', 'Low', 'Close']
ohlc.index = pd.to_datetime(df['날짜'])

# 차트 그리기
fig, axes = plt.subplots(nrows=2, sharex=True, figsize=(16, 10))

# 봉차트 색상 설정
mc = mpf.make_marketcolors(up='r', down='b')
s = mpf.make_mpf_style(marketcolors=mc)

# 봉차트 그리기
mpf.plot(ohlc, type='candle', ax=axes[0])

# 이동평균선 그리기
axes[0].plot(df['MA5'], label='MA5', color='orange')
axes[0].plot(df['MA20'], label='MA20', color='green')

# 매매 신호 표시
axes[0].scatter(df.index, df['Buy'], label='Buy', color='green', marker='^', alpha=1)
axes[0].scatter(df.index, df['Sell'], label='Sell', color='red', marker='v', alpha=1)

# 종가 그리기
axes[1].plot(df['종가'], label='Close Price', color='blue')

# 차트 설정
axes[0].set_title('Candlestick Chart with Moving Averages')
axes[0].legend(loc='upper left')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Price')

# 차트 출력
plt.show()
