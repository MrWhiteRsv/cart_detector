""" This program is responsible on checking the monitor functionality. """ 

import getopt
import sys
import time

import src.utils.monitor
import src.utils.monitor
from src.utils.colors import Colors
monitor = src.utils.monitor

def main(argv):
 
  monitor.init()
  monitor.clear()
  monitor.show_beacon_on(Colors.PURPLE)
  monitor.show_quality(Colors.YELLOW)
  monitor.show_arrow_bottom()
  for val in range(64):
    monitor.show_counter_0(val)
    monitor.show_counter_1(val / 2)
    time.sleep(0.1)
  time.sleep(5)
  

if __name__ == '__main__':
  main(sys.argv[1:])
