//

// Example for the MCP49x2 *dual* DACs

// For the single MCP49x1 series, see the other bundled example sketch.

//

#include <SPI.h>         // Remember this line!
#include <DAC_MCP49xx.h>
#include <analogWave.h>

#define SS_PIN 10 // The Arduino pin used for the slave select / chip select
#define LDAC_PIN 7 // The Arduino pin used for the LDAC (output synchronization) feature

// Set up the DAC. 
// First argument: DAC model (MCP4902, MCP4912, MCP4922)
// Second argument: SS pin (10 is preferred)
// (The third argument, the LDAC pin, can be left out if not used)

DAC_MCP49xx dac(DAC_MCP49xx::MCP4902, SS_PIN, LDAC_PIN);     //the first argument was changed from MCP49x2(original code) to MCP4902 to apply to this DAC
analogWave wave(DAC_MCP49xx);   // Create an instance of the analogWave class, using the DAC pin

int freq = 10;  // in hertz, change accordingly
float i = 0;

void setup() {

  Serial.begin(115200);
  // Set the SPI frequency to 1 MHz (on 16 MHz Arduinos), to be safe.
  // DIV2 = 8 MHz works for me, though, even on a breadboard.
  // This is not strictly required, as there is a default setting.
  dac.setSPIDivider(SPI_CLOCK_DIV16);
  // Use "port writes", see the manual page. In short, if you use pin 10 for
  // SS (and pin 7 for LDAC, if used), this is much faster.
  // Also not strictly required (no setup() code is needed at all).
  dac.setPortWrite(true);
  // Pull the LDAC pin low automatically, to synchronize output
  // This is true by default, however.
  dac.setAutomaticallyLatchDual(true);
  wave.
}

 

// Output something slow enough that a multimeter can pick it up.

// For MCP4902, use values below (but including) 255.


void loop() {
  float sound = 125*(sin(i*4*3.14)+1);
  dac.output2((sound),(-sound));
  Serial.println(sound);
  i+= 0.5;
}
