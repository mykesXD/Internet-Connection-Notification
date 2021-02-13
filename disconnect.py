import os
import io
import subprocess
import time
import sys
from win10toast import ToastNotifier
from datetime import datetime,timedelta


toast = ToastNotifier()
online = True
waiting = False
disconnected = False
IPAddress = "google.com" #Put here your IP Address that you wish to ping or you can just leave it like this
lastTime = "that im going to code this"
print("Loading...")
def ping(ip):
    ip = ip.split()
    ping = ip[4][5:]
    os.system("cls")
    print("Ping = " + ping.decode("utf-8"))
def checkConnection():
    global disconnected
    global waiting
    global online
    global lastTime
    output = subprocess.check_output(f"ping -n 1 {IPAddress} | find \"TTL\"", shell=True)
    if disconnected == False:
        currentTime = datetime.now()
        lastTime = currentTime.strftime("%H:%M:%S")
        disconnected = True
        toast.show_toast("Internet CONNECTED","Have fun surfing!",duration=5,icon_path="internetOn.ico")
    online = False
    waiting = False
    ping(output)
def sendNotification():
    global disconnected
    global waiting
    global online
    global lastTime
    if online == False:
        currentTime = datetime.now()
        FMT = '%H:%M:%S'
        upTime = datetime.strptime(currentTime.strftime("%H:%M:%S"), FMT) - datetime.strptime(lastTime, FMT)
        #if upTime.days < 0:
        #    upTime = timedelta(days=0,seconds=upTime.seconds, microseconds=upTime.microseconds)
        with io.open('data.txt', 'a', encoding='utf8') as f: 
            #my ISP support is shit so recording the disconnects to check patterns, collect evidence .etc and trying to uncover the culprit.
            text = currentTime.strftime("%Y-%m-%d,%H:%M:%S,")+str(upTime)+"\n"
            f.write(text)
        toast.show_toast("Internet DISCONNECTED","Unable to reach ISP...",duration=5,icon_path="internetOff.ico")
        disconnected = False
    else:
        if online == True and waiting == False:
            print("Your device is not connected to the internet.") #It has to be the ISP right? i checked everything 
            waiting = True #waiting for myself to die
    online = True
while(True):
    try:
        checkConnection()
        #Bonus feature while checking your internet connection :)
    except:
        time.sleep(3) #Waits for 3 seconds in case it's just a packet loss. If it goes on longer than 3 seconds? too bad. Suck on this fake alert
        try:
            checkConnection()
        except:
            sendNotification()
    time.sleep(1)
