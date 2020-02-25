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

bool SC_MCU_DRVR::checkWiFiConnection()
{
    displayLCDScreen(DataDisplayTypes::CLEAR);
    displayLCDScreen(DataDisplayTypes::WAITPOINT);
    Serial.print("Connection to WiFi is not established. Waiting.");
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
    Serial.print("Connected to ");
    Serial.print(WIFI_INST_STRUCT.WIFI_SSID);
    Serial.print("!!! | IP Address |> ");
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
        Serial.println("Connection to WiFi was lost. Attempting ReConnection...");
        return (checkWiFiConnection() ? true : false);
    }
}

void SC_MCU_DRVR::displayLCDScreen(DataDisplayTypes Screens)
{
    switch (Screens)
    {
    case DataDisplayTypes::WAITPOINT:
        LCD_DRVR.setCursor(0, 0);
        LCD_DRVR.print("Smart Classroom Sys.");
        LCD_DRVR.setCursor(0, 1);
        LCD_DRVR.print(" Ver. 02222020-2327");
        LCD_DRVR.setCursor(0, 2);
        LCD_DRVR.print(" Interactless Mgmt.");
        LCD_DRVR.setCursor(0, 3);
        LCD_DRVR.print(" Connecting to SSID");
        break;

    case DataDisplayTypes::WAIT_CLEAR:
        LCD_DRVR.setCursor(0, 3);
        LCD_DRVR.print("     Connected!     ");
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
        ENV_INST_CONT.DHT11_TEMP = TempSens.getTemperature();
        ENV_INST_CONT.DHT11_HUMID = TempSens.getHumidity();
        ENV_INST_CONT.DHT11_HT_INDX = TempSens.computeHeatIndex(ENV_INST_CONT.DHT11_TEMP, ENV_INST_CONT.DHT11_HUMID, false);
        LCD_DRVR.setCursor(0, 0);
        LCD_DRVR.print(DEV_INST_CREDENTIALS.DEV_CR_ASSIGNED);
        LCD_DRVR.print(F(" | "));
        LCD_DRVR.print(DEV_INST_CREDENTIALS.DEV_CR_ROOM);
        LCD_DRVR.setCursor(0, 1);
        LCD_DRVR.print(F("S:"));
        LCD_DRVR.print((AUTH_INST_CONT.AUTH_CR_DOOR) ? "Lockd" : "UnLkd");
        LCD_DRVR.print(F(" | T:"));
        LCD_DRVR.print(ENV_INST_CONT.DHT11_TEMP, 1);
        LCD_DRVR.print(F("C"));
        LCD_DRVR.setCursor(0, 2);
        LCD_DRVR.print(F("H:"));
        LCD_DRVR.print(ENV_INST_CONT.DHT11_HUMID, 1);
        LCD_DRVR.print(F("% | HTI:"));
        LCD_DRVR.print(ENV_INST_CONT.DHT11_HT_INDX, 1);
        LCD_DRVR.print(F("C"));

        Serial.print("DEV REPORT | T, P: ");
        Serial.print(ENV_INST_CONT.DHT11_TEMP);
        Serial.print("C | HTI: ");
        Serial.print(ENV_INST_CONT.DHT11_HT_INDX);
        Serial.print("C | HUD: ");
        Serial.print(ENV_INST_CONT.DHT11_HUMID);
        Serial.println("%");
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
            AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE = false;
            AUTH_INST_CONT.AUTH_CR_DOOR = true;
            LCD_DRVR.print(F("> Invalid UID!"));
            return;
        }
        else
        {
            digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, LOW);
            digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, LOW);
            digitalWrite(SENS_DAT_PINS_PUBLIC::RELAY_THRD_PIN, LOW);
            AUTH_INST_CONT.AUTH_CR_DOOR = false;
            AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE = true;
            LCD_DRVR.setCursor(0, 3);
            LCD_DRVR.print(F("> Verified UID: "));
            LCD_DRVR.print(AUTH_INST_CONT.AUTH_USER_ID_FNGRPRNT);
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
            LCD_DRVR.print(F("> Ready.            "));
        }
        return;
    }
}

inline bool SC_MCU_DRVR::FNGRPRNT_isLEDState(bool whatState, bool changeOnFalse)
{
    bool retState = (whatState == AUTH_INST_CONT.AUTH_FP_LED_STATE) ? true : false;
    Serial.print(F("FNGRPRNT_isLEDState | "));
    Serial.print(F("Given State |> "));
    Serial.print(whatState);
    Serial.print(F(" | changedOnFalse |> "));
    Serial.print(changeOnFalse);
    Serial.print(F(" | funcReturn |> "));
    Serial.println(retState);

    // If we dont need to change anything and we just want the state then just return bool.
    if (!changeOnFalse)
    {
        return retState;
    }
    else // We return the same thing from above except we do some extra steps.
    {
        if (!retState)
            FNGRPRNT_InverseLEDState();
    }
}

inline void SC_MCU_DRVR::FNGRPRNT_InverseLEDState()
{
    Serial.print(F("FNGRPRNT_InverseLEDState | "));
    Serial.print(F("Before |> "));
    Serial.print(AUTH_INST_CONT.AUTH_FP_LED_STATE);
    Serial.print(F(" | After |> "));
    Serial.println(!AUTH_INST_CONT.AUTH_FP_LED_STATE);
    // Inverse the output whenever this function was executed.
    AUTH_INST_CONT.AUTH_FP_LED_STATE = !AUTH_INST_CONT.AUTH_FP_LED_STATE;
    FPController.set_led(AUTH_INST_CONT.AUTH_FP_LED_STATE);
    return;
}
