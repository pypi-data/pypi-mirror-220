@ECHO OFF

set VER=%1

IF "a%VER%"=="a" (
    ECHO tag required ^(ex: 0.5^)
    exit /b
)

IF not "a%VER%"=="adev" (
    git tag %VER%
    git push --tags
)

set CURRENT=%~dp0
set RELEASE=%CURRENT%release
set RELEASE_TEMP=%CURRENT%release_temp


cd /d %~dp0


del /Q /S %RELEASE%
del /Q /S %RELEASE_TEMP%
mkdir %RELEASE%
mkdir %RELEASE_TEMP%

rye run pyinstaller.exe bufap\cli\bufap-cli.spec --distpath %RELEASE_TEMP%

COPY bufap\cli\bufap-getall.bat %RELEASE_TEMP%
COPY README.md %RELEASE_TEMP%

pushd %RELEASE_TEMP%
powershell compress-archive -Force * %RELEASE%\bufap-%VER%.zip
popd

