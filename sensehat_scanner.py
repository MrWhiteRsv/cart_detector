import time
import threading
import utils

from sense_hat import SenseHat
    
class SensehatScanner:
 
  worker = None
  logger = None
  sense = None
  
  repeated_timer_inst = None

  def start(self, logger):
    self.logger = logger
    self.repeated_timer_inst = utils.RepeatedTimer(5, self.log_scan)
    self.worker = threading.Thread(target = self.start_continous_scan)
    self.sense = SenseHat()
    self.worker.do_run = True 
    self.worker.start()
    self.repeated_timer_inst.start()
  
  def stop(self):
    self.logger = None
    self.repeated_timer_inst.stop()
    self.worker.do_run = False
    self.worker.join()

  def log_scan(self):
    self.logger.log_gyro(
        time.time(),
        self.orientation['yaw'],
        self.orientation['pitch'],
        self.orientation['roll'])

  def start_continous_scan(self):
    print 'starting continous sensehat scan'
    yaw = 0
    while True:
      if (not getattr(self.worker, "do_run", True)) :
        break;
      gyro_only = self.sense.get_gyroscope()
      self.sense.set_pixel(0, int(yaw/45), 0, 0, 0)
      self.orientation = self.sense.get_orientation_degrees()
      yaw = self.orientation['yaw']
      # print yaw
      self.logger.log_gyro_raw(
          time.time(),
          self.orientation['yaw'],
          self.orientation['pitch'],
          self.orientation['roll'])
      self.sense.set_pixel(0, int(yaw/45), 0, 255, 0)
      #accel_only = self.sense.get_accelerometer()
      #print("get_accelerometer p: {pitch}, r: {roll}, y: {yaw}".format(**accel_only)) 
    print 'stopped continous self.sensehat scan' 
      