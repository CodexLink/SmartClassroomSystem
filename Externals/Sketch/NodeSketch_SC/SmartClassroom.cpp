/*
    ! Smart Classroom IoT Function Definition | SmartClassroom.cpp
    * 01/16/2020 | Janrey "CodexLink" Licas | http://github.com/CodexLink

    ! In Collaboration with
        - Ronald Langaoan Jr. |> Hardware Designer and Manager
        - Janos Angelo Jantoc |> Hardware Designer and Assistant Programmer
        - Joshua Santos |> Hardware Manager and Builder
        - Johnell Casey Murillo Panotes |> Hardware Assistant

    @required_by: Smart Classroom IoT Function Declarative Header | SmartClassroom.h
                : Smart Classroom IoT Sketch | NodeSketch_SC.ino

    @description: The library used to function the intention of the scanner device in Smart Classroom System.
                : Each has environment scanning and scheduler sense incorporated with the DJango Server.
                : This file only contains function definitions of a function declaratives from the first element of the @required_by.

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

/*
    ! Class Initializations | CPP File — START

    @status: Done
    @concept: It is a set of class instiantated from local CPP file that contains all class functions but not included in the class given from the SC Library Header.
    @context:  Why?
    @context:      - The main reason is, we cannot initialize them with Arguments in Brackets.
    @context:      - The initialization style is a method from a C++ 14 from which gives us the ability to give the parent object the ability to access functions from the instantiated objects.
    @context:      - The candidates such as SoftwareSerial, GT5X and GT5X_DeviceInfo (which is correlated with GTX5X Object Initializer) produces an error from which I cannot solve.
    @context:      - The complexity of the problem given when they're initialized in the class context is very high. To which, I have to do 'this' method as my conclusion since relying on the stackoverflow for so long I cannot fix it.
    @issue:  Disadvantages
    @issue:      - I don't know what would be the disadvantage since I'm not that kind of aware from the performance.
    @issue:      - But in the end, it might violate the CPP rules.

*/
SoftwareSerial FP_WIRE(SC_MCU_DRVR::SENS_DAT_PINS_PUBLIC::FNGR_RX_PIN, SC_MCU_DRVR::SENS_DAT_PINS_PUBLIC::FNGR_TX_PIN);
GT5X FPController(&FP_WIRE);
GT5X_DeviceInfo FP_DEV_INFO;
//  ! Class Initializations | CPP File — END

/*
    ! Class Constructor — START

    @status: Done
    @concept: The Class Object To Perform when Initialized from any scope as long as the library exist from that desired location of class initialization.
    @data: Fields Required are (1) BAUD_RATE, (2) SSID of WiFi and (3) PW of WiFi
    @context: Copies Given Arguments to the Class 'WIFI_INST_STRUCT' Structure
    @insight: This was the very first function to be finished. This was intended before to make things easier to debug and switch stuffs.
*/
SC_MCU_DRVR::SC_MCU_DRVR(uint16_t SUPPLIED_BAUD_RATE, const char *SUPPLIED_SSID, const char *SUPPLIED_PW, const String SUPPLIED_SERVER_IP_ADDRESS, const uint16_t SUPPLIED_SERVER_PORT)
{
    __BAUD_RATE = SUPPLIED_BAUD_RATE;
    strcpy(WIFI_INST_STRUCT.WIFI_SSID, SUPPLIED_SSID);
    strcpy(WIFI_INST_STRUCT.WIFI_PW, SUPPLIED_PW);
    SERVER_IP_ADDRESS = SUPPLIED_SERVER_IP_ADDRESS;
    SERVER_PORT = SUPPLIED_SERVER_IP_ADDRESS;
}
//    ! Class Constructor — END

