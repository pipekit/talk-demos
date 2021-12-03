from pathlib import Path
import numpy as np
import pandas as pd
from distributed import Client

# Set reusable constants
KNOWN_CITIES = ["Barcelona", "Bilbao", "Madrid", "Seville", "Valencia"]
DATADIR = Path("data")

# Define a task to be scaled out with Dask
def get_windiest_city(date: str) -> str:
    """For the given `date` find the city with the windiest day from our datasets"""

    date = pd.Timestamp(date)

    max_wind_speed = -1000
    windiest_city = "unknown"

    for city in KNOWN_CITIES:
        # Read datafile
        datafile = DATADIR / f"{city}.parquet"
        weather_data = pd.read_parquet(datafile)

        # Get data for the given day
        weather_data_day = weather_data.loc[date]

        # Update hottest city
        if weather_data_day.wind_speed >= max_wind_speed:
            windiest_city = city
            max_wind_speed = weather_data_day.wind_speed

    print(f"Windiest city at timestamp {date} is {windiest_city}")

    return windiest_city


###################
# Dask pipeline
def pipeline(cluster_address: str):
    """A simple Dask pipeline which searches for the windiest city in Spain. Requires passing in an
    IP address (`cluster_address`) for a pre-existing dask cluster"""
    # Create a dask client
    client = Client(address=cluster_address)

    # Get a list of all timestamps to evaluate
    timestamps = pd.read_csv(DATADIR / "timestamps.csv").dt_iso

    # Submit dask tasks via the "futures" interface
    futures = []
    for timestamp in timestamps[:10]:
        future = client.submit(get_windiest_city, timestamp)
        futures.append(future)

    # Gather the response from each future
    results = client.gather(futures)

    # Write the results
    counted_results = np.unique(results, return_counts=True)
    counted_results = pd.Series(
        counted_results[1], index=counted_results[0], name="windy_city_counts"
    )
    counted_results.to_csv("result.csv")

    # Report the result
    print(f"The Windiest city is {counted_results.index[np.argmax(counted_results)]}")


if __name__ == "__main__":
    import sys

    cluster_address = sys.argv[1]

    pipeline(cluster_address)
