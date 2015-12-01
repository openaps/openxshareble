
"""
openxshareble
"""

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
  return ""

use = Registry( )
get_uses = use.get_uses

class BLEUsage (Use, app.App):

  __init__ = Use.__init__
  def before_main (self, args, app):

    serial = self.device.get('serial', '')
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
class list_dexcom (BLEUsage):
  """
  Scan the environment looking for Dexcom devices.
  """

  disconnect_on_after = True
  def main (self, args, app):
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

      """
      def __call__ (self, args, app):
        return super(Klass, self).__call__(args, app)
      """
      before_main = Klass.before_main
      after_main = Klass.after_main
      __call__ = Klass.__call__
      """
      def main (self, args, app):
        return super(usage, self).main(args, app)
      """

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