/*
    ! Parent Class -> Begin() Function — Second Layer of Class Initialization

    @status: Done
    @concept: Initializes All Other Instantiated Class Sub Initializer Function (This means, instantiated class similar begin() function)
    @context: This will be the first one to output for each MCU to be rebooted and powered up.
    @issue: We cannot clear text from which the NodeMCU produces some invalid characters everytime they were booted or restarted from their current state.
*/
void SC_MCU_DRVR::begin()
{
    // * We first set our Baud RATE to show our Serial Prints everytime it was called.
    Serial.begin(__BAUD_RATE);

    Serial.println();
    Serial.println(F("Smart Classroom IoT Sketch | NodeSketch_SC.ino"));
    Serial.println(F("01/16/2020 | By Janrey 'CodexLink' Licas | http://github.com/CodexLink"));

    Serial.println(F("In Collaboration with:"));
    Serial.println(F("    - Ronald Langaoan Jr. |> Hardware Designer and Manager"));
    Serial.println(F("    - Janos Angelo Jantoc |> Hardware Designer and Assistant Programmer"));
    Serial.println(F("    - Joshua Santos |> Hardware Manager and Builder"));
    Serial.println(F("    - Johnell Casey Murillo Panotes |> Hardware Assistant"));

    LCD_DRVR.begin(); // * Start LCD I2C 20x4 Instance
    WiFi.begin(WIFI_INST_STRUCT.WIFI_SSID, WIFI_INST_STRUCT.WIFI_PW); // * We start connecting to our given value of WiFi SSD and PW.
    FP_WIRE.begin(__BAUD_RATE); // Software Serial, Related to Serial Objects. Start with BAUD Rate similarly to Serial Instantiation to communicate with some devices attached to it. (Technically Used for Fingerprint Communication)
    FPController.begin(&FP_DEV_INFO); // ! Start FP GT5X Driver
    FPController.set_led(false); // ! Set Fingerprint LED to False To See if it could follow instruction from the MCU.
    EEPROM.begin(CONST_VAL::EEPROM_MAX_BYTE); // * Start Emulated EEPROM to be used to Retrieve / Save Data from the Last MCU Session with recent communication with the Server.

    // ! We can execute this function only if we did some factory configuration.
    if (!SketchForceStructOverride || DEV_INST_CREDENTIALS.DEV_CR_ASSIGNMENT == NULL || DEV_INST_CREDENTIALS.DEV_CR_SHORT_NAME == NULL || DEV_INST_CREDENTIALS.DEV_CR_UUID == NULL || DEV_INST_CREDENTIALS.DEV_UUID == NULL || DEV_INST_CREDENTIALS.AUTH_DEV_USN == NULL || DEV_INST_CREDENTIALS.AUTH_DEV_PWD == NULL)
    {
        retrieveMetaData();
    }
    else
    {
        saveMetaData();
    }

    pinMode(RESTATED_DEV_PINS::ESP_LED, OUTPUT);
    pinMode(RESTATED_DEV_PINS::MCU_LED, OUTPUT);

    pinMode(SENS_DAT_PINS::PIR_DAT_PIN, INPUT);
    TempSens.setup(SENS_DAT_PINS::TEMP_HUD_DAT_PIN, DHTesp::DHT11);

    pinMode(SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, OUTPUT);
    digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, HIGH);

    pinMode(SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, OUTPUT);
    digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, HIGH);

    LCD_DRVR.noBacklight();
    LCD_DRVR.clear();
    delay(500);
    LCD_DRVR.backlight();
    FPController.set_led(true);
    return;
}
//  ! Parent Class -> Begin() Function — Second Layer of Class Initialization

// ! A Function to Retrieve EEPROM MetaData

// * Usually at this point, we have two variables to fill with.
// ! Contains 14 Bit Address | Device AUTH Name
// ! Contains 32 Bit Address | Device AUTH PWD

