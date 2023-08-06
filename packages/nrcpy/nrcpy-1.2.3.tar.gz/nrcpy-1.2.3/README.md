# Nrcpy

Nrcpy is a Python package for working with NRC devices. It provides a convenient interface to connect to an NRC device, send commands, and retrieve information from the device.

## 🔥 Installation

You can install `nrcpy` using pip:

```shell
pip install nrcpy
```
## 🪧 Usage
Here is an example of how to use nrcpy to connect to an NRC device and control the relays:
```python
from nrcpy import NrcDevice

# Configure the device
ip = '192.168.1.200'
port = 23
username = 'admin'
password = 'admin'

# Create an instance of NrcDevice
nrc = NrcDevice((ip, port, username, password))

# Open connection
nrc.connect()

# Login
if nrc.login():
    # Control the relays
    nrc.relayContact(1, 500)
    nrc.relayContact(2, 1000)
    nrc.relayOff(1)
    nrc.relayOn(2)

    # Get relays status
    relays_status = nrc.getRelaysValues()
    relay_1_status = nrc.getRelayValue(1)
    relay_2_status = nrc.getRelayValue(2)

    print(f'Relays Status (hex): {relays_status}')
    print(f'Relay 1 Status: {relay_1_status}')
    print(f'Relay 2 Status: {relay_2_status}')
else:
    print('Error in login')

# Close connection
nrc.disconnect()

```
