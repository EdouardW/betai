#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras

PG_HOST = 'localhost'
PG_DATABASE = 'betai'
PG_USER = 'postgres'
PG_PASSWORD = 'dodu'
PG_PORT = '5432'


class SQLUtil():

    @classmethod
    def play_sql(cls, liste):
        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(user=PG_USER,
                                          password=PG_PASSWORD,
                                          host=PG_HOST,
                                          port=PG_PORT,
                                          database=PG_DATABASE)

            cursor = connection.cursor()

            for clubs in liste:
                cursor.execute("INSERT into public.clubs(nom_datacouk) VALUES (%s)", [clubs])
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

