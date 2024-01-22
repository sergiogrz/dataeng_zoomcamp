#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from sqlalchemy import create_engine

# download data
url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
os.system(f"wget -nc {url}")

# load data to a dataframe
df = pd.read_csv("taxi_zone_lookup.csv")

# create a connection to Postgres
engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")
engine.connect()

# insert the data into the database
df.to_sql(name="taxi_zones", con=engine, if_exists="replace")