#!/usr/bin/env pwsh
# Oracle Database Setup Script for Windows (PowerShell)
# This script configures the Oracle database after Docker Compose starts

param(
    [string]$OracleHost = "localhost",
    [string]$OraclePort = "1521",
    [string]$OracleService = "XEPDB1",
    [string]$OraclePassword = "YourStrongPassword123"
)

Write-Host "=== Oracle Database Setup Script ===" -ForegroundColor Green
Write-Host "Configuring Oracle Database for DM_ACADEMICO..." -ForegroundColor Yellow

# Function to wait for Oracle to be ready
function Wait-ForOracle {
    param(
        [string]$OracleHostName,
        [string]$Port,
        [string]$Service,
        [string]$SysPassword,        [int]$MaxRetries = 60,
        [int]$RetryInterval = 20
    )
    
    Write-Host "Waiting for Oracle Database to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds $RetryInterval
    for ($i = 1; $i -le $MaxRetries; $i++) {        try {            # Try to connect to Oracle using sqlplus through docker (CDB root for Common users)
            $testSql = "SELECT 1 FROM DUAL;"
            $connectResult = docker exec oracle_db bash -c "echo '$testSql' | sqlplus -s sys/$SysPassword@XE as sysdba" 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Oracle Database is ready!" -ForegroundColor Green
                return $true
            }
        }
        catch {
            # Connection failed, continue waiting
        }
        
        Write-Host "Attempt $i/$MaxRetries - Oracle not ready yet. Waiting $RetryInterval seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds $RetryInterval
    }
    
    Write-Host "Timeout waiting for Oracle Database. Please check if the container is running properly." -ForegroundColor Red
    return $false
}

# Function to execute SQL script in Oracle as a specific user
function Invoke-OracleSqlAsUser {
    param(
        [string]$SqlFile,
        [string]$OracleHostName,
        [string]$Port,
        [string]$Service,
        [string]$User,
        [string]$Password
    )
    
    Write-Host "Executing SQL script: $SqlFile as user $User" -ForegroundColor Cyan
    
    # Copy SQL file to container
    docker cp "$SqlFile" oracle_db:/tmp/$(Split-Path $SqlFile -Leaf)
      # Execute SQL script
    $scriptName = Split-Path $SqlFile -Leaf
    docker exec oracle_db sqlplus -s "$User/$Password@${OracleHostName}:${Port}/$Service" "@//tmp/$scriptName"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SQL script executed successfully: $SqlFile" -ForegroundColor Green
        return $true
    } else {
        Write-Host "Error executing SQL script: $SqlFile" -ForegroundColor Red
        return $false
    }
}

# Function to execute SQL script in Oracle
function Invoke-OracleSql {
    param(
        [string]$SqlFile,
        [string]$OracleHostName,
        [string]$Port,
        [string]$Service,
        [string]$SysPassword
    )
    
    Write-Host "Executing SQL script: $SqlFile" -ForegroundColor Cyan
    
    # Copy SQL file to container
    docker cp "$SqlFile" oracle_db:/tmp/$(Split-Path $SqlFile -Leaf)
      # Execute SQL script
    $scriptName = Split-Path $SqlFile -Leaf
    docker exec oracle_db sqlplus -s "sys/$SysPassword@${OracleHostName}:${Port}/$Service as sysdba" "@//tmp/$scriptName"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SQL script executed successfully: $SqlFile" -ForegroundColor Green
        return $true
    } else {
        Write-Host "Error executing SQL script: $SqlFile" -ForegroundColor Red
        return $false
    }
}

# Main execution
try {
    # Check if Docker is running
    docker ps > $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Docker is not running. Please start Docker first." -ForegroundColor Red
        exit 1
    }
    
    # Check if Oracle container is running
    $oracleContainer = docker ps --filter "name=oracle_db" --format "table {{.Names}}" | Select-String "oracle_db"
    if (-not $oracleContainer) {
        Write-Host "Oracle container is not running. Starting Docker Compose..." -ForegroundColor Yellow
        docker-compose up -d oracle
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to start Oracle container." -ForegroundColor Red
            exit 1
        }
    }
    
    # Wait for Oracle to be ready
    if (-not (Wait-ForOracle -OracleHostName $OracleHost -Port $OraclePort -Service $OracleService -SysPassword $OraclePassword)) {
        exit 1
    }
    
    # Get the directory where this script is located
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $initScriptsDir = Join-Path $scriptDir "init_scripts"
    
    # Execute tablespace creation
    $tablespaceScript = Join-Path $initScriptsDir "create_tablespace.sql"
    if (Test-Path $tablespaceScript) {
        if (-not (Invoke-OracleSql -SqlFile $tablespaceScript -OracleHostName $OracleHost -Port $OraclePort -Service $OracleService -SysPassword $OraclePassword)) {
            Write-Host "Warning: Tablespace creation failed. It might already exist." -ForegroundColor Yellow
        }
    }
      # Execute user creation
    $userScript = Join-Path $initScriptsDir "create_user.sql"
    if (Test-Path $userScript) {        if (Invoke-OracleSql -SqlFile $userScript -OracleHostName $OracleHost -Port $OraclePort -Service "XE" -SysPassword $OraclePassword) {
            Write-Host "User C##DM_ACADEMICO created successfully!" -ForegroundColor Green
        } else {
            Write-Host "Failed to create user C##DM_ACADEMICO" -ForegroundColor Red
            exit 1
        }
    }
    
    # Execute database schema creation
    $dataDir = Join-Path $scriptDir "data"
    $schemaScript = Join-Path $dataDir "dm_academico.sql"
    if (Test-Path $schemaScript) {
        Write-Host "Creating database schema and tables..." -ForegroundColor Yellow
        if (Invoke-OracleSqlAsUser -SqlFile $schemaScript -OracleHostName $OracleHost -Port $OraclePort -Service $OracleService -User "C##DM_ACADEMICO" -Password "YourPassword123") {
            Write-Host "Database schema created successfully!" -ForegroundColor Green
        } else {
            Write-Host "Warning: Schema creation failed. Tables might already exist." -ForegroundColor Yellow
        }
    } else {
        Write-Host "Warning: Schema file not found: $schemaScript" -ForegroundColor Yellow
    }
    
    Write-Host "" -ForegroundColor White
    Write-Host "=== Oracle Database Setup Complete ===" -ForegroundColor Green
    Write-Host "You can now use the following connection details:" -ForegroundColor Cyan
    Write-Host "Host: $OracleHost" -ForegroundColor White
    Write-Host "Port: $OraclePort" -ForegroundColor White
    Write-Host "Service: $OracleService" -ForegroundColor White
    Write-Host "User: C##DM_ACADEMICO" -ForegroundColor White
    Write-Host "Password: YourPassword123" -ForegroundColor White
    Write-Host ""
    Write-Host "Environment variables for .env file:" -ForegroundColor Cyan
    Write-Host "ORACLE_HOST=$OracleHost" -ForegroundColor White
    Write-Host "ORACLE_PORT=$OraclePort" -ForegroundColor White
    Write-Host "ORACLE_SERVICE=$OracleService" -ForegroundColor White
    Write-Host "ORACLE_USER=C##DM_ACADEMICO" -ForegroundColor White
    Write-Host "ORACLE_PASSWORD=YourPassword123" -ForegroundColor White
    
} catch {
    Write-Host "An error occurred: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
