import sys
import os
import datetime

from visual import *
from random import *

scene2 = display(title='Rendering points to 3d Space',
     x=0, y=0, width=800, height=600,
     center=(400,300,0) )

f = frame() #creates a new frame to work with
  
class PointReader():
  def __init__(self,inlineData="",filename="collision.log", sourceFolder=".",size="",status=""):
    
    if (os.path.isfile(sourceFolder + "/"+ filename)):      
      #print "File " + filename+ " already esists, appending to existing file."
      fh = open(sourceFolder+"/"+filename , "r")

      data = fh.readline()
      
      while (data):
        data = fh.readline()
        #print data
        
        if len(data)>1: 
          index, point = data.split(" ")
          #x,y = point.strip("[")
          
          
          #point = point.strip("[")
          
          point = "".join(list(point)[1:-2])
          
          x, y = point.split(",")
          #point = point.strip("[").strip("]")
          #print type(point)
          print x, y 
          
          sphere(frame=f, pos=vector(int(x),int(y),0), radius=5, color=color.white)
          #print a.strip("]")
        
      fh.close()



#r = PointReader()