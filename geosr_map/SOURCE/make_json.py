#-*- coding: utf-8 -*-
# TO MAKE INPUT FILE FOR MFC(Marine Forecast Chart)
# 20190811 HGChoe
# 20190922 HGChoe For Typhoon
# 20191014 HGChoe For 16 types
# 20201015 HGChoe For S111 and 7days

from netCDF4 import Dataset
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
import sys
import os

### SET VARIABLE NAME
## GET ARGUMENTS
yyyymmdd = str(sys.argv[1])
shortDay = 2
## LIST FOR MAIN LOOP
liFcstdate = [ 0, 1, 2, 3, 4, 5, 6 ]
#liFcstdate = [ 0, 1, 2] # 7 days forecast
liTimestep = [ 9, 16 ] # KST 09. 16
liAreaname = [ 'kor', 'inc', 'bus', 'sok', 'gun', \
               'mok', 'jej', 'yeo', 'ton', 'poh', \
               'tae', 'heu', 'wan', 'hup', 'don', \
               'ull', 'bae', 'gye', 'yeg', 'ieo', \
               'koren', 'onb' ]

#ppark new area range test
#liAreaname = [ 'wan', 'gye', 'yeg' ,'mok', 'heu' ]

# Model File Name
filenmYES3K = "YES3K_"+yyyymmdd+"00.nc"
filenmCWW3  =  "CWW3_"+yyyymmdd+"00.nc"
filenmRWW3  =  "RWW3_"+yyyymmdd+"00.nc"
filenmWW3   =   "WW3_"+yyyymmdd+"00.nc"
filenmWRF   =   "WRF_"+yyyymmdd+".nc"
# Area Name for LonLat
arealarge = {'kor':'KOREA', 'inc':'INCHEON', 'bus':'BUSAN', 'sok':'SOKCHO', 'gun':'GUNSAN', \
             'mok':'MOKPO', 'jej':'JEJU', 'yeo':'YEOSU', 'ton':'TONGYEONG', 'poh':'POHANG', \
             'tae':'TAEAN', 'heu':'HEUKSANDO', 'wan':'WANDO', 'hup':'HUPO', 'don':'DONGHAE', \
             'ull':'ULLEUNGDO', 'bae':'BAENGNYEONGDO', 'gye':'GYEOKYEOLBIYEOLDO', 'yeg':'YEONGGWANG', 'ieo':'IEODO', \
             'koren':'KOREAEN', 'onb':'ONBADA'}
# Area Name for Date
areakorea = {'kor':'인천', 'inc':'인천', 'bus':'부산', 'sok':'속초', 'gun':'군산', \
             'mok':'목포', 'jej':'제주', 'yeo':'여수', 'ton':'통영', 'poh':'포항', \
             'tae':'태안', 'heu':'흑산도', 'wan':'완도', 'hup':'울진', 'don':'동해', \
             'ull':'울릉도', 'bae':'인천', 'gye':'태안', 'yeg':'영광', 'ieo':'제주', \
             'koren':'인천', 'onb':'인천'}

# Area Name for English
areaenglish = {
    '속초'     : 'Sokcho',     \
    '포항'     : 'Pohang',     \
    '울산'     : 'Ulsan',      \
    '부산'     : 'Busan',      \
    '거제도'   : 'Geojedo',    \
    '제주'     : 'Jeju',       \
    '여수'     : 'Yeosu',      \
    '진도'     : 'Jindo',      \
    '목포'     : 'Mokpo',      \
    '군산'     : 'Gunsan',     \
    '안흥'     : 'Anheung',    \
    '인천'     : 'Incheon',    \
    '안산'     : 'Ansan',      \
    '평택'     : 'Pyeongtaek', \
    '대산'     : 'Daesan',     \
    '보령'     : 'Boryeong',   \
    '어청도'   : 'Eocheongdo', \
    '장항'     : 'Janghang',   \
    '위도'     : 'Wido',       \
    '영광'     : 'Yeonggwang', \
    '흑산도'   : 'Heuksando',  \
    '완도'     : 'Wando',      \
    '거문도'   : 'Geomundo',   \
    '고흥발포' : 'Goheung',    \
    '통영'     : 'Tongyeong',  \
    '마산'     : 'Masan',      \
    '서귀포'   : 'Seogwipo',   \
    '성산포'   : 'Seongsanpo', \
    '모슬포'   : 'Moseulpo',   \
    '추자도'   : 'Chujado',    \
    '후포'     : 'Hupo',       \
    '묵호'     : 'Mukho',      \
    '울릉도'   : 'Ulleungdo',  \
    '강릉'     : 'Gangneung',  \
    '울진'     : 'Uljin'       
}

