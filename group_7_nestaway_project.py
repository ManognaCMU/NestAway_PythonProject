"""
@fileName: group_7_nestaway_project.py
@Author: 
Sai Manogna Pentyala - spentyal@andrew.cmu.edu
"""

"""
This is the main file from which our application starts
It takes inputs from the user, and provides general information
about the place chosen by the user, top 5 houses in that area,
crime chart in Pittsburgh, crime chart in the area chosen,
a google map image showing the houses and CMU.

This file imports all the other remaining supporting programs like,
grocery_restaurant_scraping, bus_stop_csv_read, google_static_maps_api,
hotpads_scraping, google_static_maps_api_coordinates, area_vibes_scrap
and python libraries like pandas, Image, matplotlib.pyplot.
"""

# import required modules
import grocery_restaurant_scraping as gr
import bus_stop_csv_read as bs
import pandas as pd
import google_static_maps_api as gsma
from PIL import Image
import hotpads_scraping as hpsr
import google_static_maps_api_coordinates as gsmac
import area_vibes_scrap as avs
import matplotlib.pyplot as plt  # for pie chart

# formatting options for the dataframes
pd.set_option('display.expand_frame_repr', False)
pd.set_option("display.max_colwidth", 120)
pd.options.display.width = None
pd.options.display.max_columns = None
pd.options.display.max_rows = None

# list that holds the input
inputList = []

# method where the user gives his input parameters
# based on the input parameters, top 5 houses in that area,
# bus routes information, groceries information and
# crime rate information is displayed. Along with this,
# a crime pie chart and google maps image is displayed
def choose_area():
    """
     This is a helper method
     to show the menu and get input fom user
     """
    print('\n')
    print('We have selected few areas where CMU students mostly live !')
    print('Choose an area that you would like to stay in ?')
    while True:
        print("""
1.SQUIRREL HILL SOUTH
2.SQUIRREL HILL NORTH
3.GREENFIELD
4.EAST LIBERTY 
5.NORTH OAKLAND
6.OAKLAND
7.EXIT
        """)
        input_area = input("Enter the number(1~7) ")
        if input_area.isdigit():
            if int(input_area) == 7:
                print('\n')
                print('THANK YOU FOR USING NEST AWAY !')
                quit()
            elif int(input_area) not in [1, 2, 3, 4, 5, 6]:
                print('\n')
                print('Invalid Input! Please Enter a Valid Choice and Try again !')
            else:
            ############################################################
            # get input from console
            ############################################################
                print('Input your minimum budget($) ', end='')
                input_min_budget = (input())

                print('Input your maximum budget($) ', end='')
                input_max_budget = (input())

                print('Input number of beds ', end='')
                input_beds = (input())
                # handling edge case scenarios - if the inputs are present
                if (input_min_budget and input_max_budget and input_beds):
                    # handling edge case scenarios - if the inputs are valid digits
                    if (input_min_budget.isdigit() and input_max_budget.isdigit() and input_beds.isdigit()):
                        input_min_budget = int(input_min_budget)
                        input_max_budget = int(input_max_budget)
                        # handling edge case scenarios - if the max budget is >= min budget
                        if input_max_budget >= input_min_budget:
                            if int(input_beds) > 0:
                                input_beds = int(input_beds)
                                inputList.append(input_min_budget)
                                inputList.append(input_max_budget)
                                inputList.append(input_beds)
                                break;
                            else:
                                print('\n')
                                print('Number of beds should be greater than 0! Please Try again !')                                
                        else:
                            print('\n')
                            print('Maximum budget should be greater than or equal to Minimum budget! Please Try again !')
                    else:
                        print('\n')
                        print('Input should be a valid number! Please Enter a Valid Choice and Try again !')
                else:
                    print('\n')
                    print('Invalid Input! Please Enter a Valid Choice and Try again !')
        else:
            print('\n')
            print('Invalid Input! Please Enter a Valid Choice and Try again !')

    return int(input_area)


