# Sutro

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

This component integrates Home Assistant with Sutro (https://mysutro.com/), a device that enables automated remote monitoring of the temperature as well as the chlorine/bromine, pH, and alkalinity levels.

**This component will set up the following platforms.**

| Platform        | Description                      |
| --------------- | -------------------------------- |
| `sensor`        | Show measurements from Sutro.    |
| `binary_sensor` | Show device state from Sutro.    |
| `todo`          | Show recommendations from Sutro. |

![example][exampleimg]

## Installation
You can install the Sutro integration in one of two ways - using HACS or by manually copying the files into the custom_integrations folder of your Home Assistant. The HACS option is significantly quicker and allows for easy updating in the future.

## Using HACS
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ydogandjiev&repository=hass-sutro&category=integration)
1. Click the link above to open the Sutro integration in HACS or just search for it by name in the HACS UI and click on it
2. Click on the "Download" button
3. Restart Home Assistant
4. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Sutro"

## Manual
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `sutro`.
4. Download _all_ the files from the `custom_components/sutro/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Sutro"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/sutro/translations/en.json
custom_components/sutro/__init__.py
custom_components/sutro/api.py
custom_components/sutro/binary_sensor.py
custom_components/sutro/config_flow.py
custom_components/sutro/const.py
custom_components/sutro/entity.py
custom_components/sutro/manifest.json
custom_components/sutro/sensor.py
custom_components/sutro/todo.py
```

## Configuration is done in the UI

To configure the integration, you need to provide the e-mail and password for your Sutro account:
![login][loginimg]

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/ydogandjiev
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/ydogandjiev/hass-sutro.svg?style=for-the-badge
[commits]: https://github.com/ydogandjiev/hass-sutro/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[loginimg]: login.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/ydogandjiev/hass-sutro.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40ydogandjiev-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ydogandjiev/hass-sutro.svg?style=for-the-badge
[releases]: https://github.com/ydogandjiev/hass-sutro/releases
[user_profile]: https://github.com/ydogandjiev
