
from dexcom_reader import readdata
import xml.etree.ElementTree as etree


class Device (readdata.Dexcom):
  """
  Local shim of original readdata.Dexcom from dexcom_reader.
  This simply replaces some of the logic to set up the data transport
  mechanisms.
  """
  def __init__ (self, uart):
    # assign serial port/uart device
    self.uart = uart

  def Connect (self):
    return True

  @property
  def port (self):
    return self.uart

  def Disconnect (self):
    return True

  def flush (self):
    return True

  def write (self, data, *args, **kwargs):
    # the usb protocol is exactly the same, the ble protocol adds a
    # prefix of 0x01, 0x01 to every message written.
    prefix = str(bytearray([ 0x01, 0x01 ]))
    return self.port.write(prefix + data, *args, **kwargs)

