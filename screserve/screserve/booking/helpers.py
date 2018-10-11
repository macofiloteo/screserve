import datetime

def RegularOrExcursion(bookingTime):
   startExcursionTime = datetime.time(7,30,0)
   endExcursionTime = datetime.time(12,30,0)
   return (startExcursionTime < bookingTime and endExcursionTime > bookingTime) 