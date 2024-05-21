#define out_DAC0 2
#define out_DAC1 3

volatile byte adcPin = 0;
volatile byte prevadcPin = 0;

int inputAudio;
int inputAudioInv;

volatile int input;
volatile boolean adcDone;

void setup() {
  Serial.begin(9600);

  setupADC();
  setupPWM();
}

void setupADC() {
  cli(); //disable interrupts

  ADCSRA = 0;
  ADCSRB = 0;

  ADMUX = bit (REFS0) | (adcPin & 0x07) | (1 << ADLAR);

  ADCSRA |= (1 << ADPS2); // 16 prescaler, 76.9kHz
  // ADCSRA |= (1 << ADPS2) | (1 << ADPS0); // 32 prescaler - 16mHz/32=500kHz 500kHz/13=38.5kHz
  ADCSRA |= (1 << ADIE); //enable interrupts when measurement complete
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

void setupPWM() {

}
 
void loop() {
  if (adcDone) {
    Serial.print(adcPin);
    Serial.print(" - ");
    Serial.println(input);
    delay(1000);
    adcDone = false;
  }

  // if (prevadcPin == 0) {
  //   inputAudio = input;
  // } else if (prevadcPin == 1) {
  //   inputAudioInv = input;
  // }
  // Serial.print("A0:");
  // Serial.print(inputAudio);
  // Serial.print(",");
  // Serial.print("A1:");
  // Serial.print(inputAudioInv);
  // Serial.print(",");
  // Serial.println("Min:0,Max:255");
}

ISR(ADC_vect) {
  ADC_low = ADCL;
  ADC_high = ADCH;
  input = ((ADC_high << 8) | ADC_low) + 0x8000; // make a signed 16b value

  // Change which analogue input is read from
  switch(adcPin) {
    case 0:
      adcPin = 1;
      ADMUX = bit(REFS0) | (adcPin & 0x07) | (1 << ADLAR);
      prevadcPin = 0;
    break;
    // case 1:
    //   ADMUX = bit(REFS0) | (adcPin & 0x07) | (1 << ADLAR);
    //   prevadcPin = 1;
    //   if (adcPin == 2) {
    //     adcPin = 3;
    //   } else if (adcPin == 3) {
    //     adcPin = 4;
    //   } else {
    //     adcPin = 2;
    //   }
    // break;
    default:
      adcPin = 0;
      ADMUX = bit(REFS0) | (adcPin & 0x07) | (1 << ADLAR);
      prevadcPin = 1;
    break;
  }

  adcDone = true;
  // Signal processing here:

  // Write to digital output here:
  // OCR1AL = ((input + 0x8000) >> 8); // convert to unsigned, send out high byte
  // OCR1BL = input; // send out low byte
}