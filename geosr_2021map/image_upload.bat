@echo off
set yyyymmdd=%Date:~0,4%%Date:~5,2%%Date:~8,2%
set objDirectory=C:\Utility\apache-tomcat-9.0.22\webapps\daily_ocean2021\

rem scp -P10001 root@10.27.90.57:/home/model/result/YES3K_7d/%yyyymmdd%00/YES3K_%yyyymmdd%00.nc ./
rem scp -P10001 root@10.27.90.57:/home/model/result/WRF/%yyyymmdd%00/wrf_dm2_7d/wrfdm2_%yyyymmdd%_*.nc ./WRF_%yyyymmdd%.nc
rem scp -P10001 root@10.27.90.57:/home/model/result/WW3_7d/%yyyymmdd%00/WW3_%yyyymmdd%00.nc ./
rem "C:\Program Files (x86)\GnuWin32\bin\wget.exe" http://10.27.90.53:8080/opendap/external/FORECAST_QUOTIENT/CWW3_%yyyymmdd%00.nc
rem "C:\Program Files (x86)\GnuWin32\bin\wget.exe" http://10.27.90.53:8080/opendap/external/FORECAST_QUOTIENT/RWW3_%yyyymmdd%00.nc
rem if not exist YES3K_%yyyymmdd%00.nc "C:\Program Files (x86)\GnuWin32\bin\wget.exe" http://10.27.90.53:8080/opendap/application/Tidal_atlas/YES3K/YES3K_%yyyymmdd%00.nc  
rem if not exist WRF_%yyyymmdd%.nc scp -P10001 root@10.27.90.57:/home/model/result/WRF/%yyyymmdd%00/wrf_dm2/wrfdm2_%yyyymmdd%_*.nc ./WRF_%yyyymmdd%.nc
rem copy SOURCE\*.py

rem echo MAKE JSON... (APPRX. 5 min)
rem echo START TIME:
rem time /t
rem python make_json.py %yyyymmdd%

rem echo MAKE TEMP MAP... (APPRX. 10 min)
rem echo START TIME:
rem time /t
rem python make_mapinput.py %yyyymmdd%
rem temp_loess.exe

rem echo END TIME:
rem time /t

rem xcopy .\RESULT\*.* %objDirectory%RESULT\ /S /E /Q /Y

rem del *.json *.py *.nc

cd D:\geosr_2021map\ImageDownUpload
python ImageDownUpload.py