
from PIL import Image
import pyautogui
import qrcode
import time
import socket
import sys
import subprocess
import re



def GetIp():
    """
    Get the computers ip address
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    name = s.getsockname()[0]
    s.close()
    return name

def GenerateQr(data):
    """
    Receives data which corresponds to the link of the website controller, generates a qr code, saves the qr code and opens the image with windows photo viewer
    data -> string
    """    
    img = qrcode.make(data)
    img.save("connect.jpg")

    im = Image.open("connect.jpg")
    
    im.show()


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)


def stopMusic():
    """
    To be called by the flask server, it will stop whatever music is playing
    """
    p = subprocess.Popen(["TASKKILL", "/IM", "vlc.exe"])
    print("Music has been stopped")


def startMusic(path):
    """
    To be called by the flask server. Will receive a path to a music and start playing that music is
    path -> string (path from server)
    """
    p = subprocess.Popen(["vlc", path])
    print(f"Music {path} has started")
    return True



def changeVolume(increment):
    message = "volumeup" if increment > 0 else "volumedown" 
    for x in range(increment):
        pyautogui.press(message)
        time.sleep(0.1)