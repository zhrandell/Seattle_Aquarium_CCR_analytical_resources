import pandas as pd
from pymavlink import mavutil
from datetime import datetime, timezone
import math
import pytz
import os
from geopy.distance import geodesic
import folium
import random

# Constants for the area calculation
reference_width = 1.15  # Width in meters at 0.66m altitude
reference_height = 0.66  # Reference altitude in meters
reference_area = 0.9545  # Known area at reference height in square meters

# Function to calculate width based on altitude
def calculate_width(altitude):
    if altitude > 0:
        return reference_width * (altitude / reference_height)
    else:
        return 0

# Function to calculate area based on the altitude
def calculate_area(altitude):
    if altitude > 0:
        return reference_area * (altitude / reference_height) ** 2
    else:
        return 0

# Function to calculate the total displacement (distance) from DVLx and DVLy
def calculate_distance(dvlx, dvly):
    distance = math.sqrt(dvlx**2 + dvly**2)
    return distance

# Prompt the user to enter the tlog file path and save location
logfile = input("Enter the path to your .tlog file: ")
site_number = input("Enter the site number/ name: ")
save_location = input("Enter the path to save the transects folder: ")

transects_folder = os.path.join(save_location, "transects")
if not os.path.exists(transects_folder):
    os.makedirs(transects_folder)
    print(f"Created folder: {transects_folder}")
else:
    print(f"Folder already exists: {transects_folder}")

# Get transect start and end times
transects = []
for i in range(1, 5):
    start_time_str = input(f"Enter start time for transect {i} (HH:MM:SS) or leave blank: ")
    end_time_str = input(f"Enter end time for transect {i} (HH:MM:SS) or leave blank: ")
    
    if start_time_str and end_time_str:
        transects.append((start_time_str, end_time_str))
    else:
        break  # Stop if no more transects are entered

# Connect to the tlog file
try:
    mav = mavutil.mavlink_connection(logfile)
except FileNotFoundError:
    print(f"Error: File '{logfile}' not found.")
    exit(1)

# Initialize storage for data and variables
data = {}
count = {}
latest_time = None
lat, lon, dvlx, dvly, altitude, depth, heading = (None,)*7

# Set the Pacific Time zone using pytz
pacific = pytz.timezone('US/Pacific')
file_date_str = None

