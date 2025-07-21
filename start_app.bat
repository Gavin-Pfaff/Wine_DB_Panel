@echo off
title Wine Cellar Application
cd /d "%~dp0"
echo Current Directory: %CD%
echo ========================================
echo    Starting Wine Cellar Application
echo ========================================
echo.

echo [1/3] Starting Flask Backend Server...
start "Wine Backend" cmd /k "cd /d %~dp0backend && python WINE_DB_APP.py"

echo [2/3] Waiting for backend to initialize...
timeout /t 10 /nobreak >nul

echo [3/3] Starting Electron Frontend...
npm start




echo.
echo ========================================
echo    Wine Cellar App is now running!
echo ========================================
echo    Backend:  http://localhost:5000
echo    Frontend: Opened in your browser
echo.
echo    Press any key to close this window
echo    (Backend will keep running)
echo ========================================

pause >nul