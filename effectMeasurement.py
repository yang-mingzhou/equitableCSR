from utils.dataloader import StationData
from utils.osmGraph import GraphFromHmlFile
import os

dataFolder = "./data"
stationFileName = "stationData_MN.csv"
stationData = StationData(os.path.join(dataFolder, stationFileName), download = True)

graphFileName = "hennepinCounty.graphml"
graph = GraphFromHmlFile(os.path.join(dataFolder, graphFileName))
print(len(graph.edgesGdf))