# temperatureMonitor

Simple Python script to monitor the temperature using Adafruit's MCP9808 I2C sensor and associated Python library.

Assumes that a Raspberry Pi is connected via I2C to the MCP9808 with I2C address 0x18 (see below for I2C detect output).

## Setup

Follow instructions [here](https://github.com/adafruit/Adafruit_Python_MCP9808) to install required Python library for the sensor itself.

Set up a Gmail account from which the data will be sent.  This doesn't need to be the account that you receive data from.  Put the account
username and password into sample_email_config.json (or another json file, you can pass it as a command line argument).

Make sure you've run:

    sudo pip install pytz

To install the timezone libraries.  You can alter the timezone in the source code to fit your needs.

### I2C setup

This is the result from `sudo i2cdetect -y 1` on the Raspberry Pi connected to the MCP9808:

         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- 18 -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    70: -- -- -- -- -- -- -- --

##  Usage
### Options Explanation
`-v`                    : use verbose mode, printing every reading to the screen

`-l`                    : prints data to the CSV file with default log file name "/home/pi/temperature_data.csv

`--log`                 : prints data to the CSV file with the provided file name

`--config`              : file path to the config file not currently used

`--iterations`          : the number of temperature readings to take and then average. Default is 1

## Example

Running:

    python tempMonitor.py

Will take one temperature reading and print it to the screen

Running:

    python tempMonitor.py --log ./results.csv --iterations 360

Will take 360 measurements and log the average to results.csv. This project is essentially a fork of [this repository](https://github.com/ms5991/temperatureMonitor), but this one is better for actual applications, the other one isn't very user friendly.