// ! We have to make sure that this function DOES only retrieve some functions and then off we go.
inline void SC_MCU_DRVR::retrieveMetaData()
{
    Serial.println();
    Serial.println(F("Structure Data has No Default Content. Retrieving Values..."));
    if (EEPROM.read(CONST_VAL::EEPROM_CR_ASSIGNED_CHAR_START_ADDR) != NULL)
    {

        Serial.println(F("EEPROM Stored Data Byte Detected!"));
        for (size_t structBytes = CONST_VAL::NULL_CONTENT; structBytes < sizeof(DEV_CREDENTIALS); structBytes++)
        {
            structStorage[structBytes] = EEPROM.read(CONST_VAL::EEPROM_CR_ASSIGNED_CHAR_START_ADDR + structBytes);
        }
        Serial.println(F("Retrieved Meta Data: "));
        Serial.print(F("DEV_CR_ASSIGNMENT |> "));
        Serial.println(DEV_INST_CREDENTIALS.DEV_CR_ASSIGNMENT);
        Serial.print(F("DEV_CR_SHORT_NAME |> "));
        Serial.println(DEV_INST_CREDENTIALS.DEV_CR_SHORT_NAME);
        Serial.print(F("DEV_CR_UUID |> "));
        Serial.println(DEV_INST_CREDENTIALS.DEV_CR_UUID);
        Serial.print(F("DEV_UUID |> "));
        Serial.println(DEV_INST_CREDENTIALS.DEV_UUID);
        Serial.print(F("AUTH_DEV_USN |> "));
        Serial.println(DEV_INST_CREDENTIALS.AUTH_DEV_USN);
        Serial.print(F("AUTH_DEV_PWD |> "));
        Serial.println(DEV_INST_CREDENTIALS.AUTH_DEV_PWD);
        Serial.print(F("CURRENT_COURSE_CODENAME |> "));
        Serial.println(DEV_INST_CREDENTIALS.CURRENT_COURSE_CODENAME);
        Serial.print(F("AUTH_USER_ID_FNGRPRNT |> "));
        Serial.println(DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT);
        EEPROM.end();
        Serial.println(F("EEPROM Data Retrival to Structured Data was Finished."));
        Serial.println();
    }
    else
    {
        Serial.println(F("EEPROM Stored Data is NULL. Please reupload the sketch with a new structured data to get started!"));
        do
        {
            yield();
            delay(10000);
        } while (1);
    }
    return;
}

// ! A Function to Save MetaData to EEPROM
// * Requires Everytime we do REQUEST.
inline void SC_MCU_DRVR::saveMetaData()
{
    Serial.println();
    Serial.println(F("Structured Data with Content Changing nor Updated Detected. Saving Those Values..."));
    Serial.println();
    Serial.println(F("Meta Data From Structured Data: "));
    Serial.print(F("DEV_CR_ASSIGNMENT |> "));
    Serial.println(DEV_INST_CREDENTIALS.DEV_CR_ASSIGNMENT);
    Serial.print(F("DEV_CR_SHORT_NAME |> "));
    Serial.println(DEV_INST_CREDENTIALS.DEV_CR_SHORT_NAME);
    Serial.print(F("DEV_CR_UUID |> "));
    Serial.println(DEV_INST_CREDENTIALS.DEV_CR_UUID);
    Serial.print(F("DEV_UUID |> "));
    Serial.println(DEV_INST_CREDENTIALS.DEV_UUID);
    Serial.print(F("AUTH_DEV_USN |> "));
    Serial.println(DEV_INST_CREDENTIALS.AUTH_DEV_USN);
    Serial.print(F("AUTH_DEV_PWD |> "));
    Serial.println(DEV_INST_CREDENTIALS.AUTH_DEV_PWD);
    Serial.print(F("CURRENT_COURSE_CODENAME |> "));
    Serial.println(DEV_INST_CREDENTIALS.CURRENT_COURSE_CODENAME);
    Serial.print(F("AUTH_USER_ID_FNGRPRNT |> "));
    Serial.println(DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT);
    Serial.println();
    Serial.println(F("Saving Those Values..."));
    if (EEPROM.read(CONST_VAL::EEPROM_CR_ASSIGNED_CHAR_START_ADDR) != NULL)
    {
        Serial.println(F("EEPROM Data is not NULL. Deleting them..."));
        for (int storageBytes = 0; storageBytes < CONST_VAL::EEPROM_MAX_BYTE; storageBytes++)
        {
            EEPROM.write(storageBytes, 0);
        }
        Serial.println(F("EEPROM Data Deleted."));
    }

    Serial.println(F("Saving Structured Data to EEPROM."));
    for (size_t structBytes = CONST_VAL::NULL_CONTENT; structBytes < sizeof(DEV_CREDENTIALS); structBytes++)
    {
        EEPROM.write(CONST_VAL::EEPROM_CR_ASSIGNED_CHAR_START_ADDR + structBytes, structStorage[structBytes]);
    }
    EEPROM.commit();
    EEPROM.end();
    Serial.println(F("EEPROM Data Save Done."));
    Serial.println();
    return;
}

