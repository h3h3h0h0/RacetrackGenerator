import OSMHandler
import GISGrabber
from copy import deepcopy
import queue

#this is a class designed to wrap all the things needed to describe a completed map that is ready to be used
class CombinedMap:
    #init from coordinates
    def __init__(self, url, l, b, r, t, fileName, directional):
        grabber = GISGrabber(url)
        grabber.getArea(l, b, r, t, fileName)

        self.roadMap = grabber.readFile(fileName)
        self.roadGraph = grabber.toGraph(self.roadMap, directional)
        self.directional = directional

    #this is to create a new "refined" (i.e. narrowed down to specific road types/surfaces) class
    def refine(self, allowedTypes, allowedSurfaces):
        rc = deepcopy(self)
        rc.roadMap = GISGrabber.getPaths(rc.roadMap, allowedTypes, allowedSurfaces)
        rc.roadGraph = GISGrabber.toGraph(rc.roadMap, rc.directional)

        return rc

    #makes a route based on a set of points
    def makeRoute(self, ids):
        route = []
        length = 0
        l = [0 for i in range(len(self.roadGraph.adj))]
        vis = [False for i in range(len(self.roadGraph.adj))]
        q = queue.Queue()

