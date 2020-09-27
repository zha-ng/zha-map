# zha-map
Build ZHA network topology map.

[zha-map](https://github.com/zha-ng/zha-map) integration commponent for [Home Assistant](https://www.home-assistant.io) allow you to make a ZHA (Zigbee Home Automation) network topology map.

Requires that you are already using the [ZHA](https://www.home-assistant.io/integrations/zha/) integration commponent in Home Assistant.

Zigbee network mapping with zha-map can help you identify weak points like bad links between your devices.

# Installation Instructions

1. Install the zha_map custom component
   - https://github.com/zha-ng/zha-map
1. Add zha_map: to your configuration.yaml and restart Home Assistant
1. Wait for a scan to complete (logs to DEBUG, or use the new zha_map service to scan on demand)
1. Install one of the visualization cards:
   - https://github.com/dmulcahey/zha-network-visualization-card
   - https://github.com/Samantha-uk/zigzag
1. Add to your lovelace global config as type: module
1. Add custom card (works best in panel mode): - type: 'custom:zha-network-visualization-card'

# Usage

The Zigbee coordinator will be represented by a rectangle at the top. Any device that serves as Zigbee router (usually all devices running on Mains electricity / grid power) will represented as ovals, and Zigbee end-device (usually battery powered sensors) will be represented by as circles.

The lines between those representions show all the possible paths through Zigbee mesh. The numbers on the lines represent the ??LQI?? for the path. Sometimes lines may show two numbers seperated by a forward slash. The first number is ??????? and the second number is ???

|LQI [(about)](https://www.silabs.com/community/wireless/zigbee-and-thread/knowledge-base.entry.html/2012/06/28/how_do_i_obtain_lqi-pS4D)|Color|
|--|--|
| > 192 | Green |
| 129 - 192 | Yellow |
|  < 129 | Red |
| ?not determined yet? | Grey |
