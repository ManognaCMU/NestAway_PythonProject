"""
@fileName: google_static_maps_api_coordinates.py
@Author: 
Sai Manogna Pentyala - spentyal@andrew.cmu.edu
"""

# Python program to get coordinates of specified location using  
# Google Static Maps API, which is inturn used to find the nearest bus stop
# This file imports requests module
# This file is imported by group_7_nestaway_project
  
# importing required modules 
import requests
  
# API key
api_key = "AIzaSyAqXLgpQhHm6rNqCH-2x67Xu3aeJVHT0Ak"

# method to fetch the coordinates of the 
# addresses passed through this method
def get_coordinates(address):

    # replace the spaces in address with a hyphen
    address = address.replace(" ","-")
    address = address.replace("#","")

    # URL to hit the API
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="+ address + ",Pittsburgh,PA&key="+api_key
    
    # get method of requests module 
    # return response object 
    response = requests.get(url)
    
    # processing to fetch the latitude and longitude
    responseStr = response.text
    locationIndex = responseStr.index("\"location\" : {")
    responseArr = responseStr[locationIndex::]
    location = str(responseArr)
    fromLoc = location.index("\"lat\" : ")
    fromEndLoc = location.index(",")
    toLoc = location.index("\"lng\" : ")
    latitude = location[fromLoc+8:fromEndLoc:]
    longitudeLoc = location[toLoc::]
    longStr = str(longitudeLoc)
    longFromLoc = longStr.index("\"lng\" : ")
    longToLoc = longStr.index(" },")
    longitude = longStr[longFromLoc+8:longToLoc:]
    
    # a list which contains the latitude and longitude
    coordinatesList = []
    latitude = latitude.strip()
    longitude = longitude.strip()
    coordinatesList.append(latitude)
    coordinatesList.append(longitude)

    return coordinatesList
