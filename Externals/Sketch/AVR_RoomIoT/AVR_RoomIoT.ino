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
    NodeServer.send(200, "text/plain", String("{'DATA_HEADER': {'CR_IDNTY': '") + SC.DEV_INST_CREDENTIALS.DEV_CR_ASSIGNED + String("', 'CR_UID': '") + SC.DEV_INST_CREDENTIALS.DEV_UID + String("'}, 'DATA_SENS': {'CR_TEMP': '") + SC.ENV_INST_CONT.DHT11_TEMP + String("', 'CR_HUMD': '") + SC.ENV_INST_CONT.DHT11_HUMID + String("', 'CR_HTINX': '") + SC.ENV_INST_CONT.DHT11_HT_INDX + String("', 'PIR_MOTION': {'PIR_OTPT':'") + SC.ENV_INST_CONT.PIR_OPTPT + String("', 'PIR_OTPT_TIME_TRIGGER': '") + SC.ENV_INST_CONT.PIR_MILLIS_TRIGGER + String("'}}, 'DATA_AUTH': {'AUTH_ID':'") + SC.AUTH_INST_CONT.AUTH_USER_ID_FNGRPRNT + String("', 'AUTH_STATE': '") + SC.AUTH_INST_CONT.AUTH_FGPRT_STATE + String("'}, 'DATA_STATE': {'DOOR_STATE': '") + SC.AUTH_INST_CONT.AUTH_CR_DOOR + String("', 'ACCESS_STATE': '") + SC.AUTH_INST_CONT.AUTH_CR_ACCESS + String("', 'ELECTRIC_STATE': '") + SC.AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE + String("'}}"));
    digitalWrite(SC.RESTATED_DEV_PINS::ESP_LED, HIGH);
}

// Put some Argument Checking Here. But first finalized the request input and outputs.
// https://robotzero.one/sending-data-esp8266-to-esp8266/
void HandleGET_SetInstance()
{
    if (!NodeServer.authenticate(SC.DEV_INST_CREDENTIALS.AUTH_DEV_USN, SC.DEV_INST_CREDENTIALS.AUTH_DEV_PWD))
    {
        return NodeServer.requestAuthentication();
    }

    digitalWrite(SC.RESTATED_DEV_PINS::ESP_LED, LOW);
    if (NodeServer.arg("lock_state") == "True")
    {
        digitalWrite(SC_MCU_DRVR::SENS_DAT_PINS_PUBLIC::RELAY_THRD_PIN, LOW);
        SC.AUTH_INST_CONT.AUTH_CR_DOOR = !SC.AUTH_INST_CONT.AUTH_CR_DOOR;
        NodeServer.send(200, "text/plain", "LOCK_STATE |> CHANGE TO ENABLED |> OK");
    }
    else if (NodeServer.arg("lock_state") == "False")
    {
        digitalWrite(SC_MCU_DRVR::SENS_DAT_PINS_PUBLIC::RELAY_THRD_PIN, HIGH);
        SC.AUTH_INST_CONT.AUTH_CR_DOOR = !SC.AUTH_INST_CONT.AUTH_CR_DOOR;
        NodeServer.send(200, "text/plain", "LOCK_STATE |> CHANGE TO DISABLED |> OK");
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
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, LOW);
        SC.AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE = true;
        NodeServer.send(200, "text/plain", "ELECTRIC_STATE |> CHANGED TO 'ENABLED' |> OK");
    }
    else if (NodeServer.arg("electric_state") == "False")
    {
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, HIGH);
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, HIGH);
        SC.AUTH_INST_CONT.NON_AUTH_ELECTRIC_STATE = false;
        NodeServer.send(200, "text/plain", "ELECTRIC_STATE |> CHANGED TO 'DISABLED' |> OK");
    }


    // This disables all access from the classroom. The relays will be turned off.
    if (NodeServer.arg("cr_access") == "True")
    {
        digitalWrite(SC_MCU_DRVR::SENS_DAT_PINS_PUBLIC::RELAY_THRD_PIN, LOW);
        SC.AUTH_INST_CONT.AUTH_CR_DOOR = !SC.AUTH_INST_CONT.AUTH_CR_DOOR;
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, LOW);
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, LOW);
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_THRD_PIN, LOW);
        SC.AUTH_INST_CONT.AUTH_CR_ACCESS = true;
        NodeServer.send(200, "text/plain", "CR_ACCESS |> CHANGED TO 'ENABLED' |> OK");
    }

    else if (NodeServer.arg("cr_access") == "False")
    {
        digitalWrite(SC_MCU_DRVR::SENS_DAT_PINS_PUBLIC::RELAY_THRD_PIN, HIGH);
        SC.AUTH_INST_CONT.AUTH_CR_DOOR = !SC.AUTH_INST_CONT.AUTH_CR_DOOR;
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_FRST_PIN, HIGH);
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_SCND_PIN, HIGH);
        digitalWrite(SC.SENS_DAT_PINS_PUBLIC::RELAY_THRD_PIN, HIGH);
        SC.AUTH_INST_CONT.AUTH_CR_ACCESS = false;
        NodeServer.send(200, "text/plain", "CR_ACCESS |> CHANGED TO 'DISABLED' |> OK");
    }


    // ! Two of these arguments has need to be supplied both before we can run the if statement scope under it.
    if (NodeServer.arg("dev_uid_replace") && NodeServer.arg("dev_name_replace"))
    {
    }

    // This requires multiple logical function.
    if (NodeServer.arg("cr_automate") == "")
    {
    }

    digitalWrite(SC.RESTATED_DEV_PINS::ESP_LED, HIGH);
}