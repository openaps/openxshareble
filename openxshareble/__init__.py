
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

  def before_main (self, args, app):
    self.prolog( )
    self.setup_dexcom( )
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
  """
  def before_main (self, args, app):
    return ""
  def after_main (self, args, app):
    return ""
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

