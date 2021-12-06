
import os
import sys
import socket
import signal
import asyncio
import subprocess
import websockets
import http.server
import multiprocessing

import pyautogui
import qrcode
from PIL import Image

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



#vou querer ver o meu ip
#vou querer lancar um thread para o web server
#vou querer mostrar um qr code para ligar ao site



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
            p = subprocess.Popen(["vlc", fileList[int(message)]])
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
    fileList = [x for x in os.listdir("cantados") if x.split(".")[-1] == "mp4"]
    

    print("Starting server")

    myIp = GetIp()
    port = 4443
    myServer = multiprocessing.Process(target=WebServer, args=(myIp,port,))
    myServer.start()

    GenerateQr(f"http://{myIp}:{port}")

    print("Starting socket")
    asyncio.get_event_loop().run_until_complete(websockets.serve(echo, myIp, 4442))
    asyncio.get_event_loop().run_forever()


