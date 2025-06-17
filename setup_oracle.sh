#!/bin/bash
# Oracle Database Setup Script for Unix/Linux (Bash)
# This script configures the Oracle database after Docker Compose starts

# Default configuration
ORACLE_HOST="${ORACLE_HOST:-localhost}"
ORACLE_PORT="${ORACLE_PORT:-1521}"
ORACLE_SERVICE="${ORACLE_SERVICE:-XEPDB1}"
ORACLE_PASSWORD="${ORACLE_PASSWORD:-YourStrongPassword123}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Oracle Database Setup Script ===${NC}"
echo -e "${YELLOW}Configuring Oracle Database for DM_ACADEMICO...${NC}"

# Function to wait for Oracle to be ready
wait_for_oracle() {
    local service=$3
    local password=$4
    local max_retries=${5:-60}
    local retry_interval=${6:-15}
    
    echo -e "${YELLOW}Waiting for Oracle Database to be ready...${NC}"
    
    for ((i=1; i<=max_retries; i++)); do
        if docker exec oracle_db bash -c "echo 'SELECT 1 FROM DUAL;' | sqlplus -s sys/$password@XE as sysdba" >/dev/null 2>&1; then
            echo -e "${GREEN}Oracle Database is ready!${NC}"
            return 0
        fi
        
        echo -e "${YELLOW}Attempt $i/$max_retries - Oracle not ready yet. Waiting $retry_interval seconds...${NC}"
        sleep $retry_interval
    done
    
    echo -e "${RED}Timeout waiting for Oracle Database. Please check if the container is running properly.${NC}"
    return 1
}

# Function to execute SQL script in Oracle
execute_oracle_sql() {
    local sql_file=$1
    local service=$4
    local password=$5
    
    echo -e "${CYAN}Executing SQL script: $sql_file${NC}"
    
    # Copy SQL file to container
    docker cp "$sql_file" "oracle_db:/tmp/$(basename "$sql_file")"
    
    # Execute SQL script
    local script_name
    script_name=$(basename "$sql_file")
    # Use XE (CDB root) for all SQL scripts since they handle container switching internally
    if docker exec oracle_db sqlplus -s sys/$password@XE as sysdba "@/tmp/$script_name"; then
        echo -e "${GREEN}SQL script executed successfully: $sql_file${NC}"
        return 0
    else
        echo -e "${RED}Error executing SQL script: $sql_file${NC}"
        return 1
    fi
}

# Main execution
main() {
    # Check if Docker is running
    if ! docker ps >/dev/null 2>&1; then
        echo -e "${RED}Docker is not running. Please start Docker first.${NC}"
        exit 1
    fi
    
    # Check if Oracle container is running
    if ! docker ps --filter "name=oracle_db" --format "table {{.Names}}" | grep -q "oracle_db"; then
        echo -e "${YELLOW}Oracle container is not running. Starting Docker Compose...${NC}"
        if ! docker-compose up -d oracle; then
            echo -e "${RED}Failed to start Oracle container.${NC}"
            exit 1
        fi
    fi
    
    # Wait for Oracle to be ready
    if ! wait_for_oracle "" "" "$ORACLE_SERVICE" "$ORACLE_PASSWORD"; then
        exit 1
    fi
    
    # Get the directory where this script is located
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    INIT_SCRIPTS_DIR="$SCRIPT_DIR/init_scripts"
    
    # Execute tablespace creation
    TABLESPACE_SCRIPT="$INIT_SCRIPTS_DIR/create_tablespace.sql"
    if [[ -f "$TABLESPACE_SCRIPT" ]]; then
        if ! execute_oracle_sql "$TABLESPACE_SCRIPT" "" "" "$ORACLE_SERVICE" "$ORACLE_PASSWORD"; then
            echo -e "${YELLOW}Warning: Tablespace creation failed. It might already exist.${NC}"
        fi
    fi
    
    # Execute user creation
    USER_SCRIPT="$INIT_SCRIPTS_DIR/create_user.sql"
    if [[ -f "$USER_SCRIPT" ]]; then
        if execute_oracle_sql "$USER_SCRIPT" "" "" "$ORACLE_SERVICE" "$ORACLE_PASSWORD"; then
            echo -e "${GREEN}User C##DM_ACADEMICO created successfully!${NC}"
        else
            echo -e "${RED}Failed to create user C##DM_ACADEMICO${NC}"
            exit 1
        fi
    fi
    
    # Execute database schema creation
    DATA_DIR="$SCRIPT_DIR/data"
    SCHEMA_SCRIPT="$DATA_DIR/dm_academico.sql"
    if [[ -f "$SCHEMA_SCRIPT" ]]; then
        echo -e "${YELLOW}Creating database schema and tables...${NC}"
        if execute_oracle_sql "$SCHEMA_SCRIPT" "" "" "$ORACLE_SERVICE" "$ORACLE_PASSWORD"; then
            echo -e "${GREEN}Database schema created successfully!${NC}"
        else
            echo -e "${YELLOW}Warning: Schema creation failed. Tables might already exist.${NC}"
        fi
    else
        echo -e "${YELLOW}Warning: Schema file not found: $SCHEMA_SCRIPT${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}=== Oracle Database Setup Complete ===${NC}"
    echo -e "${CYAN}You can now use the following connection details:${NC}"
    echo -e "${WHITE}Host: $ORACLE_HOST${NC}"
    echo -e "${WHITE}Port: $ORACLE_PORT${NC}"
    echo -e "${WHITE}Service: $ORACLE_SERVICE${NC}"
    echo -e "${WHITE}User: C##DM_ACADEMICO${NC}"
    echo -e "${WHITE}Password: YourPassword123${NC}"
    echo ""
    echo -e "${CYAN}Environment variables for .env file:${NC}"
    echo -e "${WHITE}ORACLE_HOST=$ORACLE_HOST${NC}"
    echo -e "${WHITE}ORACLE_PORT=$ORACLE_PORT${NC}"
    echo -e "${WHITE}ORACLE_SERVICE=$ORACLE_SERVICE${NC}"
    echo -e "${WHITE}ORACLE_USER=C##DM_ACADEMICO${NC}"
    echo -e "${WHITE}ORACLE_PASSWORD=YourPassword123${NC}"
}

# Run main function
main "$@"
