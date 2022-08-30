from apiKeys import NRELapi,Censusapi
import requests

def getRequest(url, query):
    return requests.get(url, params= query)

stationQuery = {'api_key':NRELapi.getKey(),'fuel_type':'E85,ELEC','state':'CA','limit':'2'}
stationUrl = 'https://developer.nrel.gov/api/alt-fuel-stations/v1.json'
stationData = getRequest(stationUrl, stationQuery)

censusUrl = 'https://api.census.gov/data/2019/acs/acs1'
censusQuery = {'get': 'NAME,B01001_001E', 'key':Censusapi.getKey()}
censusData = getRequest(censusUrl, censusQuery)

print("test charging station:" + stationData.text)
print("test census data: "+ censusData.text)