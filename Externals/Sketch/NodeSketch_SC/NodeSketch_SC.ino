/*
    ! Smart Classroom IoT Sketch | NodeSketch_SC.ino
    * 01/16/2020 | Janrey "CodexLink" Licas | http://github.com/CodexLink

    ! In Collaboration with
        - Ronald Langaoan Jr. |> Hardware Designer and Manager
        - Janos Angelo Jantoc |> Hardware Designer and Assistant Programmer
        - Joshua Santos |> Hardware Manager and Builder
        - Johnell Casey Murillo Panotes |> Hardware Assistant

    @required_by   : Smart Classroom IoT Data Stream Handler | SC_DSH.py
    @pre-requisites: Smart Classroom IoT Function Declarative Header | SmartClassroom.h
                   : Smart Classroom IoT Function Definition | SmartClassroom.cpp

    @description: A Sketch Designed To Associate with NodeMCU Devices to Communicate with Django Server.
                : This sketch is served to many NodeMCU candidates to be used later.
                : Each will have different configurations. From IP as Client, Target Schedule, Authentication ID and so on.
                : Things won't work out if the DJango Server Properities Associated to the device that has this sketch has not the same configuration or properties.

    ! Copyright (C) 2020  Janrey "CodexLink" Licas

    * This program is free software: you can redistribute it and/or modify
    * it under the terms of the GNU General Public License as published by
    * the Free Software Foundation, either version 3 of the License, or
    * (at your option) any later version.

    * This program is distributed in the hope that it will be useful,
    * but WITHOUT ANY WARRANTY; without even the implied warranty of
    * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    * GNU General Public License for more details.

    * You should have received a copy of the GNU General Public License
    * along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

#include "SmartClassroom.h"

SC_MCU_DRVR SC(9600, "HW_EcLi284255H_Cdx", "@Li2019_b015@", "192.168.100.5", 8000);
//SC_MCU_DRVR SC(9600, "CodexLink", "01010101", "192.168.100.5", 8000);
//SC_MCU_DRVR SC(9600, "SCMainServer", "TIP-QC-SC-NODE-PARENT", "192.168.100.5", 8000);
ESP8266WebServer NodeServer(80); // ! Make this public. Cause a lot of CONFLICTS.

// Unreferenced / Unclassed functions
void HandleGET_Sens();
void HandlePOST_SetMode();

void setup()
{
    SC.begin();
    NodeServer.on("/RequestData", HTTP_GET, HandleGET_Sens);
    NodeServer.on("/RequestInstance", HTTP_GET, HandleGET_SetInstance);
    NodeServer.begin();
    SC.displayLCDScreen(SC.DataDisplayTypes::CLEAR_OFF_DISP);
}

void loop()
{
    while (SC.mntndWiFiConnection())
    {
        SC.displayLCDScreen(SC.DataDisplayTypes::DISP_CR_INFO);
        SC.authCheck_Fngrprnt();
        NodeServer.handleClient();
        delay(100);
    }
}

void HandleGET_Sens()
{
    if (!NodeServer.authenticate(SC.DEV_INST_CREDENTIALS.AUTH_DEV_USN, SC.DEV_INST_CREDENTIALS.AUTH_DEV_PWD))
    {
        return NodeServer.requestAuthentication();
    }
    digitalWrite(SC.RESTATED_DEV_PINS::ESP_LED, LOW);
    NodeServer.send(200, "text/plain", String("{'DATA_HEADER': {'CR_IDENTITY': '") + SC.DEV_INST_CREDENTIALS.DEV_CR_ASSIGNMENT + String("', 'CR_SHORT_NAME': '") + SC.DEV_INST_CREDENTIALS.DEV_CR_SHORT_NAME + String("', 'CR_UUID': '") + SC.DEV_INST_CREDENTIALS.DEV_CR_UUID + String("', 'DEV_NAME': '") + SC.DEV_INST_CREDENTIALS.AUTH_DEV_USN + String("', 'DEV_UUID': '") + SC.DEV_INST_CREDENTIALS.DEV_UUID + String("', 'CURR_COURSE_SESSION': '") + SC.DEV_INST_CREDENTIALS.CURRENT_COURSE_CODENAME + String("'}, 'DATA_SENS': {'CR_TEMP': '") + SC.ENV_INST_CONT.DHT11_TEMP + String("', 'CR_HUMD': '") + SC.ENV_INST_CONT.DHT11_HUMID + String("', 'CR_HTINX': '") + SC.ENV_INST_CONT.DHT11_HT_INDX + String("', 'PIR_MOTION': {'PIR_OPTPT':'") + SC.ENV_INST_CONT.PIR_OPTPT + String("', 'PIR_OTPT_TIME_TRIGGER': '") + SC.ENV_INST_CONT.PIR_MILLIS_TRIGGER + String("'}}, 'DATA_AUTH': {'AUTH_ID':'") + SC.DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT + String("', 'AUTH_STATE': '") + SC.AUTH_INST_CONT.AUTH_FGPRT_STATE + String("'}, 'DATA_STATE': {'DOOR_STATE': '") + SC.AUTH_INST_CONT.AUTH_CR_DOOR + String("', 'ACCESS_STATE': '") + SC.AUTH_INST_CONT.AUTH_CR_ACCESS + String("', 'ELECTRIC_STATE': '") + SC.AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE + String("'}}"));
    digitalWrite(SC.RESTATED_DEV_PINS::ESP_LED, HIGH);
}

void HandleGET_SetInstance()
{
    if (!NodeServer.authenticate(SC.DEV_INST_CREDENTIALS.AUTH_DEV_USN, SC.DEV_INST_CREDENTIALS.AUTH_DEV_PWD))
    {
        return NodeServer.requestAuthentication();
    }

    digitalWrite(SC.RESTATED_DEV_PINS::ESP_LED, LOW);
    if (NodeServer.arg("lock_state") == "True")
    {
        digitalWrite(SC_MCU_DRVR::SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, HIGH);
        SC.AUTH_INST_CONT.AUTH_CR_DOOR = false;
        NodeServer.send(200, "text/plain", "LOCK_STATE |> CHANGE TO LOCK |> OK");
    }
    else if (NodeServer.arg("lock_state") == "False")
    {
        digitalWrite(SC_MCU_DRVR::SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, LOW);
        SC.AUTH_INST_CONT.AUTH_CR_DOOR = true;
        NodeServer.send(200, "text/plain", "LOCK_STATE |> CHANGE TO UNLOCK |> OK");
    }

    if (NodeServer.arg("dev_rstrt") == "initiate")
    {
        NodeServer.send(200, "text/plain", "DEV RESTART |> OK");
        delay(300);
        ESP.restart();
    }

    if (NodeServer.arg("electric_state") == "True")
    {
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, LOW);
        SC.AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE = true;
        NodeServer.send(200, "text/plain", "ELECTRIC_STATE |> CHANGED TO 'ENABLED' |> OK");
    }
    else if (NodeServer.arg("electric_state") == "False")
    {
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, HIGH);
        SC.AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE = false;
        NodeServer.send(200, "text/plain", "ELECTRIC_STATE |> CHANGED TO 'DISABLED' |> OK");
    }

    // This disables all access from the classroom. The relays will be turned off.
    if (NodeServer.arg("cr_access") == "True")
    {
        SC.AUTH_INST_CONT.AUTH_CR_ACCESS = true;
        NodeServer.send(200, "text/plain", "CR_ACCESS |> CHANGED TO 'ENABLED' |> OK");
    }

    else if (NodeServer.arg("cr_access") == "False")
    {
        SC.AUTH_INST_CONT.AUTH_CR_DOOR = false;
        SC.AUTH_INST_CONT.AUTH_CR_ACCESS = false;
        SC.sketchForceStop = true;
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, HIGH);
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, HIGH);
        NodeServer.send(200, "text/plain", "CR_ACCESS |> CHANGED TO 'DISABLED' |> OK");
    }

    // ! Two of these arguments has need to be supplied both before we can run the if statement scope under it.
    if (NodeServer.arg("dev_sched_user_course_replace") && NodeServer.arg("dev_sched_user_assign_replace"))
    {
        char CHECKPOINT_CURRENT_COURSE_CODENAME[11];
        strcpy(CHECKPOINT_CURRENT_COURSE_CODENAME, SC.DEV_INST_CREDENTIALS.CURRENT_COURSE_CODENAME);
        uint16_t CHECKPOINT_AUTH_USER_ID_FNGRPRNT = SC.DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT;
        Serial.println(F("Update | Server Sent Request of Schedule Replacement!"));
        NodeServer.arg("dev_sched_user_course_replace").toCharArray(SC.DEV_INST_CREDENTIALS.CURRENT_COURSE_CODENAME, 11);
        SC.DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT = NodeServer.arg("dev_sched_user_assign_replace").toInt();

        SC.ForceEEPROMUpdate = ((CHECKPOINT_AUTH_USER_ID_FNGRPRNT != SC.DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT || strcmp(CHECKPOINT_CURRENT_COURSE_CODENAME, SC.DEV_INST_CREDENTIALS.CURRENT_COURSE_CODENAME) != 0)) ? true : false;

        if (SC.ForceEEPROMUpdate)
        {
            Serial.println();
            Serial.print(F("BEFORE | Course Code On Time Scope: "));
            Serial.println(SC.DEV_INST_CREDENTIALS.CURRENT_COURSE_CODENAME);
            Serial.print(F("BEFORE | Fingerprint ID: "));
            Serial.println(SC.DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT);
            Serial.println();
            Serial.print(F("AFTER | Course Code On Time Scope: "));
            Serial.println(SC.DEV_INST_CREDENTIALS.CURRENT_COURSE_CODENAME);
            Serial.print(F("AFTER | Fingerprint ID: "));
            Serial.println(SC.DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT);
            Serial.println(F("NodeMCU | Schedule Sync Data Updated!"));
        }
        else
        {
            Serial.println(F("NodeMCU | Schedule Data Remains The Same! Ignoring Save State."));
        }
        NodeServer.send(200, "text/plain", "SCHEDULE REPLACEMENT |> CHANGED | OK");
    }

    digitalWrite(SC.RESTATED_DEV_PINS::ESP_LED, HIGH);
    return;
}