#!/bin/bash

# HRM Project - Startup Script for Linux/Mac
# Usage: ./run_dev.sh [command]
# Commands: web, celery, beat, all, stop

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print header
echo ""
echo "=================================================="
echo "HRM Project - Development Server Startup"
echo "=================================================="
echo ""

# Check if python is available
if ! command -v python &> /dev/null; then
    echo -e "${RED}ERROR: Python not found. Please install Python or activate virtual environment.${NC}"
    exit 1
fi

# Check if in virtual environment
if [[ -z "$VIRTUAL_ENV" ]] && [[ ! -f "venv/bin/activate" ]]; then
    echo -e "${YELLOW}WARNING: Virtual environment not activated. Consider running:${NC}"
    echo "  source venv/bin/activate  (Linux/Mac)"
    echo "  or"
    echo "  venv\Scripts\activate  (Windows)"
    echo ""
fi

# Parse arguments
COMMAND="${1:-all}"

case "$COMMAND" in
    web)
        echo -e "${BLUE}Starting Django Development Server...${NC}"
        echo -e "${BLUE}Server will be available at: http://localhost:8000${NC}"
        python manage.py runserver
        ;;
    
    celery)
        echo -e "${BLUE}Starting Celery Worker...${NC}"
        echo -e "${YELLOW}Make sure Redis is running on localhost:6379${NC}"
        celery -A config worker -l info
        ;;
    
    beat)
        echo -e "${BLUE}Starting Celery Beat (Scheduler)...${NC}"
        echo -e "${YELLOW}Make sure Redis is running on localhost:6379${NC}"
        celery -A config beat -l info
        ;;
    
    redis)
        echo -e "${BLUE}Starting Redis Server...${NC}"
        if ! command -v redis-server &> /dev/null; then
            echo -e "${RED}ERROR: redis-server not found. Please install Redis.${NC}"
            echo "  macOS: brew install redis"
            echo "  Ubuntu/Debian: sudo apt-get install redis-server"
            echo "  Or download from: https://redis.io/download"
            exit 1
        fi
        redis-server
        ;;
    
    all)
        echo ""
        echo -e "${GREEN}To run all services, open multiple terminal windows and run:${NC}"
        echo ""
        echo -e "${YELLOW}Terminal 1 - Redis:${NC}"
        echo "  ./run_dev.sh redis"
        echo ""
        echo -e "${YELLOW}Terminal 2 - Django Web Server:${NC}"
        echo "  ./run_dev.sh web"
        echo ""
        echo -e "${YELLOW}Terminal 3 - Celery Worker:${NC}"
        echo "  ./run_dev.sh celery"
        echo ""
        echo -e "${YELLOW}Terminal 4 (Optional) - Celery Beat:${NC}"
        echo "  ./run_dev.sh beat"
        echo ""
        echo -e "${GREEN}Or use Docker:${NC}"
        echo "  docker-compose up -d --build"
        echo ""
        ;;
    
    stop)
        echo ""
        echo -e "${YELLOW}To stop services:${NC}"
        echo "  - Press Ctrl+C in each terminal window"
        echo ""
        echo -e "${YELLOW}Or with Docker:${NC}"
        echo "  docker-compose down"
        echo ""
        ;;
    
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        echo ""
        echo -e "${GREEN}Available commands:${NC}"
        echo "  web   - Start Django development server"
        echo "  celery- Start Celery worker"
        echo "  beat  - Start Celery beat scheduler"
        echo "  redis - Start Redis server"
        echo "  all   - Show instructions for running all services"
        echo "  stop  - Show how to stop services"
        echo ""
        exit 1
        ;;
esac
