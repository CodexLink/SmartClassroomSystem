#include "SmartClassroom.h"

SC_MCU_DRVR::SC_MCU_DRVR(uint16_t BAUD_RATE, const char *SSID, const char *PW)
{
    __BAUD_RATE = BAUD_RATE;
    strcpy(WIFI_SSID, SSID);
    strcpy(WIFI_PW, PW);
}

void SC_MCU_DRVR::begin()
{
    Serial.begin(__BAUD_RATE);
    LCD_DRVR.begin();
    WiFi.begin(WIFI_SSID, WIFI_PW); //WiFi connection
    TempSens.begin();
    LCD_DRVR.noBacklight();
    LCD_DRVR.clear();
    delay(500);
    LCD_DRVR.backlight();
    return;
}

bool SC_MCU_DRVR::checkWiFiConnection()
{
    displayLCDScreen(DataDisplayTypes::CLEAR);
    displayLCDScreen(DataDisplayTypes::WAITPOINT);
    Serial.print("Connection to WiFi is not established. Waiting.");
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(1000);
    }
    Serial.println();
    Serial.print("Connected to ");
    Serial.print(WIFI_SSID);
    Serial.print("!!! | Reference |> ");
    Serial.println(WiFi.localIP());
    displayLCDScreen(DataDisplayTypes::CLEAR);
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
        Serial.println("Connection to WiFi is lost. Awaiting Connection...");
        return (checkWiFiConnection() ? true : false);
    }
}

void SC_MCU_DRVR::displayLCDScreen(DataDisplayTypes Screens)
{
    switch (Screens)
    {
    case DataDisplayTypes::WAITPOINT:

        LCD_DRVR.setCursor(0, 0);
        LCD_DRVR.print("Smart Classroom");
        LCD_DRVR.setCursor(0, 1);
        LCD_DRVR.print("Connecting...");
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
    case DataDisplayTypes::DISP_DATA:
        DHT_Temp = TempSens.readTemperature();
        DHT_Humid = TempSens.readHumidity();
        DHT_HTIndx = TempSens.computeHeatIndex(DHT_Temp, DHT_Humid, false);
        LCD_DRVR.setCursor(0, 0);
        LCD_DRVR.print("TEMP: ");
        LCD_DRVR.print(DHT_Temp);
        LCD_DRVR.print("C");
        LCD_DRVR.setCursor(0, 1);
        LCD_DRVR.print("HT IDX: ");
        LCD_DRVR.print(DHT_HTIndx);
        LCD_DRVR.print("C");
        LCD_DRVR.setCursor(0, 2);
        LCD_DRVR.print("HUMID: ");
        LCD_DRVR.print(DHT_Humid);
        LCD_DRVR.print("%");
        Serial.print("REPORT > TEMP: ");
        Serial.print(DHT_Temp);
        Serial.print("C | HT INDEX: ");
        Serial.print(DHT_HTIndx);
        Serial.print("C | HUMID: ");
        Serial.print(DHT_Humid);
        Serial.println("%");
        break;
    case DataDisplayTypes::DISP_NEXT_SCHED:
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