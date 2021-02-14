#!/usr/bin/env python

class Club:
    nom: str
    WebURL: str

    def __init__(self, nom, webURL):
        self.name = nom
        self.webURL = webURL

    def _getName(self):
        return self.nom

    def _getWebURL(self):
        return self.webURL


class Pays:
    id_pays: int
    nom_pays: str

class Championnat:
    id_pays: int
    nom_pays: str
    id_championnat: int
    nom_championnat: str
    WebURL: str

    def __init__(self, id_pays='null', nom_pays='null', id_championnat='null', nom_championnat='null', webURL='null'):
        self.id_pays = id_pays
        self.nom_pays = nom_pays
        self.id_championnat = id_championnat
        self.nom_championnat = nom_championnat
        self.webURL = webURL

    def _getName(self):
        return self.nom

    def _getWebURL(self):
        return self.webURL
