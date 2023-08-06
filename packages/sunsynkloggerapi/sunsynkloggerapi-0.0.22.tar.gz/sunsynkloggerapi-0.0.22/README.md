# SunSynk Logger API
This Python library retrieves data on your Sunsynk Inverter (with SunSynk Logger), photovoltaic panels, and battery if you have one.

See <https://www.sunsynk.org/> for more information on Sunsynk inverters.

This code was developed on a Single SunSynk 5k with Panels and 1x BMS Connected and has not been tested against any other combinations.

This implementation does not interface directly with the SunSynk logger. Instead it connects to the SunSynk API and collects the information from there.

> DISCLAIMER: Use at your own risk!

## SunSynk Python Library

The Python library is available through pip:

```bash
pip install sunsynkloggerapi
```

## Example Usage

```python
import sunsynkloggerapi

sunsynk = sunsynkloggerapi.SunSynkLoggerAPI()
username = ""   # https://www.sunsynk.net Username
password = ""   # https://www.sunsynk.net Pasword

if  not sunsynk._isAuthenticated:
  await sunsynk.Login(username, password)
  await sunsynk.read()
  for i in sunsynk.inverters:
	  print("Inverter : (" + str(i.sn) +") " + i.alias)
```

## Credits

This library has been inspired by the amazing work of the following projects

https://github.com/kellerza/sunsynk