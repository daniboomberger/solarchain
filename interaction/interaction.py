from date.dateHandler import dateHandler

class interaction():

    def userInteraction(self, start_date, end_date, street_Name):
        start_date = input('Enter the starting Date(2020-01-01 00:00:00): ')
        end_date = input('Enter the starting Date(2020-01-01 00:00:00): ')
        street_Name = input('Enter the street name: ')
        start_date, end_date = dateHandler().convertDate(start_date, end_date) 
        return start_date, end_date, street_Name