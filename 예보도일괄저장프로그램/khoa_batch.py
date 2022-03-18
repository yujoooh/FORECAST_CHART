import os
import shutil
import time
import datetime
from selenium import webdriver
import pandas as pd

#원하는 기간 조정
datelist = pd.date_range(start = '20220101', end = '20220131')
datelist = datelist.strftime('%Y%m%d').tolist()


drivernm = 'chromedriver'

#지역 원하는 지역 추가하면됨
liType = ['KOREA', 'POHANG']

#당일, 내일, 모레 도면, 필요시 조정
liDate = [ 0 ] # [+0day, +1day, +2day]

#09시, 16시 도면
liHour = ['09', '16']

# Connection of WebDriver
driver = webdriver.Chrome(drivernm)

#fpath 경로 각자 환경에 맞게 수정
fpath = 'C:/Users/geosr_fcstidx/Downloads/예보도일괄저장프로그램/png'
baseURL = 'http://www.khoa.go.kr/khoa/lifeforecast/seaCondImageDown.do?'
for date in datelist:
    for regType in liType:
        for delta in liDate:
            for hour in liHour:
                url = baseURL + 'type=' + regType + '&forecastDay=' + date + '&forecastHour=' + hour
                print(url)        # PRINT URL
                driver.get(url)   # To Get MFC
                filenm  = 'do_' + regType.lower() +  '_' +date + '_' +hour + '.png'
                #orgfile = os.path.join(os.environ['USERPROFILE'],'Downloads',filenm)
                time.sleep(2) # Time Interval
                #print(orgfile)    # PRINT Filename
                shutil.move('C:/Users/geosr_fcstidx/Downloads/'+filenm, fpath+'/' + date +'/'+ filenm)
                #shutil.move(orgfile, fpath + date)
driver.quit()                