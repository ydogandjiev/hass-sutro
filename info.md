[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

This component integrates Home Assistant with Sutro (https://mysutro.com/), a device that enables automated remote monitoring of the temperature as well as the chlorine/bromine, pH, and alkalinity levels.

**This component will set up the following platforms.**

| Platform        | Description                                          |
| --------------- | ---------------------------------------------------- |
| `sensor`        | Show info from Sutro Smart Pool Monitor Support API. |

![example][exampleimg]

{% if not installed %}

## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Sutro Smart Pool Monitor Support".

{% endif %}

## Configuration is done in the UI

<!---->

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[commits-shield]: https://img.shields.io/github/commit-activity/y/ydogandjiev/hass-sutro.svg?style=for-the-badge
[commits]: https://github.com/ydogandjiev/hass-sutro/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license]: https://github.com/ydogandjiev/hass-sutro/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/ydogandjiev/hass-sutro.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40ydogandjiev-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ydogandjiev/hass-sutro.svg?style=for-the-badge
[releases]: https://github.com/ydogandjiev/hass-sutro/releases
[user_profile]: https://github.com/ydogandjiev
