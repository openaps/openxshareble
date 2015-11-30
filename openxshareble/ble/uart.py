
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART as OriginalUART
import Queue
import uuid
from attrs import Attrs

class ShareUART (OriginalUART):
  ADVERTISED = [Attrs.CradleService]
  # SERVICES = [Attrs.DeviceService]
  SERVICES = [Attrs.CradleService]
  CHARACTERISTICS = [Attrs.AuthenticationCode, Attrs.Command, Attrs.Response, Attrs.ShareMessageReceiver, Attrs.ShareMessageResponse, Attrs.HeartBeat, Attrs.DeviceService, Attrs.PowerLevel]

  UART_SERVICE_UUID = Attrs.CradleService
  TX_CHAR_UUID = Attrs.Command
  RX_CHAR_UUID = Attrs.Response
  pass
class Share2UART (OriginalUART):
  # ADVERTISED = [Attrs.CradleService2]
  # ADVERTISED = [Attrs.VENDOR_UUID]
  ADVERTISED = [Attrs.VENDOR_UUID]
  # SERVICES = [Attrs.DeviceService]
  # SERVICES = [Attrs.CradleService2, Attrs.VENDOR_UUID]
  SERVICES = [Attrs.VENDOR_UUID, Attrs.DeviceService]
  # CHARACTERISTICS = [Attrs.AuthenticationCode2, Attrs.Command2, Attrs.Response2, Attrs.ShareMessageReceiver2, Attrs.ShareMessageResponse2, Attrs.HeartBeat2, Attrs.DeviceService, Attrs.PowerLevel]
  CHARACTERISTICS = [ ]

  HEARTBEAT_UUID = Attrs.HeartBeat2
  # UART_SERVICE_UUID = Attrs.CradleService2
  UART_SERVICE_UUID = Attrs.VENDOR_UUID
  TX_CHAR_UUID = Attrs.ShareMessageReceiver2
  RX_CHAR_UUID = Attrs.ShareMessageResponse2
  SendDataUUID = Attrs.ShareMessageReceiver2
  RcveDataUUID = Attrs.ShareMessageResponse2
  CommandUUID  = Attrs.Command2
  ResponseUUID = Attrs.Response2
  AUTH_UUID    = Attrs.AuthenticationCode2
  def __init__(self, device, **kwds):
      """Initialize UART from provided bluez device."""
      # Find the UART service and characteristics associated with the device.
      self._uart = device.find_service(self.UART_SERVICE_UUID)
      print self._uart
      self._queue = Queue.Queue()
      r = device.is_paired
      print "paired?", r
      if not r:
        print "pairing..."
        # help(device._device)
        # help(device._device.Pair)
        device.pair( )
        # device._device.Pair( )
        print "paired"
        print device.advertised
        print "finding service"
        self._uart = device.find_service(self.UART_SERVICE_UUID)
        print "SERVICE", self._uart
      for svc in device.list_services( ):
        print svc.uuid, svc.uuid == self.UART_SERVICE_UUID, svc, svc._service
        print "CHARACTERISTICS"
        chrsts = svc.list_characteristics( )
        for chtr in chrsts:
          print chtr.uuid, chtr, chtr._characteristic
      # print device.list_services( )
      self.serial = kwds.pop('SERIAL', None)
      self.setup_dexcom( )
      self.pair_auth_code(self.serial)
  def set_serial (self, SERIAL):
    self.serial = SERIAL
  def pair_auth_code (self, serial):
      print "sending auth code"
      self._auth = self._uart.find_characteristic(self.AUTH_UUID)
      print self._auth
      # self._auth.
      msg = bytearray(serial + "000000")
      self._auth.write_value(str(msg))
  def setup_dexcom (self):
    self.remainder = bytearray( )
    self._tx = self._uart.find_characteristic(self.TX_CHAR_UUID)
    self._rx = self._uart.find_characteristic(self.RX_CHAR_UUID)
    # Use a queue to pass data received from the RX property change back to
    # the main thread in a thread-safe way.
    self._heartbeat = self._uart.find_characteristic(self.HEARTBEAT_UUID)
    if not self._heartbeat.notifying:
      self._heartbeat.start_notify(self._heartbeat_tick)
    self._char_rcv_data = self._uart.find_characteristic(self.RcveDataUUID)
    if self._rx.notifying:
      self._rx.stop_notify( )
    if not self._rx.notifying:
      self._rx.start_notify(self._rx_received)
  def _heartbeat_tick (self, data):
    print "_heartbeat_tick", str(data).encode('hex')
  def _on_rcv (self, data):
    print "_on_rcv", str(data).encode('hex')

  def read (self, size=1, timeout_sec=None):
    spool = bytearray( )
    spool.extend(self.remainder)
    self.remainder = bytearray( )
    while len(spool) < size:
      spool.extend(self.pop(timeout_sec=timeout_sec))
      time.sleep(.100)
    self.remainder.extend(spool[size:])
    return str(spool[:size])
  def pop (self, timeout_sec=None):
    return super(Share2UART, self).read(timeout_sec=timeout_sec)

class BothShare (ShareUART):
  ADVERTISED = ShareUART.ADVERTISED + Share2UART.ADVERTISED
  # SERVICES = [Attrs.DeviceService]
  SERVICES =  ShareUART.SERVICES + Share2UART.SERVICES
  CHARACTERISTICS =  ShareUART.SERVICES + Share2UART.SERVICES
  

  UART_SERVICE_UUID = Attrs.CradleService2
  TX_CHAR_UUID = Attrs.Command2
  RX_CHAR_UUID = Attrs.Response2
  pass

class UART (Share2UART):
  pass

