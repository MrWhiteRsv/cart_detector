from colors import Colors
import unicornhat as unicorn

def init():
    unicorn.set_layout(unicorn.AUTO)
    unicorn.rotation(0)
    unicorn.brightness(0.5)
    
def clear():
  for row in range(8):
    for col in range(4):
      set_pixel(row, col, Colors.BLACK)
  unicorn.show()
  
def show_counter_0(val):
  # print 'monitor half revolution:', counter
  set_pixel(0, 0, Colors.BLACK if val & 1 == 0 else Colors.RED)
  set_pixel(0, 1, Colors.BLACK if val & 2 == 0 else Colors.RED)
  set_pixel(1, 0, Colors.BLACK if val & 4 == 0 else Colors.RED)
  set_pixel(1, 1, Colors.BLACK if val & 8 == 0 else Colors.RED)
  set_pixel(2, 0, Colors.BLACK if val & 16 == 0 else Colors.RED)
  set_pixel(2, 1, Colors.BLACK if val & 32 == 0 else Colors.RED)
  unicorn.show()
  
def show_counter_1(val):
  # print 'monitor half revolution:', counter
  set_pixel(0, 2, Colors.BLACK if val & 1 == 0 else Colors.GREEN)
  set_pixel(0, 3, Colors.BLACK if val & 2 == 0 else Colors.GREEN)
  set_pixel(1, 2, Colors.BLACK if val & 4 == 0 else Colors.GREEN)
  set_pixel(1, 3, Colors.BLACK if val & 8 == 0 else Colors.GREEN)
  set_pixel(2, 2, Colors.BLACK if val & 16 == 0 else Colors.GREEN)
  set_pixel(2, 3, Colors.BLACK if val & 32 == 0 else Colors.GREEN)
  unicorn.show()
  
def show_beacon_on(color):
  for row in range(3, 5):
    for col in range(0, 4):
      set_pixel(row, col, color)
  unicorn.show()
  
def show_beacon_off():
  for row in range(3, 4):
    for col in range(0, 3):
      set_pixel(row, col, Colors.BLACK)
  unicorn.show()
  
def show_quality(color):
  for row in range(5, 8):
    col = 3
    set_pixel(row, col, color)
  unicorn.show()  

def clear_direction():
  for row in range(5, 8):
    for col in range(0, 3):
      set_pixel(row, col, Colors.BLACK)
  unicorn.show()
  
def clear_direction_stop():
  for row in range(5, 8):
    for col in range(0, 3):
      set_pixel(row, col, Colors.RED)
  unicorn.show()
      
def show_show_arrow_right():
  color = Colors.YELLOW
  clear_direction()
  set_pixel(6, 0, color)
  set_pixel(6, 1, color)
  set_pixel(6, 2, color)
  set_pixel(7, 1, color)
  unicorn.show()
  
def show_show_arrow_left():
  color = Colors.YELLOW
  clear_direction()
  set_pixel(6, 0, color)
  set_pixel(6, 1, color)
  set_pixel(6, 2, color)
  set_pixel(5, 1, color)
  unicorn.show()
  
def show_show_arrow_top():
  color = Colors.YELLOW
  clear_direction()
  set_pixel(5, 1, color)
  set_pixel(6, 1, color)
  set_pixel(7, 1, color)
  set_pixel(6, 0, color)
  unicorn.show()
  
def show_show_arrow_bottom():
  color = Colors.YELLOW
  clear_direction()
  set_pixel(5, 1, color)
  set_pixel(6, 1, color)
  set_pixel(7, 1, color)
  set_pixel(6, 2, color)
  unicorn.show()
""" internals """   
def set_pixel(row, col, rgb_color):
  unicorn.set_pixel(row, col,
      rgb_color.value[0], rgb_color.value[1], rgb_color.value[2])
    
""" Deprecated """
"""
class Monitor():
  
  def __init__(self):
    unicorn.set_layout(unicorn.AUTO)
    unicorn.rotation(0)
    unicorn.brightness(0.5)
     
  def set_pixel(self, row, col, color):
     (r, g, b) = self.rgb_of_color(color);
     unicorn.set_pixel(row, 3 - col, r, g, b)
     
  def notify_beacon(self, color):
    for row in range(0, 2):
      for col in range(0, 4):
        self.set_pixel(row, col, color)
    unicorn.show()
    
  def notify_turn(self, counter):
    # print 'monitor half revolution:', counter
    self.set_pixel(2, 0, 'black' if counter & 1 == 0 else 'yellow')
    self.set_pixel(3, 0, 'black' if counter & 2 == 0 else 'yellow')
    self.set_pixel(2, 1, 'black' if counter & 4 == 0 else 'yellow')
    self.set_pixel(3, 1, 'black' if counter & 8 == 0 else 'yellow')
    self.set_pixel(2, 2, 'black' if counter & 16 == 0 else 'yellow')
    self.set_pixel(3, 2, 'black' if counter & 32 == 0 else 'yellow')
    self.set_pixel(2, 3, 'black' if counter & 64 == 0 else 'yellow')
    self.set_pixel(3, 3, 'black' if counter & 128 == 0 else 'yellow')
    unicorn.show()
    
#  "" " Internals. "" "
  def set_pixel(self, row, col, color):
     (r, g, b) = self.rgb_of_color(color);
     unicorn.set_pixel(row, 3 - col, r, g, b)
     
  #deprecated
  def rgb_of_color(self, color):
    return {
        'red': (200, 30, 30),
        'green': (30, 200, 30),
        'blue': (30, 30, 200),
        'black': (0, 0, 0),
        'yellow': (255, 255, 80),
        'purple': (128,0,128),
    }.get(color, (255, 255, 255))
"""