import osmium as osm

from DataStructures import NodeData, RoadData, RoadMap

class OSMHandler(osm.SimpleHandler):
    #the regular init function for osmium, with 2 dictionaries for road nodes and road ways
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.roadNodes = {}
        self.roadWays = {}

    #this handler only really processes ways, and gets road nodes from the data in each way
    def way(self, o):
        #puts it in only if the way is considered some kind of road
        #note that due to how dictionaries work, it doesn't need to check for repeat entries
        if "highway" in o.tags:
            wayID = o.id
            roadType = o.tags.get("highway")
            surface = ""
            #surface data is sometimes inconsistent, so we need this if statement
            if "surface" in o.tags:
                surface = o.tags.get("surface")
            nodes = []

            #for each node, add the corresponding data to the nodes dictionary, and adds the ID to the array for that way
            for n in o.nodes:
                nodeID = n.id
                nodeLat = n.location.lat
                nodeLon = n.location.lon

                nodes.append(nodeID)
                self.roadNodes[nodeID] = NodeData(nodeLat, nodeLon)

            self.roadWays[wayID] = RoadData(roadType, surface, nodes)

    def exportData(self):
        return RoadMap(self.roadNodes, self.roadWays)