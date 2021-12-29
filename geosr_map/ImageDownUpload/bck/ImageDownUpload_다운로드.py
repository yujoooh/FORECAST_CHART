# 20191128 : hgchoe : To Download and Upload Marine Forecast Chart

import os
import shutil
import time
import datetime
import cx_Oracle
from selenium import webdriver

HOME_PATH = "D:\\geosr_2021map\\ImageDownUpload"
DOWNLOAD_PATH = "C:\\Users\\Administrator\\Downloads"
OBJECT_PATH = "D:\\geosr_2021map\\ImageDownUpload\\downloads"
CONID = "OCEAN_WEB"
CONPW = "infoshfl03"
CONINFO = "10.27.90.16:1521/mgis"

day0 =  datetime.datetime.now().strftime('%Y%m%d')

os.chdir(HOME_PATH)

# Download Loop function
def down_upload_loop(liType, liDate):
    # Location and Logging`
    os.chdir(OBJECT_PATH)
    flog = open('..\\logs\\'+day0+'.log', 'a', encoding='utf-8')
    # URL Information
    baseURL = 'http://localhost:8080/daily_ocean2021/'
    for regType in liType:
        for date in liDate:
            for hour in liDate[date]:
                for try_index in range(5): ### If some error occurs, Loop 5 times.
                    try: ### MAIN
                        # START LOGGING
                        tstr = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
                        flog.write(f"[{tstr} > {regType[3:].upper()}${date}${str(hour).zfill(2)}${regType+str(date)+str(hour).zfill(2)+'.png'}] 해황도 생성 시작!!\n")
                        # Remove PNG
                        try:
                            os.remove(os.path.join(DOWNLOAD_PATH, regType+'.png'))
                        except OSError:
                            pass                        
                        # WebDriver
                        url = baseURL + regType + '.html?date=' + str(date+1).zfill(2) + '&time=' + str(hour).zfill(2)
                        driver.get(url)
                        time.sleep(4)
                        driver.find_element_by_id('image_down').click()
                        time.sleep(3)
                        shutil.move(os.path.join(DOWNLOAD_PATH, regType+'.png'), os.path.join(OBJECT_PATH, regType+str(date)+str(hour).zfill(2)+'.png'))
                        with open(f"{regType+str(date)+str(hour).zfill(2)+'.png'}", 'rb') as img:
                            imgdata = img.read()
                    except Exception as ex: ### CHECK ERROR
                        print(ex)
                        # END LOGGING
                        tstr = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
                        flog.write(f"[{tstr} > {regType[3:].upper()}${date}${str(hour).zfill(2)}${regType+str(date)+str(hour).zfill(2)+'.png'}] 해황도 생성 완료!!\n")
                        continue ### GOTO next 'try_index'
                    # END LOGGING
                    tstr = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
                    flog.write(f"[{tstr} > {regType[3:].upper()}${date}${str(hour).zfill(2)}${regType+str(date)+str(hour).zfill(2)+'.png'}] 해황도 생성 완료!!\n")
                    break
    flog.close()

# Information of Selenium (Chrome)
drivernm = 'chromedriver'

# Chrome options
options = webdriver.ChromeOptions()
profile = {"download.default_directory": DOWNLOAD_PATH, "download.prompt_for_download": False, "download.directory_upgrade": True, "profile.default_content_setting_values.automatic_downloads": 1}
options.add_experimental_option("prefs", profile)

# Connection of WebDriver
driver = webdriver.Chrome(drivernm, options=options)
# Connection of Oracle
con = cx_Oracle.connect(CONID, CONPW, CONINFO)
cur = con.cursor()

# DB Connection Test
liType = ['do_temp']
liDate = { 0: [99] }
down_upload_loop(liType, liDate)

# Main Run
liType = [ 'do_korea', 'do_incheon', 'do_busan', 'do_sokcho', 'do_gunsan', \
           'do_mokpo', 'do_jeju', 'do_yeosu', 'do_tongyeong', 'do_pohang', \
           'do_taean', 'do_heuksando', 'do_wando', 'do_hupo', 'do_donghae', \
           'do_ulleungdo', 'do_baengnyeongdo', 'do_gyeokyeolbiyeoldo', 'do_yeonggwang', 'do_ieodo', \
           'do_koreaen' ]
liDate = { 0: [9,16], 1: [9,16], 2: [9,16], \
          3: [9], 4: [9], 5: [9], 6: [9] }

down_upload_loop(liType, liDate)

# Onbada Run
liType = [ 'do_onbada_bg', 'do_onbada_tw' ]
liDate = { 1: [9,16], 2:[9,16] }
down_upload_loop(liType, liDate)
liType = [ 'do_onbada_hi', 'do_onbada_lo' ]
liDate = { 1: [9], 2:[9] }
down_upload_loop(liType, liDate)

# Disconnection of WebDriver
driver.quit()
# Disconnection of Oracle
cur.close()
con.close()
