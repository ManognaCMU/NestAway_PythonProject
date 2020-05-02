"""
@fileName: google_static_maps_api.py
@Author: 
Sai Manogna Pentyala - spentyal@andrew.cmu.edu
"""

# Python program to get a google map image of 
# specified location using Google Static Maps API 
# It imports requests module
# This file is imported by group_7_nestaway_project
  
# importing required modules 
import requests 
  
# API key
api_key = "AIzaSyAqXLgpQhHm6rNqCH-2x67Xu3aeJVHT0Ak"

# method to create the google map image
# accepts the address of the houses to be viewed on the map
def display_google_map_image(addressList):
     
    # captures the URL to hit the API
    url = "https://maps.googleapis.com/maps/api/staticmap?size=512x512&maptype=roadmap\&markers=size:mid%7Ccolor:red%7Clabel:C%7C4800+Forbes+Avenue,Pittsburgh,PA"    

    loop_cnt = 1

    # frame the URL with each address
    for address in addressList:
        address = address.replace(" ","+") 
        address = address.replace("#","")
        url = url + "&markers=color:blue%7Clabel:" + str(loop_cnt) + "%7C" + address + ",Pittsburgh,PA"
        loop_cnt += 1
            
    
    url = url + "&key=" + api_key
    
    # get method of requests module 
    # return response object 
    response = requests.get(url) 
    
    # wb mode is write binary mode
    # google_image is created
    f = open('google_map_image', 'wb') 
  
    # response.content gives content, 
    # in this case gives image 
    f.write(response.content) 
  
    # close method of file object 
    # save and close the file 
    f.close()
