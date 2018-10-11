@echo off
setlocal
:PROMPT
cmd /k "C:\xampp\htdocs\screserve\Scripts\activate.bat & python C:\xampp\htdocs\screserve-master\manage.py dumpdata >> %USERPROFILE%/Desktop/screserve_data.json"
set /P ConfirmJson=Check if screserve.json is created in your Desktop. Press any key to exit...
endlocal