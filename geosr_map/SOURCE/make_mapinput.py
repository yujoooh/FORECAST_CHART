#-*- coding: utf-8 -*-
# TO MAKE INPUT FILE FOR TEMP MAP OF MFC(Marine Forecast Chart)
# 20201014 HGChoe

import pandas as pd
import json
import sys
import os

### SET VARIABLE NAME
## GET ARGUMENTS
yyyymmdd = str(sys.argv[1]) # yyyymmdd
filenmYES3K = "YES3K_"+yyyymmdd+"00.nc"

### CHECK input.json
if os.path.exists("input.json"):
    os.remove("input.json")

### LOAD_INDEX
df = pd.read_csv('INPUT/on_map_base.inp', sep='\\s+', encoding='UTF-8', index_col=0)

### LIST FOR LOOP
liFcstdate = [ 0, 1, 2, 3, 4, 5, 6 ] # 7 days forecast
liTimestep = [ 0, 7 ] # KST 09, 16
# KST today 09:00 -  0 timestep - 00:00 UTC
# KST today 10:00 -  1 timestep - 01:00 UTC
liAreaname = ['KOREA', 'INCHEON', 'BUSAN', 'SOKCHO', 'GUNSAN', \
            'MOKPO', 'JEJU', 'YEOSU', 'TONGYEONG', 'POHANG', \
            'TAEAN', 'HEUKSANDO', 'WANDO', 'HUPO', 'DONGHAE', \
            'ULLEUNGDO', 'BAENGNYEONGDO', 'GYEOKYEOLBIYEOLDO', 'YEONGGWANG', 'IEODO', \
            'KOREAEN', 'ONBADA']

### MAIN LOOP
## MAP_INPUT_JSON
map_input_json = dict()
temp_map = []
for areaname in liAreaname:
    for fcstdate in liFcstdate:
        for timestep in liTimestep:
            # CALCULATE khoastep
            khoastep = timestep + fcstdate * 24
            # TEMP_MAP
            map_comp = dict()
            map_comp["YES3K_NAME" ] = filenmYES3K
            map_comp["COAST_NAME" ] = df['COAST_NAME'][areaname]
            map_comp["RESULT_NAME"] = "temp.png"
            map_comp["OBJECT_DIR" ] = df['OBJECT_DIR'][areaname] + '\\' \
                                      + str(fcstdate+1).zfill(2) + '\\' \
                                      + str(timestep+9).zfill(2) + '\\'
            map_comp["TIME" ] = khoastep
            map_comp["TYPE" ] = "short" if int(fcstdate) < 3 else 'middle'
            map_comp["Y_0"  ] = int(df["Y_0"][areaname])
            map_comp["Y_1"  ] = int(df["Y_1"][areaname])
            map_comp["X_0"  ] = int(df["X_0"][areaname])
            map_comp["X_1"  ] = int(df["X_1"][areaname])
            map_comp["FIG_X"] = df["FIG_X"][areaname]
            map_comp["FIG_Y"] = df["FIG_Y"][areaname]
            temp_map.append(map_comp)
            # BREAK MIDDLE FORECAST
            if fcstdate > 2: break

### WRITE input.json
map_input_json["TEMP_MAP"] = temp_map
with open('input.json', 'w', encoding='UTF-8') as f_mij:
    json.dump(map_input_json, f_mij, indent="\t", ensure_ascii=False)