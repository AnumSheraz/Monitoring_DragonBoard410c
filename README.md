# Monitoring_DragonBoard410c

This is the Linux version of Monitoring your DragonBoard project taught in Internet of Things Specilization courses 2 and 3 from Coursera. 

A Flask web server is established that is handeling all the redirecting routes. The description of each routes is as follows;

1. Main page      : Hello.html page will be opened, which is a welcome page, indicating all the redirecting routes of the server.
2. /status        : Displays the health status of dragonBoard in raw json format.
3. /status/preety : Displays the health status of dragonBoard in a well-structured json format.
4. /status/live   : Opens a live.html page that indicates a real-time view of dragonBoard health status. AJAX requests are send 
                    after every 200ms to update the json data.

5. /?led=<name_of_led>&times=<blinking_time>: arguments used for controlling the actuators led's. i.e. to blink red led for 10                                                 times, we write /?led=red&times=10.

Videos:
Part 1 (code description):
https://www.youtube.com/watch?v=KCLbXccz4qQ

Part 2 (DEMO):
https://www.youtube.com/watch?v=hSS_GQmiHd4

