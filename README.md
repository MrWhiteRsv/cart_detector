# cart_detector

sudo nano /boot/config.txt

add the following at the bottom:
"dtparam=i2c_arm=on"

Then save.

Then run
sudo raspi-config

And select "Advanced Options", then option 7 I2c, and select "yes" to enable I2C.

# enable GPSD on USB0

```
root@raspberrypi:/etc/default# cat gpsd 
# Default settings for the gpsd init script and the hotplug wrapper.

# Start the gpsd daemon automatically at boot time
START_DAEMON="true"

# Use USB hotplugging to add new USB devices automatically to the daemon
USBAUTO="true"

# Devices gpsd should collect to at boot time.
# They need to be read/writeable, either by user gpsd or the group dialout.
DEVICES="/dev/ttyUSB0"

# Other options you want to pass to gpsd
GPSD_OPTIONS=""
root@raspberrypi:/etc/default# 

```
