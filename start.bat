@echo off
echo ============================================
echo    AI Legal Assistant - Starting Servers
echo ============================================
echo.

echo [1/2] Starting Python Backend (port 8000)...
start "Python Backend" cmd /k "cd /d c:\placement project\AI Legel Assistant\python_backend && python main.py"

timeout /t 3 /nobreak >nul

echo [2/2] Starting React Frontend (port 3000)...
start "React Frontend" cmd /k "cd /d c:\placement project\AI Legel Assistant\frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ============================================
echo    Both servers are running!
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo ============================================
echo.
echo Press any key to exit this window...
pause >nul
