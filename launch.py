"""
Launch script for Pizza Customer Service Agent
Starts both FastAPI backend and Streamlit frontend
"""

import subprocess
import sys
import time
import signal
from pathlib import Path

# Store process references
processes = []


def signal_handler(sig, frame):
    """Handle Ctrl+C to gracefully shutdown"""
    print("\n\nShutting down...")
    for process in processes:
        process.terminate()
    sys.exit(0)


def main():
    """Launch both backend and frontend"""
    
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print("Starting Pizza Customer Service Agent")
    
    # Get project root
    project_root = Path(__file__).parent
    
    # Start FastAPI backend
    print("\n[1/2] Starting FastAPI backend on http://localhost:8000...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=project_root
    )
    processes.append(backend_process)
    
    # Wait for backend to start
    time.sleep(3)
    
    # Start Frontend (Static File Server)
    print(f"[2/2] Starting Static Frontend on http://localhost:3000...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3000", "--directory", "frontend"],
        cwd=project_root
    )
    processes.append(frontend_process)
    
    print("\n" + "=" * 60)
    print("Application is running!")
    print("=" * 60)
    print("\nBackend API:  http://localhost:8000")
    print("Frontend UI:  http://localhost:3000")
    print("API Docs:     http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all services\n")
    
    # Wait for processes
    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()
