import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tmapgen.CombinedMap import CombinedMap
from OSMPythonTools.nominatim import Nominatim

test1 = CombinedMap(l=-80.582056, b=43.454726, r=-80.513735, t=43.486805,
                    directional=False)

#all typical roads plus on/off ramps
types = ["motorway", "trunk", "primary", "secondary", "tertiary", "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"]
#on regular paved roads only
surfaces = ["paved", "asphalt", "chipseal", "concrete"]

test1Refined = test1.refine(types, surfaces)

print(str(test1Refined.roadMap.roadWays.keys()))
print(str(test1Refined.roadGraph.idToNum))
print(str(test1Refined.makeRoute([10093608747, 310722370]).ids))