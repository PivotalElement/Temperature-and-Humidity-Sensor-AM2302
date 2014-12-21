#!/usr/bin/env python

import MySQLdb as mdb
import sys
import time
import Adafruit_DHT

# CLASSES 
# MySQLdataMngr deals with the interactions with the MySQL database
#  - init() connects to a database and throws an error if that does not work
#  - addData() writes data in MySQL database

class MySQLdataMngr():
  def __init__(self, userID, password, database):
    try:
      self.DBcon = mdb.connect('localhost', userID, password, database)
      self.cur = self.DBcon.cursor()
    except mdb.Error, e:
      print "Error %d: %s" % (e.args[0],e.args[1])
      sys.exit(1)
   
  def addData(self, dataBaseTable, values):
    fooVal = ",".join(values)
    foo = " ".join(["INSERT INTO ", dataBaseTable, "VALUES (", fooVal, ")"])
    with self.DBcon:
      self.cur.execute(foo)
      
# FUNCTIONS
# function getAM2302 gets the humidity and temperature data from the sensor and provides them with a timestamp 
#   - returns both readings with one decimal place (conform with the format in the MySQL table)

def getAM2302():
  humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302,4)
  return (time.time(), int(temperature*10)/10., int(humidity*10)/10.)

# Main Routine
def main():
  # connect to the MySQL database 
  # - replace yourID, yourPassword and yourDataBase with the values that apply to you
  dataBase = MySQLdataMngr(userID = 'yourID', password = 'yourPassword', database = 'yourDataBase')
  
  # start measuring
  while True: 
    # keep data for the last two hours in memory
    timeStamp, temp, hum = getAM2302()
    dataBase.addData("yourTable", (str(timeStamp), str(temp), str(hum)))
    time.sleep(60)

if __name__ == "__main__":
  main()
