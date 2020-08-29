from api.config import string_high_time, string_low_time
from date.dateHandler import dateHandler
from database.database import database

dateHandler = dateHandler()

class calculation():

    def __init__(self):
        self.database = database()
        self.first_run_consumption_counter = 0
        self.current_state_production = 0
        self.current_solar_production = 0
        self.last_consumption = []
        self.solar_power_provided_to_state = 0
        self.state_consumption = 0
        self.solar_consumption = 0

    def sortData(self, household_consumption, households, date, time):
        #time period for ht & nt
        low_time = dateHandler.convertStringToTime(string_low_time)
        high_time = dateHandler.convertStringToTime(string_high_time)

        #produced solar power
        solar_production = household_consumption['Produktionsmessung']

        #produced power
        state_production = household_consumption['Bidirektional']

        #calling function to calculate solar & state power consumption
        self.sortConsumptionType(solar_production, state_production, self.last_consumption['Produktionsmessung'], self.last_consumption['Bidirektional'], household_consumption)


        if self.first_run_consumption_counter == 0:
            #prevents error on first run of application sets consumption to zero
            self.sortDataFirstCalculation(household_consumption, households, date, time)
            self.first_run_consumption_counter = 1
        else:
            for device in households:
                self.state_consumption = household_consumption[device] - self.current_solar_production
                self.solar_consumption = self.current_solar_production
                

                
    
    def sortDataFirstCalculation(self, household_consumption, households, date, time):
        #always low time consumption and will be consumption zero to avoid exception
        for device in households:
            self.last_consumption.append(household_consumption[device])
            self.current_consumption = household_consumption[device] - household_consumption[device]
            #fill database with consumption data
            self.database.fillDatabaseConsumptionLowTime(self.current_solar_production, self.current_state_production, device, date, time)

    def sortConsumptionType(self, solar_production, state_production, last_solar_production, last_state_production, households):
        #calculate current 5 minute production of solar, state
        calculated_solar_consumption = solar_production - last_solar_production
        calculated_state_consumption = state_production - last_state_production

        if calculated_solar_consumption > calculated_state_consumption:
            self.solar_power_provided_to_state = calculated_solar_consumption - calculated_state_consumption
            self.current_solar_production = calculated_solar_consumption / len(households)
        else:
            self.current_solar_production = calculated_solar_consumption / len(households)
            
              

        
        

