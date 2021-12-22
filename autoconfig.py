"""
Script that will configure vlc automatically
"""
import os


def autoconfig():

    currentPath = os.getcwd()

    path = os.getenv('APPDATA')
    array = os.listdir(path)

    print(array)
    if not "vlc" in array and not "VLC" in array:
        return False

    os.chdir(os.path.join(path, "vlc"))
    myFile = open("vlcrc", "a")
    print("file has been oppened")
    for line in myFile.readlines():
        print(line)
        if line[0] != "#":
            break

print("this is going to start")
autoconfig()



