import random
from tulip import tlp

graph = tlp.newGraph()
size = 100
viewLayout = graph.getLayoutProperty("viewLayout")

# for n in graph.getNodes():
#     x = random.random() * size
#     y = random.random() * size
    
#     viewLayout[n] = tlp.Coord(x, y, 0)

# for i in range(1, 10):
#     node = tlp.node()
#     graph.addNode(node)

# get the input property from which to generate the partition
myMetric = graph.getDoubleProperty("myMetric")

# get a dictionary filled with default parameters for the algorithm
params = tlp.getDefaultPluginParameters("Equal Value", graph)

# set the input property
params["property"] = myMetric

# if you want to partition edges instead of nodes
# params["Type"] = "edges"

# if you want connected subgraphs
# params["Connected"] = True

# now we call the algorithm
graph.applyAlgorithm("Equal Value", params)

params = tlp.getDefaultPluginParameters('SVG Export', graph)
outputFile = "test.svg"
success = tlp.exportGraph('SVG Export', graph, outputFile, params)

