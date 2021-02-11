#!/usr/bin/env python

class Team:
    name: str
    WebURL: str

    def __init__(self, name, webURL):
        self.name = name
        self.webURL = webURL

    def getName(self):
        return self.name

    def getWebURL(self):
        return self.webURL


class Championnat:
    pays: str
    name: str
    WebURL: str

    def __init__(self, pays, name, webURL):
        self.pays = pays
        self.name = name
        self.webURL = webURL

    def _getName(self):
        return self.name

    def _getWebURL(self):
        return self.webURL
