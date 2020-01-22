#pragma once

// Add Some Library Here.
#include <ESP8266HTTPClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
//#include "ArduinoJSON.h"
#include "DHT.h"
#include "LiquidCrystal_I2C.h"

class SC_MCU_DRVR
{
    // ! Container that can be to reference all constant values.
    enum ConstantsVal : uint8_t
    {
        NULL_CONTENT = 0,
        MAX_REL_CHANNEL = 5,
        MAX_IP_ADDR_CHAR = 15,
        MAX_WIFI_SSD_CHAR = 32,
        MAX_WIFI_PW_CHAR = 63,
        ESP_DEFAULT_PORT = 80
    };

    enum ConstantsDev : uint8_t
    {
        LCD_ADDR = 0x27,
        LCD_W = 20,
        LCD_H = 4
    };

    // * This Container utilizes PINs to be used to scan the whole room.
    enum SensDataPins : uint8_t
    {
        PIR_DAT_PIN = 12,
        TEMP_HUD_DAT_PIN = 14,
        FNGR_DAT_PIN = NULL_CONTENT
    };

    // ! Variables
    uint16_t __BAUD_RATE = NULL_CONTENT;
    uint8_t REL_TRIGGER[ConstantsVal::MAX_REL_CHANNEL] = {NULL_CONTENT}; // ! We'll be using 4-channel relay module

    char WIFI_SSID[ConstantsVal::MAX_WIFI_SSD_CHAR] = {NULL_CONTENT};
    char WIFI_PW[ConstantsVal::MAX_WIFI_PW_CHAR] = {NULL_CONTENT};

    // To be use when DJango sends GET request.

    // ! Environmental Container Variables
    float DHT_Temp = NULL_CONTENT;
    float DHT_Humid = NULL_CONTENT;
    float DHT_HTIndx = NULL_CONTENT;

    // ! Object (Class) Instance
    LiquidCrystal_I2C LCD_DRVR{ConstantsDev::LCD_ADDR, ConstantsDev::LCD_W, ConstantsDev::LCD_H};
    DHT TempSens{SensDataPins::TEMP_HUD_DAT_PIN, DHT22};
    ESP8266WebServer NodeServer{ConstantsVal::ESP_DEFAULT_PORT};

public:
    // * Declares Data Interpretation To Be Used As A Parameter Later.
    enum DataInterpretTypes
    {
        AUTH_TYPE,
        SENS_TYPE,
        REL_TYPE
    };

    enum DataDisplayTypes
    {
        INITIALIZE,
        CLEAR,
        CLEAR_OFF_DISP,
        WAITPOINT,
        DISP_DATA,
        DISP_NEXT_SCHED,
        DISP_TIMEOUT
    };

    String DictContainer = "";

    // General Function To Be Used.
    SC_MCU_DRVR(uint16_t BAUD_RATE, const char *SSID, const char *PW);
    void begin();
    bool checkWiFiConnection();
    bool mntndWiFiConnection();
    void displayLCDScreen(DataDisplayTypes Screens);
    // Fingerprint Function
    void sendAuthenticate();

private:
    void scanSens();
    void WaitForData();

    void SendData(uint8_t TimeToSend);
    void InterpretData(DataInterpretTypes DataType);
};

// END OF FILE SMARTROOM