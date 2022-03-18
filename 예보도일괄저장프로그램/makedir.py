import os
import time
import datetime
import pandas as pd

# 2020년 1월 1일 ~ 2020년 12월 31일까지 모든 날짜 폴더 생성
# 기간 만지고 싶은 경우, start = , end = 부분 조정 
datelist = pd.date_range(start = '20220101', end = '20220131')
datelist = datelist.strftime('%Y%m%d').tolist()
for date in datelist:
    os.makedirs('png/' + date, exist_ok = True)