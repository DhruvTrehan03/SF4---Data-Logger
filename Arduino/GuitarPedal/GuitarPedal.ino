#define out_DAC0 2
#define out_DAC1 3

volatile byte adcPin = 0;
volatile byte prevadcPin = 0;

volatile int input;

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

  // ADCSRA |= (1 << ADPS2); // 16 prescaler, 76.9kHz
  ADCSRA |= (1 << ADPS2) | (1 << ADPS0); // 32 prescaler - 16mHz/32=500kHz 500kHz/13=38.5kHz
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
  // Double check this bit
  TCCR1A = (((PWM_QTY - 1) << 5) | 0x80 | (PWM_MODE << 1));
  TCCR1B = ((PWM_MODE << 3) | 0x11); // ck/1
  TIMSK1 = 0x20; // interrupt on capture interrupt
  ICR1H = (PWM_FREQ >> 8);
  ICR1L = (PWM_FREQ & 0xff);
  DDRB |= ((PWM_QTY << 1) | 0x02); // turn on outputs
}
 
void loop() {
}

ISR(ADC_vect) {
  ADC_low = ADCL;
  ADC_high = ADCH;
  input = ((ADC_high << 8) | ADC_low) + 0x8000; // make a signed 16b value

  // Digital signal processing here:

  // Write to digital output here:
  // OCR1AL = ((input + 0x8000) >> 8); // convert to unsigned, send out high byte
  // OCR1BL = input; // send out low byte
}