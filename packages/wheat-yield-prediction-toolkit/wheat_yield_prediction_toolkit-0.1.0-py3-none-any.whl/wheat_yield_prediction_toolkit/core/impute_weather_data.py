import concurrent.futures
import io
import json
import os
import time

import pandas as pd
import requests
from shapely import Point
from tqdm import tqdm


def get_weather(year, location=(-95.23525, 38.97167)):
    try:
        return get_weather_(location, year)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return pd.DataFrame()

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()


# TODO Rename this here and in `get_weather`
def get_weather_(location, year):
    base_url = r"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M_MAX,T2M_MIN,PRECTOTCORR,T2M,T2MDEW,T2MWET,TS,T2M_RANGE,RH2M,WS10M_MIN,WS10M_MAX,WS10M,ALLSKY_SFC_SW_DWN,TOA_SW_DWN,ALLSKY_SFC_SW_DNI,ALLSKY_SRF_ALB,ALLSKY_SFC_SW_DIFF,ALLSKY_KT&community=RE&longitude={longitude}&latitude={latitude}&start={year}0901&end={nextyear}0830&format=CSV"

    api_request_url = base_url.format(
        longitude=location.x, latitude=location.y, year=year, nextyear=year + 1
    )

    response = requests.get(url=api_request_url, verify=True, timeout=30.00)

    # raise an exception if response status code is not 200 OK
    response.raise_for_status()

    df = pd.read_csv(io.StringIO(response.text), skiprows=26)
    df["location"] = str(location)

    return df


def get_weather_parallel(HIST_RANGE, location):
    """
    Fetches weather data for a single location across a range of years in parallel.

    Args:
        HIST_RANGE (Tuple[int, int]): A tuple containing the start and end years for the data range.
        location (Tuple[float, float, float]): A tuple containing the latitude, longitude, and elevation of the location.

    Returns:
        pandas.DataFrame: A DataFrame containing weather data for the location across the specified years.
    """
    range_length = len(range(HIST_RANGE[0], HIST_RANGE[1]))
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(
            executor.map(
                get_weather, range(HIST_RANGE[0], HIST_RANGE[1]), [location] * range_length
            )
        )

    return pd.concat(results)


def get_weather_all_locations(HIST_RANGE, list_locations):
    """
    Fetches weather data for multiple locations across a range of years in parallel.

    Args:
        HIST_RANGE (Tuple[int, int]): A tuple containing the start and end years for the data range.
        list_locations (List[Tuple[float, float, float]]): A list of tuples containing the latitude, longitude, and elevation of each location.

    Returns:
        pandas.DataFrame: A DataFrame containing weather data for all locations across the specified years.
    """
    range_length = len(list_locations)
    print(f"Starting parallel weather data processing for {range_length} locations...")
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(
            tqdm(
                executor.map(get_weather_parallel, [HIST_RANGE] * range_length, list_locations),
                total=range_length,
            )
        )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Parallel weather data processing completed in {elapsed_time:.2f} seconds.")
    return pd.concat(results)


def save_weather_data(HIST_RANGE: tuple, list_locations: list, file_path: str):
    """
    Retrieves and saves weather data for a range of years & loactions in parallel using the NASA POWER PROVIDER python API as a parquet file.

    Args:
    - HIST_RANGE (tuple): A tuple specifying the start and end years of the time period of interest.
    - list_locations (list): list of shapely.Point() locations
    - file_path (str): The path where the parquet file will be saved.

    Example usage:
    ```
        >>> HIST_RANGE = (2010, 2019)
        >>> list_locations = [(-95.23525, 38.97167), (-107.26550, 40.98160)]
        >>> save_weather_data(HIST_RANGE, list_locations, "data/weather_data.parquet")
    ```
    """
    # Get the yield data
    weather_data = get_weather_all_locations(HIST_RANGE, list_locations)

    # Check if the path is valid
    if not os.path.exists(os.path.dirname(file_path)):
        # Create it using os.makedirs()
        os.makedirs(os.path.dirname(file_path))

    # Save the yield data as a parquet file
    weather_data.to_parquet(file_path)

    print(f"Weather data saved to {os.path.abspath(file_path)}")


# main
if __name__ == "__main__":
    # -- Test code :
    # HIST_RANGE = (2010, 2019)
    # list_locations = [(-95.23525, 38.97167), (-107.26550, 40.98160)]
    df = get_weather(2012, (-95.770, 32.929))
    # df = get_weather_all_locations(HIST_RANGE, list_locations)
    print(df.head())
