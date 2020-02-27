#include "SmartClassroom.h"

SoftwareSerial FP_WIRE(SC_MCU_DRVR::SENS_DAT_PINS_PUBLIC::FNGR_RX_PIN, SC_MCU_DRVR::SENS_DAT_PINS_PUBLIC::FNGR_TX_PIN);
GT5X FPController(&FP_WIRE);
GT5X_DeviceInfo FP_DEV_INFO;

SC_MCU_DRVR::SC_MCU_DRVR(uint16_t BAUD_RATE, const char *SSID, const char *PW)
{
    __BAUD_RATE = BAUD_RATE;
    strcpy(WIFI_INST_STRUCT.WIFI_SSID, SSID);
    strcpy(WIFI_INST_STRUCT.WIFI_PW, PW);
}

void SC_MCU_DRVR::begin()
{
    Serial.begin(__BAUD_RATE);
    LCD_DRVR.begin();
    WiFi.begin(WIFI_INST_STRUCT.WIFI_SSID, WIFI_INST_STRUCT.WIFI_PW); //WiFi connection
    FP_WIRE.begin(__BAUD_RATE);
    FPController.begin(&FP_DEV_INFO);
    FPController.set_led(false);
    EEPROM.begin(CONST_VAL::EEPROM_MAX_BYTE);

    // ! We can execute this function only if we did some factory configuration.
    if (DEV_INST_CREDENTIALS.DEV_CR_ASSIGNMENT == NULL || DEV_INST_CREDENTIALS.DEV_CR_SHORT_NAME == NULL || DEV_INST_CREDENTIALS.DEV_CR_UUID == NULL || DEV_INST_CREDENTIALS.DEV_UUID == NULL || DEV_INST_CREDENTIALS.AUTH_DEV_USN == NULL || DEV_INST_CREDENTIALS.AUTH_DEV_PWD == NULL || DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT == -1)
    {
        retrieveMetaData();
    }
    else
    {
        saveMetaData();
    }

    pinMode(RESTATED_DEV_PINS::ESP_LED, OUTPUT);
    pinMode(RESTATED_DEV_PINS::MCU_LED, OUTPUT);

    pinMode(SENS_DAT_PINS::PIR_DAT_PIN, OUTPUT);
    TempSens.setup(SENS_DAT_PINS::TEMP_HUD_DAT_PIN, DHTesp::DHT11);

    pinMode(SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, OUTPUT);
    digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, HIGH);

    pinMode(SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, OUTPUT);
    digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, HIGH);

    pinMode(SENS_DAT_PINS_PUBLIC::RELAY_THRD_PIN, OUTPUT);
    digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_THRD_PIN, HIGH);

    LCD_DRVR.noBacklight();
    LCD_DRVR.clear();
    delay(500);
    LCD_DRVR.backlight();
    FPController.set_led(true);
    return;
}

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
        Serial.print(F("AUTH_USER_ID_FNGRPRNT |> "));
        Serial.println(DEV_INST_CREDENTIALS.AUTH_USER_ID_FNGRPRNT);
        EEPROM.end();
        Serial.println(F("EEPROM Data Retrival to Structured Data Done."));
        Serial.println();
    }
    else
    {
        Serial.println(F("EEPROM Stored Data is NULL. Please reupload the sketch with structured data to get started!"));
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
    Serial.println(F("Structured Data with Content Detected. Saving Those Values..."));
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
    if (SketchTimeCheck(CONST_VAL::SCAN_PROC_REQUIRED) && !ENV_INST_CONT.PIR_OPTPT)
    {
        //AUTH_INST_CONT.AUTH_CR_DOOR = !AUTH_INST_CONT.AUTH_CR_DOOR;
        digitalWrite(RELAY_FRST_PIN, HIGH);
        digitalWrite(RELAY_SCND_PIN, HIGH);
        digitalWrite(RELAY_THRD_PIN, HIGH);
        AUTH_INST_CONT.AUTH_CR_DOOR = false;
        AUTH_INST_CONT.AUTH_FGPRT_STATE = false;
        LCD_DRVR.setCursor(0, 3);
        LCD_DRVR.print(F("> No Presence...    "));
        delay(1000);
        return false;
    }
    return true;
}

