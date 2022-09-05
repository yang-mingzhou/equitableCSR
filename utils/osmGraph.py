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
        return nodes, edges
    
    def plot(self):
        ox.plot.plot_graph(self.graph)
        return

    def getEdges(self):
        _, edges = self.graphToGdfs()
        return edges

    def getNearestNode(self, x, y):
        return ox.distance.nearest_nodes(self.graph, y, x, return_dist=True)
    
    def shortestPath(self, origin, destination):
        return ox.distance.shortest_path(self.graph, origin, destination, weight='length')
    
    
    def calPathLength(self, nodeList):
        result = 0
        for i in range(len(nodeList)-1):
            edgeLength = self.edgesGdf.loc[(nodeList[i], nodeList[i+1], 0), 'length']
            result += edgeLength
        return result
    
    def nodeList2GPSTraj(self, nodeList):
        '''
        traj: [[lat, lon]]
        '''
        traj = []
        for i in range(len(nodeList)-1):
            e = self.edgesGdf.loc[(nodeList[i], nodeList[i+1], 0)]
            if 'geometry' in e:
                xs, ys = e['geometry'].xy
                z = list(zip(xs, ys))
                l1 = list(list(zip(*z))[0])
                l2 = list(list(zip(*z))[1])
                for k in range(len(l1)):
                    traj.append([l2[k], l1[k]])
        return traj
    
    @staticmethod
    def __initGoFigure(lat, long, type='markers', label='default', size=5, color='red'):
        '''
        type = 'markers' or 'lines'
        lat/long: list, if 'type == lines'; float, else
        '''
        fig = go.Figure(go.Scattermapbox(
                    name=label,
                    mode=type,
                    lon=long,
                    lat=lat,
                    marker={'size': size, 'color': color}))
        return fig
    
    @staticmethod
    def __addTrace(fig, lat, long, type='markers', label='default', size=5, color='red'):
        fig.add_trace(go.Scattermapbox(
                    name=label,
                    mode=type,
                    lon=long,
                    lat=lat,
                    marker={'size': size, 'color': color}))
        return fig
    
    @staticmethod
    def __plotFigAndSave(fig, lat_center, long_center, filename):
        fig.update_layout(mapbox_style="stamen-terrain",
                          mapbox_center_lat=30, mapbox_center_lon=-80)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          mapbox={
                              'center': {'lat': lat_center,
                                         'lon': long_center},
                              'zoom': 9.5})
        plotly.offline.plot(fig, filename=filename, auto_open=False)
        return
         
    @staticmethod
    def plotTrajList(trajList, filename):
        '''
        trajList: [traj]
        '''
        i = 0
        for traj in trajList:
            lat, long = zip(*traj)
            # adding the lines joining the nodes
            if i == 0:
                fig = OsmGraph.__initGoFigure(lat, long, type='lines', label='traj'+str(i))
                
            else:
                fig = OsmGraph.__addTrace(fig, lat, long, type='lines', label='traj'+str(i))
            i += 1
        # getting center for plots:
        lat_center = np.mean(lat)
        long_center = np.mean(long)
        OsmGraph.__plotFigAndSave(fig, lat_center, long_center, filename)
        
    @staticmethod
    def plotPointList(pointDict, colorList,filename):
        '''
        pointDict: {"label": list of points}
        '''
        i = 0
        for label in pointDict:
            lat, long = zip(*pointDict[label])
            # adding the lines joining the nodes
            if i == 0:
                fig = OsmGraph.__initGoFigure(lat, long, type='markers', label= label, size=15, color=colorList[i])
                
            else:
                fig = OsmGraph.__addTrace(fig, lat, long, type='markers', label= label, size=15, color=colorList[i])
            i += 1
        # getting center for plots:
        lat_center = np.mean(lat)
        long_center = np.mean(long)
        OsmGraph.__plotFigAndSave(fig, lat_center, long_center, filename)
        
    @staticmethod
    def plotTrajAndPoint(trajList, pointDict, colorList, filename):
        '''
        trajList: [traj]
        pointDict: {"label": list of points}
        '''
        i = 0
        for traj in trajList:
            lat, long = zip(*traj)
            # adding the lines joining the nodes
            if i == 0:
                fig = OsmGraph.__initGoFigure(lat, long, type='lines', label='path'+str(i))
                
            else:
                fig = OsmGraph.__addTrace(fig, lat, long, type='lines', label='path'+str(i))
            i += 1
        i = 0
        for label in pointDict:
            lat, long = zip(*pointDict[label])
            fig = OsmGraph.__addTrace(fig, lat, long, type='markers', label= label, size=15, color=colorList[i])
            i += 1
        # getting center for plots:
        lat_center = np.mean(lat)
        long_center = np.mean(long)
        OsmGraph.__plotFigAndSave(fig, lat_center, long_center, filename)


    

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
        # e.g.: GraphFromPlace("Minnesota, USA")
        self.graph = ox.graph_from_place(placeQuery, network_type='drive')
        self.nodesGdf, self.edgesGdf = self.graphToGdfs()
