@echo off
set yyyymmdd=%Date:~0,4%%Date:~5,2%%Date:~8,2%
set objDirectory=C:\Utility\apache-tomcat-9.0.22\webapps\daily_ocean2021\
set rstDirectory=C:\Utility\apache-tomcat-9.0.22\webapps\%yyyymmdd%\

D:
cd D:\geosr_2021map
del *.json *.py *.nc


scp -P10001 root@10.27.90.50:/DATA/opendap/application/Tidal_atlas/YES3K_7D/YES3K_%yyyymmdd%00.nc ./
scp -P10001 root@10.27.90.50:/DATA/opendap/application/Tidal_atlas/WRF_7d/wrfdm2_%yyyymmdd%_*.nc ./WRF_%yyyymmdd%.nc
scp -P10001 root@10.27.90.50:/DATA/opendap/simulation/wave/WW3_7d/%yyyymmdd%00/WW3_%yyyymmdd%00.nc ./
scp -P10001 root@10.27.90.50:/DATA/opendap/external/KMA/CWW3/CWW3_%yyyymmdd%00.nc ./
scp -P10001 root@10.27.90.50:/DATA/opendap/external/KMA/RWW3/RWW3_%yyyymmdd%00.nc ./
if not exist YES3K_%yyyymmdd%00.nc scp -P10001 root@10.27.90.50:/DATA/opendap/application/Tidal_atlas/YES3K/YES3K_%yyyymmdd%00.nc ./
if not exist WRF_%yyyymmdd%.nc scp -P10001 root@10.27.90.50:/DATA/opendap/application/Tidal_atlas/WRF/wrfdm2_%yyyymmdd%_*.nc ./WRF_%yyyymmdd%.nc
copy SOURCE\*.py

echo MAKE JSON... (APPRX. 5 min)
echo START TIME:
time /t
python make_json.py %yyyymmdd%

echo MAKE TEMP MAP... (APPRX. 10 min)
echo START TIME:
time /t
python make_mapinput.py %yyyymmdd%
temp_loess.exe

echo END TIME:
time /t

xcopy .\RESULT\*.* %objDirectory%RESULT\ /S /E /Q /Y
xcopy .\RESULT\*.* %rstDirectory% /S /E /Q /Y

del *.json *.py *.nc

cd D:\geosr_2021map\ImageDownUpload
python ImageDownUpload.py