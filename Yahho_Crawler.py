import yfinance as yf
import pandas as pd
import os

# 사용자 입력 받기
symbol = input("종목 기호를 입력하세요 (예: AAPL): ")
start_date = input("시작일을 입력하세요 (예: 2020-01-01): ")
end_date = input("종료일을 입력하세요 (예: 2021-01-01): ")

# 입력하지 않은 항목은 기본값으로 설정
if not symbol:
    symbol = "AAPL"
if not start_date:
    start_date = "2010-01-01"
if not end_date:
    end_date = "2023-04-26"

# Yahoo Finance에서 데이터 가져오기
stock_data = yf.download(symbol, start=start_date, end=end_date)

# 데이터프레임 열 이름 변경
stock_data = stock_data.rename(columns={'Open': '시가', 'High': '고가', 'Low': '저가', 'Close': '종가', 'Volume': '거래량', 'Adj Close': '수정종가'})
stock_data.index.name = '날짜'

# 파일 이름 생성
filename = f'{symbol}({start_date.replace("-", "")}-{end_date.replace("-", "")}).csv'

# 파일 경로 생성
save_folder = "C:\\Users\\pc\\Desktop\\Stock\\"
file_path = os.path.join(save_folder, filename)

# CSV 파일로 저장
stock_data[['종가', '시가', '고가', '저가', '거래량', '수정종가']].to_csv(file_path, index=True, encoding='utf-8-sig')

print(f'데이터가 성공적으로 저장되었습니다. 파일 경로: {file_path}')
