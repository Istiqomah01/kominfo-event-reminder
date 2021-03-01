import pytz
from datetime import datetime, timedelta

WIB = pytz.timezone('Asia/Jakarta')
one_day = timedelta(days=1)

tomorrow = datetime.now(tz = WIB) + one_day

print(datetime.now(tz = WIB))
print((datetime.now(tz = WIB) + one_day).day)