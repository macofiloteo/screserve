@echo off
setlocal
:PROMPT
SET /P AREYOUSURE=Are you sure (Y/[N]) Please check if "screserve.json" exists on your Desktop?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END


if exist %USERPROFILE%/Desktop/screserve_data.json (
    cmd /k "C:\xampp\htdocs\screserve\Scripts\activate.bat & python C:\xampp\htdocs\screserve-master\manage.py loaddata %USERPROFILE%/Desktop/screserve_data.json"
) else (
    set /P doesNotExist=File does not exist! Press any key to exit
)

:END
endlocal

