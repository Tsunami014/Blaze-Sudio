@echo off
mkdir temp
cd temp
git clone https://github.com/Tsunami014/Blaze-Sudio.git
echo Removing unnececary folders for installation
rmdir "Blaze-Sudio/utils" /S /Q
rmdir "Blaze-Sudio/elementgen" /S /Q

cd Blaze-Sudio\graphics
move /Y setup.py ./../setup.py
cd ..
pip install .
cd ../..
rmdir temp /S /Q
echo done!
