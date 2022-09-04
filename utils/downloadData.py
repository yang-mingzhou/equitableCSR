from apiKeys import NRELapi,Censusapi
import requests
import pandas as pd
import io
import osmnx as ox

if __name__ == '__main__':
    
    def getRequest(url, query):
        return requests.get(url, params= query)
    
    class downloadStationData:

        # API description: https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/all/
        stationQuery = {'format':'csv',
                        'api_key':NRELapi.getKey(),
                        'status':'E', 
                        'access':'public',
                        'fuel_type':'ELEC',
                        'ev_charging_level':'1, 2, dc_fast',
                        'state':'MN',
                        'zip':'55455,55454',
                        'limit':'20'}
        stationUrl = 'https://developer.nrel.gov/api/alt-fuel-stations/v1'
        stationData = getRequest(stationUrl, stationQuery).text

        stationDF = pd.read_csv(io.StringIO(stationData))
        
        def stationDFProcessing(df):
            df[["EV Level1 EVSE Num", "EV Level2 EVSE Num", "EV DC Fast Count"]] = df[["EV Level1 EVSE Num", "EV Level2 EVSE Num", "EV DC Fast Count"]].fillna(0)
            return df[['Latitude', 'Longitude', 'EV Level1 EVSE Num', 'EV Level2 EVSE Num', 'EV DC Fast Count', 'Access Days Time', 'EV Connector Types']]
        stationDF = stationDFProcessing(stationDF)
        stationDF.to_csv("../data/station.csv")
        
    class downloadGraphData:
        ox.settings.log_console=True
        graph = ox.graph_from_place('Hennepin County, Minnesota, USA', network_type='drive')
        ox.io.save_graphml(graph, filepath="../data/hennepinCounty.graphml", gephi=False, encoding='utf-8')
        
    class loadGraphData:
        graph = ox.io.load_graphml("../data/hennepinCounty.graphml")

    # censusUrl = 'https://api.census.gov/data/2019/acs/acs1'
    # censusQuery = {'get': 'NAME,B01001_001E', 'key':Censusapi.getKey()}
    # censusData = getRequest(censusUrl, censusQuery)

    # print("test charging station:" + stationData.text)
    # print("test census data: "+ censusData.text)