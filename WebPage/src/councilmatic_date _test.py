
import datetime
from councilmatic_date import councilmatic_date

for m in range(1,31):
    adate = datetime.datetime(2019, 7, m, 0, 0)
    timestamp = councilmatic_date(adate)
    print (adate.strftime('%d'), adate.strftime('%A'),"Text that will be written out -->", timestamp)
#





