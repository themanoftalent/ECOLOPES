@Akif edit
@echo off

set "VENV_PATH=C:\virtualenvs\ghhops_00"
set "BAT_PATH=%~dp0"
set "ProjectName=PyinstallerTest"
set "VER=0.0.1b"

call "%VENV_PATH%\Scripts\activate.bat"

pushd "%BAT_PATH%"
pyinstaller --noconfirm ^
            --clean ^
            --onefile ^
            --name "%ProjectName%_%VER%" ^
            --workpath "./build" ^
            --distpath "./dist" ^
            __main__.py

popd



@REM @Akif code
@REM SET VENV_PATH=C:\virtualenvs\ghhops_00
@REM SET BAT_PATH=%~dp0

@REM SET ProjectName=PyinstallerTest
@REM SET VER=0.0.1b

@REM call "%VENV_PATH%\Scripts\activate.bat

@REM cd %BAT_PATH%
@REM pyinstaller --noconfirm ^
@REM             --clean ^
@REM             --onefile ^
@REM             --name %ProjectName%_%VER% ^
@REM             --workpath ./build ^
@REM             --distpath ./dist ^
@REM             __main__.py
