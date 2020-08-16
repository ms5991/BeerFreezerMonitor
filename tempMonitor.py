#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
import Adafruit_MCP9808.MCP9808 as MCP9808
import getopt, smtplib, json, random, sys, os, datetime
from pytz import timezone

def write_log(timestamp, temp_f, temp_c, logFile):
    toLog = '{0},{1:0.1F},{2:0.1F}\n'.format(timestamp, temp_f, temp_c)

    if os.path.isfile(logFile):
        with open(logFile, "a") as csvFile:
            csvFile.write(toLog)
    else:
        with open(logFile,"w+") as csvFile:
            csvFile.write('Timestamp,Temp_F,Temp_C\n')
            csvFile.write(toLog)

# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0

def main(argv):
    # OPTIONS EXPLAINATION
    # -l			: prints data to the CSV file with default log file name "/home/pi/temperature_data.csv
    # --log			: prints data to the CSV file with the provided file name
    # --config	: file path to the config file for DB connection. Default is ./config.json
    # --iterations	: the number of temperature readings to take. Default is 1
    try:
        opts, args = getopt.getopt(sys.argv[1:], "lfv", ["log=","iterations=","seconds=","config="])
    except getopt.GetoptError, e:
        print 'tempMonitor.py: {0}'.format(str(e))
        sys.exit(2)

    log = False
    logFile = '/home/pi/temperature_data.csv'
    configFile = 'config.json'
    iterations = 1
    verbose = False

    for opt, arg in opts:
        if opt == '-v':
            verbose = True
        elif opt == '-l':
            log = True
        elif opt == '--log':
            log = True
            logFile = arg
        elif opt == '--iterations':
            iterations = int(arg)
        elif opt == '--config':
            configFile = arg
        elif opt in ["-f","--finalOnly"]:
            finalOnly = True

    # get the sensor object
    sensor = MCP9808.MCP9808()

    maxF = -1000
    minF = 1000
    runningSumF = 0
    runningSumC = 0

    # load config data	
    with open(configFile) as conf:
        if verbose: print 'Loading json data...'
        configData = json.load(conf)

    # Initialize communication with the sensor.
    sensor.begin()

    startTime = datetime.datetime.now(timezone('US/Pacific')).strftime("%c")

    for i in range(iterations):

        # get temp from sensor
        temp_c = sensor.readTempC()

        # convert to F
        temp_f = c_to_f(temp_c)

        # check if this is max temp
        if temp_f > maxF:
            maxF = temp_f

        # check if this is min temp
        if temp_f < minF:
            minF = temp_f

        # add to running sum for average calc
        runningSumF = runningSumF + temp_f

	runningSumC = runningSumC + temp_c

        result = 'Temperature: {0:0.1F}*C / {1:0.1F}*F'.format(temp_c, temp_f)

        # print result to screen
        if verbose: print result

        # time stamp of temp reading
        timestamp = datetime.datetime.now(timezone('US/Pacific')).strftime("%c")


    # timestamp at end of average period
    endTime = datetime.datetime.now(timezone('US/Pacific')).strftime("%c")

    # calculate average
    averageF = runningSumF / iterations

    averageC = runningSumC / iterations

    # write to log file if necessary
    if log: 
        write_log(startTime, averageF, averageC, logFile)

    # message containing aggregated data
    finalMessage = "Max temp: {0:0.1F}*F\nMin temp: {1:0.1F}*F\nAverage between '{2}' and '{3}': {4:0.1F}*F".format(maxF, minF, startTime, endTime, averageF)

    # print to screen
    if verbose: print finalMessage

# call main
if __name__ == "__main__":
    main(sys.argv[1:])
