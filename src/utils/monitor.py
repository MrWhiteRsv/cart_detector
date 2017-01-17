import unicornhat as unicorn

class Monitor():
  
  def __init__(self):
    unicorn.set_layout(unicorn.AUTO)
    unicorn.rotation(0)
    unicorn.brightness(0.5)
     
  def rgb_of_color(self, color):
    return {
        'red': (200, 30, 30),
        'green': (30, 200, 30),
        'blue': (30, 30, 200),
        'black': (0, 0, 0),
        'yellow': (255, 255, 80),
        'purple': (128,0,128),
    }.get(color, (255, 255, 255))
    
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