bool SC_MCU_DRVR::checkPresence()
{
    if (SketchTimeCheck(CONST_VAL::PIR_TRIGGER_SECONDS))
    {
        if (!PIR_isPassed())
        {
            digitalWrite(RELAY_FRST_PIN, HIGH);
            digitalWrite(RELAY_SCND_PIN, HIGH);
            LCD_DRVR.setCursor(0, 3);
            LCD_DRVR.print(F("> Presence TimedOut!"));
            Serial.println(F("Presence PIR Failed! Closing Classroom..."));

            HTTPClient UpdatePOSTData;
            String DevUUID_Req = DEV_INST_CREDENTIALS.DEV_UUID;
            String CrUUID_Req = DEV_INST_CREDENTIALS.DEV_CR_UUID;
            String POSTArgs = DevUUID_Req + "/" + CrUUID_Req + "/" + DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT + "/LockState=" + AUTH_INST_CONT.AUTH_CR_DOOR;
            String RequestDest = "http://" + SERVER_IP_ADDRESS + ":" + SERVER_PORT + "/lockRemoteCall/" + POSTArgs;

            UpdatePOSTData.begin(RequestDest);
            UpdatePOSTData.addHeader("Content-Type", "text/plain");
            uint8_t ResponseRequest = UpdatePOSTData.POST("NODEMCU POST REQ |> LOCK AUTHENTICATION");
            String ResponseMsg = UpdatePOSTData.getString();
            Serial.print(F("Query | IP Target |> "));
            Serial.println(RequestDest);
            Serial.print(F("HTTP Response |> "));
            Serial.println(ResponseRequest);
            Serial.print(F("HTTP Message |> "));

            PIR_clearArray();

            AUTH_INST_CONT.AUTH_CR_DOOR = false;
            AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE = false;
            AUTH_INST_CONT.AUTH_FGPRT_STATE = false;
            sketchForceStop = true;
            //checkPresence();
            return false;
        }
        else
        {
            // Do something with the millis() double the value based on given millis();
            delay(1000);
            Serial.print(F("Presence PIR Passed! Extending Time Once Again..."));
            sketchForceStop = false;
            PIR_clearArray();
            return true;
        }
    }
    else
    {
        delay(250);
        return true;
    }
}

bool SC_MCU_DRVR::SketchTimeCheck(uint32_t TimeIntervalToMeet)
{
    uint_fast32_t sketchBaseTime = millis();
    static bool sketchRelease = true;
    static uint_fast32_t sketchPreviousHit;
    static uint_fast32_t PIR_CurrentTime;
    static uint8_t PIR_ElemIndexFocus;

    if (sketchForceStop)
    {
        sketchForceStop = false;
        sketchRelease = true;
        PIR_clearArray();
        Serial.println(F("Sketch Time Process Stopped..."));
        return false;
    }

    if (sketchRelease)
    {
        sketchPreviousHit = sketchBaseTime;
        sketchRelease = false;
    }

    Serial.print(F("Sketch Time: "));
    Serial.print(sketchBaseTime);
    Serial.print(F(" - "));
    Serial.print(sketchPreviousHit);
    Serial.print(F(" = "));
    Serial.print(sketchBaseTime - sketchPreviousHit);
    Serial.print(F(" |> Required Time To Meet: "));
    Serial.println(TimeIntervalToMeet);

    Serial.println();
    PIR_ElemIndexFocus = (uint8_t)(((sketchBaseTime - sketchPreviousHit) / 1000) / 30);
    Serial.print(F("PIR State Array |> (Focused at Index Element "));
    Serial.print(PIR_ElemIndexFocus);
    Serial.print(F(") |> ["));

    if (digitalRead(SENS_DAT_PINS::PIR_DAT_PIN) == HIGH)
        PIR_ARR_OUTPUT[PIR_ElemIndexFocus] = true;

    for (size_t PIR_ARR_ELEM = CONST_VAL::NULL_CONTENT; PIR_ARR_ELEM < CONST_VAL::PIR_DIVIDED_REQUIRED_OUTPUTS; PIR_ARR_ELEM++)
    {
        Serial.print(PIR_ARR_OUTPUT[PIR_ARR_ELEM]);
        Serial.print((PIR_ARR_ELEM + 1 == CONST_VAL::PIR_DIVIDED_REQUIRED_OUTPUTS) ? "" : ", ");
    }
    Serial.println(F("]"));

    Serial.println();

    if (!sketchRelease && (uint_fast32_t)(sketchBaseTime - sketchPreviousHit) >= TimeIntervalToMeet)
    {
        sketchRelease = true;
        sketchPreviousHit = 0;
        Serial.println(F("Sketch Time Process Finished From Target Time!"));
        return true;
    }
    else
    {
        return false;
    }
}

