import json
import threading
import time
import utils

# from sense_hat import SenseHat

from py_beacon.proximity import *

class BleScanner:
  logger = None
  worker = None
        
  def create_beacon_state(self):
    time_sec = time.time()
    res = dict()
    res['near_beacon'] = False
    res['start_ts'] = time_sec
    res['nearest_ts'] = time_sec
    res['end_ts'] = time_sec
    res['nearest_rssi'] = -200
    return res
  
  def start_continous_scan(self):
    print 'starting continous ble scan'
    supermetric_beacons = {}
    #supermetric_beacons['34:b1:f7:d3:9e:2b'] = self.create_beacon_state()
    #supermetric_beacons['34:b1:f7:d3:91:f8'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:90:9f'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9d:a3'] = self.create_beacon_state()
    scanner = Scanner()
  #  sense = SenseHat()
    while True:
      if (not getattr(self.worker, "do_run", True)):
        break
      for beacon in scanner.scan():
        fields = beacon.split(",")
        mac = fields[0]

        #print 'mac: ', mac
          
        if mac in supermetric_beacons:
          time_sec = time.time()
          rssi = int(fields[5])
          self.logger.log_ble_raw(mac, time_sec, rssi)
          
          if rssi > supermetric_beacons[mac]['nearest_rssi']:
            supermetric_beacons[mac]['nearest_ts'] = time_sec
            supermetric_beacons[mac]['nearest_rssi'] = rssi 
          supermetric_beacons[mac]['end_ts'] = time_sec
          gotCloseToBeacon = (rssi > -63 and not supermetric_beacons[mac]['near_beacon'] == True)
          gotAwayFromBeacon = (rssi < -72 and not supermetric_beacons[mac]['near_beacon'] == False)
          if gotCloseToBeacon or gotAwayFromBeacon:
            supermetric_beacons[mac]['end_ts'] = time_sec
            if gotCloseToBeacon:
              # sense.show_message("Hot")
              print 'got close to beacon: ', mac, ' at time:' , time_sec
              supermetric_beacons[mac]['near_beacon'] = True
            if gotAwayFromBeacon:
              # sense.show_message("Cold")
              self.logger.log_ble_event(mac,
                  supermetric_beacons[mac]['start_ts'],
                  supermetric_beacons[mac]['end_ts'],
                  supermetric_beacons[mac]['nearest_ts'],
                  supermetric_beacons[mac]['nearest_rssi'])
              print 'got away from beacon: ', mac, ' at time: ' , time_sec
              supermetric_beacons[mac]['near_beacon'] = False
            supermetric_beacons[mac]['start_ts'] = time_sec
            supermetric_beacons[mac]['nearest_ts'] = time_sec
            supermetric_beacons[mac]['nearest_rssi'] = rssi 
    print 'stopped continous ble scan' 

  def start(self, logger):
    self.logger = logger
    self.worker = threading.Thread(target = self.start_continous_scan)
    self.worker.do_run = True
    self.worker.start()

  def stop(self):
    self.logger = None
    self.worker.do_run = False
    


  
  


