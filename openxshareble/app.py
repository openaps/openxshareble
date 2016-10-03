
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART as OriginalUART
# from ble import uart
from ble.uart import UART
from ble.readdata import Device
import time
import atexit
import logging
log = logging.getLogger(__name__)

class App (object):
  """ A high level application object.

  Any application needing to talk to Dexcom G4 + Share will need
  to perform operations to setup the ble data transport.  This class
  mixes the UART, ble code, and provides helpful prolog and epilog
  routines that run before and after main, respectively.
  """
  def __init__ (self, **kwds):
    self.disconnect_on_after = kwds.get('disconnect_on_after', False)
    pass
  def setup_ble (self):
    self.remote = None
    self.ble = Adafruit_BluefruitLE.get_provider()
    # Initialize the BLE system.  MUST be called before other BLE calls!
    self.ble.initialize()
    # Get the first available BLE network adapter and make sure it's powered on.
    self.adapter = self.ble.get_default_adapter()
    self.adapter.power_on()
    log.info('Using adapter: {0}'.format(self.adapter.name))
    self.dexcom = None
    pass
  def setup_dexcom (self, serial=None, mac=None):
    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        # Wait for service discovery to complete for the UART service.  Will
        # time out after 60 seconds (specify timeout_sec parameter to override).
        # print device._device.GattServices
        log.info('Discovering services...')
        UART.discover(self.remote)

        # Once service discovery is complete create an instance of the service
        # and start interacting with it.
        self.uart = UART(self.remote, SERIAL=serial)


        self.dexcom = Device(self.uart)
        # log.info("DEXCOM", self.dexcom)
        if not self.dexcom:
          self.dexcom = Device(self.uart)
    except:
        # Make sure device is disconnected on exit.
        if self.disconnect_on_after:
          self.remote.disconnect()
        raise
  def prolog (self, clear_cached_data=True, disconnect_devices=True, scan_devices=True, connect=True, mac=None):
    """
    Things to do before running the main part of the application.
    """
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    if clear_cached_data:
      self.ble.clear_cached_data()


    if disconnect_devices:
      # Disconnect any currently connected UART devices.  Good for cleaning up and
      # starting from a fresh state.
      log.info('Disconnecting any connected UART devices...')
      UART.disconnect_devices()

    if scan_devices:
      # Scan for UART devices.
      log.info('Searching for UART device...')
      try:
          if mac:
            self.remote = self.select_mac(mac=mac)
          else:
            self.adapter.start_scan()
            # Search for the first UART device found (will time out after 60 seconds
            # but you can specify an optional timeout_sec parameter to change it).
            self.remote = UART.find_device()
          if self.remote is None:
              raise RuntimeError('Failed to find UART device!')
      finally:
          # Make sure scanning is stopped before exiting.
          if self.adapter.is_scanning:
            self.adapter.stop_scan()

    if connect and not self.remote.is_connected:
      log.info('Connecting to device...')
      self.remote.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                        # to change the timeout.
    log.info(self.remote.name)
    # device._device.Pair( )
    # log.info(self.ble._print_tree( ))
    for service in self.remote.list_services( ):
      log.info("services: %s %s", service, service.uuid)
    log.info("ADVERTISED")
    log.info(self.remote.advertised)

    pass
  def select_mac (self, mac=None, **kwds):
    for device in self.enumerate_dexcoms(**kwds):
      if str(device.id) == mac:
        return device
  def enumerate_dexcoms (self, timeout_secs=10):
    self.adapter.start_scan()
    # Use atexit.register to call the adapter stop_scan function before quiting.
    # This is good practice for calling cleanup code in this main function as
    # a try/finally block might not be called since this is a background thread.
    def maybe_stop ( ):
      if self.adapter.is_scanning:
        self.adapter.stop_scan( )
    # atexit.register(maybe_stop)
    log.info('Searching for UART devices...')

    # print('Press Ctrl-C to quit (will take ~30 seconds on OSX).')
    # Enter a loop and print out whenever a new UART device is found.
    start = time.time( )
    now = time.time( )
    known_uarts = set()
    while (now - start) < timeout_secs:
        # Call UART.find_devices to get a list of any UART devices that
        # have been found.  This call will quickly return results and does
        # not wait for devices to appear.
        found = set(UART.find_devices())
        # Check for new devices that haven't been seen yet and print out
        # their name and ID (MAC address on Linux, GUID on OSX).
        new = found - known_uarts
        for device in new:
            try:
                log.info('Found UART: {0} [{1}]'.format(device.name, device.id))
            except UnicodeEncodeError:
                pass
        known_uarts.update(new)
        # Sleep for a second and see if new devices have appeared.
        time.sleep(1.0)
        now = time.time( )
    self.adapter.stop_scan( )
    return known_uarts

  def epilog (self):
    """
    Things to do after running the main part of the application.
    """
    # Make sure device is disconnected on exit.
    if self.disconnect_on_after and self.remote.is_connected:
      self.remote.disconnect()
    # self.ble._gobject_mainloop.quit( )
    pass
  def set_handler (self, handler):
    self.handler = handler
  def run (self):
    self.ble.run_mainloop_with(self.main)
    pass
  def main (self):
    """
    Subclasses should replace this method.
    """
