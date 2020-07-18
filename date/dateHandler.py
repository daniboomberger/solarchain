from datetime import datetime

class dateHandler():
    
    def convertDate(self, startDate, endDate):
        startDate = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S")
        endDate = datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S")
        return startDate, endDate

    def convertDateToString(self, date):
        string_date = datetime.strftime(date, "%Y-%m-%d")
        string_datetime = datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
        return string_date, string_datetime
    
    def convertStringToTime(self, timestamp):
        time = datetime.strptime(timestamp, "%H:%M:%S").time()
        return time
    
