from api.config import string_high_time, string_low_time
from date.dateHandler import dateHandler
from database.database import database

dateHandler = dateHandler()

class calculation():

    def __init__(self):
        self.database = database()
        self.first_run_consumption_counter = 0
        self.current_state_consumption = 0
        self.current_solar_consumption
        self.last_consumption = []

    def sortData(self, household_consumption, households, date, time):
        #time period for ht & nt
        low_time = dateHandler.convertStringToTime(string_low_time)
        high_time = dateHandler.convertStringToTime(string_high_time)

        #produced solar power
        solar_production = household_consumption['Produktionsmessung']

        #produced power
        state_production = household_consumption['Bidirektional']

        if self.first_run_consumption_counter == 0: 
            self.sortDataFirstCalculation(household_consumption, households, date, time)
            self.first_run_consumption_counter = 1
        else:
            for device in households:
                self.current_consumption = household_consumption[device] - self.last_consumption[device]
                self.last_consumption = household_consumption[device]
                if low_time < time > high_time:
                    self.database.fillDatabaseConsumptionHighTime(self.current_consumption, device, date, time)
                else:
                    self.database.fillDatabaseConsumptionLowTime(self.current_consumption, device, date, time)

                
    
    def sortDataFirstCalculation(self, household_consumption, households, date, time):
        #always low time consumption and will be consumption zero to avoid exception
        for device in households:
            self.last_consumption.append(household_consumption[device])
            self.current_consumption = household_consumption[device] - household_consumption[device]
            #fill database with consumption data
            self.database.fillDatabaseConsumptionLowTime(self.current_consumption, device, date, time)
    
    def sortPowerType(self, solar_production, state_production, last_solar_production, last_state_production):
        current_solar_production = solar_production - last_solar_production
        current_state_production = state_production - last_state_production

            

        
        

