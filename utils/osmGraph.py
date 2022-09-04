import networkx as nx
import osmnx as ox
import os
import plotly.graph_objects as go
import numpy as np
import plotly


class OsmGraph:

    def __init__(self, g):
        self.graph = g
        self.nodesGdf, self.edgesGdf = self.graphToGdfs()

    def saveHmlTo(self, filename):
        ox.io.save_graphml(self.graph, filepath=filename)

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
    
    def getNearestNode(self, x, y):
        return ox.distance.nearest_nodes(self.graph, y, x, return_dist=True)
    
    def shortestPath(self, origin, destination):
        return ox.distance.shortest_path(self.graph, origin, destination, weight='length')
    
    def calculateLengthOf(path): #TODO
        pass

    @staticmethod
    def plotData(pointDict, colorList,filename):
        '''
        pointDict: {"label": list of points}
        '''
        i = 0
        for label in pointDict:
            lat, long = zip(*pointDict[label])
            # adding the lines joining the nodes
            if i == 0:
                fig = go.Figure(go.Scattermapbox(
                    name = label,
                    mode="markers",
                    lon=long,
                    lat=lat,
                    marker={'size': 15, 'color': colorList[i]}))
                
            else:
                fig.add_trace(go.Scattermapbox(
                    name= label,
                    mode="markers",
                    lon=long,
                    lat=lat,
                    marker={'size': 15, 'color': colorList[i]},))
            i += 1
        # getting center for plots:
        lat_center = np.mean(lat)
        long_center = np.mean(long)
        # defining the layout using mapbox_style
        fig.update_layout(mapbox_style="stamen-terrain",
                          mapbox_center_lat=30, mapbox_center_lon=-80)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          mapbox={
                              'center': {'lat': lat_center,
                                         'lon': long_center},
                              'zoom': 9.5})
        plotly.offline.plot(fig, filename=filename, auto_open=False)


class GraphFromHmlFile(OsmGraph):
    def __init__(self, hmlAddress):
        self.graph = ox.io.load_graphml(hmlAddress)
        self.nodesGdf, self.edgesGdf = self.graphToGdfs()


class GraphFromBbox(OsmGraph):
    def __init__(self, boundingBox):
        self.graph = ox.graph_from_polygon(boundingBox.polygon(), network_type='drive')
        self.nodesGdf, self.edgesGdf = self.graphToGdfs()


class GraphFromGdfs(OsmGraph):
    def __init__(self, nodes, edges):
        self.graph = ox.utils_graph.graph_from_gdfs(nodes, edges)
        self.nodesGdf, self.edgesGdf = nodes, edges
        
class GraphFromPlace(OsmGraph):
    def __init__(self, placeQuery):
        self.graph = ox.graph_from_place(placeQuery, network_type='drive')
        self.nodesGdf, self.edgesGdf = self.graphToGdfs()
