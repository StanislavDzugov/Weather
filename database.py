import psycopg2


class DatabaseConnection:
    def __init__(self, dbname, user, host, port, password, new_data=None):
        self.new_data = new_data
        try:
            self.connection = psycopg2.connect(
                f'dbname={dbname} user={user} host={host} password={password} port={port}'
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print('Connected')
        except Exception:
            print('Cannot connect to database')

    def create_table(self):
        create_table_command = 'CREATE TABLE weather(' \
                               'id serial PRIMARY KEY,' \
                               'weather varchar(100),' \
                               'temperature varchar(10),' \
                               'date DATE)'
        self.cursor.execute(create_table_command)

    def insert_new_data(self):
        new_dates = []
        self.cursor.execute('SELECT date FROM weather ORDER BY date DESC LIMIT 1')
        date = self.cursor.fetchall()
        for day in self.new_data:
            if not day['date'] > date[0][0]:
                insert_command = 'INSERT INTO weather (weather, temperature, date) VALUES (%s, %s, %s)'
                self.cursor.execute(insert_command, (day['weather'], day['temperature'], day['date']))

