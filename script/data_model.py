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
    pays: str
    nom: str
    WebURL: str

    def __init__(self, pays, nom, webURL):
        self.pays = pays
        self.nom = nom
        self.webURL = webURL

    def _getName(self):
        return self.nom

    def _getWebURL(self):
        return self.webURL
