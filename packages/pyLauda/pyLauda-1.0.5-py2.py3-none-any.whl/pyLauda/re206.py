"""
Driver for Thermostate Lauda RE 206
"""

__author__ = "konstantin.niehaus [ at ] dlr .de"
__copyright__ = "German Aerospace Center 2020"
__credits__ = ["Konstantin Niehaus", "Daniel Schmeling", "Andreas Westhoff"]
__license__ = "tba"
__version__ = "1.0.0"
__maintainer__ = "Konstantin Niehaus"
__email__ = "konstantin.niehaus [ at ] dlr .de"
__status__ = "Production"


import serial
from serial.serialutil import SerialException

class RE206(object):
    """ Control and read thermostat and pump of a RE 206 Lauda device
    """
    __MAX_ATTEMPTS = 5
    __OWN_TIMEOUT = 2.0


    def __init__(self, port):
        """ Start device
        :param port: Path to device mounting point i.e. /dev/ttyUSB0
        :type port: str
        """
        # Set up serial communication
        self.device = self.init_RS232_to_serial(port)
        # Wake up device
        self.start()
        # Lock panel
        self.lock_control_panel()

    def init_RS232_to_serial(self, port):
        """ Start serial communication
        :param port: Path to device mounting point i.e. /dev/ttyUSB0
        :type port: str
        """
        try:
            return serial.Serial(port=port,
                baudrate= 19200,
                rtscts=1,
                dsrdtr=0,
                timeout=1)
        except serial.SerialException:
             raise SerialException('Lauda RE206: Connection error for port: ' + port)


    def start(self):
        """ Switch on unit from standby
        """
        try:
            self.device.open()
            self.__write('START\r')
            msg = '[INFO] Start lauda RE20X at port '+str(self.device)
            return msg
        except:
            raise SerialException('Lauda RE206: Failed to start.')

    def stop(self):
        """ Switches the unit to stand-by (pump, heating, refrigeration system off)
        """
        try:
            self.__write('STOP\r')
            msg = '[INFO] Stop lauda RE20X at port '+str(self.device)
            return msg
        except:
            raise SerialException('Lauda RE206: Failed to stop.')


    def set_control_parameters(self, Xp, Tn):
        """ Set PID parameters Xp and Tn (see. manual p35)
        :param Xp: proportional value
	:type Xp: float
        :param Tn: time value
	:type Tn: float
	"""
        try:
            self.__write('OUT_PAR_00_{:3.2}'.format(Xp))
            self.__write('OUT_PAR_01_{:3.2}'.format(Tn))
            msg = '[INFO] Set Xp = '+Xp+' and '+Tn+' at port '+str(self.device)
            return msg
        except:
            raise SerialException('Lauda RE206: initialization error')


    def lock_control_panel(self):
        """ Lock control panel of lauda """

        try:
            self.__write('OUT_MODE_00_0\r')
            msg = '[INFO] lock control panel at port '+str(self.device)
            return msg
        except:
            raise SerialException('Lauda RE206: Failed to lock control panel')


    @property
    def pump(self):
        """ Read current pump level """
        self.__write('IN_SP_01\r')
        answ = str(self.device.readline())
        answ = int(answ[3:-8])
        return answ
    @pump.setter
    def pump(self, level):
        """ Set pump level
        :param level: Set level from 1 to 5
        :param type: int or float
        """
        assert level in range(1,6)
        try:
            self.__write('OUT_SP_01_{:1.0f}\r'.format(level))
            msg = '[INFO] Set pump level '+str(level)+' port '+str(self.device)
            return msg
        except:
            raise SerialException('Lauda RE206: Error during setting pump level.')


    def clear_buffer(self):
        """ Discard all pending readings """
        try:
            buf = self.device.readline()
            while buf:
                buf = self.device.readline()
            msg = '[INFO] Buffer cleared port '+str(self.device)
        except:
            raise SerialException('Lauda RE206: Error during buffer clearing.')

    def read_buffer(self):
        """ Read all pending readings """
        msg_list = []
        msg_list.append(self.device.readline())
        while self.device.readline():
            msg_list.append(self.device.readline())
        return msg_list


    @property
    def temperature(self):
        """ Get current bath temperature """
        self.__write('IN_PV_00\r')
        answ = str(self.device.readline())
        answ = float(answ[3:-5])
        return answ

    @temperature.setter
    def temperature(self, temperature):
        """ Register new set temperature
        :param temperature: New temperature in [deg C]
        :type temperature: float
        """
        try:
            self.__write('OUT_SP_00_{:03.2f}\r'.format(temperature))
            return float(temperature)

        except:
            raise SerialException('Lauda RE206: initialization error')

    def get_SetTemperature(self):
        """ Get set temperature """
        self.__write('IN_SP_00\r')
        answ = str(self.device.readline())
        answ = float(answ[3:-5])
        return answ

    def checkConnection(self):
        """ Send test request
        :return: Connection state
        :type: boolean
        """
        try:
            self.__write('IN_PV_00\r')
            self.__readline()
            return True
        except:
            return False

    def __write(self, cmd):
        self.clear_buffer()
        self.device.write(str.encode(cmd))

    def __readline(self):
        # own timeout
        attempts = 1
        out = ''
        while attempts <= self.__MAX_ATTEMPTS:
            # look for waiting bytes
            bytesWaiting = self.device.inWaiting()
            # 0 waiting bytes:
            if bytesWaiting <= 0:
                # sleep OWN_TIMEOUT seconds
                time.sleep(self.__OWN_TIMEOUT)
            else:
                # more than 0 waiting bytes:
                while bytesWaiting > 0:
                    # append to out until \r is found
                    b = self.device.read(1)
                    out += b
                    if (b == '\r' or b == '\n'):
                        return out
            # increase attempts after trying to detect waiting bytes
            attempts = attempts + 1
        # MAX_ATTEMPTS reached: raise Exception
        raise SerialException('Lauda: timed out.')


