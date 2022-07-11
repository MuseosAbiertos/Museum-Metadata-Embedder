@echo off

set VERSION=%1
REM @echo VERSION %VERSION%

IF "%VERSION%" == "" (
  @echo.
  @echo You need to provide the version
  @echo.
  exit /b
) ELSE (
  set VERSION=%1
)
set WWD=%cd%
echo %WWD%

cd ..\..

set RWD=%cd%
echo %RWD%

echo "Removing the previous build data"
REM del /s /q dist/*
REM del /s /q build/*
del /Q gmme.spec
rmdir /s /q dist
rmdir /s /s build

echo "Creating the gmme exe"
REM Always download the exiftool for windows from the exiftool.org website and rename to exiftool.exe 
REM and copy it ionside the OPackaging\windows folder
pyinstaller --onefile --noconsole --icon "%RWD%\logos\MME.ico" --add-binary "%WWD%\exiftool.exe;." --add-data ".\data\*;.\data" --add-data ".\logos\*;.\logos" --clean gmme.py

@echo Copy license
copy LICENSE dist

@echo Now do some renaming (necessary as pyinstyaller creates the name exactly as the script) and create the zip file
cd dist
mv gmme.exe Museum-Metadata-Embedder.exe
zip -r ..\Museum-Metadata-Embedder-%VERSION%-win-x86_64.zip *
cd ..
move Museum-Metadata-Embedder-%VERSION%-win-x86_64.zip %WWD%
cd %WWD%



