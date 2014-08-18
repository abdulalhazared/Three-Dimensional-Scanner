import sys
import os
import datetime
  
class Logger():
  def __init__(self,data="",filename="log.txt", destinationFolder=".",size="",status=""):
    ###today = datetime.date.today()
    
    
     
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")   
   
    #data = str(data) + ";"# + now # + "\r\n"
    data = str(data)# + "\n"
    
    if (os.path.isfile(destinationFolder + "/"+ filename)):      
      #print "File " + filename+ " already esists, appending to existing file."
      fh = open(destinationFolder+"/"+filename , "a")            
      #fh.write(str(now) + "\r\n" + "\r\n")
      fh.write(data + "\n")
      fh.close()
    else:		                
      #print "File " + filename+ " created."
      fh = open(destinationFolder+"/"+filename , "wb")
      fh.write(data + "\n")
      fh.close()
      
#Logger()
#Logger("frieocmfgoriej", "log2.txt")