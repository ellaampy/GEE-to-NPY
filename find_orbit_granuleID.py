
import ee
import os
import numpy as np
import geojson, json
from shapely.geometry import Polygon


# Trigger the authentication flow
ee.Authenticate()

# Initialize library
ee.Initialize()


def orbit_granuleID(aoi, collection_ID, start_date, end_date, orbit_pass='DESCENDING'):
  """
  returns orbit number or granule ID for Sentinel-1 or Sentinel-2 for a given area of interest
  
  aoi: area of interest e.g. geojson file
  collection_ID : GEE collection ID e.g. 'COPERNICUS/S2_SR' or 'COPERNICUS/S1_GRD'"
  start_date: collection start date
  end_date: collection end date
  
  """
  
  
    if 'S2' in collection_ID: 
        collection = ee.ImageCollection(collection_ID).filterDate(start_date,end_date).filterBounds(aoi)
        granule = collection.aggregate_array('MGRS_TILE')

    elif 'S1'  in collection_ID:
        collection = ee.ImageCollection(collection_ID).filter(ee.Filter.eq('instrumentMode', 'IW')).filterDate(start_date, end_date).filterBounds(geometry).filter(ee.Filter.eq('orbitProperties_pass', orbit_pass))
        granule = collection.aggregate_array('relativeOrbitNumber_start')
        
        
    print('Total number of orbit/granule IDs -->', granule.aggregate_count_distinct())
    print('Granule IDs -->' , granule)
    
        

