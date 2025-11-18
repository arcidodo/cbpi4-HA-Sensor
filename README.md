# Pre-release - please use with caution

# CraftBeerPI4 Sensor Plugin that reads sensors via Home Assistant
![GitHub issues](https://img.shields.io/github/issues-raw/arcidodo/cbpi4-HA-Sensor)
[![GitHub license](https://img.shields.io/github/license/craftbeerpi/craftbeerpi4)](https://github.com/craftbeerpi/craftbeerpi4/blob/master/LICENSE)
![PyPI](https://img.shields.io/pypi/v/cbpi4-HA-Sensor)




# Features
* Read sensor information from home assistant into CBPI4

# Installation
## Activate REST-API in HA
You need to activate the REST-API in your Home Assitant installation.
Normally, this is archieved by adding `"api:"` to your configuration yaml.

See more info here: https://www.home-assistant.io/integrations/api/

## Get authentication token
To authenticate this plugin against HA you need to generate a "Long-lived Access Token". 
You can generate those in your HA users profile.

A tutorial can be found here: https://www.atomicha.com/home-assistant-how-to-generate-long-lived-access-token-part-1/

*Be aware you only see this once in HA and it's quite long (180 Chars), please save it securily.*

## Install plugin
Currently we only support installation directly from the git repository:
```bash
sudo pip3 install https://github.com/arcidodo/cbpi4-HA-Sensor/archive/refs/heads/main.zip
```
Direct pip installation via repositories will come in the near future.

## Configuration
Enter the appropiate configuration:
<img width="1185" height="377" alt="Scherm­afbeelding 2025-11-18 om 23 33 12" src="https://github.com/user-attachments/assets/9271e7a7-0d2d-4f20-8aef-79444ee63259" />


# Known problems
None, *yet*. Please report via "issues"!




