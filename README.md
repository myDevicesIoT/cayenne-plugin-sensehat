# Cayenne Sense HAT Plugin
A plugin allowing the [Cayenne Pi Agent](https://github.com/myDevicesIoT/Cayenne-Agent) to access Sense HAT data and display it in the [Cayenne Dashboard](https://cayenne.mydevices.com).

## Requirements
### Hardware
* [Rasberry Pi](https://www.raspberrypi.org).
* [Sense HAT](https://www.raspberrypi.org/products/sense-hat/). If you don't have an actual Sense HAT board you can also use the [Sense HAT Emulator](https://sense-emu.readthedocs.io/en/v1.1/).

### Software
* [Cayenne Pi Agent](https://github.com/myDevicesIoT/Cayenne-Agent). This can be installed from the [Cayenne Dashboard](https://cayenne.mydevices.com).
* [Git](https://git-scm.com/).

## Getting Started
### Installation
From the command line run the following commands to install this plugin.
```
cd /etc/myDevices/plugins
sudo git clone https://github.com/myDevicesIoT/cayenne-plugin-sensehat.git
cd cayenne-plugin-sensehat
sudo python3 setup.py install
sudo service myDevices restart
```

### Using the Sense HAT Emulator
If you do not have an actual Sense HAT board and would like to use the Sense HAT Emulator instead you will need to install and run the Emulator.
1. Install the Sense HAT Emulator.
   ```
   sudo apt-get update
   sudo apt-get install python-sense-emu python3-sense-emu sense-emu-tools
   ```
2. Launch the Sense HAT Emulator from the Pi desktop.
3. Add this entry to the `SenseHAT Temperature` section in the `sensehat.plugin` file: `init_args={"use_emulator": true}`.
4. Restart the Cayenne Agent.
   ```
   sudo service myDevices restart
   ```
   Temporary widgets for the plugin should now show up in the [Cayenne Dashboard](https://cayenne.mydevices.com). You can make them permanent by clicking the plus sign.

   NOTE: If the temporary widgets do not show up try refreshing the [Cayenne Dashboard](https://cayenne.mydevices.com) or restarting the agent again using `sudo service myDevices restart`.   