"""
Code for a simple ui that will control 
"""

import tkinter as tk
import subprocess
import signal
import sys
import os


class Ui:
    def __init__(self) -> None:
        self.createUi()

    def createUi(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.geometry("150x70")
        self.root.title("Server Control")

        # Create the "Stop Server" button
        self.stop_button = tk.Button(self.root, text="Stop Server", command=self.stop_server)
        self.stop_button.pack(padx=5, pady=5)

        # Create the "Refresh Server" button
        self.refresh_button = tk.Button(self.root, text="Refresh Server", command=self.refresh_server)
        self.refresh_button.pack(padx=5, pady=5)

        # Create the status label
        self.server_status
        self.server_status = "Running"
        self.status_label = tk.Label(self.root, text=f"Status: {self.server_status}")
        self.status_label.pack(padx=5, pady=5)


    def stop_server(self):
        self.server_status = "Stopped"
        self.update_status()

    def refresh_server(self):
        self.server_status = "Running"
        self.update_status()
        
    def update_status(self):
        self.status_label.config(text=f"Status: {self.server_status}")

    def start_server(self):
        # Start the main loop
        self.root.mainloop()

def alarm_handler(signum, frame):  
    global hasAnswered, serverPID

    print("Time to poke server")
    if hasAnswered == 0:
        # means that the server has not responded in the mean time
        print("  Server has not responded")
    
    hasAnswered = 0
    # Sending the poke signal
    os.pkill(serverPID, signal.)
# Register the alarm signal with our handler
signal.signal(signal.SIGALRM, alarm_handler)
 
signal.alarm(3)  # Set the alarm after 3 seconds  


if __name__ == "__main__":

    print("Starting ui")

    print("Launching the server")
    # start the ui
    process = subprocess.Popen(["python", "server.py", str(os.getpid())])

    print("Server pid - ", process.pid)
