import datetime

def RegularOrExcursion(bookingTime):
   startExcursionTime = datetime.time(6,59,0)
   endExcursionTime = datetime.time(12,1,0)
   return (startExcursionTime < bookingTime and endExcursionTime > bookingTime) 
