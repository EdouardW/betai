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
    def play_sql(cls, request):
        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(user=PG_USER,
                                          password=PG_PASSWORD,
                                          host=PG_HOST,
                                          port=PG_PORT,
                                          database=PG_DATABASE)

            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(request)
            result = [r[0] for r in cursor.fetchall()]

            return result

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    
    @classmethod
    def mapping_name_sql(cls, nom_entree):
        connection = None
        cursor = None
        request = "select lfp from public.mapping_name where datacouk = '{}'".format(nom_entree)

        try:
            connection = psycopg2.connect(user=PG_USER,
                                          password=PG_PASSWORD,
                                          host=PG_HOST,
                                          port=PG_PORT,
                                          database=PG_DATABASE)

            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(request)
            result = [r[0] for r in cursor.fetchall()]

            return result

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    @classmethod
    def get_classement_and_forme_sql(cls, team, saison, journee):
        connection = None
        cursor = None
        if "'" in team:
            str_split = team.split("'")
            team = "{}\\'{}".format(str_split[0], str_split[1])

        request = "SELECT classement, forme_win, forme_draw, forme_lose, points, gagnes, nuls, perdus, buts, contre FROM public.classement_ligue1 where equipe = E'{}' AND saison = '{}' AND journee = '{}'".format(team, saison, str(journee))

        try:
            connection = psycopg2.connect(user=PG_USER,
                                          password=PG_PASSWORD,
                                          host=PG_HOST,
                                          port=PG_PORT,
                                          database=PG_DATABASE)

            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(request)
            result = cursor.fetchall()[0]

            return result

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()