bool SC_MCU_DRVR::SketchTimeCheck(uint32_t TimeIntervalToMeet)
{
    uint_fast32_t sketchBaseTime = millis();
    static bool sketchRelease = true;
    static uint_fast32_t sketchPreviousHit;

    if (sketchForceStop)
    {
        Serial.println(F("Sketch Time Process Stopper Initialized."));
        sketchForceStop = false;
        sketchRelease = true;
        return true;
    }

    if (sketchRelease)
    {
        sketchRelease = false;
        sketchPreviousHit = sketchBaseTime;
    }

    Serial.print(F("Sketch Time: "));
    Serial.print(sketchBaseTime);
    Serial.print(F(" - "));
    Serial.print(sketchPreviousHit);
    Serial.print(F(" > "));
    Serial.print(F(" = "));
    Serial.println(sketchBaseTime - sketchPreviousHit);

    if (!sketchRelease && (uint_fast32_t)(sketchBaseTime - sketchPreviousHit) >= TimeIntervalToMeet)
    {
        sketchRelease = true;
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
        ENV_INST_CONT.DHT11_TEMP = (isnan(ENV_INST_CONT.DHT11_TEMP) == TempSens.getTemperature()) ? ENV_INST_CONT.DHT11_TEMP : TempSens.getTemperature();
        ENV_INST_CONT.DHT11_HUMID = (isnan(ENV_INST_CONT.DHT11_HUMID) == TempSens.getHumidity()) ? ENV_INST_CONT.DHT11_HUMID : TempSens.getHumidity();
        ENV_INST_CONT.DHT11_HT_INDX = (isnan(ENV_INST_CONT.DHT11_HT_INDX) == TempSens.computeHeatIndex(ENV_INST_CONT.DHT11_TEMP, ENV_INST_CONT.DHT11_HUMID, false)) ? ENV_INST_CONT.DHT11_HT_INDX : TempSens.computeHeatIndex(ENV_INST_CONT.DHT11_TEMP, ENV_INST_CONT.DHT11_HUMID, false);
        ENV_INST_CONT.PIR_OPTPT = digitalRead(SENS_DAT_PINS::PIR_DAT_PIN);
        LCD_DRVR.setCursor(0, 0);
        LCD_DRVR.print(DEV_INST_CREDENTIALS.DEV_CR_ASSIGNMENT);
        LCD_DRVR.print(F(" | "));
        LCD_DRVR.print(DEV_INST_CREDENTIALS.DEV_CR_SHORT_NAME);
        LCD_DRVR.setCursor(0, 1);
        LCD_DRVR.print(F("S:"));
        LCD_DRVR.print((AUTH_INST_CONT.AUTH_CR_DOOR) ? "UnLkd" : "Lockd");
        LCD_DRVR.print(F(" | T:"));
        LCD_DRVR.print(ENV_INST_CONT.DHT11_TEMP, 1);
        LCD_DRVR.print(F("C"));
        LCD_DRVR.setCursor(0, 2);
        LCD_DRVR.print(F("H:"));
        LCD_DRVR.print(ENV_INST_CONT.DHT11_HUMID, 1);
        LCD_DRVR.print(F("% | HTI:"));
        LCD_DRVR.print(ENV_INST_CONT.DHT11_HT_INDX, 1);
        LCD_DRVR.print(F("C"));

        //Serial.print("MODULE REPORTS | T: ");
        //Serial.print(ENV_INST_CONT.DHT11_TEMP);
        //Serial.print("C | HTI: ");
        //Serial.print(ENV_INST_CONT.DHT11_HT_INDX);
        //Serial.print("C | HUD: ");
        //Serial.print(ENV_INST_CONT.DHT11_HUMID);
        //Serial.print("%");
        //Serial.print(" | MOTION SENS: ");
        //Serial.println(ENV_INST_CONT.PIR_OPTPT);
        digitalWrite(RESTATED_DEV_PINS::MCU_LED, HIGH);
        break;

    case DataDisplayTypes::DEBUG_FNGRPRNT_ENROLL:
        LCD_DRVR.setCursor(0, 0);
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        LCD_DRVR.setCursor(0, 1);
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        LCD_DRVR.setCursor(0, 2);
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        break;

    case DataDisplayTypes::DEBUG_FNGRPRNT_VERIFY:
        LCD_DRVR.setCursor(0, 0);
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        LCD_DRVR.setCursor(0, 1);
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        LCD_DRVR.setCursor(0, 2);
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        break;

    case DataDisplayTypes::DEBUG_MCU_GENERALIZED:
        LCD_DRVR.setCursor(0, 0);
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        LCD_DRVR.setCursor(0, 1);
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        LCD_DRVR.setCursor(0, 2);
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
        //LCD_DRVR.print();
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

        rc = FPController.verify_finger_with_template(AUTH_INST_CONT.AUTH_USER_ID_FNGRPRNT);

        if (rc != GT5X_OK)
        {
            digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, HIGH);
            digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, HIGH);
            digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_THRD_PIN, HIGH);
            LCD_DRVR.setCursor(0, 3);
            AUTH_INST_CONT.AUTH_FGPRT_STATE = false;
            LCD_DRVR.print(F("> Invalid UID!"));
            return;
        }
        else
        {
            digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, LOW);
            digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, LOW);
            digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_THRD_PIN, LOW);
            AUTH_INST_CONT.AUTH_CR_DOOR = true;
            AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE = true;

            LCD_DRVR.setCursor(0, 3);
            if (!AUTH_INST_CONT.AUTH_FGPRT_STATE)
            {
                AUTH_INST_CONT.AUTH_FGPRT_STATE = true;
                LCD_DRVR.print(F("> Access Authorized!"));
                delay(1000);
            }
            else
            {
                AUTH_INST_CONT.AUTH_CR_DOOR = false;
                AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE = false;
                AUTH_INST_CONT.AUTH_FGPRT_STATE = false;
                sketchForceStop = true;
                LCD_DRVR.print(F("> Locking Verified! "));
                delay(1000);
            }
            return;
            // Add Relay ON State.
        }
    }
    else
    {
        LCD_DRVR.setCursor(0, 3);
        if (!AUTH_INST_CONT.AUTH_CR_ACCESS)
        {
            LCD_DRVR.print(F("> Access Disabled!  "));
        }
        else
        {
            if (AUTH_INST_CONT.AUTH_FGPRT_STATE)
            {
                if (checkPresence() && FPController.is_pressed() && AUTH_INST_CONT.AUTH_CR_ACCESS)
                {
                    uint16_t rc = FPController.capture_finger();
                    if (rc != GT5X_OK)
                    {
                        return;
                    }
                    rc = FPController.verify_finger_with_template(AUTH_INST_CONT.AUTH_USER_ID_FNGRPRNT);
                    if (rc != GT5X_OK)
                    {
                        LCD_DRVR.print(F("> Invalid UID!"));
                    }
                    else
                    {
                        AUTH_INST_CONT.AUTH_FGPRT_STATE = true;
                        sketchForceStop = true;
                        LCD_DRVR.print(F("> Locking Verified! "));
                    }
                }
                else
                {
                    LCD_DRVR.print(F("> InUse. Lock Ready."));
                }
            }
            else
            {
                LCD_DRVR.print(F("> Ready.            "));
            }
        }
        return;
    }
}