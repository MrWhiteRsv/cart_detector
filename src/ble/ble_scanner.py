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
  map_mac_to_nearest_rssi = None
  map_mac_to_away_rssi = None
        
  def create_beacon_state(self):
    time_sec = time.time()
    res = dict()
    res['near_beacon'] = False
    res['start_ts'] = time_sec
    res['nearest_ts'] = time_sec
    res['end_ts'] = time_sec
    res['nearest_rssi'] = -200
    return res
    
  def init_thresholds(self):
    all_macs = ['34:b1:f7:d3:90:ff', '34:b1:f7:d3:9c:cb', '34:b1:f7:d3:9d:2f',
        '34:b1:f7:d3:9e:41', '34:b1:f7:d3:9c:a3','34:b1:f7:d3:9d:f6']
    self.map_mac_to_nearest_rssi = dict()
    self.map_mac_to_away_rssi = dict()
    for mac in all_macs:
      self.set_mac_thrsholds(mac, -47, 54)
  
  def set_mac_thrsholds(self, mac, nearest_rssi, away_rssi):
    self.map_mac_to_nearest_rssi[mac] = nearest_rssi
    self.map_mac_to_away_rssi[mac] = away_rssi
  
  def color_of_mac(self, mac):
    return {
        '34:b1:f7:d3:90:ff' : Colors.RED,
        '34:b1:f7:d3:9c:cb' : Colors.GREEN,
        '34:b1:f7:d3:9d:2f' : Colors.BLUE,
        '34:b1:f7:d3:9e:41' : Colors.YELLOW,
        '34:b1:f7:d3:9c:a3' : Colors.PURPLE,
        '34:b1:f7:d3:9d:f6' : Colors.ORANGE,
    }.get(mac, (255, 255, 255))

  def start_continous_scan(self):
    # print 'starting continous ble scan'
    supermetric_beacons = {}
    supermetric_beacons['34:b1:f7:d3:90:ff'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9c:cb'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9d:2f'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9e:41'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9c:a3'] = self.create_beacon_state()
    supermetric_beacons['34:b1:f7:d3:9d:f6'] = self.create_beacon_state()
    scanner = Scanner()

# 34:b1:f7:d3:9e:41
# 34:b1:f7:d3:92:3f
# 34:b1:f7:d3:91:55

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
          
          # print (rssi, self.map_mac_to_nearest_rssi[mac], self.map_mac_to_away_rssi[mac])
          
          self.logger.log_ble_raw(mac, time_sec, rssi)
          if rssi > supermetric_beacons[mac]['nearest_rssi']:
            supermetric_beacons[mac]['nearest_ts'] = time_sec
            supermetric_beacons[mac]['nearest_rssi'] = rssi 
          supermetric_beacons[mac]['end_ts'] = time_sec
          gotCloseToBeacon = (rssi > self.map_mac_to_nearest_rssi[mac] and not
              supermetric_beacons[mac]['near_beacon'] == True)
          gotAwayFromBeacon = (rssi < self.map_mac_to_away_rssi[mac] and not
             supermetric_beacons[mac]['near_beacon'] == False)
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
    self.init_thresholds();
    self.worker = threading.Thread(target = self.start_continous_scan)
    self.worker.do_run = True
    self.worker.start()

  def stop(self):
    self.logger = None
    self.worker.do_run = False
    


  
  


