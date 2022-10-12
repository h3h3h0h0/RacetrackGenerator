#each road contains the type and surface of road (useful for making racetracks for different types of vehicles)
#also contains the nodes that describe the road's shape in order
class RoadData:
    def __init__(self, roadType, surface, nodes):
        self.roadType = roadType
        self.surface = surface
        self.nodes = nodes

#each node only contains the latitude and longitude, since there is VERY inconsistent height data in OSM
class NodeData:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

#a wrapper for the two dictionaries that describe the nodes and ways in roads
class RoadMap:
    def __init__(self, roadNodes, roadWays):
        self.roadNodes = roadNodes
        self.roadWays = roadWays

#a graph that describes road data, with distance and azimuth between the road nodes
class RoadGraph:
    def __init__(self, nodes):
        #converts node IDs to consecutive numbers and vice-versa for ease of implementation
        self.idToNum = {}
        self.numToID = {}
        nc = 0
        for nid in nodes.keys():
            self.idToNum[nid] = nc
            self.numToID[nc] = nid
            nc += 1

        #the adjacency list (we will have to run various algorithms on this graph later)
        self.adj = [{} for i in range(nc)]

    #adds edge by node ID
    #parentID is to get the ID of the parent road, for road conditions info
    def addEdgeByID(self, id1, id2, dist, azi, parentID):
        self.addEdge(self.idToNum[id1], self.idToNum[id2]. dist, azi, parentID)

    def addEdge(self, a, b, dist, azi, parentID):
        t = [dist, azi, parentID]
        self.adj[a][b] = t
