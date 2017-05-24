import cv2
import numpy as np

class ImageComperator:

  def compare(self, img0_name, img1_name):
    img0 = cv2.imread(img0_name)
    img1 = cv2.imread(img1_name)
    height, width = img0.shape[:2]
    orb = cv2.ORB_create()
    kp0, des0 = orb.detectAndCompute(img0, None)
    kp1, des1 = orb.detectAndCompute(img1, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des0, des1) # query,train
    matches = sorted(matches, key = lambda x:x.distance)  
    res = self.create_blank(2 * width, height, (255, 0, 0))
    res[0:height, 0:width] = img0[0:height, 0:width]
    res[0:height, width:(2 * width)] = img1[0:height, 0:width]

    #print matches[:10]
    for match in matches[:10]:
      #print match.trainIdx
      #print match.queryIdx
      #print kp0[match.queryIdx].pt
      
      center0 = tuple(map((lambda x:  int(x)), kp0[match.queryIdx].pt))
      center1 = tuple(map((lambda x:  int(x)), kp1[match.trainIdx].pt))
      center1 = (center1[0] + width, center1[1])
      cv2.circle(res, center=center0, radius=5, color=(128, 0, 0), thickness=2)
      cv2.circle(res, center=center1, radius=5, color=(128, 0, 0), thickness=2)
      cv2.line(res, center0, center1, color=(128, 0, 0))
    cv2.imwrite('test.png', res)
    
    print(self.compare_impl(img0, img1))


  def compare_impl(self, img0, img1):
    orb = cv2.ORB_create()
    kp0, des0 = orb.detectAndCompute(img0, None)
    kp1, des1 = orb.detectAndCompute(img1, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    all_matches = bf.match(des0, des1) # query,train
    all_matches = sorted(all_matches, key = lambda x : x.distance)
    all_dist = list(map(lambda x :  x.distance, all_matches))
    all_dist = all_dist[1 : 10] # throw smallest value
    return sum(all_dist)/float(len(all_dist))
  
  
  def proccess_img(self, img):
    orb = cv2.ORB_create()
    kp = orb.detect(img, None)
    kp, des = orb.compute(img, kp)
    #img_with_features = img.copy()
    #cv2.drawKeypoints(img, kp, img_with_features, color=(255,0,0), flags=0)
    #cv2.imwrite('test.png', img_with_features)
  
  def create_blank(self, width, height, rgb_color):
    img = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    img[:] = color
    return img