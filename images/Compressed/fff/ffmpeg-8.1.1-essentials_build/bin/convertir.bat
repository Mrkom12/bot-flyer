@echo off
title Convertisseur Video - H.264 Compatible Web
echo ======================================
echo   CONVERTISSEUR VIDEO H.264
echo ======================================
echo.
echo Glisse ta video ici (MP4, MOV, MKV, AVI...)
echo.
set /p video=
echo.
echo Conversion en cours (patientez 2-5 min)...
echo.
ffmpeg -i "%video%" -c:v libx264 -crf 23 -preset medium -c:a aac -movflags +faststart -profile:v high -level 4.0 "%video%_H264.mp4"
echo.
echo ======================================
echo   TERMINE ! Fichier : %video%_H264.mp4
echo ======================================
pause