if __name__ == '__main__':

    loop_cnt = 0
    while True:
        ############################################################
        # read config
        ############################################################

        filename = 'place.csv'
        df = pd.read_csv(filename)

        ############################################################
        # get data from data sources
        ############################################################

        if loop_cnt == 0:
            print('WELCOME TO NEST AWAY !')
        else:
            print('\n')
            print('TRY OUR NEST AWAY WITH ANOTHER INPUT !')
        inputList = []
        input_area = choose_area()
        place = df.loc[input_area - 1]['City']
        restaurants_df = gr.scrape_groceries_restaurants('restaurant', df.loc[input_area - 1]['yellowPage'])
        groceries_df = gr.scrape_groceries_restaurants('grocery', df.loc[input_area - 1]['yellowPage'])
        bus_stops_df = bs.bus_stop_read(x1=df.loc[input_area - 1]['LATITUDE'], y1=df.loc[input_area - 1]['LONGITUDE'])
        bus_route = bus_stops_df['ROUTE'].unique()
        houses_df = hpsr.scrape_hotpads_for_houselist(df.loc[input_area - 1]['City'], inputList[0],
                                                      inputList[1], inputList[2])
        crime_dict = avs.getcrimestat(place)

        ############################################################
        # merge data
        ############################################################

        if len(houses_df) > 0:
            address_list_df = houses_df['HOUSE ADDRESS']
            distance_list = []
            bus_stop_name_list = []

            for address in address_list_df:
                # get coordinate information based on House Address
                coordinatesList = gsmac.get_coordinates(address)

                # search nearest bus stops
                house_bus_df = bs.bus_stop_read(x1=float(coordinatesList[0]), y1=float(coordinatesList[1])).sort_values(
                    'distance')

                # get bus stop information
                if len(house_bus_df) > 0:
                    house_bus_df = house_bus_df.head(1)
                    bus_stop_name_list.append(house_bus_df.iat[0, 1])
                    distance_list.append(round(house_bus_df.iat[0, 7], 1))
                else:
                    bus_stop_name_list.append('No bus stops within 1 mile')
                    distance_list.append('No data')

            # merge data
            houses_df['NEAREST BUS STOP'] = bus_stop_name_list
            houses_df['DISTANCE(miles)'] = distance_list

        ############################################################
        # Display General Information
        ############################################################

        print('\n')
        print('---GENERAL INFORMATION---')
        print('{:30s}{:<20s}'.format('Place', place))
        print('{:30s}{:<20}'.format('Restaurants within 1 mile', len(restaurants_df)))
        print('{:30s}{:<20}'.format('Grocery Stores within 1 mile', len(groceries_df)))
        print('{:30s}{:<20}'.format('Bus route within 1 mile', (','.join(bus_route))))
        print('{:30s}{:<20}'.format('Livability score', crime_dict['Livability']))
        print('{:30s}{:<20}'.format('The total crimes in the area', crime_dict['Total crimes in the area']))
        print('{:30s}{:<20}'.format('The total crimes in the city', crime_dict['Total crimes in Pittsburgh']))

        ############################################################
        # Display top 5 list of houses - based on rent
        ############################################################

        print('\n')
        print('---TOP 5 HOUSES IN', place, ' ---')

        if len(houses_df) == 1:
            print(houses_df.head(5))
            print('Only', len(houses_df), 'house is found')
        elif len(houses_df) == 0:
            print('No Houses found as per your requirements. Please try with another input.')
        elif len(houses_df) < 5:
            print(houses_df.head(5))
            print('Only', len(houses_df), 'houses are found')
        else:
            print(houses_df.head(5))

        ############################################################
        # Display top 5 list of groceries - based on distance
        ############################################################

        print('\n')
        print('---TOP 5 GROCERY STORES IN', place, ' ---')

        if len(groceries_df) == 1:
            print(groceries_df.head(5))
            print('Only', len(groceries_df), 'grocery is found')
        elif len(groceries_df) == 0:
            print('No results')
        elif len(groceries_df) < 5:
            print(groceries_df.head(5))
            print('Only', len(groceries_df), 'groceries are found')
        else:
            print(groceries_df.head(5))

        ############################################################
        # Display Crime Pie Chart
        ############################################################

        print('\n')
        print('---CRIME DATA PIE CHART ---')

        print("View the crime data on the Image")

        # Setting labels and colors
        labels = 'Violent Crime', 'PropertyCrime'
        colors = ['blue', 'green']

        # crime chart for city of pittsburgh
        plt.title("Crime in the City of Pittsburgh")
        patches, texts, _ = plt.pie(crime_dict['Pittsburgh counts'], labels=labels, colors=colors, autopct='%1.1f%%',
                                    shadow=False, startangle=140)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.show()

        # crime chart for the area
        plt.title("Crime in " + place)
        patches, texts, _ = plt.pie(crime_dict['Area counts'], labels=labels, colors=colors, autopct='%1.1f%%',
                                    shadow=False, startangle=140)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.show()

        ############################################################
        # Display Google MAP showing the locations around CMU
        ############################################################

        print('\n')
        print('---GOOGLE MAP IMAGE ---')

        display_google_map = False

        # if there are houses to display
        if len(houses_df) > 0:
            address_list = houses_df['HOUSE ADDRESS']
            display_google_map = True

            if len(address_list) > 5:
                gsma.display_google_map_image(address_list[:5:])
            else:
                gsma.display_google_map_image(address_list)

        # if there are houses to display
        if (display_google_map):
            print("View the houses on the Google Map Image")
            # opens the google map image
            img = Image.open('google_map_image', 'r')
            # shows the map
            img.show()
        else:
            print("No Houses to display on the Google Map Image")
        
        loop_cnt += 1
