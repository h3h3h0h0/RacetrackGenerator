from tmapgen.CombinedMap import CombinedMap

test1 = CombinedMap(url="https://api.openstreetmap.org/",
                    l=-80.6249862,
                    b=43.4262852,
                    r=-80.4128576,
                    t=43.4856153,
                    fileName="test1",
                    directional=True)

#all typical roads plus on/off ramps
types = ["motorway", "trunk", "primary", "secondary", "tertiary", "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"]
#on regular paved roads only
surfaces = ["paved", "asphalt", "chipseal", "concrete"]

test1Refined = test1.refine(types, surfaces)

