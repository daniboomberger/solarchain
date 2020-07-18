from configparser import ConfigParser
import psycopg2

class database():
    def config(self, filename="database/config.ini", section="postgresql"):
        
        parser = ConfigParser()
        parser.read(filename)

        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def connect(self):
        try:
            params = self.config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            print('PostgreSQL database version:')
            cursor.execute('SELECT version()')
            db_version = cursor.fetchone()
            print(db_version)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
