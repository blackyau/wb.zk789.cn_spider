@echo off
:loop
echo %time:~0,8%
python wb.py && taskkill /f /im dllhost.exe >null
pause
goto loop