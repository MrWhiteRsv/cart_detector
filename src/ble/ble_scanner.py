import json
import threading
import sys
import time

import src.utils.monitor
from py_beacon.proximity import *
from src.utils.colors import Colors

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
  
  def color_of_mac(self, mac):
    return {
        '34:b1:f7:d3:90:ff' : Colors.RED, # 34:b1:f7:d3:91:f8
        '34:b1:f7:d3:9c:cb' : Colors.GREEN,
        '34:b1:f7:d3:9d:2f' : Colors.BLUE, #34:b1:f7:d3:9e:2b
        '34:b1:f7:d3:9d:eb' : Colors.YELLOW,
        '34:b1:f7:d3:9c:a3' : Colors.PURPLE, # '34:b1:f7:d3:90:d9'
        '34:b1:f7:d3:9d:f6' : Colors.ORANGE,
    }.get(mac, (255, 255, 255))

  def start_continous_scan(self):
    # print 'starting continous ble scan'
    supermetric_beacons = {}
    supermetric_beacons['34:b1:f7:d3:90:ff'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9c:cb'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9d:2f'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9d:eb'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9c:a3'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9d:f6'] = self.create_beacon_state()
    scanner = Scanner()

    while True:
      if (not getattr(self.worker, "do_run", True)):
        break
      for beacon in scanner.scan():
        fields = beacon.split(",")
        mac = fields[0]
        # print ('ble, mac: ', mac, ', rssi: ', int(fields[5]))
        if mac in supermetric_beacons:
          time_sec = time.time()
          rssi = int(fields[5])
          self.logger.log_ble_raw(mac, time_sec, rssi)
          if rssi > supermetric_beacons[mac]['nearest_rssi']:
            supermetric_beacons[mac]['nearest_ts'] = time_sec
            supermetric_beacons[mac]['nearest_rssi'] = rssi 
          supermetric_beacons[mac]['end_ts'] = time_sec
          gotCloseToBeacon = (rssi > -48 and not supermetric_beacons[mac]['near_beacon'] == True)
          gotAwayFromBeacon = (rssi < -53 and not supermetric_beacons[mac]['near_beacon'] == False)
          if gotCloseToBeacon or gotAwayFromBeacon:
            supermetric_beacons[mac]['end_ts'] = time_sec
            if gotCloseToBeacon:
              # print ('got close to beacon: ', mac, ' at time:' , time_sec)
              # self.monitor.notify_beacon(self.color_of_mac(mac))
              src.utils.monitor.show_beacon_on(self.color_of_mac(mac))
              supermetric_beacons[mac]['near_beacon'] = True
            if gotAwayFromBeacon:
              self.logger.log_ble_event(mac,
                  supermetric_beacons[mac]['start_ts'],
                  supermetric_beacons[mac]['end_ts'],
                  supermetric_beacons[mac]['nearest_ts'],
                  supermetric_beacons[mac]['nearest_rssi'])
              # print ('got away from beacon: ', mac, ' at time: ' , time_sec)
              src.utils.monitor.show_beacon_off()
              supermetric_beacons[mac]['near_beacon'] = False
            supermetric_beacons[mac]['start_ts'] = time_sec
            supermetric_beacons[mac]['nearest_ts'] = time_sec
            supermetric_beacons[mac]['nearest_rssi'] = rssi 

  def start(self, logger):
    self.logger = logger
    self.worker = threading.Thread(target = self.start_continous_scan)
    self.worker.do_run = True
    self.worker.start()

  def stop(self):
    self.logger = None
    self.worker.do_run = False
    


  
  


