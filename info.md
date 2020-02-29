[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE.md)
[![Discord][discord-shield]][discord]

**ZHA integration: create a map of all ZHA devices.**

This add-on is a pre-requisite https://github.com/dmulcahey/zha-network-visualization-card and requires a working ZHA integration.
Every 3 hours or so, it would scan every Zigbee Router device in your network and retrieve a list of "neigbours" which is used to
create a visualization of your network

{% if not installed %}
## Installation

1. Click install.
1. Add `zha_map:` to your HA configuration.

{% endif %}
## Example configuration.yaml

```yaml
zha_map:
```

***

[discord]: https://https://discord.gg/sCQJcWq
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/custom-components/blueprint.svg?style=for-the-badge
[releases]: https://github.com/zha-ng/zha-map/releases
[license-shield]: https://img.shields.io/github/license/custom-components/blueprint.svg?style=for-the-badge
