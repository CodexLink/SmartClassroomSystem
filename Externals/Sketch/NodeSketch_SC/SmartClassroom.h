/*
    ! Smart Classroom IoT Function Declarative Header | SmartClassroom.h
    * 01/16/2020 | Janrey "CodexLink" Licas | http://github.com/CodexLink

    ! In Collaboration with
        - Ronald Langaoan Jr. |> Hardware Designer and Manager
        - Janos Angelo Jantoc |> Hardware Designer and Assistant Programmer
        - Joshua Santos |> Hardware Manager and Builder
        - Johnell Casey Murillo Panotes |> Hardware Assistant

    @required_by: Smart Classroom IoT Function Definition | SmartClassroom.cpp
                : Smart Classroom IoT Sketch | NodeSketch_SC.ino

    @description: The file that contains all mapped functions for the Smart Classroom System.
                : Each functions declared are incorporated and must have exact functions existing from the SmartClassroom.cpp.
                : So basically, this is just the structured list of functions and stuff that will be used and filled later on.

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

#pragma once

// Add Some Library Here.
#include <ESP8266HTTPClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ArduinoOTA.h>
#include "DHTesp.h"
#include <SoftwareSerial.h>
#include "LiquidCrystal_I2C.h"
#include "GT5X.h"
#include <EEPROM.h>

#define TX_OVERRIDE 3
#define SSD3 10
class SC_MCU_DRVR
{
    // ! Container that can be to reference all constant values.
    enum CONST_VAL
    {
        EEPROM_MAX_BYTE = 512,
        EEPROM_CR_ASSIGNED_CHAR_LEN = 6,
        EEPROM_CR_ROOM_CHAR_LEN = 11,
        EEPROM_DEV_USN_CHAR_LEN = 16,
        EEPROM_DEV_UID_CHAR_LEN = 32,
        EEPROM_COURSE_CODE_LENGTH = 10,
        ESP_DEFAULT_PORT = 80,
        MAX_REL_CHANNEL = 5,
        MAX_IP_ADDR_CHAR = 15,
        MAX_WIFI_SSD_CHAR = 32,
        MAX_WIFI_PW_CHAR = 63,
        MAX_STR_CR = 20,
        MAX_STR_UUID = 40,
        NULL_CONTENT = 0,
        MAX_FNGRPRNT_STORABLE = 3000,
        PIR_TRIGGER_SECONDS = 300000,
        PIR_DIVIDED_REQUIRED_OUTPUTS = 10,
        // It is always good to skip one byte before getting another data.
        // ! How does this work?
        /*
            For each data, we have to make at least one space for formality or indication of data is not joined, it is different.
            Usually we start at Address 0 or 0x00. Which is starting point of us, currently assigned in EEPROM_CR_ASSIGNED_CHAR_START_ADDR.
            Now we knew that CR_ASSIGNED consumes 6 bytes. IF that is the case then,
            The next usable data is by computation of Current Address + Consumed Address + 1
            Therefore, 0 + 6 + 1 = 0x07

            Now let 0x07 as CR_ROOM_CHAR starting address.
            Since CR_ROOM_CHAR consumes 11 Characters then we do, 0x07 + 11 + 1.
            Then we get an output of 0x12 because 0x07 + 11 is 18. Since After 0x0F is 15, we do + 3.
            Which then goes from 0x10, 0x11 and lastly, 0x12.

            Then continued.
        */
        EEPROM_CR_ASSIGNED_CHAR_START_ADDR = 0x00,
        EEPROM_CR_ROOM_CHAR_START_ADDR = 0x07, // Usually 0x06 + 1 For Skipping
        EEPROM_DEV_USN_CHAR_START_ADDR = 0x12, // Usually 0x0F is 15. Then + 3, therefore, 0x12 is 18
        EEPROM_DEV_UID_CHAR_START_ADDR = 0x23, // ...
    };

    enum CONST_DEV_PARAM
    {
        LCD_ADDR = 0x27,
        LCD_W = 20,
        LCD_H = 4
    };

    // * This Container utilizes PINs to be used to scan the whole room.
    enum SENS_DAT_PINS
    {
        TEMP_HUD_DAT_PIN = D0,
        PIR_DAT_PIN = D3,
    };

    struct WIFI_CRENDENTIALS
    {
        char WIFI_SSID[MAX_WIFI_SSD_CHAR];
        char WIFI_PW[MAX_WIFI_PW_CHAR];
    } WIFI_INST_STRUCT;

    // ! Variables
    uint16_t __BAUD_RATE = CONST_VAL::NULL_CONTENT;

    // ! Object (Class) Instance
    LiquidCrystal_I2C LCD_DRVR{CONST_DEV_PARAM::LCD_ADDR, CONST_DEV_PARAM::LCD_W, CONST_DEV_PARAM::LCD_H};
    DHTesp TempSens;
    ESP8266WebServer NodeServer{CONST_VAL::ESP_DEFAULT_PORT};

