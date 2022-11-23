import requests
import OSMHandler
from geographiclib.geodesic import Geodesic
from DataStructures import RoadMap, RoadGraph

#this uses HTTP requests to get GIS data from OpenStreetMap
class GISGrabber:

    #the URL is so that this may work with different versions of the map, and not just the current version
    def __init__(self, url):
        self.url = url
        self.handler = OSMHandler()

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

    #transform a roadmap object into a data structure that describes a graph with these roads
    #has a choice to respect original road direction or not
    def toGraph(self, rMap, directional=False):
        rNodes = rMap.roadNodes
        rWays = rMap.roadWays

        finGraph = RoadGraph(rNodes)

        #for each way, add the connection between adjacent nodes with appropriate info
        for wid in rWays.keys():
            tn = rWays[wid].nodes
            for i in range(len(tn)-1):
                lat1 = rNodes[tn[i]].lat
                lat2 = rNodes[tn[i+1]].lat
                lon1 = rNodes[tn[i]].lon
                lon2 = rNodes[tn[i+1]].lon
                dist = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)["s12"]
                az1 = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)["azi1"]
                az2 = Geodesic.WGS84.Inverse(lat2, lon2, lat1, lon1)["azi1"]
                finGraph.addEdgeByID(tn[i], tn[i+1], dist, az1, wid)
                if not directional:
                    finGraph.addEdgeByID(tn[i+1], tn[i], dist, az2, wid)

        return finGraph
