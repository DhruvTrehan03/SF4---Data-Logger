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

#include <MCP49X2.h>

MCP49X2::MCP49X2(dac_t _dac_type, uint16_t _vrefa, uint16_t _vrefb): \
           settings(MCP49X2_DEFAULT_SPI_FREQUENCY, MCP49X2_DEFAULT_SPI_BITORDER, MCP49X2_DEFAULT_SPI_DATAMODE), \
           spi(&MCP49X2_DEFAULT_SPI), \
           dac_type(_dac_type), \
           cs(-1), \
           ldac(-1), \
           shdn(-1), \
           vrefa(_vrefa), \
           vrefb(_vrefb) \
{

}

MCP49X2::~MCP49X2() {
    end();
}

void MCP49X2::set_spi(SPIClass& _spi) {
    spi = &_spi;
}

void MCP49X2::protocol(SPISettings& _settings) {
    settings = _settings;
}

void MCP49X2::protocol(uint32_t frequency, uint8_t bitorder, uint8_t mode) {
    settings = SPISettings(frequency, bitorder, mode);
}

bool MCP49X2::begin(int8_t _cs, int8_t _ldac, int8_t _shdn) {
#ifndef MCP49X2_THREE_WIRE_SPI_INTERFACE
    if (_cs >= 0) {
        cs = _cs;
        pinMode(cs, OUTPUT);
        #ifdef MCP49X2_ACTIVE_HIGH_CS_PIN
        digitalWrite(cs, LOW);
        #else
        digitalWrite(cs, HIGH);
        #endif
    }
    else
        return false; // CS pin must be set; it is not optional
#endif

    if (_ldac >= 0) {
        ldac = _ldac;
        pinMode(ldac, OUTPUT);
        digitalWrite(ldac, HIGH);
    }

    if (_shdn >= 0) {
        shdn = _shdn;
        pinMode(shdn, OUTPUT);
        digitalWrite(shdn, HIGH);
    }

    if (dac_type == MCP4902) {
        resolution = MCP4902_RESOLURION;
    }
    else if (dac_type == MCP4912) {
        resolution = MCP4912_RESOLURION;
    }
    else if (dac_type == MCP4922) {
        resolution = MCP4922_RESOLURION;
    }
    //else {
    //    return false;  // Must instantiate a DAC type. This may not be necessary as we have a default DAC type in the constructor
    //}

    // Set DAC registers' default values
    dacA.bits.addr = 0;
    dacA.bits.buf = 0;
    dacA.bits.gain = GAIN_1;
    dacA.bits.shdn = 1;
    dacA.bits.data = (2 << resolution) - 1;  // Set output voltage to the highest possible value

    dacB.bits.addr = 1;
    dacB.bits.buf = 0;
    dacB.bits.gain = GAIN_1;
    dacB.bits.shdn = 1;
    dacB.bits.data = (2 << resolution) - 1;  // Set output voltage to the highest possible value

    write(DAC_A);
    write(DAC_B);
    return true;
}

void MCP49X2::vout(dac_channel_t channel, uint16_t mV) {
    if (channel == DAC_A) {
        vouta = mV;
        dacA.bits.data = (mV << resolution) / (vrefa << (dacA.bits.gain == GAIN_1 ? 0 : 1));
        mV = (2 << resolution) - 1;  // Get the maximum voltage in binary code with respect to the given resolution
        dacA.bits.data = (dacA.bits.data <= mV) ? dacA.bits.data : mV;
    }
    else if (channel == DAC_B) {
        voutb = mV;
        dacB.bits.data = (mV << resolution) / (vrefb << (dacB.bits.gain == GAIN_1 ? 0 : 1));
        mV = (2 << resolution) - 1;  // Get the maximum voltage in binary code with respect to the given resolution
        dacB.bits.data = (dacB.bits.data <= mV) ? dacB.bits.data : mV;
    }
    // Write to the appropriate channel's register
    write(channel);
}

void MCP49X2::write(dac_channel_t channel, uint16_t data) {
    spi->beginTransaction(settings);

#ifndef MCP49X2_THREE_WIRE_SPI_INTERFACE
    #ifdef MCP49X2_ACTIVE_HIGH_CS_PIN
    digitalWrite(cs, HIGH);
    #else
    digitalWrite(cs, LOW);
    #endif
#endif

    if (channel == DAC_A) {
        if (dac_type == MCP4902)
            data = MCP4902_DAC_DATA(data);
        else if (dac_type == MCP4912)
            data = MCP4912_DAC_DATA(data);
        spi->transfer(data >> 8);
        spi->transfer(data);
    }
    else if (channel == DAC_B) {
        if (dac_type == MCP4902)
            data = MCP4902_DAC_DATA(data);
        else if (dac_type == MCP4912)
            data = MCP4912_DAC_DATA(data);
        spi->transfer(data >> 8);
        spi->transfer(data);
    }

#ifndef MCP49X2_THREE_WIRE_SPI_INTERFACE
    #ifdef MCP49X2_ACTIVE_HIGH_CS_PIN
    digitalWrite(cs, LOW);
    #else
    digitalWrite(cs, HIGH);
    #endif
#endif

    spi->endTransaction();
}

void MCP49X2::write(dac_channel_t channel) {
    spi->beginTransaction(settings);

#ifndef MCP49X2_THREE_WIRE_SPI_INTERFACE
    #ifdef MCP49X2_ACTIVE_HIGH_CS_PIN
    digitalWrite(cs, HIGH);
    #else
    digitalWrite(cs, LOW);
    #endif
#endif

    if (channel == DAC_A) {
        if (dac_type == MCP4902)
            dacA.reg = MCP4902_DAC_DATA(dacA.reg);
        else if (dac_type == MCP4912)
            dacA.reg = MCP4912_DAC_DATA(dacA.reg);
        spi->transfer(dacA.reg >> 8);
        spi->transfer(dacA.reg);
    }
    else if (channel == DAC_B) {
        if (dac_type == MCP4902)
            dacB.reg = MCP4902_DAC_DATA(dacB.reg);
        else if (dac_type == MCP4912)
            dacB.reg = MCP4912_DAC_DATA(dacB.reg);
        spi->transfer(dacB.reg >> 8);
        spi->transfer(dacB.reg);
    }
    
#ifndef MCP49X2_THREE_WIRE_SPI_INTERFACE
    #ifdef MCP49X2_ACTIVE_HIGH_CS_PIN
    digitalWrite(cs, LOW);
    #else
    digitalWrite(cs, HIGH);
    #endif
#endif

    spi->endTransaction();
}

void MCP49X2::disable(void) {
    disable(DAC_A);
    disable(DAC_B);
    if (shdn >= 0) {
        digitalWrite(shdn, LOW);
    }
}

void MCP49X2::enable(void) {
    if (shdn >= 0) {
        digitalWrite(shdn, HIGH);
    }
    enable(DAC_A);
    enable(DAC_B);
    vout(DAC_A, vouta);
    vout(DAC_B, voutb);
}
