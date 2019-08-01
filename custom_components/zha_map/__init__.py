import asyncio
import logging
import os
from datetime import timedelta

from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util.json import save_json
import zigpy.exceptions as zigpy_exc

from .helpers import LogMixin
from .neighbour import Neighbour, NeighbourType


ATTR_TOPO = 'topology'
ATTR_OUTPUT_DIR = 'output_dir'
AWAKE_INTERVAL = timedelta(seconds=60)
DOMAIN = 'zha_map'
CONFIG_OUTPUT_DIR_NAME = 'neighbours'

LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up ZHA from config."""

    if DOMAIN not in config:
        return True

    try:
        zha_gw = hass.data['zha']['zha_gateway']
    except KeyError:
        return False

    builder = TopologyBuilder(hass, zha_gw)
    hass.data[DOMAIN] = {
        ATTR_TOPO: builder,
    }
    output_dir = os.path.join(hass.config.config_dir, CONFIG_OUTPUT_DIR_NAME)
    hass.data[DOMAIN][ATTR_OUTPUT_DIR] = output_dir

    def mkdir(dir):
        try:
            os.mkdir(dir)
            return True
        except OSError as exc:
            LOGGER.error("Couldn't create '%s' dir: %s", dir, exc)
            return False

    if not os.path.isdir(output_dir):
        if not await hass.async_add_executor_job(mkdir, output_dir):
            return False

    async_track_time_interval(hass, builder.time_tracker, AWAKE_INTERVAL)
    return True


class TopologyBuilder(LogMixin):
    """Keeps track of topology."""

    log = LOGGER.log

    def __init__(self, hass, zha_gw):
        """Init instance."""
        self._hass = hass
        self._app = zha_gw
        self._in_process = None
        self._seen = {}
        self._failed = {}

    async def time_tracker(self, time=None):
        """Awake periodically."""
        if self._in_process and not self._in_process.done():
            return
        self._in_process = self._hass.async_create_task(self.build())

    async def build(self):
        self._seen.clear()
        self._failed.clear()

        seed = self._app.application_controller.get_device(nwk=0x0000)
        self.debug("Building topology starting from coordinator")
        try:
            await self.scan_device(seed)
        except zigpy_exc.ZigbeeException as exc:
            self.error("failed to scan %s device: %s", seed.ieee, exc)
            return

        # scan all seen if their neighbour table is empty
        pending = [n for n in self._seen.values() if not n.neighbours and
                   n.device_type in (NeighbourType.Coordinator.name,
                                     NeighbourType.Router.name)]
        while pending:
            for nei in pending:
                try:
                    await nei.scan()
                except (zigpy_exc.ZigbeeException, asyncio.TimeoutError):
                    self.warning("Couldn't scan %s neighbours", nei.ieee)
                    self._failed[nei.ieee] = nei
                    continue
                await self.process_neighbour_table(nei)
            pending = [n for n in self._seen.values() if not n.neighbours and
                       n.device_type in (NeighbourType.Coordinator.name,
                                         NeighbourType.Router.name)]
            if pending:
                self.debug(("Finished neighbour scan pass. New neighbours were"
                            " discovered: %s"), [n.ieee for n in pending])
            else:
                self.debug("Finished neighbour scan pass. Failed: %s",
                           self._failed.keys())
        await self.sanity_check()

    async def sanity_check(self):
        """Check discovered neighbours vs Zigpy database."""
        # do we have extra neighbours
        for nei in self._seen:
            if nei not in self._app.application_controller.devices:
                self.debug("Neighbour not in 'zigbee.db': " "%s: %s: %s",
                           nei.device.ieee, nei.manufacturer, nei.model)

        # are we missing neighbours
        for dev in self._app.application_controller.devices.values():
            if dev.node_desc.is_end_device or dev.ieee in self._seen:
                continue

            if dev.ieee in self._failed:
                self.debug(("%s (%s %s) was discovered in the neighbours "
                            "tables, but did not respond"),
                           dev.ieee, dev.manufacturer, dev.model)
            else:
                self.debug(("%s (%s %s) was not found in the neighbours "
                            "tables"), dev.ieee, dev.manufacturer, dev.model)

    async def scan_device(self, device):
        """Scan device neigbours."""
        nei = await Neighbour.scan_device(device)
        await self.process_neighbour_table(nei)

    async def process_neighbour_table(self, nei):
        for entry in nei.neighbours:
            if entry.ieee in self._seen:
                continue
            self.debug("Adding %s to all neighbours", entry.ieee)
            self._seen[entry.ieee] = entry
        await self.save_neighbours(nei)

    async def save_neighbours(self, nei):
        suffix = ''.join(['%02x' % (o,) for o in nei.ieee])
        suffix = f'_{suffix}.txt'

        file_name = os.path.join(
            self._hass.data[DOMAIN][ATTR_OUTPUT_DIR], 'neighbours' + suffix)
        self.debug("Saving %s", file_name)
        await self._hass.async_add_executor_job(save_json,
                                                file_name, nei.json())

