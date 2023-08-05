# ha-mqtt-discoverable

[![License](https://img.shields.io/github/license/unixorn/ha-mqtt-discoverable.svg)](https://opensource.org/license/apache-2-0/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/unixorn/ha-mqtt-discoverable/main.svg)](https://github.com/unixorn/ha-mqtt-discoverable)
[![Downloads](https://static.pepy.tech/badge/ha-mqtt-discoverable)](https://pepy.tech/project/ha-mqtt-discoverable)

A python 3 module that takes advantage of Home Assistant's MQTT discovery protocol to create sensors without having to define anything on the HA side.

Using MQTT discoverable devices lets us add new sensors and devices to HA without having to restart HA. This module includes scripts to make it easy to create discoverable devices from the command line if you don't want to bother writing python.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Installing](#installing)
  - [Python](#python)
  - [Docker](#docker)
- [Supported entities](#supported-entities)
  - [Binary sensor](#binary-sensor)
    - [Usage](#usage)
  - [Switch](#switch)
    - [Usage](#usage-1)
- [Device](#device)
    - [Usage](#usage-2)
- [Contributing](#contributing)
- [Scripts Provided](#scripts-provided)
  - [`hmd`](#hmd)
  - [`hmd create binary sensor`](#hmd-create-binary-sensor)
  - [`hmd create device`](#hmd-create-device)
- [Contributors](#contributors)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installing

### Python

ha-mqtt-discoverable runs on Python 3.10 or later.

`pip install ha-mqtt-discoverable` if you want to use it in your own python scripts. This will also install the `hmd` utility scripts.

### Docker

If you only need to use the command line tools, the simplest way is to use them with `docker` or `nerdctl`. It won't interfere with your system python and potentially cause you issues there.

You can use the [unixorn/ha-mqtt-discoverable](https://hub.docker.com/repository/docker/unixorn/ha-mqtt-discoverable) image on dockerhub directly, but if you add `$reporoot/bin` to your `$PATH`, the `hmd` script there will automatically run the command line tools inside a docker container with `docker` or `nerdctl`, depending on what it finds in your `$PATH`.

## Supported entities

The following Home Assistant entities are currently implemented:

- Sensor
- Binary sensor
- Switch
- Button
- Device trigger

### Binary sensor

#### Usage

The following example creates a binary sensor and sets its state:

```py
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo


# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Information about the sensor
sensor_info = BinarySensorInfo(name="MySensor", device_class="motion")

settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

# Instantiate the sensor
mysensor = BinarySensor(settings)

# Change the state of the sensor, publishing an MQTT message that gets picked up by HA
mysensor.on()
mysensor.off()

# You can also set custom attributes on the sensor via a Python dict
mysensor.set_attributes({"my attribute": "awesome"})

```

### Switch

The switch is similar to a _binary sensor_, but in addition to publishing state changes toward HA it can also receive 'commands' from HA that request a state change.
It is possible to act upon reception of this 'command', by defining a `callback` function, as the following example shows:

#### Usage

```py
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Switch, SwitchInfo
from paho.mqtt.client import Client, MQTTMessage

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Information about the switch
# If `command_topic` is defined, it will receive state updates from HA
switch_info = SwitchInfo(name="test", command_topic="command")

settings = Settings(mqtt=mqtt_settings, entity=switch_info)

# To receive state commands from HA, define a callback function:
def my_callback(client: Client, user_data, message: MQTTMessage):
    payload = message.payload.decode()
    logging.info(f"Received {payload} from HA")
    # Your custom code...

# Define an optional object to be passed back to the callback
user_data = "Some custom data"

# Instantiate the switch
my_switch = Switch(settings, my_callback, user_data)

# Change the state of the sensor, publishing an MQTT message that gets picked up by HA
my_switch.on()
my_switch.off()

```

## Device
From the [Home Assistant documentation](https://developers.home-assistant.io/docs/device_registry_index):
> A device is a special entity in Home Assistant that is represented by one or more entities.
A device is automatically created when an entity defines its `device` property.
A device will be matched up with an existing device via supplied identifiers or connections, like serial numbers or MAC addresses.

### Usage

The following example create a device, by associating multiple sensors to the same `DeviceInfo` instance.

```py
from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Define the device. At least one of `identifiers` or `connections` must be supplied
device_info = DeviceInfo(name="My device", identifiers="device_id")

# Associate the sensor with the device via the `device` parameter
# `unique_id` must also be set, otherwise Home Assistant will not display the device in the UI
motion_sensor_info = BinarySensorInfo(name="My motion sensor", device_class="motion", unique_id="my_motion_sensor", device=device_info)

motion_settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

# Instantiate the sensor
motion_sensor = BinarySensor(motion_settings)

# Change the state of the sensor, publishing an MQTT message that gets picked up by HA
motion_sensor.on()

# An additional sensor can be added to the same device, by re-using the DeviceInfo instance previously defined
door_sensor_info = BinarySensorInfo(name="My door sensor", device_class="door", unique_id="my_door_sensor", device=device_info)
door_settings = Settings(mqtt=mqtt_settings, entity=door_sensor_info)

# Instantiate the sensor
door_sensor = BinarySensor(settings)

# Change the state of the sensor, publishing an MQTT message that gets picked up by HA
door_sensor.on()

# The two sensors should be visible inside Home Assistant under the device `My device`
```

### Device trigger

The following example creates a device trigger and generates a trigger event:

#### Usage
```py
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import DeviceInfo, DeviceTriggerInfo, DeviceTrigger

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(host="localhost")

# Define the device. At least one of `identifiers` or `connections` must be supplied
device_info = DeviceInfo(name="My device", identifiers="device_id")

# Associate the sensor with the device via the `device` parameter
trigger_into = DeviceTriggerInfo(name="MyTrigger", type="button_press", subtype="button_1", unique_id="my_device_trigger", device=device_info)

settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

# Instantiate the device trigger
mytrigger = DeviceTrigger(settings)

# Generate a device trigger event, publishing an MQTT message that gets picked up by HA
# Optionally include a payload as part of the event
mytrigger.trigger("My custom payload")
```

## Contributing

Please run `black` on your code before submitting. There are `git` hooks already configured to run `black` and other checks before every commit, please run `pre-commit install` to enable them.

## Scripts Provided

The `ha_mqtt_discoverable` module also installs the following helper scripts you can use in your own shell scripts.

### `hmd`

Uses the [gitlike-commands](https://github.com/unixorn/gitlike-commands/) module to find and execute `hmd` subcommands. Allows you to run `hmd create binary sensor` and `hmd` will find and run `hmd-create-binary-sensor` and pass it all the command line options.

### `hmd create binary sensor`

Create/Update a binary sensor and set its state.

Usage: `hmd create binary sensor --device-name mfsmaster --device-id 8675309 --mqtt-user HASS_MQTT_USER --mqtt-password HASS_MQTT_PASSWORD --client-name inquisition --mqtt-server mqtt.unixorn.net --metric-name tamper --device-class motion --state off`

### `hmd create device`

Create/Update a device and set the state of multiple metrics on it.

Usage: `hmd create device --device-name coyote --device-id 8675309 --mqtt-user HASS_MQTT_USER --mqtt-password HASS_MQTT_PASSWORD --mqtt-server mqtt.example.com --model 'Rocket Skates' --manufacturer 'Acme Products' --metric-data '{"name":"Left Rocket Skate","value":93}' --metric-data '{"name":"Right Rocket Skate","value":155}' --unique-id 'hmd-26536'`

## Contributors

<a href="https://github.com/unixorn/ha-mqtt-discoverable/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=unixorn/ha-mqtt-discoverable" />
</a>

Made with [contributors-img](https://contributors-img.web.app).
