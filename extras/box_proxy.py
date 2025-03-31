# Creality K2 Box proxy class for better use in Orca Slicer and some custom things, like filament temperature, flow and other
#
# Copyright (C) 2025 Mikhail Ivanov <masluf@gmail.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

#Box Functions:
# box.get_status(current_time:datetime) ->
# {
#  'filament': 1, 
#  'state': 'connect', 
#  'auto_refill': 1, 
#  'enable': 1, 
#  'filament_useup': 1, 
#  'same_material': [['000004', '09ea7ae', ['T1A'], 'ABS'], ['000004', '0000000', ['T1B', 'T1D'], 'ABS'], ['000004', '0f4e076', ['T1C'], 'ABS']], 'T1': {'state': 'connect', 'filament': 'None', 'temperature': '27', 'dry_and_humidity': '8', 'filament_detected': 'None', 'measuring_wheel': 'None', 'version': '1.1.3', 'sn': '50000214725L525AQEQ', 'vender': ['unknown', 'unknown', 'unknown', 'unknown'], 'remain_len': ['-1', '-1', '-1', '-1'], 'color_value': ['09ea7ae', '0000000', '0f4e076', '0000000'], 'material_type': ['000004', '000004', '000004', '000004'], 'uuid': [37, 118, 48, 2, 164, 52, 183, 21, 57, 57, 54, 50]}, 'T2': {'state': 'None', 'filament': 'None', 'temperature': 'None', 'dry_and_humidity': 'None', 'filament_detected': 'None', 'measuring_wheel': 'None', 'version': '-1', 'sn': '-1', 'vender': ['-1', '-1', '-1', '-1'], 'remain_len': ['-1', '-1', '-1', '-1'], 'color_value': ['-1', '-1', '-1', '-1'], 'material_type': ['-1', '-1', '-1', '-1'], 'uuid': 'None'}, 'T3': {'state': 'None', 'filament': 'None', 'temperature': 'None', 'dry_and_humidity': 'None', 'filament_detected': 'None', 'measuring_wheel': 'None', 'version': '-1', 'sn': '-1', 'vender': ['-1', '-1', '-1', '-1'], 'remain_len': ['-1', '-1', '-1', '-1'], 'color_value': ['-1', '-1', '-1', '-1'], 'material_type': ['-1', '-1', '-1', '-1'], 'uuid': 'None'}, 'T4': {'state': 'None', 'filament': 'None', 'temperature': 'None', 'dry_and_humidity': 'None', 'filament_detected': 'None', 'measuring_wheel': 'None', 'version': '-1', 'sn': '-1', 'vender': ['-1', '-1', '-1', '-1'], 'remain_len': ['-1', '-1', '-1', '-1'], 'color_value': ['-1', '-1', '-1', '-1'], 'material_type': ['-1', '-1', '-1', '-1'], 'uuid': 'None'}}

# MACROS:
# BOX_GET_BUFFER_STATE ADDR=1
#  // buffer_state: 0x2
#  // empty
#  // buffer_state: 0x0
#  // middle
#  // buffer_state: 0x1
#  // full
#
# BOX_ERROR_CLEAR -- Clear CFS error
# BOX_BLOW -- Switch on model fan to ~3sec


#from pprint import pprint
import datetime
import inspect
from types import FunctionType
from argparse import ArgumentParser

def attributes(obj):
    disallowed_names = {
      name for name, value in getmembers(type(obj)) 
        if isinstance(value, FunctionType)}
    return {
      name: getattr(obj, name) for name in dir(obj) 
        if name[0] != '_' and name not in disallowed_names and hasattr(obj, name)}

def print_attributes(obj):
    pprint(attributes(obj))

class BoxProxy:
  def __init__(self, config):
      self.printer = config.get_printer()
      self.box = self.printer.lookup_object('box')
      self.reactor = self.printer.get_reactor()
      self.gcode = self.printer.lookup_object('gcode')
    
      #self.message = config.get('message', 'Box Proxy work!')
      
      self.gcode.register_command(
                'DUMP_OBJ_FN', self.cmd_DUMP_OBJ_FN)#, desc=self.cmd_GREET_help)
      self.gcode.register_command(
                'DUMP_OBJ', self.cmd_DUMP_OBJ)
      self.gcode.register_command(
                'BOX_DUMP', self.cmd_BOX_DUMP)
      self.gcode.register_command(
                'BOX_PRINT_ATTR', self.cmd_BOX_PRINT_ATTR)
      self.gcode.register_command(
                'BOX_SHOW_TNN_DATA', self.cmd_show_Tnn_data)
      self.gcode.register_command(
                'INSPECT', self.cmd_INSPECT)
      self.gcode.register_command(
                'CALLER', self.cmd_CALLER)
      self.gcode.register_command(
                'WORK', self.cmd_WORK)          
