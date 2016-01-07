
"""
openxshareble
"""

import os
import app
from openaps.uses.use import Use
from openaps.uses.registry import Registry


from openaps.vendors import dexcom

def configure_use_app (app, parser):
  pass

def configure_add_app (app, parser):
 pass

def configure_app (app, parser):
  pass

def configure_parser (parser):
  pass

def main (args, app):
  """
  """
  pass

def set_config (args, device):
  return ""
def display_device (device):
  return "/%s" % device.get('serial')

use = Registry( )
get_uses = use.get_uses

class BLEUsage (Use, app.App):

  __init__ = Use.__init__
  def before_main (self, args, app):

    serial = self.device.get('serial', None)
    print "INIT WITH SERIAL", serial
    self.prolog( )
    self.setup_dexcom(serial=serial)
  def after_main (self, args, app):
    self.epilog( )
  def __call__ (self, args, app):
    output = None
    self.setup_ble( )
    def run ( ):
      self.before_main(args, app)
      output = self.main(args, app)
      self.after_main(args, app)
      return output
    res = self.ble.run_mainloop_with(run, quit_with_loop=False)
    return res

@use( )
class configure (Use):
  DEXCOMRX=os.environ.get('DEXCOMRX', '')
  __doc__ = """
  Configure DEXCOMRX serial number.


  Update the configuration so that your serial number is used to communicate
  with your Dexcom G4 with Share.
  Default: {DEXCOMRX}
  """.format(DEXCOMRX=DEXCOMRX)

  __init__ = Use.__init__
  def configure_app (self, app, parser):
    parser.add_argument('--serial', default=os.environ.get('DEXCOMRX', ''), help="DexcomRX Serial Number")
  def get_params (self, args):
    return dict(serial=args.serial)
  def main (self, args, app):
    results = dict(serial=self.device.get('serial', None))
    if getattr(self.device, 'extra', None) and args.serial:
      print "serial={serial}".format(**results)
      print "saving %s" % args.serial
      results.update(serial=args.serial)
      self.device.extra.add_option('serial', results['serial'])
      self.device.store(app.config)
      app.config.save( )
    return results


@use( )
class list_dexcom (BLEUsage):
  """
  Scan the environment looking for Dexcom devices.
  """

  disconnect_on_after = True
  def main (self, args, app):
    if not self.device.get('serial', None):
      self.disconnect_on_after = False
    receivers = self.enumerate_dexcoms( )
    results = [ ]
    for device in receivers:
      results.append(dict(name=str(device.name)
        , mac=str(device.id)
        , advertised=map(str, device.advertised)))
    return results

class DexcomTask (list_dexcom):
  @classmethod
  def Emulate (Klass, usage):
    class EmulatedUsage (usage, Klass):
      __doc__ = usage.__doc__
      __name__ = usage.__name__

      before_main = Klass.before_main
      after_main = Klass.after_main
      __call__ = Klass.__call__

    EmulatedUsage.__name__ = usage.__name__
    return EmulatedUsage

def transform (existing, Emulator, Original):
  results = dict( )
  for name, usage in existing.use.__USES__.items( ):
    if issubclass(usage, Original):
      adapted = Emulator.Emulate(usage)
      adapted.__name__ = name
      if name not in results:
        results[name] = adapted
  return results


adapted = transform(dexcom, DexcomTask, dexcom.scan)
use.__USES__.update(**adapted)

