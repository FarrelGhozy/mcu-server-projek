@echo off
setlocal enabledelayedexpansion
rem download_mod.bat - download semua mod client server (Forge 1.20.1)
rem Cara pakai: klik 2x, atau download_mod.bat [folder_tujuan]
set "TARGET=%~1"
if "%TARGET%"=="" set "TARGET=%~dp0mods"
if not exist "%TARGET%" mkdir "%TARGET%"
set /a ok=0 & set /a gagal=0
echo  * Mekanism Core
call :download "Mekanism-1.20.1-10.4.16.80.jar" "https://cdn.modrinth.com/data/Ce6I4WUE/versions/uxe1WQp4/Mekanism-1.20.1-10.4.16.80.jar"
echo  * Mekanism Generators
call :download "MekanismGenerators-1.20.1-10.4.16.80.jar" "https://cdn.modrinth.com/data/OFVYKsAk/versions/Th4Czz4N/MekanismGenerators-1.20.1-10.4.16.80.jar"
echo  * Mekanism Tools
call :download "MekanismTools-1.20.1-10.4.16.80.jar" "https://cdn.modrinth.com/data/tqQpq1lt/versions/VzpFbUpF/MekanismTools-1.20.1-10.4.16.80.jar"
echo  * Architectury API
call :download "architectury-9.2.14-forge.jar" "https://cdn.modrinth.com/data/lhGA9TYQ/versions/1MKTLiiG/architectury-9.2.14-forge.jar"
echo  * Cloth Config API
call :download "cloth-config-11.1.136-forge.jar" "https://cdn.modrinth.com/data/9s6osm5g/versions/t8TXrZvZ/cloth-config-11.1.136-forge.jar"
echo  * JEI
call :download "jei-1.20.1-forge-15.20.0.130.jar" "https://cdn.modrinth.com/data/u6dRKJwZ/versions/RTFeXsvE/jei-1.20.1-forge-15.20.0.130.jar"
echo  * Veinst VeinMiner
call :download "veinst_veinminer-1.3.0-1.20.1.jar" "https://edge.forgecdn.net/files/8128/571/veinst_veinminer-1.3.0-1.20.1.jar"
echo  * JourneyMap
call :download "journeymap-1.20.1-5.10.3-forge.jar" "https://cdn.modrinth.com/data/lfHFW1mp/versions/r7FWVNCs/journeymap-1.20.1-5.10.3-forge.jar"
echo  * GraveStone
call :download "gravestone-forge-1.20.1-1.0.35.jar" "https://cdn.modrinth.com/data/RYtXKJPr/versions/q9kZE5Xo/gravestone-forge-1.20.1-1.0.35.jar"
echo  * Create
call :download "create-1.20.1-6.0.8.jar" "https://cdn.modrinth.com/data/LNytGWDc/versions/8amzvn9x/create-1.20.1-6.0.8.jar"
echo  * Create Garnished
call :download "garnished-2.1.7.b+1.20.1-neoforged.jar" "https://cdn.modrinth.com/data/6e2SlzR4/versions/tO2irH8t/garnished-2.1.7.b%2B1.20.1-neoforged.jar"
echo.
echo === Selesai: !ok! OK, !gagal! gagal -> %TARGET%
pause & exit /b
:download
set "f=%~1" & set "u=%~2"
where curl >nul 2>nul
if %errorlevel%==0 (
    curl -fsSL --retry 3 -o "%TARGET%\%f%" "%u%" >nul
) else (
    powershell -NoProfile -Command "Invoke-WebRequest -Uri '%u%' -OutFile '%TARGET%\%f%'" >nul
)
if exist "%TARGET%\%f%" ( set /a ok+=1 & echo      OK ) else ( set /a gagal+=1 & echo      GAGAL )
exit /b
