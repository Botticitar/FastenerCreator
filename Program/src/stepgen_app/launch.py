import sys
import multiprocessing
import uvicorn
import time
import tkinter as tk
from stepgen_app.main import app
from stepgen_app.gui import FastenerApp
import os

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    os.chdir(bundle_dir)

def start_backend():
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")

def start_frontend():
    root = tk.Tk()
    gui_app = FastenerApp(root)
    root.mainloop()

def main():
    multiprocessing.set_start_method('spawn', force=True)
    
    backend_proc = multiprocessing.Process(target=start_backend, daemon=True)
    backend_proc.start()
    
    time.sleep(2)
    
    try:
        start_frontend()
    finally:
        backend_proc.terminate()

if __name__ == "__main__":
    main()