"""
Driver for Thermostate Lauda RE 206
"""

import serial
import time
import sys
from serial import SerialException
import logging
import timeout_decorator
from timeout_decorator.timeout_decorator import TimeoutError

class Variocool(object):
    """
    Control and read thermostat and pump of a RE 206 Lauda device
    """
    __MAX_ATTEMPTS = 5
    __OWN_TIMEOUT = 0.25
    __DEVICE_IDENTIFIER = "VCXXXX"

    def __init__(self, port, loglvl=logging.INFO):
        """ Start device
        :param port: Path to device mounting point i.e. /dev/ttyUSB0
        :type port: str
        """
        stream_handler = logging.StreamHandler(sys.stdout)
        self.__port = port

        # Initialize logging instance
        self._log = logging.getLogger("Lauda@" + port)
        self._log.addHandler(stream_handler)
        self._log.level = loglvl

        # Set up serial communication
        self.device = self.init_RS232_to_serial(port)
        if self.device.isOpen():
            self.device.close()
        self.device.open()

    def init_RS232_to_serial(self, port):
        """ Start serial communication
        :param port: Path to device mounting point i.e. /dev/ttyUSB0
        :type port: serial.Serial
        """
        try:
            return serial.Serial(port=port,
               baudrate=9600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1)
        except SerialException:
             self._log.error("Error while opening communication.")
             raise SerialException('Lauda ' + self.__DEVICE_IDENTIFIER + ': Connection error for port: ' + port)

    def start(self):
        """ Switch on unit from standby
        """
        try:
            try:
                self.device.open()
            except serial.SerialException:
                self.device.close()
                self.device.open()
            if self.temperature is None:
                self._log.error("Temperature not set. -> Start aborted")
                raise ValueError('Lauda ' + self.__DEVICE_IDENTIFIER + ': Failed to start due to missing temperature.')

            self.__write('START')
            self._log.info("Device started")
        except SerialException:
            self._log.error("Communication error while start request")
            raise SerialException('Lauda ' + self.__DEVICE_IDENTIFIER + ': Failed to start.')

    def stop(self):
        """ Switches the unit to stand-by (pump, heating, refrigeration system off)
        """
        try:
            self.__write('STOP')
            self._log.info("Device stopped")
        except SerialException:
            self._log.error("Communication error while sending stop request")
            raise SerialException('Lauda ' + self.__DEVICE_IDENTIFIER + ': Failed to stop.')


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
            self._log.info(f"Set Xp = {Xp} and {Tn}")
        except SerialException:
            raise SerialException('Lauda ' + self.__DEVICE_IDENTIFIER + ': initialization error')


    def lock_control_panel(self):
        """ Lock control panel of lauda """
        try:
            self.__write('OUT_MODE_00_0')
            self._log.info(f"Locked control panel.")
        except SerialException:
            raise SerialException('Lauda RE206: Failed to lock control panel')


    def clear_buffer(self):
        """ Discard all pending readings """
        try:
            buf = self.device.readline()
            while buf:
                buf = self.device.readline()
            self._log.info(f"Buffer cleared port")
        except SerialException:
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
        """ Get set temperature """
        answ = self.__txrx('IN_SP_00')
        if len(answ) > 5:
            self._log.debug(f"Current set temperature {answ}.")
            answ = answ.replace(b'\r',b'').replace(b' ', b'')
            return float(answ)
        else:
            self._log.error(f"Failed to read temperature.")
            return None

    @temperature.setter
    def temperature(self, temperature):
        """ Register new set temperature
        :param temperature: New temperature in [deg C]
        :type temperature: float
        :returns: Temperature
        :rtype: float
        """
        self._log.debug(f"New set temperature {temperature}.")
        self.__write('OUT_SP_00_{:03.2f}'.format(temperature))
        return float(temperature)

    @property
    def t_ext(self):
        """ Get external temperature """
        answ = self.__txrx('IN_PV_01')
        temperature = None
        try:
            answ = answ.replace(b'\r',b'').replace(b' ', b'')
            temperature = float(answ)
        except ValueError:
            state = self.get_device_state()
            self._log.debug(f"Lauda Error {answ}, state: {state}")
        self._log.debug(f"New ext. temperature {temperature}.")
        return answ

    @t_ext.setter
    def t_ext(self, temperature):
        """ Register new external temperature
        :param temperature: New external temperature in [deg C]
        :type temperature: float
        :returns: Temperature
        :rtype: float
        """
        answ = self.__txrx('OUT_PV_05_{:03.2f}'.format(temperature))
        self._log.debug(f"New ext. temperature {temperature}.")
        return float(temperature)

    def checkConnection(self):
        """ Send test request
        :return: Connection state
        :type: boolean
        """
        try:
            self.__write('IN_PV_00')
            self.__readline()
            return True
        except:
            return False

    def get_device_state(self):
        """ Request current device status
        :return: 0 if no error occured otherwise see manuel p. 35
        :type: int
        """
        return self.__txrx('STAT')

    def RS232moduleSN(self):

        dev_str = ""
        if "tty" in self.__port:
             dev_str = self.__port.rsplit("tty",1)[1]
        return self.__txrx('VERSION_V').decode('utf-8').strip('\r\n').replace(" ", "")+"_"+dev_str

    def checkConnection(self):
        """ Send test request
        :return: Connection state
        :type: boolean
        """
        try:
            self.__write('IN_PV_00')
            self.__readline()
            return True
        except:
            return False

    def get_device_state(self):
        """ Request current device status
        :return: 0 if no error occured otherwise see manuel p. 35
        :type: int
        """
        return self.__txrx('STAT')

    @timeout_decorator.timeout(4, timeout_exception=TimeoutError)
    def test(self):
        """
        Check if device is reponsive
        :return: device availability
        :type: boolean
        """
        status = self.__txrx('STATUS').decode('utf-8').strip('\r\n')
        self._log.info(f"Device status: {status}")
        if "-1" in status:
            return False

        if "0" in status:
            return True

        return False

    def __write(self, cmd):
        try:
            self.device.write(str.encode(cmd)+b'\r')
        except SerialException:
            raise SerialException('Lauda ' +  self.__DEVICE_IDENTIFIER + ': Error while writing.')

    def __readline(self, n=0):
        out = bytearray()
        eol = b'\r'
        leneol = len(eol)
        c = None
        if self.device is None:
            self._log.error(f"Device not defined.")
            return out

        if not self.device.isOpen():
            self._log.info(f"Opening serial connection.")
            self.device.open()

        while True:
            c = self.device.read(1)
            if c:
                out += c
                if out[-leneol:] == eol:
                    break
            else:
                break

        if not out and n<30:
            self._log.warning(f"Retry reading.")
            time.sleep(0.5)
            if self.device.isOpen():
                self.device.close()
            self.device.open()
            self.read_buffer()
            self.__readline(n=n+1)

        return out

    def __txrx(self, cmd):
        """ Write command and consequently perform a read operation.
        """
        answ = None
        for i in range(3):
            self.read_buffer()
            self.__write(cmd)
            time.sleep(0.1)
            answ = self.__readline()
            if answ is not None:
                break
        print(cmd)
        print(answ)
        self._log.debug(f"CMD: {cmd}\t Return: {answ}")

        return answ

