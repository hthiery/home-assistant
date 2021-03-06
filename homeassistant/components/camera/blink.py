"""
Support for Blink system camera.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/camera.blink/
"""
import logging

from homeassistant.components.blink import BLINK_DATA, DEFAULT_BRAND
from homeassistant.components.camera import Camera

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['blink']

ATTR_VIDEO_CLIP = 'video'
ATTR_IMAGE = 'image'


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up a Blink Camera."""
    if discovery_info is None:
        return
    data = hass.data[BLINK_DATA]
    devs = []
    for name, camera in data.sync.cameras.items():
        devs.append(BlinkCamera(data, name, camera))

    add_entities(devs)


class BlinkCamera(Camera):
    """An implementation of a Blink Camera."""

    def __init__(self, data, name, camera):
        """Initialize a camera."""
        super().__init__()
        self.data = data
        self._name = "{} {}".format(BLINK_DATA, name)
        self._camera = camera
        self.response = None
        self.current_image = None
        self.last_image = None
        _LOGGER.debug("Initialized blink camera %s", self._name)

    @property
    def name(self):
        """Return the camera name."""
        return self._name

    @property
    def device_state_attributes(self):
        """Return the camera attributes."""
        return self._camera.attributes

    def enable_motion_detection(self):
        """Enable motion detection for the camera."""
        self._camera.set_motion_detect(True)

    def disable_motion_detection(self):
        """Disable motion detection for the camera."""
        self._camera.set_motion_detect(False)

    @property
    def motion_detection_enabled(self):
        """Return the state of the camera."""
        return self._camera.armed

    @property
    def brand(self):
        """Return the camera brand."""
        return DEFAULT_BRAND

    def camera_image(self):
        """Return a still image response from the camera."""
        return self._camera.image_from_cache.content
