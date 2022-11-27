import time

from .DataStructures import Route
from .GISGrabber import GISGrabber
from copy import deepcopy
import queue


# this is a class designed to wrap all the things needed to describe a completed map that is ready to be used
class CombinedMap:
    # init
    # if an area code is given, use that
    # use coordinates if no area code and coordinates are given
    # otherwise assume OSM file already exists
    def __init__(self, directional, fileName=None, aid=None, l=None, b=None, r=None, t=None):
        grabber = GISGrabber()
        if not (aid is None):
            print("getting by area ID...")
            self.roadMap = grabber.getAreaByID(aid)
        elif not (l is None or b is None or r is None or t is None):
            print("getting by bounds...")
            self.roadMap = grabber.getArea(l, b, r, t)
        elif not (fileName is None):
            print("getting by file...")
            self.roadMap = grabber.readFile(fileName)
        else:
            raise Exception("Not valid data!")

        self.roadGraph = grabber.toGraph(self.roadMap, directional)
        self.directional = directional

    # this is to create a new "refined" (i.e. narrowed down to specific road types/surfaces) class
    def refine(self, allowedTypes, allowedSurfaces):
        grabber = GISGrabber()
        rc = deepcopy(self)
        rc.roadMap = grabber.getPaths(rc.roadMap, allowedTypes, allowedSurfaces)
        rc.roadGraph = grabber.toGraph(rc.roadMap, rc.directional)

        return rc

    # makes a route based on a set of points
    def makeRoute(self, ids):
        # need more than one point to make a valid route
        if len(ids) < 2:
            raise Exception("Path needs more than 1 point!")

        for i in ids:
            if not (i in self.roadGraph.idToNum):
                raise Exception("Invalid ID in route node list!")

        # various helper variables for BFS and backtracking
        route = []
        length = 0
        l = [0 for i in range(len(self.roadGraph.adj))]
        vis = [False for i in range(len(self.roadGraph.adj))]
        parent = [None for i in range(len(self.roadGraph.adj))]
        q = queue.Queue()

        # current start/end (for each section between 2 points)
        cs = self.roadGraph.idToNum[ids[0]]
        ce = self.roadGraph.idToNum[ids[1]]
        vis[cs] = True
        q.put(cs)
        route.append(self.roadGraph.numToID[cs])

        for sec in range(1, len(ids)):
            while not q.empty():
                cur = q.get()
                for i in self.roadGraph.adj[cur].keys():
                    if (not (i in route)) and ((not vis[i]) or l[i] > l[cur] + self.roadGraph.adj[cur][i][0]):
                        parent[i] = cur
                        l[i] = l[cur] + self.roadGraph.adj[cur][i][0]
                        vis[i] = True
                        q.put(i)

            # update to total length
            length += l[ce]

            # backtracking
            curRoute = []
            curN = ce
            while curN != cs:
                curRoute.insert(0, self.roadGraph.numToID[curN])
                curN = parent[curN]
            route = route + curRoute

            l = [0 for i in range(len(self.roadGraph.adj))]
            vis = [False for i in range(len(self.roadGraph.adj))]
            parent = [None for i in range(len(self.roadGraph.adj))]

            cs = ce
            ce = self.roadGraph.idToNum[ids[sec]]
            vis[cs] = True
            q.put(cs)

        return Route(route, length)
