from api.config import string_low_time, string_high_time
from date.dateHandler import dateHandler

dateHandler = dateHandler()

class calculation():

    def __init__(self):
        self.consumption = 0
        self.last_consumption = 0

    def sortData(self, household_consumption, households, date, time):
        #time period for ht & nt
        low_time = dateHandler.convertStringToTime(string_low_time)
        high_time = dateHandler.convertStringToTime(string_high_time)

        #produced solar power
        solar_production = household_consumption['Produktionsmessung']

        for device in households:
            self.last_consumption = household_consumption[device]
