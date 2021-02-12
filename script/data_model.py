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


class Championnat:
    id_pays: int
    nom_pays: str
    id_championnat: int
    nom_championnat: str
    WebURL: str

    def __init__(self, id_pays, nom_pays, id_championnat, nom_championnat, webURL):
        self.id_pays = id_pays
        self.nom_pays = nom_pays
        self.id_championnat = id_championnat
        self.nom_championnat = nom_championnat
        self.webURL = webURL

    def _getName(self):
        return self.nom

    def _getWebURL(self):
        return self.webURL
