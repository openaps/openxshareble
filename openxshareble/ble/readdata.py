
from dexcom_reader import readdata
import xml.etree.ElementTree as etree


class Device (readdata.Dexcom):
  def __init__ (self, uart):
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
    prefix = str(bytearray([ 0x01, 0x01 ]))
    return self.port.write(prefix + data, *args, **kwargs)

