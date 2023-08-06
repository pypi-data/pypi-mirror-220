import time
import datetime, calendar
import re

class sTime:
    def __init__(self, srctime=None):
        self.datetime = srctime

    def __call__(self, srctime):
        self.datetime = srctime
        return self

    def fromstr(self, timestr, format="%Y-%m-%d"):
        self.datetime = datetime.datetime.strptime(timestr, format)
        return self

    def tostr(self, format="%Y-%m-%d"):
        return self.datetime.strftime(format)

    def last_month(self, objday=1):
        self.datetime = (self.datetime.replace(day=1) - datetime.timedelta(days=1)).replace(day=objday)
        return self

    def next_month(self, objday=1):
        week, days_num = calendar.monthrange(self.datetime.year, self.datetime.month)
        self.datetime = (self.datetime.replace(day=days_num) + datetime.timedelta(days=1)).replace(day=objday)
        return self

    def next_day(self):
        self.datetime = self.datetime + datetime.timedelta(days=1)
        return self

    def last_day(self):
        self.datetime = self.datetime - datetime.timedelta(days=1)
        return self


def timestamp2timestr(timeStamp, format="%Y-%m-%d %H:%M:%S", isMicroSecond=True, isUtc=False):
    time_function = time.gmtime if isUtc else time.localtime
    return time.strftime(format, time_function(timeStamp / (1000 if isMicroSecond else 1)))


def timestr2timestamp(timestr, format="%Y-%m-%d %H:%M:%S", isMicroSecond=True):
    timeArray = time.strptime(timestr, format)
    return int(time.mktime(timeArray)) * (1000 if isMicroSecond else 1)

def auto_parse_time_with_datefmt(timestr, datefmt):
    pattern = datefmt.replace("%Y", "(\d{4})")\
                    .replace("%j", "([0-2][0-9]{2}|3[0-5][0-9]|36[0-6])")\
                    .replace("%m", "(0[1-9]|1[0-2])")\
                    .replace("%d", "(0[1-9]|[1-2][0-9]|3[0-1])")\
                    .replace("%H", "(0[0-9]|1[0-9]|2[0-3])")\
                    .replace("%M", "([0-5][0-9])")\
                    .replace("%S", "([0-5][0-9])")
    pattern = f"{pattern}"
    match = re.findall("(%[YjHMSmd])", datefmt)
    if match is None:
        return []
    datefmt_new = "".join(match) if match else ""
    match = re.findall(pattern, timestr)
    datestr_new = ["".join(i) for i in match] if match else []
    return [datetime.datetime.strptime(i, datefmt_new) for i in datestr_new]

st = sTime()

if __name__ == '__main__':
    timestr = r"MCD19A2.A2019267.h28v05.006.2019269040927.hdf"
    datefmt = "%Y%j"
    print(auto_parse_time_with_datefmt(timestr, datefmt))