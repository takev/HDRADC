# Microphone pre-amplifier

  # |        |         |          |                       |
 --:| ------:| -------:|:-------- |:--------------------- |:----------------------------
  1 | $ 0.18 | $ 0.18  | TPD2E007 | TVS-ESD bidi 15V      | Input connector ESD protection
  2 |        |         |          | Shotky diodes         | Input connector ESD protection
  1 | $      | $       | OPA1622  | Opamp                 | Front end buffer
  1 | $      | $       | OPA1637  | Diff amplifier        | Attenuation / Anti-alias
  1 | $ 9.24 | $ 9.24  | PCM4220  | ADC                   |
  1 | $ 0.90 | $ 0.90  | ISO7730  | Digital isolator      | Level shift
  0 | $ 4.58 | $ 0.00  | SRC4192  | Sample rate converter | Convert to system clock
    |                    TMUX6211 | Audio Switch          | Resistor Ladder for gain.


## Modes of operation

### Gain Structure

 * Headroom is between NL (nominal level) and FS (full scale)
   for 24 bit master recording this is 24 dB.
 * AL (alignment level) is 9 dB below NL. This is at:
   + -24 dbFS : 24 bit master recording
   + -18 dbFS : 16 bit digital recording / broadcasting
 * 11.79 dB increased gain is needed to increase -10 dBV standard
   to +4 dBu.
 * Reuse the 11.79 dB increased gain for dual-HDR microphone input.


  | equipment         | headroom |   0 dBFS | diff Vpp | Amp Gain | Amp Gain |
  | -----------------:| --------:| --------:| --------:| --------:| --------:|
  |  PCM4220          |          |   0 dBFS |    5.6 V |    1     |   0   dB |
  |  Pro +24dBu       |  + 20 dB | + 24 dBu |   34.7 V |    0.161 |  15.9 dB | 
  |  Pro +20dBu       |  + 16 dB | + 20 dBu |   21.9 V |    0.256 |  11.8 dB |
  |  Pro +18dBu       |  + 14 dB | + 18 dBu |   17.4 V |    0.322 |   9.8 dB |
  |  Consumer +12dBV  |  + 16 dB | +  6 dBV |    5.6 V |    1     |   0   dB |
  |  Low gain         |          |          |          |   16     | +24   dB |  4 x  4
  |  mid gain         |          |          |          |   64     | +36   dB |  4 x 16
  |  High gain        |          |          |          |  256     | +48   dB | 16 x 16


Two stage amplifier

#### High level


```
               +---|XXX|--o/ o--+
               |                |
               +---|XXX|--o/ o--+-- 48V
               |
               |   1:1       1:4, 1:16                                        
               |    |-_         |-_                                            
     XLR  -----+----| _---------| _-----+--+
                    |-          |-      |  |                           
                  OPA1622     OPA1637   o  o                                    
 
                                        \  \        .151, 4:1     
                                        o  o    1:1, 1:4, 1:16    +-------+
                                        |  |              |-_     |       |
  L-Jack  -------------------o/ o--+----+--|--------------| _-----|       |
                                   |       |              |-      |       |
                 GND--|XXX|--o/ o--+       |            OPA1637   |       |
                     Zinput                |                      |       |
                                           |                      |       |
                                           |                      |PCM4220|
                                           |                      |       |
                     Zinput                |        .151, 4:1     |       |
                 GND--|XXX|--o/ o--+       |    1:1, 1:4, 1:16    |       |
                                   |       |              |-_     |       |
  R-Jack  -------------------o/ o--+-------+--------------| _-----|       |
                                                          |-      |       |
                                                        OPA1637   +-------+
```

#### Buffer

#### First stage

Input impedance:
 * Pro +4 dBu balanced line input: 100 Ohm
 * Consumer -10 dBV single ended line input: 100 Ohm
 * Condesor Microphone: 100 Ohm
 * Music instruments




```
A = Rf / Rg
0.05% tolerance, E24 series

0b0 -> x4 (0.5%)
0b1 -> x16 (0.1%)

                            |-_
                            |  -_                 
             Rg  8060       |   _------------+-----
 -----+---------|XXX|--+----| _-             |
      |                |    |-               |
      | s0  2    2700  |          Rf 32400   |
      +--o/ o---|XXX|--+-------------|XXX|---+

```

#### Second stage

We can make Rf near the recommended values in the datasheet
since this stage does not have variable imput impedance.

Switches should not be used on Rf since it can cause significant
distortion due to voltage-variable Ron in the switch. This has
less issues when used on Rg.

A 4 channel switch is shared by the differential pair to
share as much path as possible. Use trimmed resistor arrays.

 |                      | s1  | s0  | Rg    | Rf    | gain   |
 |:-------------------- | ---:| ---:| -----:| -----:| ------:|
 | Pro +24dBu           |     |     | 2700  |  407  |  0.161 |
 | Pro +20dBu           |     |     | 1720  |  407  |  0.255 |
 | Consumer +12 dBV     |     |  X  |  430  |  407  |  1.00  |
 | L/M gain (cascade)   |  X  |     |  107  |  407  |  4.00  |
 | High gain (cascase)  |  X  |  X  |   27  |  407  | 16.00  |
   

