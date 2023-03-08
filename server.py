from flask import Flask, render_template, url_for, send_from_directory
from funcs import GetIp, GenerateQr, sorted_alphanumeric, stopMusic, startMusic, changeVolume

import sys
import os



print("Hello world")
app = Flask(__name__)



#home webpage
@app.route('/')
def home():
    return render_template('home.html')


#page to start the music
@app.route("/start/<number>")
def startPlaying(number):
    print(f"Should start this music {number}")
    if int(number) > len(fileList):
        print(f"  Requested music {number} does not exist")
        return("failed")
    path = fileList[int(number) - 1]

    if startMusic(path):
        return ("accepted")
    else:
        return ("failed")

#page to stop the music
@app.route("/stop")
def stopPlaying():

    #will i need to check if the music is playing?
    print("This should stop the music")
    stopMusic()
    return ("stopped")

#page for volume changes
@app.route("/volume/<increment>")
def changeVol(increment):
    print(f"Should change the volume by: {increment}")
    changeVolume(int(increment))
    return ("volumechange")



#import the js files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    

    print("UI pid - ", sys.argv[1])
    exit()

    fileList = [os.path.join("cantados", x) for x in os.listdir("cantados") if x.split(".")[-1] == "mp4" or x.split(".")[-1] == "mkv"]
    fileList = sorted_alphanumeric(fileList)  
    
    myIp = GetIp()
    port = 4443

    print(f"Starting server http://{myIp}:{port}")


    GenerateQr(f"http://{myIp}:{port}")
    print("Starting Server")
    app.run(host=myIp, port=4443, debug=False)