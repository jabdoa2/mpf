""" Contains the Accelerometer """

import time
import math
from mpf.system.device import Device


class Accelerometer(Device):
    """Implements an accelerometer

    Args: Same as the Device parent class

    """

    config_section = 'accelerometers'
    collection = 'accelerometers'
    class_label = 'accelerometer'

    def __init__(self, machine, name, config, collection=None, validate=True):
        super(Accelerometer, self).__init__(machine, name, config, collection,
                                     platform_section='accelerometer',
                                     validate=validate)

        # TODO: better check. if platform has hardware interrupt
        if len(config['events']) == 1:
            self.platform.configure_accelerometer(self,
                tiltInterrupt=True,
                periodicRead=False,
                tiltThreshold=config['events'].keys()[0])

            self.log.info("Will use hardware interrupt")



        elif len(config['events']) > 1:
            self.platform.configure_accelerometer(self,
                tiltInterrupt=False,
                periodicRead=True)

            self.log.info("Can only handle one threshold in hardware. "
                          "Will read permanently!")


    def received_hit(self):
        self.log.debug("Received hit above threshold %s",
                config['events'].keys()[0])
        self.events.post(config['events'].values()[0])

    def _calculate_vector_length(self, x, y, z):
        return math.sqrt(x*x + y*y + z*z)

    def _calculate_angle(self, x1, y1, z1, x2, y2, z2):
        return math.acos((x1*x2 + y1*y2 + z1*z2) /
                (self._calculate_vector_length(x1, y1, z1) *
                self._calculate_vector_length(x2, y2, z2)))

    def update_acceleration(self, x, y, z):
        self.log.debug("Acceleration: %s, %s, %s", x, y, z)

        acceleration = self._calculate_vector_length(x, y, z)

        for min_acceleration in self.config['events']:
            if acceleration > min_acceleration:
                self.log.debug("Received hit above threshold %s",
                    min_acceleration)
                self.events.post(self.config['events'][min_acceleration])

