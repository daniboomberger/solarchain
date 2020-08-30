from database.database import database
from date.dateHandler import dateHandler
from api.apiHandler import apiHandler
from interaction.interaction import interaction
from api.apiDataHandler import apiDataHandler
from calculation.calculate import calculation
import datetime

#initializing used classes
db = database()
dateHandler = dateHandler()
apiHandler = apiHandler()
interaction = interaction()
apiDataHandler = apiDataHandler()
calculation = calculation()

#date variables
start_datetime = ""
end_datetime = ""
string_date = ""
string_datetime = ""
last_datetime = ""
time = ""

#stree variable
street_name = ""

#api Data list
data = []

if __name__ == "__main__":
    #Connection to database
    db.connect()

    #user interaction (return => start, end, street)
    start_datetime, end_datetime, street_name = interaction.userInteraction(start_datetime, end_datetime, street_name)
    while(start_datetime <= end_datetime):
        #convert date to string
        string_date, string_datetime = dateHandler.convertDateToString(start_datetime)
        if last_datetime != string_date:
            #get API data (return => solar data as json)       
            data = apiHandler.createTargetUrl(string_date,street_name)
            last_datetime = string_date
            apiDataHandler.handleDevices(data)
        
        #fill list household_consumption for each apartments consumption value
        household_consumption, devices = apiDataHandler.handleConsumption(data, string_datetime)
        time = start_datetime.time()

        #fill data into database sorted in (categories => HT, NT, Solar, EWZ)
        calculation.sortData(household_consumption, devices, start_datetime, time, street_name)
        start_datetime = start_datetime + datetime.timedelta(minutes=5)