//

// Example for the MCP49x2 *dual* DACs

// For the single MCP49x1 series, see the other bundled example sketch.

//

#include <SPI.h>  // Remember this line!

#include <DAC_MCP49xx.h>



// The Arduino pin used for the slave select / chip select

#define SS_PIN 10



// The Arduino pin used for the LDAC (output synchronization) feature

#define LDAC_PIN 7



// Set up the DAC.

// First argument: DAC model (MCP4902, MCP4912, MCP4922)

// Second argument: SS pin (10 is preferred)

// (The third argument, the LDAC pin, can be left out if not used)

DAC_MCP49xx dac(DAC_MCP49xx::MCP4902, SS_PIN, LDAC_PIN);  //the first argument was changed from MCP49x2(original code) to MCP4902 to apply to this DAC



void setup() {

  Serial.begin(9600);
  // Set the SPI frequency to 1 MHz (on 16 MHz Arduinos), to be safe.

  // DIV2 = 8 MHz works for me, though, even on a breadboard.

  // This is not strictly required, as there is a default setting.

  dac.setSPIDivider(SPI_CLOCK_DIV2);



  // Use "port writes", see the manual page. In short, if you use pin 10 for

  // SS (and pin 7 for LDAC, if used), this is much faster.

  // Also not strictly required (no setup() code is needed at all).

  dac.setPortWrite(true);



  // Pull the LDAC pin low automatically, to synchronize output

  // This is true by default, however.

  dac.setAutomaticallyLatchDual(true);
}



// Output something slow enough that a multimeter can pick it up.

// For MCP4902, use values below (but including) 255.

// For MCP4912, use values below (but including) 1023.

// For MCP4922, use values below (but including) 4095.

void loop() {

  // Or, to update one channel at a time:

  for (int i=0; i<=255; i+=15){
    dac.outputA(i);  //Change these values to get desired voltage 
    dac.outputB(255-i);
    delay(2500);
    Serial.println(i);
    if (i == 255){
      i = 0;
    }
  //dac.latch(); // To synchonize the two outputs
  }
}
