#!/usr/bin/env python

class Team:
    name: str
    WebUrl: str

    def __init__(self, name, webURL):
        self.name = name
        self.webURL = webURL

    def getName(self):
        return self.name

    def getWebURL(self):
        return self.webURL


class Championnat:
    name: str
    WebUrl: str

    def __init__(self, name, webURL):
        self.name = name
        self.webURL = webURL

    def getName(self):
        return self.name

    def getWebURL(self):
        return self.webURL
