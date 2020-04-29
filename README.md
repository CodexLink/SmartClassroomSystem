<h1 align="center">⛩  🏗 Smart Classroom ⌨ 🔥 </h1>

<h4 align="center"> An Embedded Systems and IoT 2nd Semester Project | Ease your class workflow by automating classroom access without the need of staff to open them for you. (Unless, you want to open parts of the room that is not designed to be accessed to you...)
</h4>
<div align="center">

![Coverage Status](https://img.shields.io/coveralls/github/CodexLink/SmartClassroomSystem?label=Code%20Coverage&logo=coveralls)
![Code Formatter](https://img.shields.io/badge/Code%20Formatter-YAPF-important)
![GitHub License](https://img.shields.io/github/license/CodexLink/SmartClassroomSystem?color=purple&label=Repo%20License)

</div>

<div align="center">

![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/codexlink/SmartClassroomSystem/master?label=CodeFactor%20Code%20Quality&logo=codefactor&logoColor=white)
![Codacy Branch Grade](https://img.shields.io/codacy/grade/f649c48ccc3a431a84cad2f7e7ac65ca/master?label=Codacy%20Code%20Quality&logo=codacy&logoColor=White)
![Dependabot Dependency Status](https://badgen.net/dependabot/CodexLink/SmartClassroomSystem/?icon=dependabot)

</div>

# Welcome

Hello! This is a repository dedicated to show the concept of a bare minimum IoT to server interaction and implementation. The concept consists of the system itself (excluding only the physical side of the project) which this concludes the context as the Smart Classroom System. It has the capabilities to reduce time consumption upon entering rooms that are authorized within the scope of a particular time.

## The Problem

Most of the day, one of the problems that the teacher and students always encountered when the class starts is the classroom locked. Sometimes, when your class is at 7:30 AM, it's safe to assume that your classroom is not yet opened. The fact that, any staff who is under those rooms are either late or literally just missing, for instance (breaktime, went out to go somewhere, etc.). Since, some of them never really learn. We have to do something about it. As those issues occur within the technology building. It's best to suit all classrooms with smart padlocks and other such. But the thing is, it is quite simple. So we have to come a more complex idea from the smart padlocks.

## The Solution

The solution was to create a Smart Classroom. The context was not all about the locks being smart padlocks. But rather, we should be able to control the whole classroom itself! From locks to electricity to environmental states. This kind of solution looks typical when looked from the outside. But if you look in the system itself, it is quite complex to do so, as it involves time and subject included and user fingerprint assignments.

## How does it work

The following consists of a various section in regards on how this system works.

### The Context

So basically, we want something to automate, right? The group managed to think of something that would help the techno core building of their school to be more technology-dependent. That is by, making all instructional rooms to be accessible without any on sight staff but only the authentication within your hands.

### The Wide Range of How It Works

So, **how does it really works!?**. In this system, we have a server and a client. The server can be Raspberry Pi 4B or any Server Computer and the Client is the NodeMCU. The server contains an accessible website to be used by staff and professors. The client which those are nodes, act as a receiver and status transmitter. Everytime there is a change in the classroom, the NodeMCU prepares the states in Dictionary Form everytime the server wants to query on the Nodes. Then the server process that state and assign those values in the database. Other than that, the server has the capability to send requests to the Nodes to change particular attributes of it. Such as the subject code to be assigned in front of the screen, explicitly change electricity and lock state without any authentication (exclusive for administrators only!).

## Table of Contents

This are the README Sections and Subsections. You can navigate through by clicking in one of those...

* ~~[Table of Contents](#table-of-contents)~~ (You're here.)
* [🔥 📁 File Structure Deconstruction](#file-structure-deconstruction)
* [Introduction to Requirements](#introduction-to-requirements)
  + [Hardware-Side Introduction](#hardware-side-introduction)
      - [Required Microcontroller](#required-microcontroller)
      - ["Why should I use ESP32 instead of ESP8266 / ESP8266EX?"](#-why-should-i-use-esp32-instead-of-esp8266---esp8266ex--)
      - [Required Components](#required-components)
  * [Software-Side Introduction](#software-side-introduction)
    + [Installation of Pre-requisites](#installation-of-pre-requisites)
      - [Upload the NodeMCU Sketch](#upload-the-nodemcu-sketch)
    + [Deployment](#deployment)
      - [Getting Started](#getting-started)
  * [Demo and Resources](#demo-and-resources)
    + [Advanced Context: Protocol](#advanced-context--protocol)
      - [Shutdown Timer Based on Motion Sensor Protocol](#shutdown-timer-based-on-motion-sensor-protocol)
      - [Classroom Locked State Change Protocol](#classroom-locked-state-change-protocol)
      - [Restrictive Accessibility Protocol](#restrictive-accessibility-protocol)
* [💁 ❔ Frequently Asked Questions](#-----frequently-asked-questions)
* [🏆 ✍ Authors](#-----authors)
* [📜 Various Credits](#---various-credits)
    + [🙇 Personal Credits](#---personal-credits)
    + [🏆  Library Credits](#----library-credits)
    + [📑  Documentation Credits](#----documentation-credits)
* [📚 License](#---license)

## 🔥 📁 File Structure Deconstruction |> [Go Back](#table-of-contents)

This repository contains a lot of varieties. Meaning you really have to know the path you're going before navigating any further without realizing where the heck are you even going... Just read it in a bare-minimum way and you will be fine 💯

```text
. <Repo Root Folder>/
├── .dependabot/ # Contains Dependabot Dependency Configuration...
│   └── config.yml
│
├── .github/ # Contains Workflow File...
│   └── workflow/
│       └── SketchWorker.yml # It is a sketch validator and worker. It outputs whether those sketches inside of the folder `NodeSketch_SC` will work or uploadable in MCU's memory.
│
├── .vscode/ # VSCode configuration.
│   └── *.json
│
├── Externals/
│   ├── AdLibs/ # Contains acknowledgement by talking to self on how to do it | Specifically made for CodexLink
│   │   └── *.md
│   │
│   ├── Commands/ # Contains only few preset commands that can be used to certain extreme conditions.
│   │   └── *.txt
│   │
│   ├── Project Plan/ # It consists of important notes to look up from what should be context of the project.
│   │   └── * .md
│   │
│   └── Sketch/
│       └── NodeSketch_SC/ # Specifically for NodeMCU Sketches.
│           ├── *.cpp
│           ├── *.h
│           └── *.ino
│
├── SmartClassroom/ # Django Project Folder
│   ├── DataSetBackups/
│   │   └── *.json
│   │
│   ├── NodeHandler/ # Django Micro App. This acknowledges any IoT MCUs by their own POST requests. This app could make changes to the databases.
│   │   ├── migrations/
│   │   │   ├── __pycache__/
│   │   │   │   └── *.pyc
│   │   │   │
│   │   │   └── __init__.py
│   │   │
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── SCControlSystem/ # Django Main Web App. This renders EVERYTHING that any user could access to...
│   │   ├── externs/
│   │   │   ├── __pycache__/
│   │   │   │   └── *.pyc
│   │   │   │
│   │   │   └── __init__.py
│   │   │
│   │   ├── management/
│   │   │   ├── __pycache__/
│   │   │   │   └── *.pyc
│   │   │   │
│   │   │   └── commands/
│   │   │       ├── backup_datasets.py
│   │   │       ├── create_definitive_groups.py
│   │   │       └── get_all_permissions.py
│   │   │
│   │   ├── migrations/ # Literally migrations...
│   │   │   ├── __pycache__/
│   │   │   │   └── *.pyc
│   │   │   │
│   │   │   └── __init__.py
│   │   │   └── ***(migrations_auto_...).py
│   │   │
│   │   ├── scripts/
│   │   │   ├── __pycache__/
│   │   │   │   └── *.pyc
│   │   │   │
│   │   │   └── SC_DSH.py # A script used by SC_ScriptInst.py. It was instantiated (spawns another window) to acknowledge IoT device communicating with the server. Requires Django-Extension to use this script.
│   │   │
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── SmartClassroom/ # Django Base Project Folder. Auto-generated by Django-admin.
│   │   ├── __pycache__/
│   │   │   └── *.pyc
│   │   │
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   └── urls.py
│   │
│   ├── static_src/ # Known as static source files. Those are used for rendering of styles and used for extra functionalities of the web-app itself.
│   │   └── css/
│   │   │   └── *.css / *.css.map
│   │   │
│   │   └── js/
│   │   │   └── *.js / *.min.js / *.js.map
│   │   │
│   │   └── rsrc/
│   │       └── *.jpg / *.png
│   │
│   ├── template_CALLABLE/ # Known as Preset Components. Those are callables and referrable to Class-Basediews.
│   │   ├── elem_inst_view.html
│   │   └── *noContextReponseOnly.html
│   │
│   ├── template_REQUIRE/ # Known as Modular Components. Those are Required Templates To Use by the template_CALLABLE HTML Candidates.
│   │   ├── footer.html
│   │   ├── header.html
│   │   ├── modals.html
│   │   ├── nav.html
│   │   └── sidebar.html
│   │
│   ├── template_REUSE/ # Known as Reusable Components. Those templates have it's own content and cannot be paired with another reusable component.
│   │   ├── 404.html
│   │   ├── classroom_control.html
│   │   ├── dashboard.html
│   │   ├── instance_listviewer.html
│   │   └── login.html
│   │
│   ├── usersrc/ # Contents that are user-generated. They will be used in rendering if provided by the user.
│   │   └── <Confidential...>
│   │
│   └── manage.py
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── SC_ScriptInst.py
```

## Introduction to Requirements |> [Go Back](#table-of-contents)

In this section, we're going to talk in the software-side and hardware-side. This should be enough if you're willing to duplicate this project both physically and virtually working. Keep in mind that this will be a bit hectic. So take time if you're willing to do something about this project.

### Hardware-Side Introduction |> [Go Back](#table-of-contents)

In this section, we will be slightly talking about the **required **microcontroller**,and the **required components**... Just so you know, ****this project is so expensive asf**** in the hardware stuff so that should be a spoiler alert for you. It took our allowance by 75% by the time we're buying the components. Anyway, let's get started.

#### Required Microcontroller |> [Go Back](#table-of-contents)

The most common typical microcontroller that the project uses is the NodeMCU v2 Lua ESP8266EX Version. We generally recommend using ESP32 which is just a slight realization after finishing this project. I myself, might guess this the PINS used in NodeMCU v2 Lua ESP8266EX Version is the same as ESP32. Though, I can't investigate further since I don't have ESP32 at the moment.

#### "Why should I use ESP32 instead of ESP8266 / ESP8266EX?" |> [Go Back](#table-of-contents)

The reason why is because of the Pin's Availability. I believe ESP32 pins are more accessible and less restrict when booting up than ESP8266. Sure, you could put a data pins on some parts of NodeMCU v2 ESP8266. But at some point in time, that would lead to boot failure. Please refer to some guides such as this [one](https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/). This site will really help you out on why investing to ESP32 is better than NodeMCU v2 Lua. Though if you think going for NodeMCU v3. The issue is literally quite the same. So be wise on what MCU to choose.

As long as the MCU has the capability to handle GT5X Instructions (For Fingerprint specifically...) and able to handle tasks by responding to requests both in POST and GET forms. And has the ability to handle the extensive stacked task as we have a Millis Management for Room Locks. Then you're good to go. Keep in mind the RAM is one of the factors to consider. As far as I developed it, I might be able to consume a lot of RAM for the tests.

#### Required Components |> [Go Back](#table-of-contents)

The components that we used, were essentially in my inventory already. So the cost of the project gets higher than I thought. That's because as a hobbyist, I find one of those are bare-minimum to withstand this project and able to make something out of it. So here's the list along with their intentions.

1. GT-521F32 Fingerprint Sensor
2. LCD 20x4 with (I^2)C Backpack
3. Two-Sided DIP Switch x2
4. PIR Motion Sensor HC-SR501
5. DC-DC Buck Converter 3A MP1584EN
6. DHT 11/22 Humidity and Temperature Module
7. Dupont-Type Jumper Wires (10 to 30 cm)
8. 12 V Powered Solenoid Lock (Magnetic)
9. 3-Channel Relay Module (with Octocoupler)
10. 12V Adapter to Jack Output (Recommended: 12V, Minimum: 9V)
11. (***Optional***) Bulb [1]
12. (***Optional***) Extension Cord [2]
13. (***Optional***) Raspberry Pi 4B [3]
14. (***Optional***) Router or Repeater [4]
15. (***Optional***) Power Jack [5]

- What's with the Adapter?
  - The reason why I gave parameters is because the project requires a voltage with sufficient reliability and better current. If you intent to make the project work by directly connecting the PWR to NodeMCU and let all components connected to it to VCC. You will feel that your NodeMCU's diode will collapse. This is where the buck converter comes in. You have to feed 9-12V to buck converter. Set output to 5.4 to 5.7V respectively. And put output in rail to be used by components + to be used by MCU via VIN pin.

  - Also, I included the minimum as a possible best minimum setup. As per the requirements says, we have 12V powered solenoid lock. That is where 12 V has to do something on it. If for in case, you have a solenoid lock or any kind of locks rated to 9V respectively. Then it is best to go for 9V Adapter. Just do the same setup as usual by setting buck converter output to given said respectively voltage and you're ready to go.

- Some components were indicated as ***optional***. Why?
  - We have ***several reasons***. For **[1]** and **[2]**, we have to indicate it as optional since we didn't provide schematics for our project. This was intended for the test of relay functionalities. For **[3]** and **[4]**, this was our usual setup. But due to Pandemic, we're unable to set it up. So instead of using it, we just use our home router and laptop to host the server. Though in this project, we already set compatibility for Raspberry Pi 4B Project Launch. Kinda a waste of time but support for it was a success. And lastly but not the least, the **[5]** power jack. This is indeed unusual, but if you're planning to use this, even as a module, it would be great! The setup of this project has a required parameter especially in the Voltage. The voltage of the project should be set to 5.4V to 5.7V. Going further down or going further up will result in unexpected behaviors!

I don't provide links to these components. That's because the supplier is not supporting different countries. So let's say we bought our parts in local shop. Which technically true. We will only provide links that supports delivery to other countries.

## Software-Side Introduction |> [Go Back](#table-of-contents)

In this section, I'll be talking from the scratch. Since this will be long enough, it's best to check the Demo and Resources Section and watch **Youtube Video Installation**. To get the knowledge on how to install the components of the project.

**DISCLAIMER**: The setup and deployment may slightly be different from what is being demonstrated in the youtube video! But the output will be the same.

### Installation of Pre-requisites |> [Go Back](#table-of-contents)

In order to move further to deployment section, I don't want to assume if you have anything installed. So it's best to install the packages / modules inside of the `requirements.txt`

1. To install, you have to change directory to the repository root level.
2. Type `pip install -r requirements.txt` and press enter.

With that, you should have the following packages / modules installed in your pip:

```text
Django (Version 3.0.5 and Above)
django_extensions (Version 2.2.9 and Above)
python-coveralls (Version 2.9.3 and Above)
coveralls (Version 2.0.0 and Above)
django-coverage-plugin (Version 1.8.0 and Above)
coverage (Version 5.1 and Above)
```

Since you have installed all of them its time to assume that you have a MariaDB Server that is online.

3. You have to create a database named `sc_db`. And leave it blank.

There will be a next step on how to put content in the `sc_db` database, so don't worry.

4. Next, we have to put models and migrations content in the `sc_db` database. With that, type `python manage.py makemigrations`.
5. Once done, type `python manage.py migrate` to apply all migrations that the Django did.
6. After that, setup up your superuser! Type `python manage.py createsuperuser` to fill the bare-minimum information needed.
7. Then, run `python manage.py runserver` and navigate to `localhost:8000` to see if things are working.

Congratulations! You did it. But that doesn't stop there. Because you have one thing left to do.

.... (***Required***) Upload NodeMCU Sketch.

#### Upload the NodeMCU Sketch |> [Go Back](#table-of-contents)

This is required since this will be your communicator in the server. To get started, follow the instructions below.

1. By File Manager / File Explorer, navigate to `Externals\Sketch\NodeSketch_SC`.

2. Open `NodeSketch_SC.ino`

3. At Line 38 Do EDIT the WiFi Target and it's credentials. The following has its own labels or required positional arguments / parameters, check `SmartClassroom.cpp` or `SmartClassroom.h`.
   - Ensure that you're connecting to where the server or the Django Server lives!

4. Connect all components to their corresponding PIN definitions declared at `SmartClassroom.h`.

5. Assuming you have NodeMCU device candidate in the board selection. (You can check by Tools > Board: XXXXXX). If NodeMCU did not show up. Then you might want to install ESP8266 package for Arduino IDE.

6. If for instance you, already have one. Then set the NodeMCU board as the target board. Set Upload Sketch From Ranges (115200 - 256000). The higher the better, the higher it is, the capacitor has to exist from EN to GND. (10uF Eletrolytic Cap).

7. Press Upload.

And... Done! Wait further and let the screen of the device to show the information such as the temperature and humidity, classroom subject and lock states.

### Deployment |> [Go Back](#table-of-contents)

In this section, we're going to talk about on how to deploy this project. The way you open the project is not intended or the usual way for this one. The project contains a script that could launch multiple instances of Command Prompts / Terminals.

Just to make things clear, there are at least three command prompts / terminal instances and those are:

1. Smart Classroom | Script Instantiator (***Base System*** | The One You Should Open)
2. Django Server Instance (Literally Runs inside ***SCControlSystem***)
3. Smart Classroom | Data Stream Handler (Inside ***SCControlSystem***, at Scripts Directory named SC_DSH.py)

#### Getting Started

1. Open your MySQL Server / MariaDB Server.
2. At the root of the repository folder, just launch `SC_ScriptInst.py`.
3. Let it do the work.

***That's it!***

If you're attempting things and it didn't go well. Please check the videos from the Demo and Resources Section. Which is located just below!

## Demo and Resources

This section should be enough to know on what you're dealing in this project.

- **Documentation**: <https://docs.google.com/document/d/1oyZ-jKiQFd_voRn4EIxYd09oBhy7ZOXVMwA2KruXPwU/edit>
- **Youtube Video Demonstration**: <https://www.youtube.com/watch?v=jpxtz1-mhd8>
- **Youtube Video Installation**: <https://www.youtube.com/watch?v=1NmTDPHD-Js>

### Advanced Context: Protocol

In this section, it shows a list of protocols to better understand how the system works.

#### Shutdown Timer Based on Motion Sensor Protocol

For every subject, we have a time limit. In our system, everytime it is unlocked for a particular time. Every 5 minutes, the motion sensor has to detect person for every 30 seconds. Now 10 scans for 30 minutes is equivalent for 5 minutes. If the scanner is in 50% state, it will continue for another 5 minutes. If the scanner is in 50% state less, it will shutdown the classroom itself.

#### Classroom Locked State Change Protocol

For every node, for it be controllable, it has receive a subject code on it. Those are automatically given by the Data Stream Handler on the system. So it may need priviledge for explicit assignment of subjects. Anyway, any other such explicit actions without any subject assignment to the classroom. Will result to its functionality as defaulted to be locked, electricity turned off. So for maintaince for instance, there should be a custom made admin subject along with time.

If for instance, the subject is the last subject, any other circumstance may be stopped in the middle of a session. So time has to be considered when using this system.

#### Restrictive Accessibility Protocol

When the accessibilities handed out to the user. Some user might even tampered it without any hindrance to it. For instance if user wants to access rooms not assigned to them. So for us to keep things safe, we have to disable links from other rooms but only displays their states to the rooms. Some rooms will only be enabled to you only if your subject linked to you is on the current time scope of the server time, it will be accessible and controllable within outside range. Any user who attempts to access rooms, will technically make you get in but you'll be recorded for the actions that is not quite acceptable. Meaning your name is in the list of logs who misused or accessed a particular room not currently assigned / focused to you.

## 💁 ❔ Frequently Asked Questions |> [Go Back](#table-of-contents)

- I feel that some parts of this project is missing... Can you tell me what is it?
  - ***Sure bro...*** There are only a few things that are ****NOT CONSIDERED**** to give away. And those are the following:
    1. PCB Design
    2. Miniature Design Layout

- ***Your code is not that very much clean / My eyes hurt! / Why would you code something much inlined and quite... stupid???***
  - All codes that were done initially was not intended to be dirty as possible. They were like that due to the fact that we have deadlines to meet. That's because I did most of the work here (In Software-Side) for 3 months straight. So I apologize for such a messy code. And yeah, the hardest part to accept when making this one is that I was still learning the necessity parts of Django to our projects.

- ***Can I use this whenever I want?***
  - Yeah, sure. But keep note that the repository has a `GPL-3.0` license. You have to read it and understand why I have to choose this one.

- ***Do I really have to meet the required components indicated here?***
  - For compatibility, of course. Since I didn't provide for the schematics, you could use different components or MCUs to your liking.

- ***How did you come with this project?***
  - Long story short, I wanted to achieve ideal time for what allocated time was for the discussions and for the waiting time to open the room. In our school, you need a staff / administrator to open the room door for you. And I as for what I know, I don't like how we wasting our time for nothing. That's because they are late as usual. One thing to mention is that we have one course-dedicated room from the technological building and the one who is assigned to that building is taking a while to open our room because he was always **LATE**, and that is always the scenario during Monday, Wednesday, and Friday. It makes me feel bad, the fact that building is highly focused on technology! So, to make at least a solution, we were able to think of this project, without actually us thinking on how hard it is gonna be. And with that, a few weeks later, this project was born.

- ***Why did you open-sourced this!? And aren't you afraid it as the Lead Developer?***
  - I don't want to put any of my works in the bookshelf from which other people doesn't see it. I want things to be accessible because that makes me want to value the hard work and sleepless nights that I throw off especially on this project. And yes, I'm not afraid of getting stolen. I always assume we could do things legal and proper. And I'm already a victim of it and know how it feels to get stolen by someone else.

- ***What would you do if someone got **stonks** from this project?***
  - I might close this one down. But I believe this project is very hard to replicate physically. I just do hope I could get something on it, or even just credits were just fine. Keep in mind that the project is just a ***bare-minimum*** setup that could be possibly done in-home or from small-scale buildings with multiple rooms. I know this type of setup is possibly expensive, but we're just showing here the concept of what IoT can do nowadays.

- ***Can I submit issues and submit a proposal for alternative methods?***
  - That's nice of you! Yes you can, just make things a bit formal. Even though I don't have a template for making it descent and formal as possible. I would just give you freedom on how would you laid out the proposals or issues. Just label things out accordingly in the labels that I made.

- ***This was such a medium-scale project!? How did you survive working on this one alone???***
  - I don't even know how I were able to survive this while learning throughout the semester. But hey, at least I wasn't suicidal or didn't got grave inside of depression. But to be honest, I did survive by just literally working on it **non stop**. You really have to sacrifice having fun and being go-happy with others. You really have to focus on it. Which in the end, **I was now quite emotionless, not being able to be happy at things that I want to be happy.** - ***DISCLAIMER - I'm not scaring you or other people at trying to sacrifice for the better, this was literally just happened due to circumstances. Maybe there's a better way to code productively and not by just coding all times and ending up at being emotionless and blame self for such stupid reasons...***

- ***I just checked the documentation and your recommendation is SO LONG! What the hell? So that means the project has a lot of flaws???***
  - I would literally agree that it has quite a few flaws. **NOT** a lot. Because the majority of the functionalities of the system pretty works well in my own perspective. I could be wrong, because the fact that, we realized that during the pandemic online sessions. And we only fixed a few things. But that fixes and adjustments didn't get committed in the repository. Which is quite disappointing. Anyway, IIRC the only problems or recommendations that I had is all about the implementation and how should I be using other components instead of having of what I currently have in the inventory.

- ***Can I ask question/s?***
  - Sure thing! Just be polite and I'll answer your question through my email indicated in my Github Profile!

## 🏆 ✍ Authors |> [Go Back](#table-of-contents)

Here are the list of authors who is taking part of the project.

- **Embedded Systems Team**
  - **Janrey Licas** - *Initial Work / Project Lead / Overall Software Design Worker / FrontEnd Design and Backend Programming* -  [CodexLink](https://github.com/CodexLink)
  - **Janos Angelo Garcia Jantoc** - *Hardware PCB Designer and Post Project Worker* - [BigBossCodes](https://github.com/BigBossCodes)
  - **Johnell Casey Murillo Panotes** - *The Participant and Initial Bare Minimum Documentation Worker* - No Account

- **Internet of Thing Team**
  - **Janrey Licas** - *Initial Work / Project Lead / Overall Software Design Worker / FrontEnd Design and Backend Programming* -  [CodexLink](https://github.com/CodexLink)
  - **Janos Angelo Garcia Jantoc** - *Hardware PCB Designer and Post Project Worker* - [BigBossCodes](https://github.com/BigBossCodes)
  - **Ronald Langaoan Jr.** - *Hardware Designer and Miniature Builder*[AliasBangis](https://github.com/AliasBangis)
  - **Joshua Santos** - *Initial Build Supporter and Joint Project Leader from Logic Circuits and Design* - No Account


## 📜 Various Credits |> [Go Back](#table-of-contents)

In this section, the maintainer will creditsto various types of entities.

### 🙇 Personal Credits |> [Go Back](#table-of-contents)

As a maintainer, I would like to give gratitude to several people who take part on this project. Those people helped / contributed that is considered gold for us.

- **Charles Ian Mascarenas** - *Schematic Inspector and for Insights Given Regarding Buck Converter and Voltage Regulator Due To Current Exactly Caught by NodeMCU's Diode for Relays and Other Such Components* - [ci-mascarenas](https://github.com/ci-mascarenas)
- **Engr. Cris Paulo Hate** - *Embedded System Instructor, Insights Given for Proper Components to Use for Locking Rooms such as *Solenoid Lock* and Insights were given for the future steps of the project. *Such as the proper use of IoT components like ESP8266*.* - Account Not Recognized.
- **Engr. Jan Justin Razon** - *Internet-of-Things Instructor, Insights Given for what things should be considered and how should the system work. Also insights given on what locking mechanism should be used for the room.* - Account Not Recognized.

### 🏆  Library Credits |> [Go Back](#table-of-contents)

- [Arduino DHT-ESP](https://github.com/beegee-tokyo/arduino-DHTesp) for Proper [DHT11/22](https://learn.adafruit.com/dht) Support in ESP Variant Devices.
- [Codacy](https://www.codacy.com/) and [CodeFactor](https://www.codefactor.io/dashboard/) for Code Quality Checking
- [Classy Class-Based Views | Django Class-Based View Inspector](https://ccbv.co.uk/) for Proper Documentation of Views used in the project.
- [Coveralls](https://www.coveralls.io/) for Code Coverage and Software Testing.
- [Coveralls for Django Plugin](https://pypi.org/project/django-coverage-plugin/) for Django Coverage Support.
- [Coveralls Github Action](https://github.com/marketplace/actions/coveralls-github-action) for Github Action Plugin Support for each Commit Instantiated.
- [Dependabot](https://dependabot.com/) for Library Dependency Version Tracking.
- [Django Documentations (Docs for v3.0)](https://docs.djangoproject.com/en/3.0/) for slight clarifications. Used for the base on learning Django in the majority.
- [Django Extensions](https://django-extensions.readthedocs.io/en/latest/) for Extra Features eliminating the unease of database management and for script runnable on the server instance.
- [Django Framework](https://www.djangoproject.com/) for Easy To Use(For Basic Usage) Web Framework.
- [Github Actions](https://github.com/features/actions) for CLI in-built within repository context to use for automation stuff.
- [Github Wiki TOC Generator](https://ecotrust-canada.github.io/markdown-toc/) for Literally Generating TOC Stuff Automatically Based on README Headers.
- [GT5X](https://github.com/brianrho/GT5X) for Proper [GT-521F52 Support](https://learn.sparkfun.com/tutorials/fingerprint-scanner-gt-521fxx-hookup-guide) instead of [official support](https://github.com/sparkfun/Fingerprint_Scanner-TTL). (This one saves my entire dignity throughout the use of the GT-521F52 Fingerprint Sensor. Kudos to this guy!)
- [Isotope](https://isotope.metafizzy.co/) and [Packery](https://packery.metafizzy.co/) for Dynamic Layout Positioning based on User-Browser Space.
- [Material 2](https://djibe.github.io/material/) for Continuously Supporting Daemonite's Material 1 Work Throughout the Whole Year.
- [SAL](https://mciastek.github.io/sal/) for Robust Animation Transition on Page Load.
- [Shields_IO](https://shields.io/) for Badge Display and Live State Servicing.
- [Visual Studio Code](https://code.visualstudio.com/) for Robust IDE and Dependable.
- [YAPF](https://github.com/google/yapf) for Standard Python Code Formatting.

### 📑  Documentation Credits |> [Go Back](#table-of-contents)

1. R. Yesodharan, R. Prince, S. Karthick, V. HariKrishnan and D. Bennaiah, "IoT based Classroom Automation using Arduino," International Open Access Journal, vol. II, no. 2, pp. 306-307, 2018.
2. T. Sali, C. Pardeshi, V. Malshette, A. Jadhav and V. Thombare, "Classroom Automation System," International Journal of Innovations in Engineering and Technology(IJIET), vol. VIII, no. 3, p. 27, 2017.
3. Creately.com. 2020. Django Architecture Flowchart | Creately. [online] Available at: <https://creately.com/diagram/iqjshero1/Django%20Architecture%20Flowchart> [Accessed 23 March 2020].

## 📚 License |> [Go Back](#table-of-contents)

This project is licensed under the GNU v3 License - see the [LICENSE](https://github.com/CodexLink/SmartClassroomSystem/blob/master/LICENSE) file for details