bool SC_MCU_DRVR::checkWiFiConnection()
{
    displayLCDScreen(DataDisplayTypes::CLEAR);
    displayLCDScreen(DataDisplayTypes::WAITPOINT);
    Serial.print(F("Connection to WiFi is not established. Waiting."));
    digitalWrite(RESTATED_DEV_PINS::MCU_LED, HIGH);
    while (WiFi.status() != WL_CONNECTED)
    {
        digitalWrite(RESTATED_DEV_PINS::ESP_LED, LOW);
        Serial.print(".");
        delay(400);
        digitalWrite(RESTATED_DEV_PINS::ESP_LED, HIGH);
        delay(400);
    }
    digitalWrite(RESTATED_DEV_PINS::ESP_LED, HIGH);
    Serial.println();
    Serial.print(F("Connected to "));
    Serial.print(WIFI_INST_STRUCT.WIFI_SSID);
    Serial.print(F("!!! | IP Address |> "));
    Serial.println(WiFi.localIP());
    displayLCDScreen(DataDisplayTypes::WAIT_CLEAR);
    delay(1000);
    displayLCDScreen(DataDisplayTypes::CLEAR_OFF_DISP);
    return true;
}

bool SC_MCU_DRVR::mntndWiFiConnection()
{
    if (WiFi.status() == WL_CONNECTED)
    {
        return true;
    }
    else
    {
        Serial.println(F("Connection to WiFi was lost. Attempting ReConnection..."));
        return (checkWiFiConnection() ? true : false);
    }
}

