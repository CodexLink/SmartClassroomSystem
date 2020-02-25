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

#define TX_OVERRIDE 3
#define SSD3 10
class SC_MCU_DRVR
{
    // ! Container that can be to reference all constant values.
    enum CONST_VAL
    {
        NULL_CONTENT = 0,
        MAX_REL_CHANNEL = 5,
        MAX_IP_ADDR_CHAR = 15,
        MAX_WIFI_SSD_CHAR = 32,
        MAX_WIFI_PW_CHAR = 63,
        ESP_DEFAULT_PORT = 80,
        MAX_STR_CR = 20,
        MAX_STR_UUID = 40,
        MAX_FNGRPRNT_STORABLE = 3000,
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
        PIR_DAT_PIN = D1,
        DEMUX_LTCH_PIN = 0,
        DEMUX_CLK_PIN = 0,
    };

    struct WIFI_CRENDENTIALS
    {
        char WIFI_SSID[MAX_WIFI_SSD_CHAR];
        char WIFI_PW[MAX_WIFI_PW_CHAR];
    } WIFI_INST_STRUCT;

    // ! Variables
    uint16_t __BAUD_RATE = CONST_VAL::NULL_CONTENT;
    uint8_t RELAY_TRIGGER[CONST_VAL::MAX_REL_CHANNEL] = {CONST_VAL::NULL_CONTENT}; // ! We'll be using 4-channel relay module

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
        uint8_t PIR_OPTPT;
        uint32_t PIR_MILLIS_TRIGGER;
    } ENV_INST_CONT;

    struct AUTH_STATE
    {
        uint8_t AUTH_FGPRT_STATE; // 1 Passed, 0 Not Passed

        bool AUTH_CR_DOOR = 1;        // 1 Locked, 0 Unlocked
        bool AUTH_CR_ACCESS = 1;      // 1 Enabled, 0 Disabled
        bool NON_AUTH_ELECTRIC_STATE = 0;      // 1 Enabled, 0 Disabled
        bool AUTH_FP_LED_STATE; // LED ON, LED OFF
        uint16_t AUTH_USER_ID_FNGRPRNT = 1; // Must be set by user.
        //int16_t AUTH_USER_ID_FNGRPRNTS[10] = -1;
    } AUTH_INST_CONT;

    const struct DEV_CREDENTIALS
    {
        char *DEV_CR_ASSIGNED;
        char * DEV_CR_ROOM;
        char *DEV_UID;
        char *AUTH_DEV_USN;
        char *AUTH_DEV_PWD;
    } DEV_INST_CREDENTIALS
    {

        .DEV_CR_ASSIGNED = "Q-5424",
        .DEV_CR_ROOM = "CompEng Lab", // Lckd, Used
        .DEV_UID = "df826e0334b84f2689e64f2c6b24a6ab",
        .AUTH_DEV_USN = "NodeMCU | Q-5424",
        .AUTH_DEV_PWD = "df826e0334b84f2689e64f2c6b24a6ab",
    };

    // General Function To Be Used.
    SC_MCU_DRVR(uint16_t BAUD_RATE, const char *SSID, const char *PW);
    void begin();
    bool mntndWiFiConnection();
    void displayLCDScreen(DataDisplayTypes Screens);
    void authCheck_Fngrprnt();
    //void

private:
    bool checkWiFiConnection();
    inline bool FNGRPRNT_isLEDState(bool whatState, bool changeOnFalse);
    inline void FNGRPRNT_InverseLEDState();
    //void InterpretData(DataInterpretTypes DataType);
};

// END OF FILE SMARTROOM