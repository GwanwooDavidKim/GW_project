import requests
import pandas as pd
from bs4 import BeautifulSoup
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os

## 크롤링할 종목 코드와 기간 설정
stock_code = input("종목 코드를 입력하세요: ")
start_date = input("시작일을 입력하세요(예: 2023.01.01): ")
end_date = input("종료일을 입력하세요(예: 2023.12.31): ")

# 폴더 선택 창 열기
#Tk().withdraw()  # to hide the small tkinter window
#save_folder = askdirectory(title='Select Folder')  # shows folder selection dialog and returns the path

# 수집할 데이터를 저장할 리스트 생성
stock_data = []

# 페이지별로 크롤링
for page in range(1, 100):
    # URL 설정
    url = f'https://finance.naver.com/item/sise_day.nhn?code={stock_code}&page={page}'
    
    # HTML 소스 가져오기
    res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.content, 'html.parser')
    
    # 마지막 페이지 번호 가져오기
    try:
        last_page = soup.select_one('td.pgRR > a').get('href').split('=')[-1]
    except AttributeError:
        last_page = 1
    
    # 데이터 추출
    rows = soup.select('table.type2 tr')
    
    for row in rows:
        if len(row.select('td')) == 7:
            date = row.select('td')[0].text.strip()
            if start_date <= date <= end_date:
                closing_price = row.select('td')[1].text.strip().replace(',', '')
                opening_price = row.select('td')[3].text.strip().replace(',', '')
                high_price = row.select('td')[4].text.strip().replace(',', '')
                low_price = row.select('td')[5].text.strip().replace(',', '')
                volume = row.select('td')[6].text.strip().replace(',', '')
                stock_data.append([date, closing_price, opening_price, high_price, low_price, volume])
    
    # 마지막 페이지까지 수집 완료 시 종료
    if page == int(last_page):
        break

# 데이터프레임 생성
df = pd.DataFrame(stock_data, columns=['날짜', '종가', '시가', '고가', '저가', '거래량'])

# 파일 경로 생성
#file_path = os.path.join(save_folder, f'주식데이터({stock_code}) {start_date}-{end_date}.csv')
save_folder = "C:\\Users\\pc\\Desktop\\Stock\\"
file_path = os.path.join(save_folder, f'주식데이터({stock_code}) {start_date}-{end_date}.csv')

# 엑셀 파일로 저장
df.to_csv(file_path, index=False, encoding='utf-8-sig')

print(f'데이터가 성공적으로 저장되었습니다. 파일 경로: {file_path}')
print(file_path)
