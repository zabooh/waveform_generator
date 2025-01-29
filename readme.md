---
parent: Harmony 3 peripheral library application examples for SAM C20/C21 family
title: DAC waveform generation with DMA 
has_children: false
has_toc: false
---

[![MCHP](https://www.microchip.com/ResourcePackages/Microchip/assets/dist/images/logo.png)](https://www.microchip.com)

# DAC waveform generation with DMA

This example application shows how to use the DAC with the DMA to generate a X KHz sinusoidal waveform with overtones without CPU intervention.

Added is a Python Programm that allows to create interactively the wavetable.

![Alt-Text](WaveformGenerator.png)

The Sampliung Rate is configured within the function TC0_TimerInitialize(). Currently it is set to 500kHz.

Here are more examples: 

    /* Configure timer period 
     *   Clock              = 48MHz
     *   TC0 Overflow       = 500kHz
     *   Timer Period Value = (48M / 500kHz) - 1 = 95
     *   Timer Period Value = (48M / 100kHz) - 1 = 479
     *   Timer Period Value = (48M /  50kHz) - 1 = 959
     *   Timer Period Value = (48M /  10kHz) - 1 = 4799
     */
    TC0_REGS->COUNT32.TC_CC[0U] = 95U;   // 500kHz
    //TC0_REGS->COUNT32.TC_CC[0U] = 479U;  // 100kHz
    //TC0_REGS->COUNT32.TC_CC[0U] = 959U;  //  50kHz
    //TC0_REGS->COUNT32.TC_CC[0U] = 4799U; //  10kHz

    

## Description

The DAC Peripheral library is used in hardware trigger mode to generate a Sine wave. The TC peripheral is configured to generate a trigger every two microseconds. Trigger is connected to the DAC using the EVSYS peripheral. DMA is used to setup a linked list to transfer sine wave samples from lookup table to the DAC "DATABUF" register. In this application, the number of DAC samples per cycle(0 to 360 degrees sine wave) is 100.

## Downloading and building the application

To clone or download this application from Github, go to the [main page of this repository](https://github.com/Microchip-MPLAB-Harmony/csp_apps_sam_c20_c21) and then click **Clone** button to clone this repository or download as zip file.
This content can also be downloaded using content manager by following these [instructions](https://github.com/Microchip-MPLAB-Harmony/contentmanager/wiki).

Path of the application within the repository is **apps/dac/dac_wav_gen_dma/firmware** .

To build the application, refer to the following table and open the project using its IDE.

| Project Name      | Description                                    |
| ----------------- | ---------------------------------------------- |
| sam_c21n_xpro.X | MPLABX project for [SAMC21N Xplained Pro Evaluation Kit](https://www.microchip.com/developmenttools/ProductDetails/atsamc21n-xpro) |
|||

## Setting up the hardware

The following table shows the target hardware for the application projects.

| Project Name| Board|
|:---------|:---------:|
| sam_c21n_xpro.X | [SAMC21N Xplained Pro Evaluation Kit](https://www.microchip.com/developmenttools/ProductDetails/atsamc21n-xpro)
|||

### Setting up [SAMC21N Xplained Pro Evaluation Kit](https://www.microchip.com/developmenttools/ProductDetails/atsamc21n-xpro)

- Connect an oscilloscope to monitor pin 1 (DAC) of 2-pin header labeled DAC-OUT
- Connect the Debug USB port on the board to the computer using a micro USB cable

## Running the Application

1. Build and Program the application using its IDE
2. Observe a sine wave of 5 KHz frequency on DAC output pin
3. Refer to the below table for dac output pin details:

| Board      | DACC output pins |
| ----------------- |-----------|
| [SAMC21N Xplained Pro Evaluation Kit](https://www.microchip.com/developmenttools/ProductDetails/atsamc21n-xpro) | pin 1 (DAC) of 2-pin header labeled DAC-OUT) |
|||