# Calendar for English
calendarEn = {  1:'Jan.',  2:'Feb.',  3:'Mar.',  4:'Apr.',  5:'May.',  6:'Jun.', \
                7:'Jul.',  8:'Aug.',  9:'Sep.', 10:'Oct.', 11:'Nov.', 12:'Dec.'  }

# DirtoInt
dirtoint = {'N':  0, 'NNE': 23, 'NE': 45, 'ENE': 68, 'E': 90, 'ESE':113, 'SE':135, 'SSE':158, \
            'S':180, 'SSW':203, 'SW':225, 'WSW':248, 'W':270, 'WNW':293, 'NW':315, 'NNW':338}

### LOAD YES3K NC FILE
ncYES3K = Dataset(filenmYES3K)
print('YES3K Loaded')
# LOAD WAVE NC FILE
ncWW3 = Dataset(filenmWW3)
print('WW3 Loaded')
try:
    ncWAVE = Dataset(filenmCWW3)
    stWAVE = 'CWW3'
except:
    try:
        ncWAVE = Dataset(filenmRWW3)
        stWAVE = 'RWW3'
    except:
        ncWAVE = Dataset(filenmWW3)
        stWAVE = 'WW3'
print('0~2days WAVE: '+stWAVE)
# LOAD WRF NC FILE
ncWRF = Dataset(filenmWRF)
print('WRF Loaded')


