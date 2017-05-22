import json
import threading
import sys
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

from src.utils.colors import Colors

class ImageScanner:
  logger = None
  worker = None
  camera = None
  name = "pic"
  picture_counter = 0
  controller = None
  
  def start_continous_scan(self):
    while True:
      if (getattr(self.worker, "do_run", True)):
    	self.snap()
      time.sleep(1)

  def start(self):
    self.worker.do_run = True

  def stop(self):
    self.worker.do_run = False
    
  def snap(self):
    rawCapture = PiRGBArray(self.camera)
    self.camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    image_name = self.name + '_' + str(self.picture_counter) + '.png'
    cv2.imwrite(self.name + '_' + str(self.picture_counter) + '.png', image)
    self.controller.publish_log('took image ' + image_name)
    self.picture_counter += 1
    
  def init(self, logger, name, controller):
    self.logger  = logger
    self.camera = PiCamera()
    # allow the camera to warmup
    time.sleep(0.1)
    picture_counter = 0
    self.worker = threading.Thread(target = self.start_continous_scan)
    self.worker.do_run = False
    self.worker.start()
    self.name = name
    self.controller = controller
    
  def set_name(self, name):
    self.name = name

  