# Loop through messages in the tlog file
while True:
    msg = mav.recv_match(blocking=False)
    if msg is None:
        break

    if msg.get_type() == "SYSTEM_TIME":
        unix_time = msg.time_unix_usec / 1e6
        if unix_time > 0:
            latest_time = datetime.fromtimestamp(unix_time, tz=timezone.utc).astimezone(pacific)
            second_key = latest_time.replace(microsecond=0)
            date = latest_time.strftime('%Y-%m-%d')
            time = latest_time.strftime('%H:%M:%S')
            if file_date_str is None:
                file_date_str = latest_time.strftime('%Y_%m_%d')

            if second_key not in data:
                data[second_key] = [date, time, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                count[second_key] = 0

    elif msg.get_type() == "GPS_RAW_INT":
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7

    elif msg.get_type() == "VFR_HUD":
        depth = msg.alt

    elif msg.get_type() == "LOCAL_POSITION_NED":
        dvlx = msg.x
        dvly = msg.y

    elif msg.get_type() == "RANGEFINDER":
        altitude = msg.distance

    elif msg.get_type() == "ATTITUDE":
        yaw = msg.yaw
        heading = (math.degrees(yaw) + 360) % 360

    if latest_time:
        data[second_key][2] += lat if lat is not None else 0
        data[second_key][3] += lon if lon is not None else 0
        data[second_key][4] += dvlx if dvlx is not None else 0
        data[second_key][5] += dvly if dvly is not None else 0
        data[second_key][6] += altitude if altitude is not None else 0
        data[second_key][7] += depth if depth is not None else 0
        data[second_key][8] += heading if heading is not None else 0
        data[second_key][9] += calculate_width(altitude) if altitude is not None else 0
        data[second_key][10] += calculate_area(altitude) if altitude is not None else 0
        count[second_key] += 1

# Average the values for each second
for second_key in data:
    if count[second_key] > 0:
        data[second_key][2] /= count[second_key]
        data[second_key][3] /= count[second_key]
        data[second_key][4] /= count[second_key]
        data[second_key][5] /= count[second_key]
        data[second_key][6] /= count[second_key]
        data[second_key][7] /= count[second_key]
        data[second_key][8] /= count[second_key]
        data[second_key][9] /= count[second_key]
        data[second_key][10] /= count[second_key]

csv_files = []  # To store CSV file paths for mapping

# Clip data into transects and adjust DVLx, DVLy
for i, (start_time_str, end_time_str) in enumerate(transects):
    start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
    end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
    transect_data = [row for row in data.values() if start_time <= datetime.strptime(row[1], '%H:%M:%S').time() <= end_time]

    if len(transect_data) > 0:
        initial_dvlx = transect_data[0][4]
        initial_dvly = transect_data[0][5]

        for idx, row in enumerate(transect_data):
            if idx > 0:
                row[4] = row[4] - initial_dvlx
                row[5] = row[5] - initial_dvly

        transect_data[0][4] = 0
        transect_data[0][5] = 0

    for row in transect_data:
        row[4] = round(row[4], 4)
        row[5] = round(row[5], 4)
        row[6] = round(row[6], 2)
        row[7] = round(row[7], 2)
        row[8] = round(row[8], 2)
        row[9] = round(row[9], 2)
        row[10] = round(row[10], 4)

    df_transect = pd.DataFrame(transect_data, columns=['Date', 'Time', 'Latitude', 'Longitude', 
                                                       'DVLx', 'DVLy', 'Altitude', 'Depth', 'Heading', 'Width', 'Area_m2'])

    if file_date_str is None:
        file_date_str = "unknown_date"

    csv_filename = f"{file_date_str}_{site_number}_T{i+1}.csv"
    csv_full_path = os.path.join(transects_folder, csv_filename)
    df_transect.to_csv(csv_full_path, index=False)
    print(f"Transect {i+1} saved to '{csv_full_path}'.")
    csv_files.append(csv_full_path)  # Add CSV file for mapping

    # Perform cumulative DVLlat/DVLlon calculation
    df = pd.read_csv(csv_full_path)
    scale_factor = 0.00227306
    df.at[0, 'DVLlat'] = df.at[0, 'Latitude']
    df.at[0, 'DVLlon'] = df.at[0, 'Longitude']

    for j in range(1, len(df)):
        dvlx = df.at[j, 'DVLx'] * scale_factor
        dvly = df.at[j, 'DVLy'] * scale_factor
        distance = calculate_distance(dvlx, dvly)
        bearing = df.at[j, 'Heading']
        previous_latlon = (df.at[j-1, 'DVLlat'], df.at[j-1, 'DVLlon'])
        new_position = geodesic(meters=distance).destination(previous_latlon, bearing)
        df.at[j, 'DVLlat'] = new_position.latitude
        df.at[j, 'DVLlon'] = new_position.longitude

    # Reorder columns to have DVLlat and DVLlon before Altitude
    df = df[['Date', 'Time', 'Latitude', 'Longitude', 'DVLx', 'DVLy', 'DVLlat', 'DVLlon', 'Altitude', 'Depth', 'Heading', 'Width', 'Area_m2']]

    # Save the DataFrame with reordered columns
    df.to_csv(csv_full_path, index=False)
    print(f"Corrected DVLlat/DVLlon saved to '{csv_full_path}'.")

# Function to generate a random color in hex format
def get_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Function to load CSV files and create a map with multiple transects
def create_map_with_transects(csv_files):
    if not csv_files:
        print("No CSV files provided for mapping.")
        return

    # Initialize map (centered based on first file's midpoint)
    data_first = pd.read_csv(csv_files[0])
    midpoint_lat = data_first['Latitude'].mean()
    midpoint_lon = data_first['Longitude'].mean()
    m = folium.Map(location=[midpoint_lat, midpoint_lon], zoom_start=15)

    # Loop through selected CSV files and add transect lines to the map
    for csv_file in csv_files:
        data = pd.read_csv(csv_file)

        # Create a list of lat/lon tuples for the transect (Latitude/Longitude)
        transect_coords = list(zip(data['Latitude'], data['Longitude']))

        # Create a list of DVLlat/DVLlon tuples for the transect (if columns exist)
        if 'DVLlat' in data.columns and 'DVLlon' in data.columns:
            dvl_coords = list(zip(data['DVLlat'], data['DVLlon']))
        else:
            dvl_coords = []

        # Get file name for labeling (without extension)
        file_name = os.path.basename(csv_file).replace('.csv', '')

        # Generate random colors for both transects (Latitude/Longitude and DVLlat/DVLlon)
        latlon_color = get_random_color()
        dvl_color = get_random_color()

        # Add the Latitude/Longitude transect line to the map
        folium.PolyLine(transect_coords, color=latlon_color, weight=2.5, opacity=1, tooltip=f"{file_name} Lat/Lon").add_to(m)

        # Add the DVLlat/DVLlon transect line to the map (if available)
        if dvl_coords:
            folium.PolyLine(dvl_coords, color=dvl_color, weight=2.5, opacity=1, tooltip=f"{file_name} DVLlat/DVLlon").add_to(m)

    # Save the map to the same directory as the first CSV file
    output_html = os.path.join(os.path.dirname(csv_files[0]), 'combined_transect_map_with_dvl.html')
    m.save(output_html)

    print(f"Map saved to {output_html}")

# Run the function to create the map
create_map_with_transects(csv_files)

print("Processing complete.")
