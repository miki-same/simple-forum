#翌日0:00のtimestampを返す

import datetime

def next_day():
  dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
  dty,dtm,dtd=dt_now.year,dt_now.month,dt_now.day
  dt_jst = datetime.datetime(dty,dtm, dtd,tzinfo=datetime.timezone(datetime.timedelta(hours=9)))+datetime.timedelta(days=1)
  return dt_jst.timestamp()