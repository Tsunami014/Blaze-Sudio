@echo off
mkdir temp
cd temp
git clone https://github.com/Tsunami014/Blaze-Sudio.git
echo Removing unnececary folders for installation
rmdir "Blaze-Sudio/utils" /S /Q
rmdir "Blaze-Sudio/elementgen" /S /Q

echo Testing for Powershell...
setlocal
CALL :GETPARENT PARENT
IF /I "%PARENT%" == "powershell" echo Running in powershell, if you see some errors, QUICKLY CLOSE THIS DOWN OR IT WILL INSTALL THE WRONG THING!!!
endlocal

cd Blaze-Sudio\graphics
move /Y setup.py ./../setup.py
cd ..
pip install .
cd ../..
rmdir temp /S /Q
GOTO :EOF

:GETPARENT
SET "PSCMD=$ppid=$pid;while($i++ -lt 3 -and ($ppid=(Get-CimInstance Win32_Process -Filter ('ProcessID='+$ppid)).ParentProcessId)) {}; (Get-Process -EA Ignore -ID $ppid).Name"

for /f "tokens=*" %%i in ('powershell -noprofile -command "%PSCMD%"') do SET %1=%%i
