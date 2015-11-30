
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


use = Registry( )

class BLEUsage (app.App, Use):

  def __call__ (self, args, app):
    output = None
    def run ( ):
      self.before_main(args, app)
      output = self.main(args, app)
      self.after_main(args, app)
      return output
    self.ble.run_mainloop_with(run)
    return output

@use( )
class list_dexcom (Use):
  """
  Scan the environment looking for Dexcom devices.
  """
  """
  def before_main (self, args, app):
    return ""
  def after_main (self, args, app):
    return ""
  """
  def main (self, args, app):
    return ""

