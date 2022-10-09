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