### MAIN LOOP
for areaname in liAreaname:
    for fcstdate in liFcstdate:
        for timestep in liTimestep:
            # Model Timestep
            khoastep =        (timestep-9) + fcstdate * 24
             # KST today 09:00 -  0 timestep - 00:00 UTC
             # KST today 10:00 -  1 timestep - 01:00 UTC
            kmastep  = int((timestep-9)/3) + fcstdate *  8
             # KST today 09:00 -  0 timestep - 00:00 UTC
             # KST today 12:00 -  1 timestep - 03:00 UTC
            
            # Chart Date
            chartdate = (datetime.strptime(yyyymmdd, '%Y%m%d') + timedelta(days=fcstdate)).strftime('%Y%m%d')
            # Chart Time
            charttime = timestep

            # CHECK JSON
            objDir = os.path.join('RESULT', 'data_'+arealarge[areaname].lower(), str(fcstdate+1).zfill(2), str(timestep).zfill(2))
            if not os.path.exists(objDir):
                os.makedirs(objDir)
            if os.path.exists(os.path.join(objDir, "on_map.json")):
                os.remove(os.path.join(objDir, "on_map.json"))
            if os.path.exists(os.path.join(objDir, "chart_radar.json")):
                os.remove(os.path.join(objDir, "chart_radar.json"))

            ### MAIN
            on_map_json = dict()
            chart_radar_json = dict()

            ## BASE_MAP
            df_base = pd.read_csv('INPUT/on_map_base.inp', sep='\\s+', encoding='UTF-8', index_col=0)
            base_map = dict()
            base_map["MAP_URL"] = "temp.png"
            base_map["MAP_BOUNDARY_TL_LAT"] = df_base['LAT1'][arealarge[areaname]]
            base_map["MAP_BOUNDARY_TL_LNG"] = df_base['LON0'][arealarge[areaname]]
            base_map["MAP_BOUNDARY_BR_LAT"] = df_base['LAT0'][arealarge[areaname]]
            base_map["MAP_BOUNDARY_BR_LNG"] = df_base['LON1'][arealarge[areaname]]

            on_map_json["BASE_MAP"] = [base_map]

            ## TODAY_DATE
            df_date = pd.read_csv('INPUT/04_SunNMoon/'+areakorea[areaname]+'.txt', sep='\\s+', header=None, encoding='UTF-8', index_col=0, engine="python")
            df_date.columns = ['Lunar', 'S1', 'S2', 'S3', 'M1', 'M2', 'M3', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6']
            df_date.index.name = 'DATE'
            yyyy  = int(chartdate[0:4])
            sm    = int(chartdate[4:6])
            sd    = int(chartdate[6:8])
            lunar = df_date['Lunar'][int(chartdate)]
            lm    = int(lunar[0:2])
            ld    = int(lunar[3:5])
            if sm >= lm:
                lyyyy = yyyy
            else:
                lyyyy = yyyy-1
            today_date = dict()
            if areaname == 'koren':
                today_date["DATE"] = str(sd) + ' ' + calendarEn[sm] + ' ' + str(yyyy)
                today_date["TIME"] = str(charttime-9).zfill(2) + ":00 UTC"
                today_date["LUNAR_DATE"] = "Lunar date " + str(ld) + ' ' + calendarEn[lm] + ' ' + str(lyyyy)
            else:
                today_date["DATE"] = str(yyyy) + "년 " + str(sm) + "월 " + str(sd) + "일" 
                today_date["TIME"] = str(charttime) + "시"
                today_date["LUNAR_DATE"] = "음력 " + str(lm) + "월 " + str(ld) + "일"
            on_map_json["TODAY_DATE"] = today_date

            ## SUNnMOON TIME
            chart_legend = dict()
            chart_legend["SUN_TIME_01"]  = df_date['S1'][int(chartdate)][0:5]
            chart_legend["SUN_TIME_02"]  = df_date['S2'][int(chartdate)][0:5]
            chart_legend["SUN_TIME_03"]  = df_date['S3'][int(chartdate)][0:5]
            chart_legend["MOON_TIME_01"] = df_date['M1'][int(chartdate)][0:5]
            chart_legend["MOON_TIME_02"] = df_date['M2'][int(chartdate)][0:5]
            chart_legend["MOON_TIME_03"] = df_date['M3'][int(chartdate)][0:5]
            chart_legend["MOON_STEP"] = str(ld)
            chart_radar_json["CHART_LEGEND"] = chart_legend

            ## WTWH
            water_temp_wave_height = []
            try:
                df_wtwh = pd.read_csv('INPUT/INP_ONMAP_WTWH/on_map_wtwh_'+areaname+'.inp', sep='\\s+', header=None, encoding='UTF-8', index_col=0)
                df_wtwh.columns = ['LAT', 'LON', 'YES3K_LAT', 'YES3K_LON', 'CWW3_AREA', 'CWW3_LAT', 'CWW3_LON', 'RWW3_LAT', 'RWW3_LON', 'WW3_LAT', 'WW3_LON', 'WRF_LAT', 'WRF_LON']
                df_wtwh.index.name = 'ID'

                for wtwh_id in df_wtwh.index:
                    wtwh_comp = dict()
                    wtwh_comp["ID"] = wtwh_id
                    wtwh_comp["LAT"] = df_wtwh['LAT'][wtwh_id]
                    wtwh_comp["LON"] = df_wtwh['LON'][wtwh_id]
                    if fcstdate > shortDay: # FOR MIDDLE FORECAST
                        wtwh_comp[ "WATER_TEMP"] = f"{ncYES3K.variables['temp'][khoastep-9:khoastep+15,df_wtwh.YES3K_LAT[wtwh_id],df_wtwh.YES3K_LON[wtwh_id]].mean(axis=0):.1f}"
                        wtwh_comp["WAVE_HEIGHT"] = f"{max(ncWW3.variables['Hsig'][khoastep-9:khoastep+15,df_wtwh.WW3_LAT[wtwh_id],df_wtwh.WW3_LON[wtwh_id]].max(axis=0), 0.1):.1f}"
                        wvelU = ncWRF.variables['Uwind'][khoastep-9:khoastep+15,df_wtwh.WRF_LAT[wtwh_id],df_wtwh.WRF_LON[wtwh_id]]
                        wvelV = ncWRF.variables['Vwind'][khoastep-9:khoastep+15,df_wtwh.WRF_LAT[wtwh_id],df_wtwh.WRF_LON[wtwh_id]]
                        wvel  = (wvelU**2 + wvelV**2)**0.5
                        ## 풍속이 최대일때의 U,V 성분 추출 --> 최대 풍속일때의 풍향 표시    
                        wdeg = np.rad2deg(np.arctan2(wvelV[np.argmax(wvel)],wvelU[np.argmax(wvel)]))
                        wdeg = np.array(wdeg)
                        wdeg[wdeg<0]+= 360
                        #print(wdeg)
                        ## 최대풍속 산출
                        wvel = wvel[np.argmax(wvel)]
                    else:
                        wtwh_comp["WATER_TEMP"] = f"{ncYES3K.variables['temp'][khoastep,df_wtwh.YES3K_LAT[wtwh_id],df_wtwh.YES3K_LON[wtwh_id]]:.1f}"
                        if   stWAVE == 'CWW3':
                            wtwh_comp["WAVE_HEIGHT"] = f"{max(ncWAVE.variables['hsig'+df_wtwh.CWW3_AREA[wtwh_id]][kmastep,df_wtwh.CWW3_LAT[wtwh_id],df_wtwh.CWW3_LON[wtwh_id]], 0.1):.1f}"
                        elif stWAVE == 'RWW3':
                            wtwh_comp["WAVE_HEIGHT"] = f"{max(ncWAVE.variables['hsig1_dajn'][kmastep,df_wtwh.RWW3_LAT[wtwh_id],df_wtwh.RWW3_LON[wtwh_id]], 0.1):.1f}"
                        else:
                            wtwh_comp["WAVE_HEIGHT"] = f"{max(ncWAVE.variables['Hsig'][khoastep,df_wtwh.WW3_LAT[wtwh_id],df_wtwh.WW3_LON[wtwh_id]], 0.1):.1f}"
                        #print('hgchoe2')
                        wvelU = ncWRF.variables['Uwind'][khoastep,df_wtwh.WRF_LAT[wtwh_id],df_wtwh.WRF_LON[wtwh_id]]
                        wvelV = ncWRF.variables['Vwind'][khoastep,df_wtwh.WRF_LAT[wtwh_id],df_wtwh.WRF_LON[wtwh_id]]
                        wvel  = (wvelU**2 + wvelV**2)**0.5
                        wdeg = np.rad2deg(np.arctan2(wvelV,wvelU))
                        wdeg[wdeg<0]+= 360
                        #print('hgchoe3')
                    wtwh_comp["WIND"] = f"{max(wvel, 1.0):2.0f}"
                    wtwh_comp["WIND_DIR"] = f"{wdeg :2.0f}"
                                                
                    water_temp_wave_height.append(wtwh_comp)
                    #print("success")
            except Exception as e:
                print("error", e)
                pass
            on_map_json["WATER_TEMP_WAVE_HEIGHT"] = water_temp_wave_height

            ## Local WTWH
            local_water_temp_wave_height = []
            try:
                df_lwtwh = pd.read_csv('INPUT/INP_ONMAP_LWTWH/on_map_lwtwh_'+areaname+'.inp', sep='\\s+', header=None, encoding='UTF-8', index_col=0)
                df_lwtwh.columns = ['LAT', 'LON', 'YES3K_LAT', 'YES3K_LON', 'CWW3_AREA', 'CWW3_LAT', 'CWW3_LON', 'RWW3_LAT', 'RWW3_LON', 'WW3_LAT', 'WW3_LON', 'WRF_LAT', 'WRF_LON']
                df_lwtwh.index.name = 'ID'                
                for lwtwh_id in df_lwtwh.index:
                    lwtwh_comp = dict()
                    lwtwh_comp["ID"] = lwtwh_id
                    lwtwh_comp["LAT"] = df_lwtwh['LAT'][lwtwh_id]
                    lwtwh_comp["LON"] = df_lwtwh['LON'][lwtwh_id]
                    if fcstdate > shortDay: # FOR MIDDLE FORECAST
                        lwtwh_comp[ "WATER_TEMP"] = f"{ncYES3K.variables['temp'][khoastep-9:khoastep+15,df_lwtwh.YES3K_LAT[lwtwh_id],df_lwtwh.YES3K_LON[lwtwh_id]].mean(axis=0):.1f}"
                        lwtwh_comp["WAVE_HEIGHT"] = f"{max(ncWW3.variables['Hsig'][khoastep-9:khoastep+15,df_lwtwh.WW3_LAT[lwtwh_id],df_lwtwh.WW3_LON[lwtwh_id]].max(axis=0), 0.1):.1f}"
                    else:
                        lwtwh_comp["WATER_TEMP"] = f"{ncYES3K.variables['temp'][khoastep,df_lwtwh.YES3K_LAT[lwtwh_id],df_lwtwh.YES3K_LON[lwtwh_id]]:.1f}"
                        if   stWAVE == 'CWW3':
                            lwtwh_comp["WAVE_HEIGHT"] = f"{max(ncWAVE.variables['hsig'+df_lwtwh.CWW3_AREA[lwtwh_id]][ kmastep,df_lwtwh.CWW3_LAT[lwtwh_id],df_lwtwh.CWW3_LON[lwtwh_id]], 0.1):.1f}"
                        elif stWAVE == 'RWW3':
                            lwtwh_comp["WAVE_HEIGHT"] = f"{max(ncWAVE.variables['hsig1_dajn'][kmastep,df_lwtwh.RWW3_LAT[lwtwh_id],df_lwtwh.RWW3_LON[lwtwh_id]], 0.1):.1f}"
                        else:
                            lwtwh_comp["WAVE_HEIGHT"] = f"{max(ncWAVE.variables['Hsig'][khoastep,df_lwtwh.WW3_LAT[lwtwh_id],df_lwtwh.WW3_LON[lwtwh_id]], 0.1):.1f}"
                    
                    local_water_temp_wave_height.append(lwtwh_comp)
            except:
                pass
            on_map_json["LOCAL_WATER_TEMP_WAVE_HEIGHT"] = local_water_temp_wave_height

            ## Local WTWH Wind
            local_water_temp_wave_height_wind = []
            try:
                df_lwtwhw = pd.read_csv('INPUT/INP_ONMAP_LWTWHW/on_map_lwtwhw_'+areaname+'.inp', sep='\\s+', header=None, encoding='UTF-8', index_col=0)
                df_lwtwhw.columns = ['LAT', 'LON', 'YES3K_LAT', 'YES3K_LON', 'CWW3_AREA', 'CWW3_LAT', 'CWW3_LON', 'RWW3_LAT', 'RWW3_LON', 'WW3_LAT', 'WW3_LON', 'WRF_LAT', 'WRF_LON']
                df_lwtwhw.index.name = 'ID'                
                for lwtwhw_id in df_lwtwhw.index:
                    lwtwhw_comp = dict()
                    lwtwhw_comp["ID"] = lwtwhw_id
                    lwtwhw_comp["LAT"] = df_lwtwhw['LAT'][lwtwhw_id]
                    lwtwhw_comp["LON"] = df_lwtwhw['LON'][lwtwhw_id]
                    if fcstdate > shortDay: # FOR MIDDLE FORECAST
                        lwtwhw_comp[ "WATER_TEMP"] = f"{ncYES3K.variables['temp'][khoastep-9:khoastep+15,df_lwtwhw.YES3K_LAT[lwtwhw_id],df_lwtwhw.YES3K_LON[lwtwhw_id]].mean(axis=0):.1f}"
                        lwtwhw_comp["WAVE_HEIGHT"] = f"{max(ncWW3.variables['Hsig'][khoastep-9:khoastep+15,df_lwtwhw.WW3_LAT[lwtwhw_id],df_lwtwhw.WW3_LON[lwtwhw_id]].max(axis=0), 0.1):.1f}"
                        wvelU = ncWRF.variables['Uwind'][khoastep-9:khoastep+15,df_lwtwhw.WRF_LAT[lwtwhw_id],df_lwtwhw.WRF_LON[lwtwhw_id]]
                        wvelV = ncWRF.variables['Vwind'][khoastep-9:khoastep+15,df_lwtwhw.WRF_LAT[lwtwhw_id],df_lwtwhw.WRF_LON[lwtwhw_id]]
                        wvel  = (wvelU**2 + wvelV**2)**0.5
                        ## 풍속이 최대일때의 U,V 성분 추출 --> 최대 풍속일때의 풍향 표시    
                        wdeg = np.rad2deg(np.arctan2(wvelV[np.argmax(wvel)],wvelU[np.argmax(wvel)]))
                        wdeg = np.array(wdeg)
                        wdeg[wdeg<0]+= 360
                        #print(wdeg)
                        ## 최대풍속 산출
                        wvel = wvel[np.argmax(wvel)]
                    else:
                        lwtwhw_comp["WATER_TEMP"] = f"{ncYES3K.variables['temp'][khoastep,df_lwtwhw.YES3K_LAT[lwtwhw_id],df_lwtwhw.YES3K_LON[lwtwhw_id]]:.1f}"
                        if   stWAVE == 'CWW3':
                            lwtwhw_comp["WAVE_HEIGHT"] = f"{max(ncWAVE.variables['hsig'+df_lwtwhw.CWW3_AREA[lwtwhw_id]][kmastep,df_lwtwhw.CWW3_LAT[lwtwhw_id],df_lwtwhw.CWW3_LON[lwtwhw_id]], 0.1):.1f}"
                        elif stWAVE == 'RWW3':
                            lwtwhw_comp["WAVE_HEIGHT"] = f"{max(ncWAVE.variables['hsig1_dajn'][kmastep,df_lwtwhw.RWW3_LAT[lwtwhw_id],df_lwtwhw.RWW3_LON[lwtwhw_id]], 0.1):.1f}"
                        else:
                            lwtwhw_comp["WAVE_HEIGHT"] = f"{max(ncWAVE.variables['Hsig'][khoastep,df_lwtwhw.WW3_LAT[lwtwhw_id],df_lwtwhw.WW3_LON[lwtwhw_id]], 0.1):.1f}"
                        wvelU = ncWRF.variables['Uwind'][khoastep,df_lwtwhw.WRF_LAT[lwtwhw_id],df_lwtwhw.WRF_LON[lwtwhw_id]]
                        wvelV = ncWRF.variables['Vwind'][khoastep,df_lwtwhw.WRF_LAT[lwtwhw_id],df_lwtwhw.WRF_LON[lwtwhw_id]]
                        wvel  = (wvelU**2 + wvelV**2)**0.5
                        wdeg = np.rad2deg(np.arctan2(wvelV,wvelU))
                        wdeg[wdeg<0]+= 360
                    lwtwhw_comp["WIND"] = f"{max(wvel, 1.0):2.0f}"
                    lwtwhw_comp["WIND_DIR"] = f"{wdeg :2.0f}"
                    
                    local_water_temp_wave_height_wind.append(lwtwhw_comp)
            except :
                pass
            on_map_json["LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND"] = local_water_temp_wave_height_wind

            ## S111-CUR
            s111_cur = []
            try:
                df_s111 = pd.read_csv('INPUT/INP_ONMAP_S111CUR/on_map_s111_'+areaname+'.inp', sep='\\s+', header=None, encoding='UTF-8', index_col=0)
                df_s111.columns = ['LAT', 'LON', 'YES3K_LAT', 'YES3K_LON']
                df_s111.index.name = 'ID'
                for s111_id in df_s111.index:
                    s111_comp = dict()
                    s111_comp["ID"]  = s111_id
                    s111_comp["LAT"] = df_s111['LAT'][s111_id]
                    s111_comp["LON"] = df_s111['LON'][s111_id]
                    velU = ncYES3K.variables['u'][khoastep,df_s111.YES3K_LAT[s111_id],df_s111.YES3K_LON[s111_id]]
                    velV = ncYES3K.variables['v'][khoastep,df_s111.YES3K_LAT[s111_id],df_s111.YES3K_LON[s111_id]]
                    s111_comp["CUR_SPD"] = f"{(velU**2 + velV**2)**0.5:.4f}"
                    s111_comp["CUR_DIR"] = f"{np.arctan2(velU, velV)*180.0/np.pi:.4f}"
                    if velU == 0 and velV == 0:
                        continue
                    else:
                        s111_cur.append(s111_comp)
            except:
                pass
            on_map_json["S111_CUR"] = s111_cur
                

            ## FLOOD
            df_flood = pd.read_csv('INPUT/INP_ONMAP_FLOOD/on_map_flood_'+areaname+'.inp', sep='\\s+', header=None, encoding='UTF-8', index_col=0)
            df_flood.columns = ['FLOOD', 'POS', 'NAME', 'LAT', 'LON']
            df_flood.index.name = 'ID'
            flood_risk_area = []
            for flood_id in df_flood.index:
                flood_comp = dict()
                flood_comp["ID"] = flood_id
                if areaname == 'koren':
                    flood_comp["NAME"] = areaenglish[ df_flood['NAME'][flood_id] ]
                else:
                    flood_comp["NAME"] = df_flood['NAME'][flood_id]
                flood_comp["MARKER_POS"] = df_flood['POS'][flood_id]
                flood_comp["LON"] = df_flood['LON'][flood_id]
                flood_comp["LAT"] = df_flood['LAT'][flood_id]
                try:
                    df_fflood = pd.read_fwf('INPUT/03_Flood/'+df_flood['NAME'][flood_id]+'.dat', widths=[4,2,2,2,6,6], header=None, encoding='EUC-KR', skiprows=0)
                    df_fflood.columns = ['YYYY', 'MM', 'DD', 'LOGICAL', 'STIME', 'ETIME']
                    df_fflood = df_fflood.set_index(['YYYY', 'MM', 'DD'])
                except:
                    df_fflood = pd.DataFrame(data=[0], index=[[yyyy],[sm],[sd]], columns=['LOGICAL'])
                    df_fflood.index.name = ('YYYY','MM','DD','TYPE')
                    pass
                if df_flood['FLOOD'][flood_id] == 'T' or df_fflood.LOGICAL[yyyy,sm,sd] == 1:
                    flood_comp["FLOOD"] = 'T'
                else:
                    flood_comp["FLOOD"] = 'F'
                if df_fflood.LOGICAL[yyyy,sm,sd] == 1:
                    flood_comp["DISPLAY"] = "Y"
                    flood_comp["ATTENTION_SPAN"] = [df_fflood.STIME[yyyy,sm,sd],df_fflood.ETIME[yyyy,sm,sd]]
                elif areaname == 'kor' and df_flood['NAME'][flood_id] in ['평택', '영광', '강릉', '울진']:
                    flood_comp["DISPLAY"] = "C"
                    flood_comp["ATTENTION_SPAN"] = ["    ","    "]
                elif areaname == 'koren' and df_flood['NAME'][flood_id] in ['평택', '영광', '강릉', '울진']:
                    flood_comp["DISPLAY"] = "C"
                    flood_comp["ATTENTION_SPAN"] = ["    ","    "]    
                else:
                    flood_comp["DISPLAY"] = "N"
                    flood_comp["ATTENTION_SPAN"] = ["    ","    "]
                if flood_comp["FLOOD"] == 'T':
                    flood_risk_area.append(flood_comp)
            on_map_json["FLOOD_RISK_AREA"] = flood_risk_area

            ## TIDAL CURRENT
            current_info = []
            try:
                df_current = pd.read_csv('INPUT/INP_ONMAP_CURRENT/on_map_current_'+areaname+'.inp', sep='\\s+', header=None, encoding='UTF-8', index_col=0)
                df_current.columns = ['HPOS', 'VPOS', 'NAME', 'LAT', 'LON', 'LOW', 'HIGH', 'TYPE', 'FILE']
                df_current.index.name = 'ID'
                for current_id in df_current.index:
                    current_comp = dict()
                    current_comp["ID"] = current_id
                    current_comp["NAME"] = df_current['NAME'][current_id]
                    current_comp["LON"] = df_current['LON'][current_id]
                    current_comp["LAT"] = df_current['LAT'][current_id]
                    current_comp["MARKER_POS"] = df_current['HPOS'][current_id]
                    current_comp["MARKER_V_POS"] = df_current['VPOS'][current_id]
                    df_tcurrent = pd.read_fwf('INPUT/02_Tide_Station/'+df_current['FILE'][current_id], widths=[10,6,6,4,4], header=None, encoding='EUC-KR', skiprows=4)
                    df_tcurrent.columns = ['DATE', 'MINTIME', 'MAXTIME', 'DIR', 'SPD']
                    df_tcurrent['DATE'] = df_tcurrent['DATE'].fillna(method='ffill')
                    df_tcurrent = df_tcurrent.set_index('DATE')
                    tcurrent = df_tcurrent.loc[(df_tcurrent.index == str(yyyy)+'-'+str(sm).zfill(2)+'-'+str(sd).zfill(2)) & df_tcurrent.MAXTIME.notna()]
                    cur_infos = []
                    for cur_id in range(len(tcurrent)):
                        cur_info = dict()
                        if pd.notna(tcurrent.MINTIME.iloc[cur_id]):
                            cur_info["MIN_CUR_TIME"] = tcurrent.MINTIME.iloc[cur_id]
                        else:
                            cur_info["MIN_CUR_TIME"] = ""
                        if pd.notna(tcurrent.MAXTIME.iloc[cur_id]):
                            cur_info["MAX_CUR_TIME"] = tcurrent.MAXTIME.iloc[cur_id]
                            cur_info["CUR_DIRECT"  ] = str(dirtoint[tcurrent.DIR.iloc[cur_id]])
                            cur_info["CUR_SPEED"   ] = tcurrent.SPD.iloc[cur_id]
                        else:
                            cur_info["MAX_CUR_TIME"] = ""
                            cur_info["CUR_DIRECT"  ] = ""
                            cur_info["CUR_SPEED"   ] = ""
                        cur_infos.append(cur_info)
                    current_comp["CUR_INFO"] = cur_infos
                    current_comp["DEG_FE"]   = [ str(df_current['LOW'][current_id]), str(df_current['HIGH'][current_id]), df_current['TYPE'][current_id] ]

                    current_info.append(current_comp)
            except Exception as e:
                print(e)
                pass
            on_map_json["CURRENT_INFO"] = current_info

            ## CHART RADAR
            df_chart = pd.read_csv('INPUT/INP_CHART_RADAR/chart_radar_'+areaname+'.inp', sep='\\s+', header=None, encoding='UTF-8')
            df_chart.columns = ['NAME']
            chart = []
            idindex = 0
            for chart_name in df_chart['NAME']:
                idindex += 1
                chart_comp = dict()
                chart_comp["ID"] = "CRD_" + f'{idindex:2d}'
                if areaname == 'koren':
                    chart_comp["POS_NAME"] = areaenglish[chart_name]
                else:
                    chart_comp["POS_NAME"] = chart_name
                df_tide = pd.read_csv('INPUT/01_Tide/'+chart_name+' 예측조위(극치)_20220101_20221231.txt', sep='\\s+', header=None, encoding='EUC-KR', skiprows=7, index_col=[0,1,2,5], engine="python")
                df_tide.columns = ['HH', 'MM', 'Hgt']
                df_tide.index.name = ('YYYY','MM','DD','TYPE')
                chart_comp["TIDE_HIGH_VALUE_01"]=""
                chart_comp["TIDE_HIGH_TIME_01"] ="--:--"
                chart_comp["TIDE_LOW_VALUE_01"] =""
                chart_comp["TIDE_LOW_TIME_01"]  ="--:--"
                chart_comp["TIDE_HIGH_VALUE_02"]=""
                chart_comp["TIDE_HIGH_TIME_02"] ="--:--"
                chart_comp["TIDE_LOW_VALUE_02"] =""
                chart_comp["TIDE_LOW_TIME_02"]  ="--:--"
                # HIGH TIDE
                try:
                    high_tide_sorted = df_tide.loc[yyyy,sm,sd,'MAX',:].values[df_tide.loc[yyyy,sm,sd,'MAX',:].values[:,2].argsort()]
                    ht_state = len(high_tide_sorted)
                    for index_ht in range(-1, -1-ht_state, -1):
                        chart_comp["TIDE_HIGH_VALUE_"+str(-index_ht).zfill(2)] = str(high_tide_sorted[index_ht,2])
                        chart_comp["TIDE_HIGH_TIME_" +str(-index_ht).zfill(2)] = str(high_tide_sorted[index_ht,0]).zfill(2) + ":" + str(high_tide_sorted[index_ht,1]).zfill(2)
                        chart_comp["TIDE_HIGH_VALUE_02"] = str(high_tide_sorted[index_ht,2])
                except:
                    pass
                # LOW TIDE
                try:
                    low_tide_sorted  = df_tide.loc[yyyy,sm,sd,'MIN',:].values[df_tide.loc[yyyy,sm,sd,'MIN',:].values[:,2].argsort()]
                    lt_state = len(low_tide_sorted)
                    for index_lt in range(-1, -1-lt_state, -1):
                        chart_comp["TIDE_LOW_VALUE_"+str(-index_lt).zfill(2)] = str(low_tide_sorted[index_lt,2])
                        chart_comp["TIDE_LOW_TIME_" +str(-index_lt).zfill(2)] = str(low_tide_sorted[index_lt,0]).zfill(2) + ":" + str(low_tide_sorted[index_lt,1]).zfill(2)
                        chart_comp["TIDE_LOW_VALUE_02"] = str(low_tide_sorted[index_lt,2])
                except:
                    pass
                chart.append(chart_comp)
            chart_radar_json["CHART"] = chart

            ## SAVE JSON
            with open(os.path.join(objDir, "on_map.json"), 'w', encoding='UTF-8') as f_onmap:
                json.dump(on_map_json, f_onmap, indent="\t", ensure_ascii=False)
            with open(os.path.join(objDir, "chart_radar.json"), 'w', encoding='UTF-8') as f_chartradar:
                json.dump(chart_radar_json, f_chartradar, indent="\t", ensure_ascii=False)

            # BREAK MIDDLE FORECAST
            if fcstdate > shortDay: break
            
ncYES3K.close()
ncWW3.close()
ncWAVE.close()
ncWRF.close()