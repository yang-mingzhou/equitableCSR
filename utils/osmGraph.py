import networkx as nx
import osmnx as ox
import os


class OsmGraph:

    def __init__(self, g):
        self.graph = g
        self.nodesGdf, self.edgesGdf = self.graphToGdfs()

    def saveHmlTo(self, folderAddress):
        ox.save_graphml(self.graph, filepath=os.path.join(folderAddress, 'osmGraph.graphml'))

    def graphToGdfs(self):
        nodes, edges = ox.graph_to_gdfs(self.graph, nodes=True, edges=True)
        if "u" not in edges.columns:
            edges = edges.reset_index()
        return nodes, edges

    def getEdges(self):
        _, edges = self.graphToGdfs()
        return edges

    def getEdgesDict(self):
        _, edges = self.graphToGdfs()
        return edges.to_dict('index')


class GraphFromHmlFile(OsmGraph):
    def __init__(self, hmlAddress):
        self.graph = ox.load_graphml(hmlAddress)
        self.nodesGdf, self.edgesGdf = self.graphToGdfs()


class GraphFromBbox(OsmGraph):
    def __init__(self, boundingBox):
        self.graph = ox.graph_from_polygon(boundingBox.polygon(), network_type='drive')
        self.nodesGdf, self.edgesGdf = self.graphToGdfs()


class GraphFromGdfs(OsmGraph):
    def __init__(self, nodes, edges):
        self.graph = ox.utils_graph.graph_from_gdfs(nodes, edges)
        self.nodesGdf, self.edgesGdf = nodes, edges