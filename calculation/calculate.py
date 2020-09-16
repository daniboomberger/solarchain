from api.config import string_high_time, string_low_time
from date.dateHandler import dateHandler
from database.database import database

dateHandler = dateHandler()

'''
    TODO: fill last_solar_energy, apartment_count
'''

class calculation():

    def __init__(self):
        #consumption of apartment (five min)

        #consumtion of solar power
        self.solar_consumption = ''

        #consumption of state power
        self.state_consumption = ''

        #apartment = device (to know for database) 
        self.apartment = ''

        #datetime to save for database
        self.datetime = ''

        #street name for database
        self.street = ''

        #HT or NT time
        self.timezone_consumption = 0

        #consumption price calculated with factors (time zone (HT or NT), solar or state)
        self.counter = 0

        #value to calculate five min consumption (old value)
        self.last_total_consumption = {}

        #solar energy produced of last five min
        self.last_total_solar_energy = ''

        #apartment counter
        self.apartment_count = 0

        #spare solar produced energy 
        self.spare_solar_production = 0

        #this is the magical dictionary for all the information needed in the invoice (apartment {solar_consumption, solar_price, state_consumption, state_price, high_tariff, low_tariff})
        self.all_informations = {}

    '''
        params: household_consumption => dict {apartments: consumption}
                devices => list (all apartments)
                date => datetime (current time of json)
                time => time (to check wether it's HT or NT)
                street_name => street name (name of the house)
    '''    
    def sortData(self, household_consumption, devices,date, time, street_name):
        self.datetime = date
        self.street = street_name
        self.apartment_count = len(devices) - 1

        #string to time (to check NT and HT)
        NT_time = dateHandler.convertStringToTime(string_low_time)
        HT_time = dateHandler.convertStringToTime(string_high_time)

        #check if time is in NT zone {22:00:00 - 06:00:00} or HT Zone {06:00:00 - 22:00:00}
        if NT_time <= time >= HT_time: 
            self.timezone_consumption = 0 #HT    
        else: 
            self.timezone_consumption = 1 #NT
        
        for apartment in devices:
            self.apartment = apartment
            if self.counter == 0:
                self.solar_consumption, self.state_consumption,self.last_total_consumption, self.last_total_solar_energy = 0, 0, household_consumption[apartment], household_consumption['Produktionsmessung']
            else:
                self.solar_consumption = round(self.calculatedSolarConsumptionPerApartment(household_consumption['Produktionsmessung']), 2)
                self.state_consumption = round(self.calculateConsumption(household_consumption[apartment], self.last_total_consumption[apartment]) - self.solar_consumption, 2) #calculates state consumption (total_consumption - solar_consumption)
                #print(f'{date} ------------ {str(apartment)} ---------------- {self.solar_consumption} ------------ {self.state_consumption}')
                if self.solar_consumption != 0:
                    print(f'solar -> {self.solar_consumption}')
                    print(f'state -> {self.state_consumption}')
                    print(f'total -> {round(self.solar_consumption + self.state_consumption, 2)}')
        
        self.last_total_solar_energy = household_consumption['Produktionsmessung']
        self.last_total_consumption = household_consumption
        self.counter = 1
        

    def calculateConsumption(self, total_consumption, last_total_consumption):
        return float(total_consumption) - float(last_total_consumption) #returns five minute consumption value
    
    def calculatedSolarConsumptionPerApartment(self, solar_energy):
        #print(self.last_total_solar_energy)
        return (float(solar_energy) - float(self.last_total_solar_energy)) / float(self.apartment_count) #returns consumed solar per apartment 
              

        
        

