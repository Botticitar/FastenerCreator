import uvicorn
import webbrowser
from threading import Timer
from stepgen_app.main import app

def open_browser():
    """Opens the local default web browser to the application address."""
    webbrowser.open("http://127.0.0.1:8080")

def main():
    Timer(1.5, open_browser).start()
    
    print("--- Bosch Fastener Generator ---")
    print("Launching Web GUI at http://127.0.0.1:8080")
    print("Press Ctrl+C to stop the server.")
    
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")

if __name__ == "__main__":
    main()