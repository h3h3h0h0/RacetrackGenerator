import current as current

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
        #need more than one point to make a valid route
        if len(ids) < 2:
            raise Exception("Path needs more than 1 point!")

        #various helper variables for BFS and backtracking
        route = []
        length = 0
        l = [0 for i in range(len(self.roadGraph.adj))]
        vis = [False for i in range(len(self.roadGraph.adj))]
        parent = [None for i in range(len(self.roadGraph.adj))]
        q = queue.Queue()

        #current start/end (for each section between 2 points)
        cs = self.roadGraph.idToNum[ids[0]]
        ce = self.roadGraph.idToNum[ids[1]]
        vis[cs] = True
        q.put(cs)

        for sec in range(1, len(self.roadGraph.adj)):
            while not q.empty():
                cur = q.get()
                for i in self.roadGraph.adj[cur].keys():
                    if (not i in route) and ((not vis[i]) or l[i] > l[cur]+self.roadGraph.adj[cur][i][0]):
                        parent[i] = cur
                        l[i] = l[cur]+self.roadGraph.adj[cur][i][0]
                        vis[i] = True
                        q.put(i)

            length += l[ce]
            curRoute = []
            curN = ce
            while True:
                curRoute.insert(0, curN)


