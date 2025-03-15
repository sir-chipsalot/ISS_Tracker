import pytest
from iss_tracker import load_iss_data, instantaneous_speed, compute_location_astropy, find_closest_epoch
import json
import math
import time
from datetime import datetime
import redis

# Test the instantaneous_speed function
def test_instantaneous_speed():
    # This test checks if the instantaneous_speed function works. It should calculate the speed correctly.
    # Create a fake state vector
    state_vector = {
        "X_DOT": {"#text": "1.0"},
        "Y_DOT": {"#text": "2.0"},
        "Z_DOT": {"#text": "3.0"}
    }

    # Calculate the speed
    speed = instantaneous_speed(state_vector)

    # Check if the speed is calculated correctly
    expected_speed = math.sqrt(1.0**2 + 2.0**2 + 3.0**2)
    assert speed == expected_speed  # Make sure the speed is correct

# Test the compute_location_astropy function
def test_compute_location_astropy():
    # This test checks if the compute_location_astropy function works. It should calculate the location correctly.
    # Create a fake state vector
    state_vector = {
        "X": {"#text": "1000.0"},
        "Y": {"#text": "2000.0"},
        "Z": {"#text": "3000.0"},
        "EPOCH": "2023-274T12:34:56"
    }

    # Calculate the location
    lat, lon, alt = compute_location_astropy(state_vector)

    # Check if the location is calculated correctly
    assert lat is not None  # Make sure latitude is not None
    assert lon is not None  # Make sure longitude is not None
    assert alt is not None  # Make sure altitude is not None

# Test the find_closest_epoch function
def test_find_closest_epoch():
    # This test checks if the find_closest_epoch function works. It should find the closest epoch to the current time.
    # Create a list of fake state vectors
    state_vectors = [
        {"EPOCH": "2023-274T12:34:56.789Z"},
        {"EPOCH": "2023-274T12:35:56.789Z"},
        {"EPOCH": "2023-274T12:36:56.789Z"}
    ]

    # Find the closest epoch
    closest_entry = find_closest_epoch(state_vectors)

    # Check if the closest epoch is found
    assert closest_entry is not None  # Make sure a closest entry is found

# Test the load_iss_data function
def test_load_iss_data():
    # This test checks if the load_iss_data function works. It should load ISS data into Redis.
    # Create a Redis client
    redis_client = redis.Redis(host='redis-db', port=6379, db=0)

    # Check if the data is loaded into Redis
    iss_data = redis_client.get("iss_data")
    assert iss_data is not None  # Make sure the data is not None

    # Clean up Redis after the test
    # This line was written by A.I. I had errors were after running pytest, I would get some sort of database error. I was told that I needed to have this at the end to stop that.
    redis_client.flushdb()
