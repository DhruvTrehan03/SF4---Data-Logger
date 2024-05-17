/* This example shows how to use the MCP49X2 DAC Series (MCP4902, MCP4912 and MCP4922)
   from Microchip Inc. to produce 2 variable voltage outputs using its dual DAC (DAC_A & DAC_B) channels.

   Created by Elochukwu Ifediora on Jan. 19, 2023
*/

#include <MCP49X2.h>

#define EXAMPLE_CS_PIN      13

MCP49X2 DAC;               // MCP4922 is the default
//MCP49X2 DAC(MCP4902);    // Uses MCP4902
//MCP49X2 DAC(MCP4912);    // Uses MCP4912
//MCP49X2 DAC(MCP4922);    // Uses MCP4922

void setup (void) {
    Serial.begin(115200);
    Serial.println(F("\nMCP49X2 Digital-to-Analog Converter (DAC) example\n"));

    SPI.begin();
    if (!DAC.begin(EXAMPLE_CS_PIN)) {
        Serial.println(F("\nError: DAC Initialization failed. Please set CS pin\n"));
        while(1)
            delay(50);
    }

    DAC.vout(DAC_A, 2500);  // Voltage in mV
    DAC.vout(DAC_B, 2000);  // Voltage in mV
}

void loop (void) {
    
}
