# Project Plan for Prelim | Created by Janrey Licas

## Devices To Be Used
We can have Raspberry Pi (3B / 4B) as a web server
NodeMCU (ESP8266) can be denoted as main part of each classroom
	Here for instance, we have two miniature classrooms to be installed in this part of project showcasing.

## NodeMCU Context
NodeMCU contains the following sensors to be used to scan the classroom:
1. PIR Motion Sensor
2. Temperature and Humidity Sensor
3. Fingerprint Sensor
4. and lastly Relay Module
## Notes
This might be enough for the NodeMCU to function properly. So I guess it's not possible to have an insufficient number of pins
to be used here.

In some cases, NodeMCU may require to use any heatsinks, we don't know how hot is it gonna get.
But the good news here is that, we could usually do anything faster in NodeMCU part. That's because it only does Sensor Reading and wait commands to the python django server.


## Some Questionable Ethics
* WE CANNOT put all MCUs to interfaces via USB. Because we might be questioned, what if the classroom is so far from the server, are we still gonna use USB to interface with the server? No.
* If we used Wireless AP to communicate with the server, then we can place the classroom at any limited possible range.

## Raspberry Pi Intentions
In Raspberry Pi, that MCU will be the act as a main server. The thing that is dependent variable here is just the switch from where Raspberry Pi can make connections to every MCU.

Raspberry Pi literally just functions as a web server, no other such expected GPIO to be used. NodeMCU plays that part.

## Communication Data Layout
In NodeMCU, we usually send the data usually in dictionary format. This gives us the ability to access the data safely and easy.

For instance, `{'classroom_electricty':'enabled', 'classroom_temp','31C'}`

In NodeMCU, we usually have to send different types of data towards raspberry pi.
> We have 3 types of data.
- Authentication
- - Dictionary Keys and Their Expected Result
- - - `sdsdsd`
- Sensor Data
- - Dictionary Keys and Their Expected Result
- - - `sdsdsd`
- Relay Status
- - Dictionary Keys and Their Expected Result
- - - `sdsdsd`

### Protocols
Here lies, the protocols set about how much query should we have done at a minute or something else, something like that.
	- Release Information of at least 1 Minute for NodeMCU Sensors Info
	- Give Information Instantly at Commands of Authentication and Relay Modules and React Immediately

** Slightly on confirmed. In any case, we should do review about the things that we have said here sooner or later.

## DJango Server Context
Raspberry Pi Django Server usually needs the following views:
- Login, ITSO Supervisor and Teachers
- - Dashboard, Both for (1) ITSO Supervisor and (2) Teachers
- - - Usually contains the following:
- - - - (1) ITSO Supervisor
- - - - - See Classroom Logs | Recent Activity
- - - - - See Classroom Information and Sensors
- - - - - See Classroom Schedules (I guess?)
- - - - - Enable / Disable Use Out of Classroom (Override)
- - - - - Add Classroom (Hardworking Feature / To Be Done On Future / Design Only)
- - - - - Manually Turn Off Classroom Electricity
- - - - - Explicit Lock and Unlock Classroom (Doesn't Need Any Card To Bypass)
- - - - (2) Teachers
- - - - - See Classroom Information and Sensors
- - - - - Enable / Disable Use Out of Classroom (Override, At Their Time)
- - - - - Manually Turn Off Classroom Electricity At Their Time

## App Directories
- /home
- - /login
- - /<user_info>/
- - - /dashboard
- - - /classroom // Shows All Classroom as List
- - - - /classroom/<clasroom_number>/logs
- - - - /classroom/<clasroom_number>/info
- - - - /classroom/<clasroom_number>/schedule
- - - - /classroom/<clasroom_number>/actions/electricity=enable | disable
- - - - /classroom/<clasroom_number>/actions/lock | unlock = true | false



## Database
Since we read multiple articles to use MQTT broker. We have to do somethin other than that. Since, we want to run
multiple instance of particular programs, I have to laid out all database that shows distinct clear sense of what're we about to do.
- DJango DB | Staff and Teachers and their Unique Authentication
- External  | Temperature and Sensors, Requires View for DJango To Read Those At Database
- DJango DB | Classroom Information
- DJango DB | Classroom Recent Activity Logging

** That is all.

From this day, January 14 at 9:17. I'm expecting to be at 50% at February 14 in any case on where disturbance is present.