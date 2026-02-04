import subprocess
import time
import os
import signal
import sys
import threading

def stream_output(process, prefix):
    """
    Streams output from a process and prints it with a prefix.
    """
    try:
        for line in iter(process.stdout.readline, ''):
            if not line:
                break
            print(f"[{prefix}] {line.strip()}")
    except Exception as e:
        print(f"[{prefix}] Error reading output: {e}")
    finally:
        process.stdout.close()

def run_project():
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BACKEND_DIR = os.path.join(BASE_DIR, "backend")
    FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

    print("\n🚀 Starting AgroGPT Enterprise System...")
    print("---------------------------------------")

    # 1. Start Backend
    print("🌱 Launching Backend (FastAPI)...")
    backend_env = os.environ.copy()
    
    # We use uvicorn via module execution to ensure the current env's uvicorn is used
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000", "--host", "127.0.0.1"],
        cwd=BACKEND_DIR,
        env=backend_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Start thread to show backend logs
    backend_thread = threading.Thread(target=stream_output, args=(backend_process, "BACKEND"), daemon=True)
    backend_thread.start()

    # Wait a moment for backend to initialize
    time.sleep(3)

    # 2. Start Frontend
    print("🎨 Launching Frontend (React)...")
    npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
    
    frontend_process = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=FRONTEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Start thread to show frontend logs
    frontend_thread = threading.Thread(target=stream_output, args=(frontend_process, "FRONTEND"), daemon=True)
    frontend_thread.start()

    print("---------------------------------------")
    print("✅ System Initialization Commands Sent!")
    print("   👉 Frontend: http://localhost:5173")
    print("   👉 Backend:  http://localhost:8000")
    print("---------------------------------------")
    print("Observation mode active. Press Ctrl+C to stop servers...")

    try:
        while True:
            time.sleep(1)
            # Check if processes are still alive
            if backend_process.poll() is not None:
                print(f"❌ Backend process terminated with exit code {backend_process.returncode}")
                break
            if frontend_process.poll() is not None:
                print(f"❌ Frontend process terminated with exit code {frontend_process.returncode}")
                break
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
    finally:
        # Cleanup
        if backend_process.poll() is None:
            if os.name == 'nt':
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(backend_process.pid)], capture_output=True)
            else:
                backend_process.terminate()
        
        if frontend_process.poll() is None:
            if os.name == 'nt':
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(frontend_process.pid)], capture_output=True)
            else:
                frontend_process.terminate()
        
        print("👋 Status: All processes terminated. Goodbye!")

if __name__ == "__main__":
    run_project()
