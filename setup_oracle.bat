@echo off
echo ======================================
echo Oracle Database Setup for MDX_LEARN
echo ======================================
echo.

echo [1/3] Starting Oracle container with Docker Compose...
docker-compose up -d oracle
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to start Oracle container
    pause
    exit /b 1
)

echo.
echo [2/3] Waiting for Oracle to initialize...
timeout /t 10 /nobreak > nul

echo.
echo [3/3] Running Oracle configuration script...
powershell -ExecutionPolicy Bypass -File "setup_oracle.ps1"

echo.
echo ======================================
echo Setup completed!
echo You can now use the Oracle database.
echo ======================================
pause
