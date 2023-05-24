# BleepVna
### A High-Resolution, Full-Band Antenna Analyzer for deepVNA

The idea for this software came when I wanted to characterise the few dozens antennas in my collection. I wanted to be able to do multiple high resolution scans, average them together and then output a plot file, where all the resonances of the scanned antenna are highlighted.
I found currently available software lacking this functionality. There is software who can do quite detailed scans. Which I used at first. But then I had to convert the touchstone files to csv, do the calculations in excel and generate the plots myself. Which is quite a bit of work. BleepVNA does all that with a single command.

![Example of a plot done with BleepVNA](/img/samplePlot.png)
Example of a plot done with BleepVNA

## A word of caution
I am a coder by trait. But I'm in no way an expert in RF Networks. Nor am I particularly versed in Python. In fact this is one of my fits larger Python projects. I'm sure I did a lot wrong here. So this software should be considered at most an beta version. If you find something wrong, missing or otherwise sketchy, please do let me know by opening an issue right here in this repo.

## Aknowledgements
This software is loosely based on [https://github.com/ttrftech/NanoVNA/tree/master/python](url) by ttrftech [https://github.com/ttrftech](url)

## Compatibility
I wrote this software with a deepVNA 101. So this is the only device currently testet. Although this software should also work with nanoVNA. Also, my deepVNA seems to produce some sketchy outputs from time to time. That's why this software has some error correcting mechanisms.

## License & Waranty
BleepVNA is free software and comes with ABSOLUTELY NO WARRANTY.

BleepVNA is licensed under the GNU General Public License v3.0. See LICENSE (in project root) for more information.

## Installation
You need to have python3 and pip3 installed for this software to work.

Run:

`pip3 install -r requirements.txt`

from the root of this software to install all the needed python3 libraries.

After that you have to configure your VNA settings in settings.ini (in project root)

```
[vna]
# The VID of your VNA
VID = 0x0483

# The PID of your VNA
PID = 0x5740

# Minimum Frequency in Herz
minFreq = 10000

# Maximum Frequency in Herz
maxFreq = 1500000000


[scanning]
# Delay between sending the scan command to the VNA and reading the results
readDelay = .2

# Max errors before BleepVNA gives up and quits
maxConsecutiveErrors = 5


[logging]
# Leave this section as is. Only modify if you know exactly what you are doing
```

## Usage

## Examples
- Show all possible configuration options:

`python3 BeepVna.py --help`

- Run a scan from min to max frequency (set in settings.ini) named 'testing' with all settings on default:

`python3 BeepVna.py -n testing`

- Run a scan from min to max frequency (set in settings.ini) named 'testing' with 300 scan points

`python3 BeepVna.py -n testing -p 300`

- Run a scan from min to max frequency (set in settings.ini) named 'testing' with a scan stepping of 1MHz

`python3 BeepVna.py -n testing -t 1m`

- Same as above but with 5 consecutive runs

`python3 BeepVna.py -n testing -t 1m -r 5`

- Same as above but also calculate the average of the runs

`python3 BeepVna.py -n testing -t 1m -r 5 -a`

- Same as above but also generate csvs and plots

`python3 BeepVna.py -n testing -t 1m -r 5 -a -c -l`

or

`python3 BeepVna.py -n testing -t 1m -r 5 -acl`



# ToDo
- Timer error if quit after x consecutive errors
- implement --overwrite function
