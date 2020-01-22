// ! Room Scanner | By Janrey "CodexLink" Licas
// * Created on 01/16/2019
// For use in room scanning only.

#include "SmartClassroom.h"

SC_MCU_DRVR SC(9600, "HW_EcLi284255H_Cdx", "@Li2019_b015@");
ESP8266WebServer NodeServer(80); // ! Make this public. Cause a lot of CONFLICTS.

// Unreferenced / Unclassed functions
void HandleGET_Sens();
void HandlePOST_SetMode();

void setup()
{
    SC.begin();
    NodeServer.on("/RequestSens", HTTP_GET , HandleGET_Sens);
    NodeServer.on("/ChangeMode", HTTP_POST, HandlePOST_SetMode);
    NodeServer.begin();
    SC.displayLCDScreen(SC_MCU_DRVR::DataDisplayTypes::CLEAR_OFF_DISP);
}

void loop()
{
    while (SC.mntndWiFiConnection())
    {
        SC.displayLCDScreen(SC_MCU_DRVR::DataDisplayTypes::DISP_DATA);
        NodeServer.handleClient();
        delay(100);
    }
}

void HandleGET_Sens()
{
    NodeServer.send(200, "text/plain", String("sdjoisdajoi") + String("asdsadsad"));
}

void HandlePOST_SetMode()
{
    NodeServer.send(200, "sdjoisdajoi");
}