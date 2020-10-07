# zha-map
Build ZHA network topology map.

[zha-map](https://github.com/zha-ng/zha-map) integration commponent for [Home Assistant](https://www.home-assistant.io) allow you to make a ZHA (Zigbee Home Automation) network topology map.

Requires that you are already using the [ZHA](https://www.home-assistant.io/integrations/zha/) integration commponent in Home Assistant.

Zigbee network mapping with zha-map can help you identify weak points like bad links between your devices.

# Installation Instructions

1. Install the zha_map custom component
- https://github.com/zha-ng/zha-map
2. Add zha_map: to your configuration.yaml and restart Home Assistant
3. Wait for a scan to complete (logs to DEBUG, or use the new zha_map service to scan on demand)
4. Install one of the visualization cards:
- https://github.com/dmulcahey/zha-network-visualization-card
- https://github.com/Samantha-uk/zigzag
5. Add to your lovelace global config as type: module
6. Add custom card (works best in panel mode): - type: 'custom:zha-network-visualization-card'

# Usage
The Zigbee coordinator will be represented by a rectangle at the top. Any device that serves as Zigbee router (usually all devices running on Mains electricity / grid power) will represented as ovals, and Zigbee end-device (usually battery powered sensors) will be represented by as circles.

The lines between those representions show all the possible paths through Zigbee mesh. Any path with a LQI over 192 is shown as green, LQI 129-192 is shown as yellow, and anything 128 and lower is shown as red.

# Related projects

### zha-network-visualization-card
**[zha-network-visualization-card](https://github.com/dmulcahey/zha-network-visualization-card)** is a custom lovelace element for [Home Assistant](https://www.home-assistant.io/) that visualizing your ZHA Zigbee network. Zigbee network mapping with zha-map can help you identify weak points like bad links between your devices. It relies on the data provided by the [zha-map](https://github.com/zha-ng/zha-map) integration commponent.

### Zigzag
**[Zigzag](https://github.com/Samantha-uk/zigzag)** is an custom card/panel for [Home Assistant](https://www.home-assistant.io/) that displays a graphical layout of Zigbee devices and the connections between them. Zigzag can be installed as a panel or a custom card and relies on the data provided by the [zha-map](https://github.com/zha-ng/zha-map) integration commponent.

### Zigpy
**[zigpy](https://github.com/zigpy/zigpy)** is [Zigbee protocol stack](https://en.wikipedia.org/wiki/Zigbee) integration project to implement the **[Zigbee Home Automation](https://www.zigbee.org/)** standard as a Python library. Zigbee Home Automation integration with zigpy allows you to connect one of many off-the-shelf Zigbee adapters using one of the available Zigbee radio library modules compatible with zigpy to control Zigbee devices. There is currently support for controlling Zigbee device types such as binary sensors (e.g. motion and door sensors), analog sensors (e.g. temperature sensors), lightbulbs, switches, and fans. Zigpy is tightly integrated with [Home Assistant](https://www.home-assistant.io)'s [ZHA component](https://www.home-assistant.io/components/zha/) and provides a user-friendly interface for working with a Zigbee network.