#      self.printer.register_event_handler(
#           'klippy:ready', self._ready_handler)
  def cmd_INSPECT(self, gcmd):
    obj =  self.box.box_action
    fName = gcmd.get('N', 'Tn_action') #getattr(obj, fName)
    fSig = getattr(obj, fName)
    if inspect.isfunction(fSig) or inspect.ismethod(fSig):
        #s = inspect.getsource(fSig)
        res = inspect.getargspec(fSig)
        strn = ";".join(str(x) for x in res  )
        #self.gcode.respond_info(strn)
        #self.gcode.respond_info(s)
        strn = str(inspect.signature(fSig))
        self.gcode.respond_info(strn)
        
        for param in inspect.signature(fSig).parameters.values():
          self.gcode.respond_info("Parameter: %s" % {param.name})
          self.gcode.respond_info("Type: %s"% {param.annotation})
          self.gcode.respond_info("Default: %s" % {param.default})
          self.gcode.respond_info("Kind: %s" % {param.kind})
          self.gcode.respond_info("---")
    
        return len(inspect.signature(fSig).parameters.values())
    elif inspect.isclass(fSig):
      for attr in dir(fSig):
        self.gcode.respond_info("obj.%s = %r" % (attr, getattr(fSig, attr))) 
    else:
        self.gcode.respond_info(str(fSig))
    return 0
        
  def cmd_CALLER(self, gcmd):
    argCnt = self.cmd_INSPECT(gcmd)
    obj =  self.box.box_action
    fName = gcmd.get('N', 'blow')
    fSig = getattr(obj, fName)
    if argCnt != 0:
      s = gcmd.get('P', '')
      l = s.split(",")
      fSig(*l)
    else:
      fSig()
    
  def cmd_WORK(self, gcmd):
    obj =  self.box
    a = gcmd.get('A', 0)
    tnn = gcmd.get('TNN', 'T1A')
    
    ###########box
    
    ###########box_action
    #obj.communication_extrude_process(1, 1, '', a) #(addr, num, trigger='', stage=2, report_err=True, extrude=None) #error on second parameter
    #obj.check_same_box(tnn)
    #obj.box_extrude_material_part(tnn) #(tnn, retry=[0, 0, 0, 0]) LOAD material but have some errors
    
    #obj.box_extrude_material(tnn)  #Load material but change temp
    #obj.extrude_process_auto_retry_process(tnn, a, [1,1,1,1]) #(tnn, type, retry=[0, 0, 0, 0]) DO NOTHING
    #obj.box_extrude_material_stage8(tnn)

    #adr = gcmd.get_int('ADR', 1)
    #a = gcmd.get_int('A', 0)
    #num = gcmd.get_int('NUM', 0)
    #obj.communication_set_pre_loading(adr, a, num, True) #(addr, action, num=15, force=False) Work, but do nothing
    
    #tnn = gcmd.get('TNN', 'T1A')
    #obj.box_extrude_material(tnn)
    
    #obj.check_flush_temp_and_extrude([0, 0, 0, 0], [1], 234, 237, 100, False) #(length, index, temp, max_temp, velocity, max_temp_flush=False)
    #obj.check_and_extrude(1, 100) #(extrude, velocity, wait=True)
    
    #obj.Tn_Extrude(True, [100], 234, [226, 227, 228, 229], None, tnn) #(extrude, velocity, temp, max_temp=None, percent=None, tnn=None) WORK but only extrude. CFS do nothing!
    #obj.communication_extrude2_process(1 #(addr, num, trigger)
        
  def cmd_DUMP_OBJ(self, gcmd):
      objN = gcmd.get('O', 'box')
      obj =  self.printer.lookup_object(objN)
      for attr in dir(obj):
        self.gcode.respond_info("obj.%s = %r" % (attr, getattr(obj, attr))) 
  
  def cmd_DUMP_OBJ_FN(self, gcmd):
      objN = gcmd.get('O', 'box')
      obj =  self.printer.lookup_object(objN)
      fName = gcmd.get('N', 'cmd_get_buffer_state')
      fSig = getattr(obj, fName)
      if inspect.isfunction(fSig) or inspect.ismethod(fSig):
        res = inspect.getargspec(fSig)
        strn = ";".join(str(x) for x in res  )
        self.gcode.respond_info(strn)
      else:
        self.gcode.respond_info(str(fSig)) #(";".join(str(x) for x in fSig  ))
        
  def cmd_GREET(self, gcmd):
      #msg = self.box.state #gcmd.get('MSG', 'Default MSG')
      #self.gcode.respond_info('Box: ' + self.box.filament)
      self.gcode.respond_info(vars(self.box))
      #dump(self.box)
      #self._greet(msg)
  def cmd_BOX_DUMP(self, gcmd):
      fName = gcmd.get('N', 'cmd_get_buffer_state')
      fSig = getattr(self.box, fName)
      #sig = inspect.signature(self.box.cmd_get_buffer_state)
      if inspect.isfunction(fSig) or inspect.ismethod(fSig):
        res = inspect.getargspec(fSig)
        strn = ";".join(str(x) for x in res  )
        self.gcode.respond_info(strn)
      else:
        self.gcode.respond_info(str(fSig)) #(";".join(str(x) for x in fSig  ))
      #self.gcode.respond_info(str(sig))
      #self.gcode.respond_info(str(sig.parameters['eventime']))
      
      current_time = datetime.datetime.now()
      #val = self.box.get_status(current_time)
      #val = self.box.get_status(cmd_get_buffer_state)
      #self.gcode.respond_info(str(val))
      
      #box = self.box
      #self.dump(box)
  def cmd_BOX_PRINT_ATTR(self, gcmd):
      obj = self.box
      for attr in dir(obj):
        self.gcode.respond_info("obj.%s = %r" % (attr, getattr(obj, attr)))
        
  def cmd_show_Tnn_data(self, gcmd):
      self.box.cmd_show_Tnn_data(gcmd)
  
 # def _greet(self, msg, eventtime=None):
  #    self.gcode.respond_info(self.message)
   #   self.gcode.respond_info(msg)
    #  return self.reactor.NEVER


def load_config(config):
    return BoxProxy(config)