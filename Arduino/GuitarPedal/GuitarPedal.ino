#include <SPI.h>         // Remember this line!
#include <DAC_MCP49xx.h>

#define SS_PIN 10 // The Arduino pin used for the slave select / chip select
#define LDAC_PIN 7 // The Arduino pin used for the LDAC (output synchronization) feature

int input;
byte adcPin = 0;

DAC_MCP49xx dac(DAC_MCP49xx::MCP4902, SS_PIN, LDAC_PIN);     //the first argument was changed from MCP49x2(original code) to MCP4902 to apply to this DAC


void setup() {
  // Serial.begin(115200);

  setupADC();
  setupDAC();
}

void setupADC() {
  cli(); //disable interrupts

  ADCSRA = 0;
  ADCSRB = 0;

  ADMUX = bit (REFS0) | (adcPin & 0x07) | (1 << ADLAR);

  //ADCSRA |= (1 << ADPS2); // 16 prescaler, 76.9kHz
  // ADCSRA |= (1 << ADPS2) | (1 << ADPS0); // 32 prescaler - 16mHz/32=500kHz 500kHz/13=38.5kHz
  ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // 128 prescaler, 9.6kHz;
  ADCSRA |= (1 << ADIE);
  ADCSRA |= (1 << ADATE); // enabble auto trigger
  ADCSRA |= (1 << ADEN); //enable ADC
  ADCSRA |= (1 << ADSC); //start ADC measurements

  bitSet (DIDR0, ADC0D);  // disable digital buffer on A0
  bitSet (DIDR0, ADC1D);  // disable digital buffer on A1
  bitSet (DIDR0, ADC2D);  // disable digital buffer on A2
  bitSet (DIDR0, ADC3D);  // disable digital buffer on A3
  bitSet (DIDR0, ADC4D);  // disable digital buffer on A4
  bitSet (DIDR0, ADC5D);  // disable digital buffer on A5

  sei(); //enable interrupts
}

void setupDAC() { 
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
}
 
void loop() {
}

ISR(ADC_vect) {
  input = ADCH;
  // Serial.print(input);
  // Serial.print(',');
  // Serial.print(0);
  // Serial.print(',');
  // Serial.println(255);
  dac.output2((input),(-input));
  // Digital signal processing here:

}