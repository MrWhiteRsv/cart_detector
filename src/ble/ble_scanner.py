import json
import threading
import sys
import time

from py_beacon.proximity import *

class BleScanner:
  logger = None
  monitor = None
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
  
  def color_of_mac(self, mac):
    return {
        '34:b1:f7:d3:91:c8' : 'red',
        '34:b1:f7:d3:9c:cb' : 'green',
        '34:b1:f7:d3:91:e4' : 'blue',
        '34:b1:f7:d3:9d:eb' : 'yellow',
        '34:b1:f7:d3:90:8e' : 'purple',
    }.get(mac, (255, 255, 255))
    
  def start_continous_scan(self):
    # print 'starting continous ble scan'
    supermetric_beacons = {}
    supermetric_beacons['34:b1:f7:d3:91:c8'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9c:cb'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:91:e4'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9d:eb'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:90:8e'] = self.create_beacon_state()
    scanner = Scanner()

    while True:
      if (not getattr(self.worker, "do_run", True)):
        break
      for beacon in scanner.scan():
        fields = beacon.split(",")
        mac = fields[0]   
        if mac in supermetric_beacons:
          time_sec = time.time()
          rssi = int(fields[5])
          # print ('JJJ ble, mac: ', mac, ', rssi: ', rssi)
          sys.stdout.flush()
          self.logger.log_ble_raw(mac, time_sec, rssi)
          if rssi > supermetric_beacons[mac]['nearest_rssi']:
            supermetric_beacons[mac]['nearest_ts'] = time_sec
            supermetric_beacons[mac]['nearest_rssi'] = rssi 
          supermetric_beacons[mac]['end_ts'] = time_sec
          gotCloseToBeacon = (rssi > -67 and not supermetric_beacons[mac]['near_beacon'] == True)
          gotAwayFromBeacon = (rssi < -78 and not supermetric_beacons[mac]['near_beacon'] == False)
          if gotCloseToBeacon or gotAwayFromBeacon:
            supermetric_beacons[mac]['end_ts'] = time_sec
            if gotCloseToBeacon:
              # print 'got close to beacon: ', mac, ' at time:' , time_sec
              self.monitor.notify_beacon(self.color_of_mac(mac))
              supermetric_beacons[mac]['near_beacon'] = True
            if gotAwayFromBeacon:
              self.logger.log_ble_event(mac,
                  supermetric_beacons[mac]['start_ts'],
                  supermetric_beacons[mac]['end_ts'],
                  supermetric_beacons[mac]['nearest_ts'],
                  supermetric_beacons[mac]['nearest_rssi'])
              # print 'got away from beacon: ', mac, ' at time: ' , time_sec
              self.monitor.notify_beacon('black')
              supermetric_beacons[mac]['near_beacon'] = False
            supermetric_beacons[mac]['start_ts'] = time_sec
            supermetric_beacons[mac]['nearest_ts'] = time_sec
            supermetric_beacons[mac]['nearest_rssi'] = rssi 

  def start(self, logger, monitor):
    self.logger = logger
    self.monitor = monitor
    self.worker = threading.Thread(target = self.start_continous_scan)
    self.worker.do_run = True
    self.worker.start()

  def stop(self):
    self.logger = None
    self.worker.do_run = False
    


  
  


