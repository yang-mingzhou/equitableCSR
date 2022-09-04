from utils.apiKeys import NRELapi,Censusapi
import requests
import pandas as pd
import io
import osmnx as ox
import geopandas as gpd

class DataLoader:
    def __init__(self, state = 'MN', stateID = '27') -> None:
        self.state = state
        self.stateID = stateID
        
    def __stationDFProcessing(df):
            df[["EV Level1 EVSE Num", "EV Level2 EVSE Num", "EV DC Fast Count"]] = df[["EV Level1 EVSE Num", "EV Level2 EVSE Num", "EV DC Fast Count"]].fillna(0)
            return df[['ZIP','Latitude', 'Longitude', 'EV Level1 EVSE Num', 'EV Level2 EVSE Num', 'EV DC Fast Count', 'Access Days Time', 'EV Connector Types']]        
          
    def downloadStationDataAndSaveTo(self, filename):
        # API description: https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/all/
        stationQuery = {'format':'csv',
                        'api_key':NRELapi.getKey(),
                        'status':'E', 
                        'access':'public',
                        'fuel_type':'ELEC',
                        'ev_charging_level':'1, 2, dc_fast',
                        'state':self.state,
                        'limit':'all'}
        stationUrl = 'https://developer.nrel.gov/api/alt-fuel-stations/v1'
        stationData = requests.get(stationUrl, params = stationQuery).text
        stationDF = pd.read_csv(io.StringIO(stationData))
        stationDF = self.__stationDFProcessing(stationDF)
        stationDF.to_csv(filename)
        return stationDF
    
    def downloadCensusDataAndSaveTo(self, filename):
        # B01001_001E: population
        getAttributes = "NAME,B01001_001E"
        censusData = requests.get("https://api.census.gov/data/2020/acs/acs5?get="+ getAttributes +
                                  "&for=block%20group:*&in=state:"+ self.stateID +"&in=county:*&in=tract:*&key="+Censusapi.getKey())
        censusDataJson = censusData.json()
        censusDF=pd.DataFrame(censusDataJson[1:], columns=censusDataJson[0])
        censusDF['GEOID'] = censusDF['state'] + censusDF['county'] + censusDF['tract'] + censusDF['block group']
        censusDF = censusDF.drop(columns = ["state", "county", "tract", 'block group'])
        mnBlockGroupShp = gpd.read_file("https://www2.census.gov/geo/tiger/TIGER2020/BG/tl_2020_"+ self.stateID +"_bg.zip")
        censusDF = mnBlockGroupShp.merge(censusDF, on = "GEOID")
        censusDF['INTPTLAT'] = pd.to_numeric(censusDF['INTPTLAT'],errors='coerce')
        censusDF['INTPTLON'] = pd.to_numeric(censusDF['INTPTLON'],errors='coerce')
        censusDF.to_csv(filename)
        return censusDF
    
    @staticmethod
    def readCSV(filename):
        return pd.read_csv(filename)
    
    
if __name__ == '__main__':
    pass