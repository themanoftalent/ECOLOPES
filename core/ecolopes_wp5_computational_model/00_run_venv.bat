@echo off

set "VENV_PATH=C:\virtualenvs\ghhops_00"
call "%VENV_PATH%\Scripts\activate.bat"

for %%A in ("%~dp0.") do (
  set "ProjectName=%%~nxA"
  set "ParentFolderName=%%~dpA"
)

pushd "%ParentFolderName%"

echo [BAT]: Running %ProjectName% from %cd%

python -m %ProjectName%

pause
popd



@echo off

@REM SET VENV_PATH=C:\virtualenvs\ghhops_00
@REM call "%VENV_PATH%\Scripts\activate.bat

@REM for /f %%q in ("%~dp0.") do SET ProjectName=%%~nxq
@REM FOR %%A IN ("%~dp0.") DO SET ParentFolderName=%%~dpA
@REM cd %ParentFolderName%

@REM ECHO [BAT]: Running %ProjectName% from %ParentFolderName%

@REM python -m %ProjectName%

@REM PAUSE