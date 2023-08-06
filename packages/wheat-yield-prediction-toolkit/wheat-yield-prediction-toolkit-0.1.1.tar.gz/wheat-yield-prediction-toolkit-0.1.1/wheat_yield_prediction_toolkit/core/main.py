import os

import pandas as pd
from impute_weather_data import (
    get_weather_all_locations,
    get_weather_parallel,
    save_weather_data,
)
from preprocessor import pre_process_weather, pre_process_yield
from yield_data_collector import get_yield_parallel

# Define the data path
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
RAW_DATA = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA = os.path.join(DATA_DIR, "processed")


# Set the start and end years
# Define the historical range : the last considered year id upper_bound - 1
HIST_RANGE = [1996, 2022]

yield_df = get_yield_parallel(HIST_RANGE[0], HIST_RANGE[1])

# Get counties boundries :
yield_df = pre_process_yield(yield_df)

print(yield_df.head())

# Get all unique locations, of yield_df : 'centroid'
# get weather data :
# weather_df = get_weather_all_locations(HIST_RANGE, yield_df["centroid"].unique().tolist())

# # Save the weather data to parquet :
path_to_save_weather = os.path.join(RAW_DATA, "weather-data", "historical-weather-data.parquet")
# save_weather_data(HIST_RANGE, yield_df["centroid"].unique().tolist(), path_to_save_weather)

# print(weather_df)

# Read the weather data from parquet :
weather_df = pd.read_parquet(path_to_save_weather)

print(weather_df)

weather_df = pre_process_weather(weather_df)

# locations_list = yield_df["centroid"].unique().tolist()

# check if all locations in locations_list are in df, if not use get_weather_parallel(HIST_RANGE, location) to get it
# create a set of unique locations from the weather_df dataframe
# existing_locations = set(weather_df["location"].unique())


# if new_locations := [
#     location
#     for location in locations_list
#     if str(location) not in existing_locations
# ]:
#     print(f"Fetching weather data for {len(new_locations)} new locations...")
#     new_weather_data = pd.concat([get_weather_parallel(HIST_RANGE, location) for location in new_locations])
#     weather_df = pd.concat([weather_df, new_weather_data])

# print(weather_df)

# save the new df :
# path_to_save_weather_v2 = os.path.join(RAW_DATA, 'weather-data', 'historical-weather-data-v2.parquet')
# weather_df.to_parquet(path_to_save_weather_v2)
