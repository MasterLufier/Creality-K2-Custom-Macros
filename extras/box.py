#from .box_wrapper import MultiColorMeterialBoxWrapper
#def load_config(config):
#    return(MultiColorMeterialBoxWrapper(config))

from .box_wrapper import MultiColorMeterialBoxWrapper, BoxAction, BoxState
import functools

def decor(gcode, fn):
    def wrapper(*args, **kwargs):
        gcode.respond_info(f"DBG: {fn.__name__} args={args} kwargs={kwargs}")
        res = fn(*args, **kwargs)
        if(res != False and res != True):
          gcode.respond_info(f"DBG: {fn.__name__} returned {res}")
        return res
    return wrapper

class BoxWrapper(MultiColorMeterialBoxWrapper):
  def __init__(self, config):
      super().__init__(config)
      self.box_action.blow =  decor(self.gcode, self.box_action.blow)
      self.box_action.send_data = decor(self.gcode, self.box_action.send_data)
      #decor(self.gcode, self.box_action.)
      
      self.box_action.box_extrude_material = decor(self.gcode, self.box_action.box_extrude_material)
      self.box_action.box_extrude_material_part = decor(self.gcode, self.box_action.box_extrude_material_part)
      self.box_action.box_extrude_material_stage8 = decor(self.gcode, self.box_action.box_extrude_material_stage8)
      self.box_action.box_retrude_material = decor(self.gcode, self.box_action.box_retrude_material)
      self.box_action.box_retrude_material_filament_err_part = decor(self.gcode, self.box_action.box_retrude_material_filament_err_part)
      
      self.box_action.check_and_extrude = decor(self.gcode, self.box_action.check_and_extrude)
      #self.box_action.check_connect = decor(self.gcode, self.box_action.check_connect) # called every 1 sec with 1-2-3-4 addr 
      self.box_action.check_flush_temp_and_extrude = decor(self.gcode, self.box_action.check_flush_temp_and_extrude)
      self.box_action.check_material_refill = decor(self.gcode, self.box_action.check_material_refill)
      self.box_action.check_rfid_valid = decor(self.gcode, self.box_action.check_rfid_valid)
      self.box_action.check_same_box = decor(self.gcode, self.box_action.check_same_box)
      self.box_action.check_speed_and_extrude = decor(self.gcode, self.box_action.check_speed_and_extrude)
      
      self.box_action.communication_create_connect  = decor(self.gcode, self.box_action.communication_create_connect)
      self.box_action.communication_ctrl_connection_motor_action = decor(self.gcode, self.box_action.communication_ctrl_connection_motor_action)
      self.box_action.communication_extrude2_process = decor(self.gcode, self.box_action.communication_extrude2_process)
      self.box_action.communication_extrude_process = decor(self.gcode, self.box_action.communication_extrude_process)
      #self.box_action.communication_get_box_state = decor(self.gcode, self.box_action.communication_get_box_state)
      #self.box_action.communication_get_buffer_state = decor(self.gcode, self.box_action.communication_get_buffer_state)
      #self.box_action.communication_get_filament_sensor_state = decor(self.gcode, self.box_action.communication_get_filament_sensor_state)
      #self.box_action.communication_get_hardware_status = decor(self.gcode, self.box_action.communication_get_hardware_status)
      #self.box_action.communication_get_remain_len = decor(self.gcode, self.box_action.communication_get_remain_len)
      #self.box_action.communication_get_rfid = decor(self.gcode, self.box_action.communication_get_rfid)
      #self.box_action.communication_get_version_sn = decor(self.gcode, self.box_action.communication_get_version_sn)
      #self.box_action.communication_measuring_wheel  = decor(self.gcode, self.box_action.communication_measuring_wheel)
      self.box_action.communication_retrude_process = decor(self.gcode, self.box_action.communication_retrude_process)
      self.box_action.communication_set_box_mode = decor(self.gcode, self.box_action.communication_set_box_mode)
      self.box_action.communication_set_pre_loading = decor(self.gcode, self.box_action.communication_set_pre_loading)
      self.box_action.communication_test  = decor(self.gcode, self.box_action.communication_test)
      self.box_action.communication_tighten_up_enable  = decor(self.gcode, self.box_action.communication_tighten_up_enable)
      
      self.box_action.disable_filament_sensor = decor(self.gcode, self.box_action.disable_filament_sensor)
      self.box_action.disable_heart_process = decor(self.gcode, self.box_action.disable_heart_process)
      self.box_action.enable_filament_sensor = decor(self.gcode, self.box_action.enable_filament_sensor)
      self.box_action.enable_heart_process = decor(self.gcode, self.box_action.enable_heart_process)
      self.box_action.extrude_process_auto_retry_process = decor(self.gcode, self.box_action.extrude_process_auto_retry_process)
      
      self.box_action.extrude_process_auto_retry_process = decor(self.gcode, self.box_action.extrude_process_auto_retry_process)
      self.box_action.extrude_process_stage7 = decor(self.gcode, self.box_action.extrude_process_stage7)
      self.box_action.extruder_extrude = decor(self.gcode, self.box_action.extruder_extrude)
      
      self.box_action.find_objs = decor(self.gcode, self.box_action.find_objs)
      self.box_action.get_flush_len = decor(self.gcode, self.box_action.get_flush_len)
      self.box_action.get_flush_max_temp = decor(self.gcode, self.box_action.get_flush_max_temp)
      self.box_action.get_flush_temp = decor(self.gcode, self.box_action.get_flush_temp)
      self.box_action.get_flush_velocity = decor(self.gcode, self.box_action.get_flush_velocity)
      self.box_action.get_material_max_extrusion_speed = decor(self.gcode, self.box_action.get_material_max_extrusion_speed)
      self.box_action.get_material_target_max_temp = decor(self.gcode, self.box_action.get_material_target_max_temp)
      self.box_action.get_material_target_temp = decor(self.gcode, self.box_action.get_material_target_temp)

      self.gcode.register_command(
                'DUMP_BOX_ACTION', self.cmd_DUMP_BOX_ACTION)#, desc=self.cmd_GREET_help)

  def cmd_DUMP_BOX_ACTION(self, gcmd):
      obj =  self.box_action #self.printer.lookup_object(objN)
      for attr in dir(obj):
        self.gcode.respond_info("obj.%s = %r" % (attr, getattr(obj, attr))) 
     
def load_config(config):
    return BoxWrapper(config)