public:
    // * Declares Data Interpretation To Be Used As A Parameter Later.
    enum DataDisplayTypes
    {
        INITIALIZE,
        CLEAR,
        CLEAR_OFF_DISP,
        WAITPOINT,
        WAIT_CLEAR,
        DISP_CR_INFO,
        DEBUG_FNGRPRNT_ENROLL,
        DEBUG_FNGRPRNT_VERIFY,
        DEBUG_MCU_GENERALIZED, // Generalized Test. Meaning MCU and with its components are being tested.

    };

    enum RESTATED_DEV_PINS
    {
        ESP_LED = D4,
        MCU_LED = D0

    };

    enum SENS_DAT_PINS_PUBLIC
    {
        FNGR_TX_PIN = D5,
        FNGR_RX_PIN = D6,
        RELAY_FRST_PIN = D7,
        RELAY_SCND_PIN = TX_OVERRIDE,
        RELAY_THRD_PIN = SSD3,
        //RELAY_FRTH_PIN = D8,  Unused due to PIN Pulled LOW which would result to device not botting up.
    };

    // ! Environmental Module Outputs
    struct ENV_MOD_OTPT
    {
        float DHT11_TEMP;
        float DHT11_HUMID;
        float DHT11_HT_INDX;
        bool PIR_OPTPT;
        uint32_t PIR_MILLIS_TRIGGER;
    } ENV_INST_CONT;

    struct AUTH_STATE
    {
        bool AUTH_CR_DOOR = 0;              // 1 Unlocked, 0 Locked
        bool AUTH_CR_ACCESS = 1;            // 1 Enabled, 0 Disabled
        bool NON_AUTH_ELECTRIC_STATE = 0;   // 1 Enabled, 0 Disabled
        bool AUTH_FGPRT_STATE = 0;          // 1 For Currently Authenticated, Else Not Authenticated
    } AUTH_INST_CONT;

    struct DEV_CREDENTIALS
    {
        char DEV_CR_ASSIGNMENT[CONST_VAL::EEPROM_CR_ASSIGNED_CHAR_LEN + 1] = "Q-5424" /**/;
        char DEV_CR_SHORT_NAME[CONST_VAL::EEPROM_CR_ROOM_CHAR_LEN + 1] = "CompEng Lab" /**/;
        char DEV_CR_UUID[CONST_VAL::EEPROM_DEV_UID_CHAR_LEN + 1] = "df826e0334b84f2689e64f2c6b24a6ab" /**/;
        char DEV_UUID[CONST_VAL::EEPROM_DEV_UID_CHAR_LEN + 1] = "e776ffc28b524d318624bc39d7efea0e" /**/;

        char AUTH_DEV_USN[CONST_VAL::EEPROM_DEV_USN_CHAR_LEN + 1] = "NodeMCU | Q-5424" /**/;
        char AUTH_DEV_PWD[CONST_VAL::EEPROM_DEV_UID_CHAR_LEN + 1] = "e776ffc28b524d318624bc39d7efea0e" /**/;

        char CURRENT_COURSE_CODENAME[CONST_VAL::EEPROM_COURSE_CODE_LENGTH + 1];
        uint16_t AUTH_USER_ID_FNGRPRNT = 0; // Must be set by user.
    } DEV_INST_CREDENTIALS;


    // ! Referrable to saveMetaData and retrieveMetaData
    // ! The code below is a uin8_t (unsigned char pointer variable) that stores the address of the struct DEV_CREDENTIALS.
    // * They're converted to uint8_t or typecasted to uint8_t to be iterrable as object.
    uint8_t *structStorage = (uint8_t *)&DEV_INST_CREDENTIALS;
    bool sketchForceStop;

    // Make a struct for this one.
    const String SERVER_IP_ADDRESS = "192.168.100.5";
    const uint16_t SERVER_PORT = 8000;

    bool PIR_ARR_OUTPUT[CONST_VAL::PIR_DIVIDED_REQUIRED_OUTPUTS] = {0};
    bool ForceEEPROMUpdate = false;
    //# of True +0 # of False
    /* PIR Calculation */


    // Constructor
    SC_MCU_DRVR(uint16_t BAUD_RATE, const char *SSID, const char *PW);
    void begin();
    bool mntndWiFiConnection();
    void displayLCDScreen(DataDisplayTypes Screens);
    void authCheck_Fngrprnt();
    //void
    bool SketchTimeCheck(uint32_t TimeIntervalToMeet);
    inline void saveMetaData();

private:
    inline void retrieveMetaData();

    bool checkPresence();
    bool checkWiFiConnection();

    // Outputs PIR Array Set
    void PIR_updateArray();
    void PIR_outputState();
    // Checks if PIR pass the percentage to check if we have to maintain the state of the classroom.
    bool PIR_isPassed();
    //void InterpretData(DataInterpretTypes DataType);
};

// END OF FILE SMARTROOM