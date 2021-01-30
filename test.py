import datetime
import schedule
import time

def testing():
    print(datetime.datetime.now())

schedule.every(10).seconds.do(testing)

while True:
    schedule.run_pending()
    time.sleep(1)