import requests

r = requests.post('http://localhost:5000/new_location', json={
    "name": "Harthöfl", "location": 
    [49.19804441699764, 12.202481321134304],
    "temperature": 22.22,
    "humidity": 82.22,
    "pressure": 9999.00})
r = requests.post('http://localhost:5000/new_location', json={
    "name": "Hof", "location": 
    [49.20594821713479, 12.217637779826969],
    "temperature": 11.11,
    "humidity": 66.66,
    "pressure": 1000.11})