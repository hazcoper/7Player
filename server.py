
import os
import re
import sys
import socket
import signal
import asyncio
import subprocess
import http.server
import multiprocessing

from PIL import Image
import websockets
import pyautogui
import qrcode

def signal_handler(sig, frame):
    print("Sinal para fechar foi recebido")
    myServer.terminate()
    sys.exit(0)

def killServer(sig, frame):
    global httpd

    print("Server has been told to shutdown")
    httpd.shutdown()

def GenerateQr(data):
    img = qrcode.make(data)
    img.save("connect.jpg")

    im = Image.open("connect.jpg")
    
    im.show()


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)


async def echo(websocket, path):
    async for message in websocket:
        
        print(f"Got a new message {message}")

        # proc = subprocess.Popen(f"vlc {fileList[int(message)]}", stdin = subprocess.PIPE, stdout = subprocess.PIPE)
        # os.system(f"vlc {fileList[int(message)]}")
        if not message.isdigit():
            #quer dizer que nao e um numero, entao vai ser volume up or volume down
            pyautogui.press(message)
            name = await websocket.send(f"volumechange")
        elif int(message) < len(fileList):
            print("sending message accepted")
            name = await websocket.send(f"accepted")
            p = subprocess.Popen(["vlc", fileList[int(message)-1]])
        else:
            print("sending message failsd")
            name = await websocket.send(f"failed")

def WebServer(ip, port):
    global httpd

    signal.signal(signal.SIGTERM, killServer)
    print("Starting Web Site")

    server_address = (ip, port)
    print(server_address)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

    httpd.serve_forever()

def GetIp():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    name = s.getsockname()[0]
    s.close()
    return name


if __name__ == "__main__":

    global myServer

    signal.signal(signal.SIGINT, signal_handler)
    fileList = [os.path.join("cantados", x) for x in os.listdir("cantados") if x.split(".")[-1] == "mp4" or x.split(".")[-1] == "mkv"]
    fileList = sorted_alphanumeric(fileList)    

    print("Starting server")

    myIp = GetIp()
    port = 4443
    myServer = multiprocessing.Process(target=WebServer, args=(myIp,port,))
    myServer.start()

    GenerateQr(f"http://{myIp}:{port}")

    print("Starting socket")
    asyncio.get_event_loop().run_until_complete(websockets.serve(echo, myIp, 4442))
    asyncio.get_event_loop().run_forever()


