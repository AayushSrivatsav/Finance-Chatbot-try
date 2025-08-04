#!/bin/bash

# Finance RAG Chatbot Startup Script
# This script starts both the backend and frontend services

set -e

echo "🚀 Starting Finance RAG Chatbot..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    print_success "Python 3 found: $(python3 --version)"
}

# Check if Node.js is installed
check_node() {
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 16+ first."
        exit 1
    fi
    print_success "Node.js found: $(node --version)"
}

# Check if npm is installed
check_npm() {
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    print_success "npm found: $(npm --version)"
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r ../requirements.txt
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating example..."
        cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# News API Configuration
NEWS_API_KEY=your_news_api_key_here

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000

# RAG Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=text-embedding-ada-002
LLM_MODEL=gpt-3.5-turbo
EOF
        print_warning "Please edit backend/.env with your API keys before starting the application."
    fi
    
    cd ..
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    cd ..
}

# Start backend
start_backend() {
    print_status "Starting backend server..."
    
    cd backend
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Start the server
    print_success "Backend server starting on http://localhost:8000"
    python main.py &
    
    BACKEND_PID=$!
    echo $BACKEND_PID > backend.pid
    
    cd ..
}

# Start frontend
start_frontend() {
    print_status "Starting frontend server..."
    
    cd frontend
    
    print_success "Frontend server starting on http://localhost:3000"
    npm start &
    
    FRONTEND_PID=$!
    echo $FRONTEND_PID > frontend.pid
    
    cd ..
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for backend
    print_status "Waiting for backend..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            print_success "Backend is ready!"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "Backend failed to start within 30 seconds"
            exit 1
        fi
        sleep 1
    done
    
    # Wait for frontend
    print_status "Waiting for frontend..."
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            print_success "Frontend is ready!"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "Frontend failed to start within 30 seconds"
            exit 1
        fi
        sleep 1
    done
}

# Cleanup function
cleanup() {
    print_status "Shutting down services..."
    
    # Kill backend
    if [ -f "backend/backend.pid" ]; then
        kill $(cat backend/backend.pid) 2>/dev/null || true
        rm backend/backend.pid
    fi
    
    # Kill frontend
    if [ -f "frontend/frontend.pid" ]; then
        kill $(cat frontend/frontend.pid) 2>/dev/null || true
        rm frontend/frontend.pid
    fi
    
    print_success "Services stopped"
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup SIGINT

# Main execution
main() {
    print_status "Finance RAG Chatbot Startup Script"
    print_status "=================================="
    
    # Check prerequisites
    check_python
    check_node
    check_npm
    
    # Setup services
    setup_backend
    setup_frontend
    
    # Start services
    start_backend
    sleep 2
    start_frontend
    
    # Wait for services
    wait_for_services
    
    print_success "🎉 Finance RAG Chatbot is running!"
    print_status "Frontend: http://localhost:3000"
    print_status "Backend API: http://localhost:8000"
    print_status "API Docs: http://localhost:8000/docs"
    print_status ""
    print_status "Press Ctrl+C to stop all services"
    
    # Keep script running
    wait
}

# Run main function
main 