```
A = Rf / Rg
0.05% tolerance, E24 series

0b0000 -> x.151
0b0001 -> x.255 (exact)
0b0010 -> x1 (1%)
0b0110 -> x4 (2%)
0b1100 -> x16 (1%)

                            |-_
                            |  -_     47          
             Rg  2700       |   _----|XXX|---+-----
 -----+---------|XXX|--+----| _-             |
      |                |    |-               |
      | s0  2    3900  |          Rf  360    |
      +--o/ o---|XXX|--+-------------|XXX|---+
      | s1  2     470  |
      +--o/ o---|XXX|--+
      | s2  2     130  |
      +--o/ o---|XXX|--+
      | s3  2     30   |
      +--o/ o---|XXX|--+

```


### Phantom power
Phantom power can be switched between: off, P12, P24 and P48.
Each requires different resistance connecting to the input:
 - P12 - 680 Ohm
 - P24 - 1.2 kOhm
 - P48 - 6.81 kOhm

Using a solid state relay for this should be viable in reguards to
adde noise or distortion. Switching will be noisy, but should not happen
during operation.

### Input Impedance
The inputs are very high impedance and can be used by instruments.

Resistors can be switched in for specific impedances to change the sound
of instruments and dynamic microphones.

### Stereo operation
There is a switch for line/microphone mode. In line mode two lines
can be connected and the ADC is in stereo mode. Both amplifiers
have the same gain.

The jacks will handle TSR (differential) and TS (single-ended)
line input.

Lines are connected to two Jack input, the switches inside the
two Jacks are used to:
 - Connect system ground to ADC-ground
 - Remove the 20 dB difference in gain between the two channels.
   (Needs two switches)
 - Remove the connection that connects both ADCs together.
   (Needs two switches)

A "pad-switch" of +11.79 dB is added to the gain of the amplifiers when
-10 dBv used.


### Mono HDR mode
The top 20 dB of the ADC (PCM4220) has significantly added noise.
In mono-mode the single XLR input is split to both channels of
the ADC circuit. One of the channels has 0.125 less amplification,
in the digital circuit two channels are mixed/blended to
improve noise, possibly gaining about 2 bits of resolution.



The differential signal are connected with a 1-10 MOhm resistors
from the input of the amplifier to ADC-ground. These resistors
do not need to be removed in Stereo operation. This is used
to float the ground of isolated amplifier to the centre
of the differential input.



### Fixed / Float power
When phantom power is turned on the power supply is floating in
such a way that the common-mode voltage of the ADC is equal to
the long-time average of the common-mode voltage of the
eft/first microphone input.

When phantom power is turned off the power supply is no longer
floating and fixed to in such a way that the common-mode voltage of
the ADC is equal to the system-ground.

## Components

### TDP2E007 2-Channel ESD protection
TPD2E007 is a bidirectional protection with a 15V breakdown voltage.
Specifically designed for audio interface connection, it should be connected
to both the hot and cold wire and floating ground.

### Input opamps
These opamps are configured as voltage followers and work as high impendance
inputs.

The OPA1612 has the best specifications. But the INA1620 has resistors that may be used for
the gain settings, and also includes EMI filtering. The INA1620 also can deliver twice the current
up to 120mA @ 60C. The high current allows for smaller resistors.

Price: $2.42 (x2 -> $4.84)

 * OPA1612 SoundPlus High-Performance, Bipolar-Input Audio Operational Amplifiers
 * INA1620 High-Fidelity Audio Operational Amplifier With Integrated Thin-Film Resistrors and EMI filter

### OPA1632 Fully Differential I/O Audio Amplifier
This amplifier is used for:
 * Attenuating the audio signal to the level of the ADC.
 * Centering the differential signal around the common mode voltage of the ADC
 * Low-pass filter for anti-aliasing.

Price: $1.15 (x2 -> $2.30)

### Audio switches
MAX4602 Low distortion dual supply (no zero crossing)


### PCM4220 123 dB SNR Stereo Audio ADC with PCM output
The best ADC from Texas Instruments.
ADC should run at 192 kHz to reduce latency of sample rate conversion.

Sample rate conversion is required as the ADC needs to run from a very stable
<40ps jitter clock.

The left-right clock can be used to synchronize the power supplies.

All configuration pins will be fixed.

The ADC will run from a floating power supply.

- Price: $9.24
- Analogue power: 65mA @ 4V
- Digital power: 24mA @ 3.3V
- Master clock: 64 * 192kHz = 12.288Mhz, <40ps jitter
- Output clock: 12.288Mhz (master)
- Output data: 12.288Mhz
- Output LRCL: 192kHz (master)

### ISO7730 High-speed, Robust-EMC Reiforced and basic triple-channel digital isolator
The three I2S signals are passed between floating and global power using
this IC which can handle up to 100Mbps.

The isolator will add significant jitter.

- Price: $0.90
- Float power: 25mW, 8mA @ 3.3V
- Global power: 125mW, 38mA @ 3.3V

### SRC4192 144dB High-End Sample Rate Converter
The SRC will synchronize the output form the ADC to a global sample rate.

The SRC is powered from the global 3.3V digital power supply. The outputs
from the ADC need to be level-shifted from the floating 3.3V to the global
3.3V.

Four SRCs can be daisy chained, with up to 8 channels in a single TDM stream.

The master clock could be generated from the PLL of the headphone DAC.

- Price: $4.58
- Digital power: 68mA @ 3.3V
- Reference clock: From global 256 * 192kHz = 49.152MHz



