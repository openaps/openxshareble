
# openxshareble

A pure python ble driver for Dexcom G4 + Share suitable for openaps.


## Install

This depends on 
[my patches](https://github.com/adafruit/Adafruit_Python_BluefruitLE/pull/8)
to Adafruit's ble library.

Install dependencies from source:
```bash
git clone -b wip/bewest/custom-gatt-profile https://github.com/bewest/Adafruit_Python_BluefruitLE.git
cd Adafruit_Python_BluefruitLE
sudo python setup.py develop
```

Install `openxshareble`
```bash
git clone https://github.com/bewest/openxshareble.git
cd openxshareble
sudo python setup.py develop
```

Check installation, press `q` to quit.
```bash
pydoc openxshareble
```

## Use

This module is intended to be used by `openaps`.
Install openaps, configure an instance.
```bash
sudo easy_install -ZU openaps
openaps init share-demo
cd share-demo
```

```bash
openaps device show
```
### Vendor
Openaps **vendors** are specific implementations.  openaps can makes it
possible to **use** things that **vendors** provide, using the **device**
configuration.

Devices can only be added to openaps when a suitable vendor provides uses.  In
this case, we want `openxshareble` module to provide uses for the G4+Share
device, so we'll add it as a vendor.
Make available as an openaps vendor.

```bash
openaps vendor add openxshareble
```

### Device
Openaps **device**s the configuration that tells openaps which vendors you are using.
To configure a device, openaps needs to know the vendor providing the uses, and
we also store a friendly name to refer to it later.

Let's create a **device** called `share`, with a configuration so that it uses
the new `openxshareble` **vendor**:
```bash
openaps device add share openxshareble 
openaps use share -h
```

Built in help menu:
```

bewest@bewest-MacBookPro:~/Documents/openaps$ openaps use share  -h
usage: openaps-use share [-h] USAGE ...

optional arguments:
  -h, --help            show this help message and exit

## Device share:
  vendor openxshareble

  openxshareble



  USAGE                 Usage Details
    calibrations        read calibration entry records
    configure           Configure DEXCOMRX serial number.
    glucose             glucose
    iter_calibrations   read last <count> calibration records, default 10, eg:
    iter_calibrations_hours
                        read last <hours> of calibration records, default 1,
                        eg:
    iter_glucose        read last <count> glucose records, default 100, eg:
    iter_glucose_hours  read last <hours> of glucose records, default 1, eg:
    iter_sensor
    iter_sensor_hours
    iter_sensor_insertions
                        read last <count> sensor insertion, removal, and
                        expiration records, default 10, eg:
    iter_sensor_insertions_hours
                        read last <hours> of sensor insertion, removal, and
                        expiration records, default 1, eg:
    list_dexcom         Scan the environment looking for Dexcom devices.
    scan                scan for usb stick
    sensor              Fetch Sensor (raw) records from Dexcom receiver.
    sensor_insertions   read sensor insertion, removal, and expiration records
                        of sensors
bewest@bewest-MacBookPro:~/Documents/openaps$

```

### Use

Now we can **use** the `share` device, the same way as any other device in
`openaps`.  In particular, notice the uses here are the exact same as the uses
available for the classic cabled version of the `dexcom` vendor.  The `uses`
have automatically been converted, the only difference is the wireless ble
function.  Congratulations on cutting the cords!

### Configuring wireless usage
Before we can fetch any data from our receiver, we need to pair to it.  In
particular, this process requires knowledge of the Dexcom serial number.
Replace `SM512345678` with the serial printed on the back of your own Dexcom
G4+Share receiver.

This module only works on Dexcom G4+Share Receivers, and none others.
Examples of viewing available receivers (debug output, mostly), and the
`configure` use:
```bash
openaps use share list_dexcom
openaps use share -h
openaps use share configure -h

```
##### `openaps use share configure`
Here's what the `configure` command looks like:
```bash
bewest@bewest-MacBookPro:~/Documents/openaps$ openaps use share  configure -h
usage: openaps-use share configure [-h] [--serial SERIAL]

  Configure DEXCOMRX serial number.

optional arguments:
  -h, --help       show this help message and exit
  --serial SERIAL  DexcomRX Serial Number

  Update the configuration so that your serial number is used to communicate
  with your Dexcom G4 with Share.
  Default: 

```

Similar to `decocare` and the `medtronic` vendors, this module needs to know
the serial number of the remote device, in order to talk to the correct device.
There are two ways to use this command, the first is to use the environment
variable `DEXCOMRX`, eg, replace `HELLO` with your own `SM12345678` serial
number.

```bash
# prints nothing first time
openaps use share configure

# sets share serial number to HELLO
DEXCOMRX=HELLO openaps use share configure
# watch it say HELLO back ;-)
openaps use share configure
DEXCOMRX=HELLO openaps use share configure
openaps use share configure
```

Example clearing the serial number:
```bash
openaps use share configure --serial ''
# print/test/list the results with no arguments
openaps use share configure
openaps use share configure --serial None
```

Example configuring:
```bash
# replace SM12345678 with your own serial number
openaps use share configure --serial SM512345678
# print/test/list the results with no arguments
openaps use share configure
openaps use share -h
```

### Example reports
Additional commands, these may be helpful in actually using the data in an
openaps loop.
```bash
openaps use share iter_glucose_hours 3
openaps report add monitor/share-glucose.json  JSON  share iter_glucose_hours 3
openaps report  invoke monitor/share-glu
openaps report  invoke monitor/share-glucose.json
openaps use tz -h
openaps use tz glucose monitor/share-glucose.json
openaps use tz  rezone monitor/share-glucose.json
openaps use tz  rezone -h monitor/share-glucose.json
openaps use tz  rezone --date system_time --date display_time  monitor/share-glucose.json
openaps use tz  rezone --date system_time --date display_time  monitor/share-glucose.json  | json -e "this.trend = this.trend_arrow; this.device = 'share'; this.sgv = this.glucose; this.type='sgv'"  
openaps use tz  rezone --date system_time --date display_time  monitor/share-glucose.json  | json -e "this.trend = this.trend_arrow; this.device = 'share'; this.sgv = this.glucose; this.type='sgv'; this.dateString = this.display_time"
openaps use tz  rezone --date system_time --date display_time  monitor/share-glucose.json  | json -e "this.trend = this.trend_arrow; this.device = 'share'; this.sgv = this.glucose; this.type='sgv'; this.dateString = this.display_time" | head
openaps use cgm -h
openaps report add monitor/share-glucose-zoned.json  JSON  tz  rezone --date system_time --date display_time  monitor/share-glucose.json
```

# License

See `LICENSE`
The MIT License (MIT)

Copyright (c) 2015 Ben West

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

