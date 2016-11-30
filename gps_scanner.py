from gps3 import gps3

import time
import threading

import utils
    
class GpsScanner:
 
  worker = None
  logger = None
  
  repeated_timer_inst = None
  recent_scan_time_utc_sec = None
  recent_lat = None
  recent_lon = None
  
  def open(self):
    self.repeated_timer_inst = utils.RepeatedTimer(5, self.log_scan)
    self.worker = threading.Thread(target = self.start_continous_scan)
    self.worker.do_run = True
    self.worker.start()

  def start(self, logger):
    self.logger = logger
    self.repeated_timer_inst.start()
  
  def stop(self):
    self.logger = None
    self.repeated_timer_inst.stop()
    
  def close(self):
    self.stop()
    self.worker.do_run = False
    self.worker.join()

  def log_scan(self):
    print 'log_gps_event'
    self.logger.log_gps_event(self.recent_scan_time_utc_sec,
        self.recent_lat, self.recent_lon)
    
  def start_continous_scan(self):
    print 'starting continous gps scan' 
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()
    for new_data in gps_socket:
      if (not getattr(self.worker, "do_run", True)) :
        break;
      if new_data:
        data_stream.unpack(new_data)
        lat = data_stream.TPV['lat']
        lon = data_stream.TPV['lon']
        if (utils.is_number(lat) and utils.is_number(lon)):
          self.recent_lat = lat
          self.recent_lon = lon
          self.recent_scan_time_utc_sec = time.time()
          print('gps  ', lat, ', ', lon)
        else:
          print 'bad scan'
          # print(data_stream.TPV) 
    print 'stopped continous gps scan'   


      