void SC_MCU_DRVR::displayLCDScreen(DataDisplayTypes Screens)
{
    switch (Screens)
    {
    case DataDisplayTypes::WAITPOINT:
        LCD_DRVR.setCursor(0, 0);
        LCD_DRVR.print(F("Smart Classroom Sys."));
        LCD_DRVR.setCursor(0, 1);
        LCD_DRVR.print(F(" Ver. 02222020-2327"));
        LCD_DRVR.setCursor(0, 2);
        LCD_DRVR.print(F(" Interactless Mgmt."));
        LCD_DRVR.setCursor(0, 3);
        LCD_DRVR.print(F("   Connecting ...   "));
        break;

    case DataDisplayTypes::WAIT_CLEAR:
        LCD_DRVR.setCursor(0, 3);
        LCD_DRVR.print(F("     Connected!     "));
        break;

    case DataDisplayTypes::CLEAR:
        LCD_DRVR.clear();
        break;

    case DataDisplayTypes::CLEAR_OFF_DISP:
        LCD_DRVR.noBacklight();
        LCD_DRVR.clear();
        delay(500);
        LCD_DRVR.backlight();
        break;

    case DataDisplayTypes::DISP_CR_INFO:
        digitalWrite(RESTATED_DEV_PINS::MCU_LED, LOW);
        if (isnan(TempSens.getTemperature() && isnan(TempSens.getHumidity())))
        {
            ENV_INST_CONT.DHT11_TEMP = ENV_INST_CONT.DHT11_TEMP;
            ENV_INST_CONT.DHT11_HUMID = ENV_INST_CONT.DHT11_HUMID;
        }
        else
        {
            ENV_INST_CONT.DHT11_TEMP = TempSens.getTemperature();
            ENV_INST_CONT.DHT11_HUMID = TempSens.getHumidity();
        }
        ENV_INST_CONT.PIR_OPTPT = (digitalRead(SENS_DAT_PINS::PIR_DAT_PIN) == HIGH) ? true : false;
        LCD_DRVR.setCursor(0, 0);
        LCD_DRVR.print(DEV_INST_CREDENTIALS.DEV_CR_ASSIGNMENT);
        LCD_DRVR.print(F(" | "));
        LCD_DRVR.print(DEV_INST_CREDENTIALS.DEV_CR_SHORT_NAME);
        LCD_DRVR.setCursor(0, 1);
        LCD_DRVR.print(F("S:"));
        LCD_DRVR.print((AUTH_INST_CONT.AUTH_CR_DOOR) ? "UnLckd for " : "Locked for ");
        LCD_DRVR.print(DEV_INST_CREDENTIALS.CURRENT_COURSE_CODENAME);
        LCD_DRVR.setCursor(0, 2);
        LCD_DRVR.print(F("T:"));
        LCD_DRVR.print(ENV_INST_CONT.DHT11_TEMP, 1);
        LCD_DRVR.write(223);
        LCD_DRVR.print(F("C | H:"));
        LCD_DRVR.print(ENV_INST_CONT.DHT11_HUMID, 1);
        LCD_DRVR.print(F("%"));
        Serial.print(F("MODULE REPORTS | T: "));
        Serial.print(ENV_INST_CONT.DHT11_TEMP);
        Serial.print(F("C | HUD: "));
        Serial.print(ENV_INST_CONT.DHT11_HUMID);
        Serial.print(F("%"));
        Serial.print(F(" | MOTION SENS: "));
        Serial.println(ENV_INST_CONT.PIR_OPTPT);
        digitalWrite(RESTATED_DEV_PINS::MCU_LED, HIGH);
        break;

    case DataDisplayTypes::DEBUG_FNGRPRNT_ENROLL:
        LCD_DRVR.setCursor(0, 0);
        LCD_DRVR.print(F("SC FNGRPRNT ENROLL"));
        LCD_DRVR.setCursor(0, 1);
        LCD_DRVR.print(F("User Registration"));
        LCD_DRVR.setCursor(0, 2);
        LCD_DRVR.print(F("> Target ID: "));
        LCD_DRVR.print(SER_INPUT_ID);
        LCD_DRVR.setCursor(0, 3);
        while (1)
        {
            while (!Serial.available())
            {
                yield();
            }
            SER_INPUT_RAW = Serial.read();
            if (isdigit(SER_INPUT_RAW))
                break;
            SER_INPUT_ID *= 10;
            SER_INPUT_ID += SER_INPUT_RAW - '0';
            LCD_DRVR.print(F("> Input ID at SERL!"));
            yield();
            ;
        }
        LCD_DRVR.print(F("> Ready..."));

    case DataDisplayTypes::DEBUG_FNGRPRNT_VERIFY:
        LCD_DRVR.setCursor(0, 0);
        LCD_DRVR.print(F("SC FNGRPRNT VERIFY"));
        LCD_DRVR.setCursor(0, 1);
        LCD_DRVR.print(F("User Verification"));
        LCD_DRVR.setCursor(0, 2);
        LCD_DRVR.print(F("> Valid ID: "));
        LCD_DRVR.setCursor(0, 3);
        LCD_DRVR.print(F("> Ready To Scan."));
        break;

    default:
        break;
    }
    return;
}

