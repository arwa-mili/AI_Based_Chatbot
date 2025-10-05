#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

check_prerequisites() {
    print_info "Checking prerequisites..."
    
    local missing_deps=()
    
    if ! command_exists python3; then
        missing_deps+=("python3")
    fi
    
    if ! command_exists node; then
        missing_deps+=("node")
    fi
    
    if ! command_exists npm; then
        missing_deps+=("npm")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing dependencies: ${missing_deps[*]}"
        print_info "Please install the missing dependencies and try again."
        exit 1
    fi
    
    print_success "All prerequisites are installed"
}

# Setup backend
setup_backend() {
    print_info "Setting up Django backend..."
    
    cd back || exit 1
    
    if [ ! -d "venv" ]; then
        print_info "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    print_info "Installing Python dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Please create it before running the application."
    fi
    
    print_info "Running database migrations..."
    python manage.py migrate
    
    print_info "Seeding languages..."
    python manage.py seed_languages
    
    print_success "Backend setup completed"
    cd ..
}

# Setup frontend
setup_frontend() {
    print_info "Setting up React frontend..."
    
    cd front || exit 1
    
    if [ ! -d "node_modules" ]; then
        print_info "Installing npm dependencies..."
        npm install
        print_success "Frontend dependencies installed"
    else
        print_info "Node modules already exist. Skipping installation."
    fi
    
    print_success "Frontend setup completed"
    cd ..
}

run_backend() {
    print_info "Starting Django backend..."
    cd back || exit 1
    source venv/bin/activate
    python manage.py runserver &
    BACKEND_PID=$!
    print_success "Backend started (PID: $BACKEND_PID)"
    cd ..
}

# Run frontend
run_frontend() {
    print_info "Starting React frontend..."
    cd front || exit 1
    npm start &
    FRONTEND_PID=$!
    print_success "Frontend started (PID: $FRONTEND_PID)"
    cd ..
}



# Stop all processes
cleanup() {
    print_info "Stopping all processes..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        print_success "Backend stopped"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        print_success "Frontend stopped"
    fi
    
    # Kill any remaining node and python processes related to the project
    pkill -f "react-scripts start" 2>/dev/null
    pkill -f "manage.py runserver" 2>/dev/null
    
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

# Main script
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  setup       Setup both frontend and backend"
    echo "  run         Run both frontend and backend"
    echo "  all         Setup and run both frontend and backend"
    echo "  docker      Run using Docker"
    echo "  backend     Setup and run only backend"
    echo "  frontend    Setup and run only frontend"
    echo "  help        Show this help message"
    echo ""
}

# Parse command line arguments
if [ $# -eq 0 ]; then
    show_usage
    exit 0
fi

case "$1" in
    setup)
        check_prerequisites
        setup_backend
        setup_frontend
        print_success "Setup completed successfully!"
        ;;
    run)
        check_prerequisites
        run_backend
        run_frontend
        print_success "Application is running!"
        print_info "Backend: http://localhost:8000"
        print_info "Frontend: http://localhost:3000"
        print_info "Press Ctrl+C to stop all services"
        wait
        ;;
    all)
        check_prerequisites
        setup_backend
        setup_frontend
        run_backend
        run_frontend
        print_success "Application is running!"
        print_info "Backend: http://localhost:8000"
        print_info "Frontend: http://localhost:3000"
        print_info "Press Ctrl+C to stop all services"
        wait
        ;;
    backend)
        check_prerequisites
        setup_backend
        run_backend
        print_success "Backend is running at http://localhost:8000"
        print_info "Press Ctrl+C to stop the backend"
        wait
        ;;
    frontend)
        check_prerequisites
        setup_frontend
        run_frontend
        print_success "Frontend is running at http://localhost:3000"
        print_info "Press Ctrl+C to stop the frontend"
        wait
        ;;
    help)
        show_usage
        ;;
    *)
        print_error "Unknown option: $1"
        show_usage
        exit 1
        ;;
esac