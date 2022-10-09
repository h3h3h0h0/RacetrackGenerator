import requests

from DataStructures import NodeData, RoadData, RoadMap

#this uses HTTP requests to get GIS data from OpenStreetMap
class GISGrabber:

    #the URL is so that this may work with different versions of the map, and not just the current version
    def __init__(self, url, handler):
        self.url = url
        self.handler = handler

    #get the map info for the area bounded by the specific coordinates, stores it in a file with the specified name
    def getArea(self, l, b, r, t, fileName):
        fullURL = self.url + "/api/0.6/map?bbox=" + str(l) + "," + str(b) + "," + str(r) + "," + str(t)
        rawAnswer = requests.get(fullURL)

        status = rawAnswer.status_code
        if status == 400:
            raise Exception("Bad Request! (Error 400)")
        elif status == 509:
            raise Exception("Bandwidth Limit Exceeded! (Error 509)")
        else:
            f = open((fileName + ".osm"), "w")
            f.write(rawAnswer.text)
            f.close()

    def readFile(self, fileName):
        self.handler.apply_file(fileName + ".osm")
        return self.handler.exportData()

    #extracts only suitable roadway data from raw data
    def getPaths(self, raw, allowedTypes, allowedSurfaces):
        finNodes = {}
        finWays = {}

        #if some road matches conditions, it is added to finWays and its nodes are added to finNodes
        for rid in raw.roadWays.keys():
            if raw.roadWays[rid].roadType in allowedTypes and raw.roadWays[rid].surface in allowedSurfaces:
                finWays[rid] = raw.roadWays[rid]
                for nid in raw.roadWays[rid].nodes:
                    finNodes[nid] = raw.roadNodes[nid]

        return RoadMap(finNodes, finWays)


