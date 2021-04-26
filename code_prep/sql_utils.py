import psycopg2
import psycopg2.extras


PG_HOST = 'localhost'
PG_DATABASE = 'postgres'
PG_USER = 'postgres'
PG_PASSWORD = 'dodu'
PG_PORT = '5432'

class SQLUtil():

    def __init__(self):
        self.cursor = None
        self.connection = None
        try:
            self.connection = psycopg2.connect(user=PG_USER,
                                          password=PG_PASSWORD,
                                          host=PG_HOST,
                                          port=PG_PORT,
                                          database=PG_DATABASE)

            self.cursor = self.connection.cursor()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
    
    def _run_request(self, step_name, list_request):
        for request in list_request:
            try:
                self.cursor.execute(request)

            except (Exception, psycopg2.Error) as error:
                print(f"Error while {step_name} ", error)

        self.connection.commit()

    def create_table(self):
        list_request = []
        request = """
            CREATE TABLE IF NOT EXISTS ligue1.sas_global_match 
               (saison VARCHAR(20),
                ligue VARCHAR(20),
                journee INT, 
                date DATE,
                id_match VARCHAR(20),
                result VARCHAR(5),
                hometeam VARCHAR(50),
                awayteam VARCHAR(50),
                home_score VARCHAR(50),
                away_score VARCHAR(50),
                date_scrap TIMESTAMP
                )"""
        list_request.append(request)
        self._run_request('creating table: global match:', list_request)

    def import_json(self, data_list):
        list_request = []
        print('IMPORT JSON')
        print(data_list)
        print('---')
        request = """
            INSERT into ligue1.sas_global_match 
            VALUES
            (%(saison)s,
            %(ligue)s,
            %(journee)s,
            %(date)s,
            %(id_match)s,
            %(result)s,
            %(hometeam)s,
            %(awayteam)s,
            %(home_score)s,
            %(away_score)s,
            %(date_scrap)s); """

        try:
            self.cursor.execute(request, data_list)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            print(f"Error while IMPORT JSON'", error)

        


    def close(self):
        self.cursor.close()
        self.connection.close()    
    


    @classmethod
    def play_sql_journee(cls, liste):
        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(user=PG_USER,
                                          password=PG_PASSWORD,
                                          host=PG_HOST,
                                          port=PG_PORT,
                                          database=PG_DATABASE)

            cursor = connection.cursor()

            cursor.execute("INSERT into public.journee_ligue1(saison, ligue, journee, date, home_team, home_score, away_score, away_team, resultat, date_ajout) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [x for x in liste])
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()