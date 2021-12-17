@echo off

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%

echo YR : %YEAR%
echo MN : %MONTH%
echo DY : %DAY%

set TODAY=%YEAR%%MONTH%%DAY%
echo %TODAY%

rem

set logfile=./log/%TODAY%.log

set start_time=%time% 
echo 'batch file start time :' %start_time% > %logfile%
echo '===[Process Start]====================================================='  >> %logfile%
call run2021.bat >> %logfile%
set end_time=%time%
echo '===[Process Complete]=================================================='  >> %logfile%
echo %start_time%  %end_time%  >> %logfile%