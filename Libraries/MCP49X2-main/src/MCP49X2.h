/*
  Per ipsum, et cum ipso, et in ipso,
  est tibi Deo Patri omnipotenti in unitate Spiritus Sancti,
  omnis honor et gloria per omnia saecula saeculorum...

  Copyright (c) 2023 Elochukwu Ifediora. All Rights Reserved
  Contact:  <ifediora elochukwu c @ gmail dot com>
  
  Arduino Library to support the MCP49X2 Series Digital-to-Analog converter (DAC)
  MCP4902, MCP4912 and MCP4922 Microchip's DACs are supported

  For information on installing libraries, see: http://www.arduino.cc/en/Guide/Libraries

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
*/


#ifndef _MCP49X2_H_INCLUDED
#define _MCP49X2_H_INCLUDED

#if (ARDUINO >= 100)
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif

#include <SPI.h>

#ifdef __cplusplus
extern "C" {
#endif

// Uncomment the code line just below if you want to make the MCP49X2 chip select pin an active high pin
#define MCP49X2_ACTIVE_HIGH_CS_PIN
//#define MCP49X2_THREE_WIRE_SPI_INTERFACE

#define MCP49X2_DEFAULT_SPI            SPI
#define MCP49X2_DEFAULT_SPI_FREQUENCY  20000000
#define MCP49X2_DEFAULT_SPI_BITORDER   MSBFIRST
#define MCP49X2_DEFAULT_SPI_DATAMODE   SPI_MODE3
#define MCP49X2_DEFAULT_CS_PIN         -1
#define MCP49X2_DEFAULT_LDAC_PIN       -1
#define MCP49X2_DEFAULT_SHDN_PIN       -1
#define MCP49X2_DEFAULT_VREF_A         3300   // In millivolts
#define MCP49X2_DEFAULT_VREF_B         3300   // In millivolts
#define MCP4902_DAC_DATA(value)        ((uint16_t) (value << 4) & 0B1111111111110000)
#define MCP4912_DAC_DATA(value)        ((uint16_t) (value << 2) & 0B1111111111111100)

typedef enum dac_channel_types {
  DAC_A,
  DAC_B
} dac_channel_t;

typedef enum dac_types {
  MCP49XX,
  MCP4902,
  MCP4912,
  MCP4922
} dac_t;

typedef enum dac_resolution {
  MCP49XX_RESOLURION = 0,
  MCP4902_RESOLURION = 8,
  MCP4912_RESOLURION = 10,
  MCP4922_RESOLURION = 12
} dac_resolution_t;

typedef enum dac_gain {
  GAIN_2,
  GAIN_1
} dac_gain_t;

typedef union dac_register {
  uint16_t reg;
  struct reg_bits {
    /* The bit fields in the 16-bit register. Their description and possible values are included as comments*/
    uint16_t data  : 12;  // DAC Input Data bits: 8-bits for MCP4902, 10-bits for MCP4912, 12-bits for MCP4922
    uint16_t shdn  : 1;   // Active mode operation. 0 = VOUT is unavailable, 1 = VOUT is available
    uint16_t gain  : 1;   // Output Gain Selection bit: 0 = 2 x (VOUT = VREF * D/2^RESOLUTION), 1 = 1 x (VOUT = VREF * D/2^RESOLUTION)
    uint16_t buf   : 1;   // VREF Input Buffer Control bit: 0 = Unbuffered, 1 = Buffered
    uint16_t addr  : 1;   // DACA or DACB Selection bit: 0 = DAC A, 1 = DAC B
  } bits __attribute__ ((__packed__));
} dac_register_t;

#ifdef __cplusplus
}
#endif

class MCP49X2 {
  public:
    MCP49X2(dac_t _dac_type  = MCP4922, uint16_t _vrefa = MCP49X2_DEFAULT_VREF_A, uint16_t _vrefb = MCP49X2_DEFAULT_VREF_B);
    ~MCP49X2();
    
    bool begin(int8_t _cs=MCP49X2_DEFAULT_CS_PIN, int8_t _ldac=MCP49X2_DEFAULT_LDAC_PIN, int8_t _shdn=MCP49X2_DEFAULT_SHDN_PIN);
    void set_spi(SPIClass& _spi);
    void protocol(SPISettings& _settings);
    void protocol(uint32_t frequency=MCP49X2_DEFAULT_SPI_FREQUENCY, uint8_t bitorder=MCP49X2_DEFAULT_SPI_BITORDER, uint8_t mode=MCP49X2_DEFAULT_SPI_DATAMODE);
    
    void vout(dac_channel_t channel, uint16_t mV);
    void write(dac_channel_t channel, uint16_t data);
    void write(dac_channel_t channel);
    void disable(void);
    void enable(void);
    
    inline void gain(dac_channel_t channel, dac_gain_t gain) { \
        if (channel == DAC_A) \
            dacA.bits.gain = (gain == GAIN_1 ? 1 : 0); \
        else if (channel == DAC_B) \
            dacB.bits.gain = (gain == GAIN_1 ? 1 : 0); \
        write(channel); \
    }; \
    
    inline void enable(dac_channel_t channel) { \
        if (channel == DAC_A) \
            dacA.bits.shdn = 1; \
        else if (channel == DAC_B) \
            dacB.bits.shdn = 1; \
        write(channel); \
    }; \

    inline void disable(dac_channel_t channel) { \
        if (channel == DAC_A) \
            dacA.bits.shdn = 0; \
        else if (channel == DAC_B) \
            dacB.bits.shdn = 0; \
        write(channel); \
    }; \
    
    inline void latch(void) { \
        if (ldac >= 0) { \
            digitalWrite(ldac, LOW); \
            delayMicroseconds(1); \
            digitalWrite(ldac, HIGH); \
        } \
    }; \
    
    inline void enable_buffer(dac_channel_t channel) { \
        if (channel == DAC_A) \
            dacA.bits.buf = 1; \
        else if (channel == DAC_B) \
            dacB.bits.buf = 1; \
        write(channel); \
    }; \
    
    inline void disable_buffer(dac_channel_t channel) { \
        if (channel == DAC_A) \
            dacA.bits.buf = 0; \
        else if (channel == DAC_B) \
            dacB.bits.buf = 0; \
        write(channel); \
    }; \
    
    // This doesn't read form the DACs but returns the last value written to the DAC. It acts like a buffer
    inline uint16_t read(dac_channel_t channel) { \
        if (channel == DAC_A) \
            return vouta; \
        else
            return voutb; \
    }; \
    
    inline void vref(dac_channel_t channel, uint16_t mV) { \
        if (channel == DAC_A) \
            vrefa = mV; \
        else
            vrefb = mV; \
    }; \
    
    inline void end(void) { \
        disable(); \
    }; \

  private:
    SPISettings settings;
    SPIClass* spi;

    dac_t dac_type;
    dac_register_t dacA;
    dac_register_t dacB;

    int8_t cs;
    int8_t ldac;
    int8_t shdn;

    uint16_t vrefa;
    uint16_t vrefb;
    uint16_t vouta;
    uint16_t voutb;
    uint8_t resolution;
};

#endif // End _MCP49X2_H_INCLUDED