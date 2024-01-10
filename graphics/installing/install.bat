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
IF /I "%PARENT%" == "powershell" GOTO :ISPOWERSHELL
IF /I "%PARENT%" == "pwsh" GOTO :ISPOWERSHELL
endlocal

echo Not running from Powershell 
cd Blaze-Sudio\graphics
move /Y setup.py ./../setup.py
cd ..
pip install .
cd ../..
rmdir temp /S /Q
exit /b 1
GOTO :EOF

:GETPARENT
SET "PSCMD=$ppid=$pid;while($i++ -lt 3 -and ($ppid=(Get-CimInstance Win32_Process -Filter ('ProcessID='+$ppid)).ParentProcessId)) {}; (Get-Process -EA Ignore -ID $ppid).Name"

for /f "tokens=*" %%i in ('powershell -noprofile -command "%PSCMD%"') do SET %1=%%i

GOTO :EOF

:ISPOWERSHELL
echo Running from Powershell
Move-item -Path "Blaze-Sudio\graphics\setup.py" -destination "Blaze-Sudio\setup.py" -force
cd Blaze-Sudio
pip install .
cd ../..
rmdir temp -recurse -force
exit /b 1
