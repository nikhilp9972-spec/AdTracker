@echo off
title Competitor Ad Tracker Server
cd /d "%~dp0"
echo ========================================================
echo   Starting Competitor Ad Tracker ^& Intelligence Engine
echo ========================================================
echo.

:: Detect Python or Py launcher
set PY_CMD=
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PY_CMD=python
) else (
    where py >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PY_CMD=py
    ) else (
        echo [ERROR] Python was not found in your system PATH!
        echo Please make sure Python 3 is installed.
        pause
        exit /b 1
    )
)

echo Using: %PY_CMD%
echo Opening browser: http://localhost:8000
echo Server running at: http://localhost:8000 (and http://127.0.0.1:8000)
echo.
echo NOTE: Keep this terminal window open while using the app!
echo ========================================================
echo.

start "" "http://localhost:8000"
%PY_CMD% app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Server exited with code %ERRORLEVEL%.
)
pause
