#include <SPI.h>
#include <DAC_MCP49xx.h>

#define SS_PIN 10
#define LDAC_PIN 7

float i = 0;
float incomingAudio;
int pot1, pot2;
bool mode = 0; // 0 is playing mode, 1 is node selector and FFT

int effect1 = 3;
int effect2 = 1;

DAC_MCP49xx dac(DAC_MCP49xx::MCP4902, SS_PIN, LDAC_PIN); // Set up the DAC. First argument: DAC model (MCP4902, MCP4912, MCP4922). Second argument: SS pin (10 is preferred). (The third argument, the LDAC pin, can be left out if not used)

// Effect functions and parameters here:
int tremolo_i = 0;
int delay_i = 0;
int chorus_i = 0;
int chorus_sin_i = 0;
const unsigned int MAX_DELAY = 1500;
// Can edit these
float fuzz_gain = 1.0;
float tremolo_modulation_freq = 0.1;
float chorus_modulation_freq = 0.1;
int delay_time = 1000;
int chorus_time = 1000;
byte delay_buffer[MAX_DELAY+1];

void setup() {
  Serial.begin(9600);
  dac.setSPIDivider(SPI_CLOCK_DIV16); // Set the SPI frequency to 1 MHz (on 16 MHz Arduinos), to be safe.
  dac.setPortWrite(true);
  dac.setAutomaticallyLatchDual(true); // Pull the LDAC pin low automatically, to synchronize output
}

void loop() {
  incomingAudio = analogRead(A0) / 511.5 - 1.0; // From -1 to 1
  pot1 = (int)analogRead(A1)/20*20; // Values go from 0-1023 but rounded down to nearest 20
  pot2 = (int)analogRead(A2)/20*20;

  float output = 0.0;

  switch (effect1) {
    case 1:
      output = incomingAudio;
      break;
    case 2:
      fuzz_gain = pot1/72.9 + 1;
      output += Fuzz(incomingAudio);
      break;
    case 3:
      tremolo_modulation_freq = pot1/1020.0 + 0.1;
      output += Tremolo(incomingAudio);
      break;
    case 4:
      output += Overdrive(incomingAudio);
      break;
    case 5:
      delay_time = pot1;
      output += Delay(incomingAudio);
      break;
    case 6:
      chorus_time = pot1;
      output += Chorus(incomingAudio);
      break;
  }
    
  switch (effect2) {
    case 1:
      output = output;
      break;
    case 2:
      fuzz_gain = pot2/68.0 + 1;
      output = Fuzz(output);
      break;
    case 3:
      tremolo_modulation_freq = pot2/1020.0 + 0.1;
      output = Tremolo(output);
      break;
    case 4:
      output = Overdrive(output);
      break;
    case 5:
      delay_time = pot2;
      output = Delay(output);
      break;
    case 6:
      chorus_time = pot2;
      output = Chorus(output);
      break;
  }
  
  output = (output+1.0)*127.5;
  dac.output2((output),(-output));


  // for (int i = 0; i < 360; i += 1) {
  //   float sine = 511.5 * sin(i * M_PI * 20 / 180) + 511.5;
  //   Serial.print((byte)((sine+1)/4-1));
  //   Serial.print(',');
  //   Serial.print(Delay(sine));
  //   Serial.print(',');
  //   Serial.print(0);
  //   Serial.print(',');
  //   Serial.println(255);
  //   delay(10);
  // }
}

void setup_playMode() {

}

float Overdrive(float signal) {
  float output;

  if (signal > 0.667) {
    output = 1;
  } else if (0.333 < signal && signal <= 0.667) {
    output = (3-(2-3*signal)*(2-3*signal))/3;
  } else if (-0.333 < signal && signal <= 0.333) {
    output = 2 * signal;
  } else if (-0.667 < signal && signal <= -0.333) {
    output = (-3+(2+3*signal)*(2+3*signal))/3;
  } else {
    output = -1;
  }

  return output;
}

float Fuzz(float signal) {
  float output;

  output = (signal/abs(signal)) * (1-exp(-fuzz_gain*abs(signal)));
  return output;
}

float Tremolo(float signal) {
  float output;

  output = sin((float)tremolo_i * M_PI * tremolo_modulation_freq / 180.0) * signal;
  tremolo_i++;
  if (tremolo_i >= 360) tremolo_i = 0;

  return output;
}

float Delay(float signal) {
  float output;
  int x = (int)((signal+1.0)*127.5); // From 0 to 255

  delay_buffer[delay_i] = (byte)x;
  delay_i++;
  if (delay_i  > MAX_DELAY) delay_i = 0;
  
  output = delay_buffer[delay_i - delay_time];
  if (delay_i < delay_time) output = delay_buffer[MAX_DELAY+1+(delay_i-delay_time)];
  output = output + x; // 0 to 511

  return output/255.5-1.0; // -1 to 1
}

float Chorus(float signal) {
  float output;
  int x = (int)((signal+1.0)*127.5); // From 0 to 255

  delay_buffer[chorus_i] = (byte)x;
  chorus_i++;
  if (chorus_i  > MAX_DELAY) chorus_i = 0;

  chorus_time = sin((float)chorus_sin_i * M_PI * chorus_modulation_freq / 180.0) * chorus_time;
  chorus_sin_i++;
  if (chorus_sin_i >= 360) chorus_sin_i = 0;
  
  output = delay_buffer[chorus_i - chorus_time];
  if (chorus_i < chorus_time) output = delay_buffer[MAX_DELAY+1+(chorus_i-chorus_time)];

  output = output + x; // 0 to 511

  return output/255.5-1.0; // -1 to 1
}