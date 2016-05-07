# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 15:27:38 2016

@author: Anum Sheraz
"""

import json, time, psutil
from flask import render_template, request
import flask, socket
import threading
from wifi import Cell
from GPIOLibrary import GPIOProcessor

GP = GPIOProcessor()

app = flask.Flask(__name__)

ipaddress=socket.gethostbyname(socket.gethostname())
print ipaddress
PORT_NUMBER = 8040
count = 0
red_led_T_lock = threading.Lock()
yellow_led_T_lock = threading.Lock()
green_led_T_lock = threading.Lock()
 


my_dict={
          "status":{
                 "Computation":{
                         "Cores":4,
                         "CPU_Usage":"35%",
                         "Memory_usage":"15.04%"
                         },
                 "Networks":{
                         "Bluetooth":True,
                         "Location_Service":"true",
                         "Wifi":{
                            "SSID": "\"Samsung S4\"",
                            "status": True                           
                             }
                         },
                         
                  "GPIO":[
                          {
                            "GPIO number": "23",
                            "value":0,
                            "Direction":"out",
                          },
                          {
                            "GPIO number": "24",
                            "value":0,
                            "Direction":"out"
                          },                      
                          {
                            "GPIO number": "25",
                            "value":0,
                            "Direction":"out"
                          },
                          {
                            "GPIO number": "26",
                            "value":0,
                            "Direction":"out"
                          },                    
                          {
                            "GPIO number": "27",
                            "value":0,
                            "Direction":"out"
                          },
                          {
                            "GPIO number": "28",
                            "value":0,
                            "Direction":"out"
                          },  
                          {
                            "GPIO number": "29",
                            "value":0,
                            "Direction":"out"
                          },
                          {
                            "GPIO number": "30",
                            "value":0,
                            "Direction":"out"
                          }, 
                          {
                            "GPIO number": "31",
                            "value":0,
                            "Direction":"out"
                          },  
                          {
                            "GPIO number": "32",
                            "value":0,
                            "Direction":"out"
                          },
                          {
                            "GPIO number": "33",
                            "value":0,
                            "Direction":"out"
                          },                         
                         ],

                    "Peripherals":{
                    "USB":[
                       {
                        "Device":"usb devices"
                       }                    
                      ]                    
                    },
                    "Last_update":"time"                           
                 }
        }
        
try:
  a=Cell.all('wlan0')
  if len(a) > 0:
        ssid = a[0]       #Cell(ssid=Maxcotec)
        ssid = str(ssid)
        ssid = ssid[10:ssid.index(")")]        
        my_dict["status"]["Networks"]["Wifi"]["SSID"] = ssid
        my_dict["status"]["Networks"]["Wifi"]["status"] = "Connected"
  else:
        my_dict["status"]["Networks"]["Wifi"]["SSID"] = "--"   
        my_dict["status"]["Networks"]["Wifi"]["status"] = "Not Connected" 
except Exception as e:
    print e


@app.route('/status/update_status', methods=['POST'])
def keep_alive():
    global my_dict
    my_dict["status"]["Last_update"] = (time.ctime())
    #print my_dict["status"].get("Last_update")
    parsed_json = json.dumps(my_dict)  
    return (parsed_json)
    
@app.route("/", methods=['GET','POST'])
def login():
    #print 'HELLO DragonBoard' 
    if request.args.get('led'):
        led=request.args.get('led')
        if request.args.get('times'):
           times=request.args.get('times')
           print ' times:', times
           led_result=LED_control(led,times)
           led_json = {"status":led_result}
           return flask.jsonify(**led_json)  
        else:
           led_result=LED_control(led,"1") 
           led_json = {"status":led_result}
           return flask.jsonify(**led_json) 
    else:
        print 'got no LED'    
        return render_template('Hello.html')

@app.route("/status")
def status():
    global my_dict
    my_dict["status"]["Last_update"] = (time.ctime())
    
 
    parsed_json = json.dumps(my_dict ,indent=4,  separators=(',', ':'), sort_keys=True)     
    print parsed_json
    return (parsed_json)
    
@app.route("/status/preety")
def preety():
    global my_dict
    my_dict["status"]["Last_update"] = (time.ctime())
    return flask.jsonify(**my_dict)                

@app.route("/status/live")
def live():
    print 'sending live.html'
    return render_template('live.html') 

def processes():
    global my_dict
    while 1:
        time.sleep(0.05)
        my_dict["status"]["Computation"]["Cores"] = psutil.NUM_CPUS
        CPU_raw = psutil.cpu_percent()
        if CPU_raw != 0:
           CPU_Usage = (CPU_raw/(100))*100
           my_dict["status"]["Computation"]["CPU_Usage"] = str(CPU_Usage) + "%"
        RAM = psutil.virtual_memory()
        my_dict["status"]["Computation"]["Memory_usage"] = str(RAM[2]) + "%"
        

        
def LED_control(led,time):
     
      global red_led_T_lock, green_led_T_lock, yellow_led_T_lock
      if led == 'red':
         time = int(time)
         if red_led_T_lock.locked() == False:   
                red_thread = threading.Thread(target=red_led, args=(time,)) 
                red_thread.start()
                return 'ok'
         else:
            return 'red LED already in use'
             
      if led == 'yellow':
         time = int(time)
        
         if yellow_led_T_lock.locked() == False:
                yellow_thread = threading.Thread(target=yellow_led, args=(time,))
                yellow_thread.start()
                return 'ok'
         else:
            return 'yellow LED already in use'
             
      if led == 'green':
         time = int(time)
         
         if green_led_T_lock.locked() == False:
              green_thread = threading.Thread(target=green_led, args=(time,))           
              green_thread.start()
              return 'ok'
         else:
            return 'green LED already in use'
             
      if led == 'all':
         time = int(time)

         if red_led_T_lock.locked() == False and green_led_T_lock.locked() == False and yellow_led_T_lock.locked() == False:
               red_thread = threading.Thread(target=red_led, args=(time,))
               yellow_thread = threading.Thread(target=yellow_led, args=(time,))
               green_thread = threading.Thread(target=green_led, args=(time,))                
               red_thread.start()
               green_thread.start()
               yellow_thread.start()
               return 'ok'
         else:
             return 'All LED\'s are already in use'
      
def red_led(times):
      Pin25 = GP.getPin25()
      Pin25.out() 
      red_led_T_lock.acquire()
      try:
         for n in range(times):
            print 'RED high ' + str(n+1)
            time.sleep(0.5)
            Pin25.high()
            my_dict["status"]["GPIO"][2]["value"] = Pin25.getValue()            
            time.sleep(0.5) 
            Pin25.low() 
            my_dict["status"]["GPIO"][2]["value"] = Pin25.getValue()  
      finally:
          Pin25.closePin()      
          red_led_T_lock.release() 
           
  

def yellow_led(times):
      Pin24 = GP.getPin24()
      Pin24.out() 
      yellow_led_T_lock.acquire()
      try:
         for n in range(times):
            print 'yellow high ' + str(n+1) 
            time.sleep(0.5)
            Pin24.high()           
            my_dict["status"]["GPIO"][1]["value"] = Pin24.getValue()  
            time.sleep(0.5)
            Pin24.low() 
            my_dict["status"]["GPIO"][1]["value"] = Pin24.getValue()  
      finally:
          Pin24.closePin()      
          yellow_led_T_lock.release() 
         
        
def green_led(times):
      Pin23 = GP.getPin23()
      Pin23.out() 
      green_led_T_lock.acquire()
      try:
          for n in range(times):
                print 'green high ' + str(n+1)
                time.sleep(0.5)
                Pin23.high()
                time.sleep(0.5)
                Pin23.low()
                my_dict["status"]["GPIO"][0]["value"] = Pin23.getValue()  
      finally:
          Pin23.closePin()      
          green_led_T_lock.release() 
 


if __name__ == '__main__':
     get_data = threading.Thread(target=processes)
     get_data.start()

     app.run("192.168.1.15", threaded=True, debug=False, port=80)
