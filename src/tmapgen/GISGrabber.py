from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim
from .OSMHandler import OSMHandler
from geographiclib.geodesic import Geodesic
from .DataStructures import RoadMap, RoadGraph, NodeData, RoadData


#this uses HTTP requests to get GIS data from OpenStreetMap
class GISGrabber:

    #the URL is so that this may work with different versions of the map, and not just the current version
    def __init__(self):
        self.op = Overpass()
        self.handler = OSMHandler()

    #get the map info for the area bounded by the specific coordinates, stores it in a file with the specified name
    def getArea(self, l, b, r, t):
        print("getArea running...")

        bbox = [b, l, t, r]

        query = overpassQueryBuilder(bbox=bbox, elementType='way', selector="highway", includeGeometry=True, out='body')
        data = self.op.query(query, timeout=1000)

        print("Main download finished!")

        return self.processOPData(data, bbox=bbox)

    def getAreaByID(self, aid):
        print("getAreaByID running...")


        query = overpassQueryBuilder(area=aid, elementType='way', selector="highway", includeGeometry=True, out='body')
        data = self.op.query(query, timeout=1000)

        print("Main download finished!")

        return self.processOPData(data, area=aid)

    def processOPData(self, data, bbox=None, area=None):
        roadNodes = {}
        roadWays = {}

        counter = 0

        nquery = None
        if not bbox is None:
            nquery = overpassQueryBuilder(bbox=bbox, elementType='node', out='body')
        elif not area is None:
            nquery = overpassQueryBuilder(area=area, elementType='node', out='body')
        ndata = self.op.query(nquery, timeout=1000)

        for w in data.ways():
            counter += 1
            print("processing highway:", w.id(), "processed:", counter, "out of", len(data.ways()), "|", len(w.nodes()), "nodes")

            wayID = w.id()
            roadType = w.tag("highway")
            surface = ""
            # surface data is sometimes inconsistent, so we need this if statement
            if "surface" in w.tags():
                surface = w.tag("surface")
            nodes = []

            idList = []
            nInfoDict = {}
            for n in w.nodes():
                idList.append(n.id())
                nInfoDict[n.id()] = None

            for n in ndata.nodes():
                if n.id() in idList:
                    nInfoDict[n.id()] = [n.lat(), n.lon()]

            # for each node, add the corresponding data to the nodes dictionary, and adds the ID to the array for that way
            for i in idList:
                if not nInfoDict[i] is None:
                    nodeID = i
                    nodeLat = nInfoDict[i][0]
                    nodeLon = nInfoDict[i][1]

                    nodes.append(nodeID)
                    roadNodes[nodeID] = NodeData(nodeLat, nodeLon)

            roadWays[wayID] = RoadData(roadType, surface, nodes)

        return RoadMap(roadNodes, roadWays)

    def readFile(self, fileName):
        self.handler.apply_file(str(fileName + ".osm"))
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
