"""
@fileName: area_vibes_scrap.py
@Author:
Sai Manogna Pentyala - spentyal@andrew.cmu.edu
"""

# This performs scraping of area vibes site
# in order to determine the crime rate of an area
# It imports request module and Beautiful soup
# It is imported by project_7_nestaway_project

import urllib.request #for url connections
from bs4 import BeautifulSoup #for scraping


#Converting the input in the required form and constructing url
#Squirrel hill north becomes squirrel+hill+north
def getcrimestat(place):
    result={}
    user_input = place
    input_area = urllib.parse.quote_plus(user_input.lower())
    url = 'https://www.areavibes.com/pittsburgh-pa/' + input_area + '/crime/'

    #Constructing the bsoup object from the html response received
    response = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(response,'lxml')
    
    #Getting the list of nav tags in the html response for the class category-menu-new cat-can-large
    #This class corresponds to the top tab in the site where livability scores are present
    nav_list = soup.find_all('nav', class_= 'category-menu-new cat-can-large')
    
    #Getting the first object
    nav = nav_list[0]
    livability=0
    #The html response from this site has spaces in between, making the type as navigatable string, therefore accessing children using c.children would give an exception here
    
    #Getting the livability score from the nav soup object
    for c in nav.children:
        if("Livability" in str(c)):
            start = str(c).find('<i>')  #index where <i> is found
            end = str(c).find('</i>')   #index where </i> is found
            start = start+3 #length of <i> is 3 so adding 3 to start
            livability = int(str(c)[start:end]) #slicing the livability score from the response
            result['Livability'] = livability

    #Making pie chart
    #list of tables in html response with class name av-default crime-cmp is-hood
    table_list = soup.findAll('table', { "class" : "av-default crime-cmp is-hood" } )
    table = table_list[0]   #Getting the first table
    #Getting the total_crimes in the city and area from the html response
    total_crimes_area=0
    total_crimes_city=0
    counter=0
    for c in table.children:
        if('summary major' in str(c)):
            for r in c.children:
                if(counter==2):
                    total_crimes_area = str(r.contents[0])
                elif(counter==3):
                    total_crimes_city=str(r.contents[0])
                counter+=1
                
    result['Total crimes in the area']=total_crimes_area
    result['Total crimes in Pittsburgh']=total_crimes_city

    
    
    #Making the lists for the pie chart
    area_counts=[]
    city_counts=[]
    for c in table.children:
        if('class="summary"' in str(c)):    #the tags containing the counts have class as summary
            counter=0
            for r in c.children:    #Can be used since there is no space here
                if(counter==2):     #Third child is area-wise counts(zero based index)
                    area_counts.append(r.contents[0])
                elif(counter==3):   #Fourth child is city-wise counts(zero based index)
                    city_counts.append(r.contents[0])
                counter+=1  #incrementing counter
                
    #This function converts the list of strings into list of integers by removing the comma 
    #For example 3458 integer is stored as 3,458. This needs to be checked for
    
    
    
    #converting the string lists to integer lists
    city_counts = to_number(city_counts)
    area_counts = to_number(area_counts)
    
    result['Pittsburgh counts']=city_counts
    result['Area counts']=area_counts
    
    return result
    
    
def to_number(numbers):
    result=[]
    #for each number, remove the characters that are non-digit and append to result
    for s in numbers:   
        n=''
        tup = tuple(s)
        for t in tup:
            if(t.isdigit()):
                n+=t
        result.append(int(n))   #appending the integer value of the number to result
    return result   #returning the result(integer list)