void SC_MCU_DRVR::authCheck_Fngrprnt()
{
    if (FPController.is_pressed() && AUTH_INST_CONT.AUTH_CR_ACCESS)
    {
        uint16_t rc = FPController.capture_finger();
        if (rc != GT5X_OK)
        {
            return;
        }

        rc = FPController.verify_finger_with_template(DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT);

        if (rc != GT5X_OK)
        {
            LCD_DRVR.setCursor(0, 3);
            LCD_DRVR.print(F("> Invalid UID!      "));
            return;
        }
        else
        { // Initialize Client for Sending POST Data
            HTTPClient UpdatePOSTData;

            String DevUUID_Req = DEV_INST_CREDENTIALS.DEV_UUID;
            String CrUUID_Req = DEV_INST_CREDENTIALS.DEV_CR_UUID;

            LCD_DRVR.setCursor(0, 3);
            if (!AUTH_INST_CONT.AUTH_FGPRT_STATE)
            {
                digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, LOW);
                digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, LOW);
                AUTH_INST_CONT.AUTH_CR_DOOR = true;
                AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE = true;
                AUTH_INST_CONT.AUTH_FGPRT_STATE = true;
                LCD_DRVR.print(F("> Access Authorized!"));
                checkPresence();
            }
            else
            {
                digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, HIGH);
                digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, HIGH);
                AUTH_INST_CONT.AUTH_CR_DOOR = false;
                AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE = false;
                AUTH_INST_CONT.AUTH_FGPRT_STATE = false;
                sketchForceStop = true;
                LCD_DRVR.print(F("> Locking Commenced!"));
                checkPresence();
            }
            String POSTArgs = DevUUID_Req + "/" + CrUUID_Req + "/" + DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT + "/LockState=" + AUTH_INST_CONT.AUTH_CR_DOOR;
            String RequestDest = "http://" + SERVER_IP_ADDRESS + ":" + SERVER_PORT + "/lockRemoteCall/" + POSTArgs;

            UpdatePOSTData.begin(RequestDest);
            UpdatePOSTData.addHeader("Content-Type", "text/plain");
            uint8_t ResponseRequest = UpdatePOSTData.POST("NODEMCU POST REQ |> LOCK AUTHENTICATION");
            String ResponseMsg = UpdatePOSTData.getString();

            delay(1000);
            Serial.print(F("Query | IP Target |> "));
            Serial.println(RequestDest);
            Serial.print(F("HTTP Response |> "));
            Serial.println(ResponseRequest);
            Serial.print(F("HTTP Message |> "));

            if (ResponseRequest == HTTP_CODE_OK)
            {
                Serial.println(ResponseMsg);
            }
            else
            {
                Serial.println(F("< Failed > | No Response."));
                LCD_DRVR.setCursor(0, 3);
                LCD_DRVR.print(F("> No Conn To Server!"));
                delay(2000);
            }
            UpdatePOSTData.end();
        }
        return;
    }
    else if (!AUTH_INST_CONT.AUTH_CR_ACCESS)
    {
        LCD_DRVR.setCursor(0, 3);
        checkPresence();
        LCD_DRVR.print(F("> Access Disabled!  "));
    }
    else if (AUTH_INST_CONT.AUTH_FGPRT_STATE)
    {
        LCD_DRVR.setCursor(0, 3);
        checkPresence();
        LCD_DRVR.print(F("> InUse. Lock Ready."));
    }
    else
    {
        LCD_DRVR.setCursor(0, 3);
        LCD_DRVR.print(F("> Ready.            "));
    }

    if (ForceEEPROMUpdate)
    {
        ForceEEPROMUpdate = false;
        saveMetaData();
    }
    return;
}

// Then clear the PIR sensor array state by for loop again.
inline void SC_MCU_DRVR::PIR_clearArray()
{
    Serial.println();
    Serial.println("PIR Array Output | Clearing...");
    for (size_t PIR_ARR_ELEM = CONST_VAL::NULL_CONTENT; PIR_ARR_ELEM < CONST_VAL::PIR_DIVIDED_REQUIRED_OUTPUTS; PIR_ARR_ELEM++)
    {
        PIR_ARR_OUTPUT[PIR_ARR_ELEM] = 0;
    }
    Serial.println("PIR Array Output | Done!");
    Serial.println();
    return;
}

bool SC_MCU_DRVR::PIR_isPassed()
{
    uint8_t Bool_TrueCount = CONST_VAL::NULL_CONTENT, Bool_FalseCount = CONST_VAL::NULL_CONTENT, PIR_Percentage = CONST_VAL::NULL_CONTENT;
    Serial.println("PIR Calculation Percentage | Time Extension Checking...");
    for (size_t PIR_ARR_ELEM = CONST_VAL::NULL_CONTENT; PIR_ARR_ELEM < CONST_VAL::PIR_DIVIDED_REQUIRED_OUTPUTS; PIR_ARR_ELEM++)
    {

        (PIR_ARR_OUTPUT[PIR_ARR_ELEM]) ? Bool_TrueCount++ : Bool_FalseCount++;
        PIR_ARR_OUTPUT[PIR_ARR_ELEM] = 0;
        // Then clear the PIR sensor array state by for loop again.
    }
    PIR_Percentage = (Bool_TrueCount * 100) / 10;

    Serial.print("Time Extension Result |> Present: ");
    Serial.print(Bool_TrueCount);
    Serial.print(" | Not-Present: ");
    Serial.println(Bool_FalseCount);

    Serial.print("Calculation Result | ");
    Serial.print(PIR_Percentage);
    Serial.println("%");
    Serial.println();

    return (PIR_Percentage * 100 >= 50) ? true : false;
}
