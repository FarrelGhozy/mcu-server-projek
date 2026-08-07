@echo off
setlocal enabledelayedexpansion
rem ==================================================================
rem  download_mod.bat - yangan server MCU (Forge 1.20.1)
rem  Cara pakai: klik ganda / dari cmd: download_mod.bat
rem  Butuh: curl (sudah tersedia di Windows 10/11)
rem ==================================================================
set "TARGET=%~1"
if "%TARGET%"=="" set "TARGET=%~dp0mods"
if not exist "%TARGET%" mkdir "%TARGET%"
echo Target folder: %TARGET%
set /a ok=0
set /a gagal=0

echo.
echo  * Mekanism Core
call :download "Mekanism-1.20.1-10.4.16.80.jar" "https://cdn.modrinth.com/data/Ce6I4WUE/versions/uxe1WQp4/Mekanism-1.20.1-10.4.16.80.jar"
echo.
echo  * Mekanism Generators
call :download "MekanismGenerators-1.20.1-10.4.16.80.jar" "https://cdn.modrinth.com/data/OFVYKsAk/versions/Th4Czz4N/MekanismGenerators-1.20.1-10.4.16.80.jar"
echo.
echo  * Mekanism Tools
call :download "MekanismTools-1.20.1-10.4.16.80.jar" "https://cdn.modrinth.com/data/tqQpq1lt/versions/VzpFbUpF/MekanismTools-1.20.1-10.4.16.80.jar"
echo.
echo  * Architectury API
call :download "architectury-9.2.14-forge.jar" "https://cdn.modrinth.com/data/lhGA9TYQ/versions/1MKTLiiG/architectury-9.2.14-forge.jar"
echo.
echo  * Cloth Config API
call :download "cloth-config-11.1.136-forge.jar" "https://cdn.modrinth.com/data/9s6osm5g/versions/t8TXrZvZ/cloth-config-11.1.136-forge.jar"
echo.
echo  * JEI
call :download "jei-1.20.1-forge-15.20.0.130.jar" "https://cdn.modrinth.com/data/u6dRKJwZ/versions/RTFeXsvE/jei-1.20.1-forge-15.20.0.130.jar"
echo.
echo  * Veinst VeinMiner
call :download "veinst_veinminer-1.3.0-1.20.1.jar" "https://edge.forgecdn.net/files/8128/571/veinst_veinminer-1.3.0-1.20.1.jar"
echo.
echo  * JourneyMap
call :download "journeymap-1.20.1-5.10.3-forge.jar" "https://cdn.modrinth.com/data/lfHFW1mp/versions/r7FWVNCs/journeymap-1.20.1-5.10.3-forge.jar"
echo.
echo  * GraveStone
call :download "gravestone-forge-1.20.1-1.0.35.jar" "https://cdn.modrinth.com/data/RYtXKJPr/versions/q9kZE5Xo/gravestone-forge-1.20.1-1.0.35.jar"

echo.
echo === Selesai: !ok! berhasil, !gagal! gagal ===
echo File ada di: %TARGET%
pause
exit /b

:download
set "f=%~1"
set "u=%~2"
where curl >nul 2>nul
if %errorlevel%==0 (
    curl -fsSL --retry 3 -o "%TARGET%\%f%" "%u%" >nul
) else (
    rem fallback pakai PowerShell buat yang gak ada curl
    powershell -NoProfile -Command "Invoke-WebRequest -Uri '%u%' -OutFile '%TARGET%\%f%'" >nul
)
if exist "%TARGET%\%f%" (
    set /a ok+=1
    echo      OK
) else (
    set /a gagal+=1
    echo      GAGAL
)
exit /b