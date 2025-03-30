from flask import Flask, jsonify, request, send_from_directory, redirect, url_for, render_template
from flask_cors import CORS
import os
import time
import threading
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/enterCities')
def enterCities():
    return send_from_directory(os.path.dirname(__file__), 'entercities.html')

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'images'), filename)

@app.route('/route', methods=['GET'])
def get_route():
    # Simulated route data
    route = {
        "start": request.args.get('start', 'New York'),
        "end": request.args.get('end', 'London'),
        "distance": "3450 nautical miles",
        "duration": "7 days 12 hours",
        "waypoints": [
            {"lat": 40.7128, "lon": -74.0060},  # New York
            {"lat": 51.5074, "lon": -0.1278}    # London
        ]
    }
    return jsonify(route)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    # Extracting form data
    start_port = request.form.get('start')
    destination_port = request.form.get('destination')
    
    # Redirect to the loading page with city data as query parameters
    return redirect(url_for('loading', city1=start_port, city2=destination_port))

@app.route('/loading')
def loading():
    city1 = request.args.get('city1', 'Unknown')
    city2 = request.args.get('city2', 'Unknown')
    start_calculations()
    # Render loading.html with city1 and city2 as template variables
    return render_template('loading.html', city1=city1, city2=city2)

# Global variable to track progress
progress = {"value": 0}

# Background thread to simulate calculations
def geo_to_pixel_scale(lat1, lon1, lat2, lon2, x1, y1, x2, y2):
    scale_x = (x2 - x1) / (lon2 - lon1)
    scale_y = (y2 - y1) / (lat2 - lat1)
    return scale_x, scale_y

def perform_calculations():
    global progress
    for i in range(1, 101):  # Simulate progress from 1% to 100%
        time.sleep(0.1)  # Simulate time taken for calculations
        progress["value"] = i

def start_calculations():
    # Start the calculations in a background thread
    calculation_thread = threading.Thread(target=perform_calculations)
    calculation_thread.start()
    return jsonify({"message": "Calculations started"}), 202

@app.route('/progress', methods=['GET'])
def get_progress():
    # Return the current progress
    return jsonify({"progress": progress["value"]})

citiesLatLon = {
    "Huston": {"lat": 29.7604, "lon": -95.3698},
    "Tampa": {"lat": 27.9506, "lon": -82.4572},
    "Mexico City": {"lat": 19.4326, "lon": -99.1332},
    "New Orleans": {"lat": 29.9511, "lon": -90.0715},
    "Cancun": {"lat": 21.1619, "lon": -86.8515},
}

citiesXY = {
    "Huston": {"x": 332, "y": 190},
    "Tampa": {"x": 1175, "y": 330 },
    "Mexico City": {"x": 117, "y": 743 },
    "New Orleans": {"x": 690, "y": 130},
    "Cancun": {"x": 890, "y": 820},
}


@app.route('/simulation', methods=['GET'])
def simulation():
    # Get start and end cities from query parameters
    start_city = request.args.get('start')
    end_city = request.args.get('end')

    # Retrieve coordinates for the start and end cities
    start_coords = citiesXY.get(start_city, {})
    end_coords = citiesXY.get(end_city, {})
    start_lats = citiesLatLon.get(start_city, {})
    end_lats = citiesLatLon.get(end_city, {})
    scale_x, scale_y = geo_to_pixel_scale(start_lats["lat"], start_lats["lon"], end_lats["lat"], end_lats["lon"],
                        start_coords["x"], start_coords["y"], end_coords["x"], end_coords["y"])
    LatLongInput = [(26, -82), (26, -81.75), (25.75, -81.5), (25.75, -81.25), (25.75, -81.0), (25.75, -80.75), (25.75, -80.5), (26.0, -80.25), (26.25, -80.0), (26.5, -79.75), (26.75, -79.5), (27.0, -79.25), (27.25, -79.0), (27.25, -78.75), (27.25, -78.5), (27.25, -78.25), (27.25, -78.0), (27.25, -77.75), (27.25, -77.5), (27.25, -77.25), (27.25, -77.0), (27.25, -76.75), (27.25, -76.5), (27.25, -76.25), (27.25, -76.0), (27.25, -75.75), (27.25, -75.5), (27.25, -75.25), (27.25, -75.0), (27.25, -74.75), (27.25, -74.5), (27.25, -74.25), (27.25, -74.0), (27.25, -73.75), (27.25, -73.5), (27.25, -73.25), (27.25, -73.0), (27.25, -72.75), (27.25, -72.5), (27.25, -72.25), (27.25, -72.0), (27.25, -71.75), (27.25, -71.5), (27.5, -71.25), (27.5, -71.0), (27.75, -70.75), (27.75, -70.5), (27.75, -70.25), (28.0, -70.0), (28.0, -69.75), (28.0, -69.5), (28.0, -69.25), (28.25, -69.0), (28.25, -68.75), (28.25, -68.5), (28.25, -68.25), (28.25, -68.0), (28.25, -67.75), (28.25, -67.5), (28.25, -67.25), (28.25, -67.0), (28.25, -66.75), (28.25, -66.5), (28.25, -66.25), (28.25, -66.0), (28.0, -65.75), (27.75, -65.5), (27.5, -65.25), (27.25, -65.0), (27.25, -64.75), (27.0, -64.5), (26.75, -64.25), (26.5, -64.0), (26.25, -64.0), (26.0, -63.75), (25.75, -63.5), (25.5, -63.25), (25.25, -63.0), (25.0, -62.75), (24.75, -62.5), (24.5, -62.25), (24.25, -62.0), (24.0, -61.75), (23.75, -61.5), (23.5, -61.25), (23.25, -61.25), (23.0, -61.5), (22.75, -61.75), (22.5, -62.0), (22.25, -62.25), (22.25, -62.5), (22.25, -62.75), (22.0, -63.0), (21.75, -63.25), (21.75, -63.5), (21.75, -63.75), (21.75, -64.0), (21.75, -64.25), (21.75, -64.5), (21.75, -64.75), (21.5, -65.0), (21.25, -65.25), (21.25, -65.5), (21.25, -65.75), (21.25, -66.0), (21.25, -66.25), (21.25, -66.5), (21.0, -66.5), (20.75, -66.5), (20.5, -66.75), (20.25, -67.0), (20.0, -67.25), (19.75, -67.5), (19.75, -67.75), (19.5, -68.0), (19.5, -68.25), (19.25, -68.5), (19.25, -68.75), (19.25, -69.0), (19.0, -69.25), (19.0, -69.5), (18.75, -69.75), (18.5, -70.0), (18.25, -70.25), (18.25, -70.5), (18.25, -70.75), (18.25, -71.0), (18.0, -71.25), (18.0, -71.5), (17.75, -71.75), (17.75, -72.0), (17.75, -72.25), (17.75, -72.5), (17.75, -72.75), (17.75, -73.0), (17.75, -73.25), (17.75, -73.5), (17.75, -73.75), (17.75, -74.0), (17.75, -74.25), (17.75, -74.5), (17.5, -74.75), (17.5, -75.0), (17.25, -75.25), (17.25, -75.5), (17.25, -75.75), (17.25, -76.0), (17.25, -76.25), (17.25, -76.5), (17.25, -76.75), (17.25, -77.0), (17.25, -77.25), (17.25, -77.5), (17.25, -77.75), (17.25, -78.0), (17.25, -78.25), (17.25, -78.5), (17.25, -78.75), (17.25, -79.0), (17.5, -79.0), (17.5, -79.25), (17.5, -79.5), (17.5, -79.75), (17.25, -80.0), (17.0, -80.25), (17.0, -80.5), (16.75, -80.75), (16.75, -81.0), (16.5, -81.0), (16.25, -81.25), (16.25, -81.5), (16.25, -81.75), (16.25, -82.0), (16.25, -82.25), (16.25, -82.5), (16.25, -82.75), (16.25, -83.0), (16.25, -83.25), (16.25, -83.5), (16.25, -83.75), (16.5, -84.0), (16.5, -84.25), (16.5, -84.5), (16.5, -84.75), (16.25, -84.75), (16.0, -85.0), (16.0, -85.25), (16.0, -85.5), (16.0, -85.75), (16.0, -86.0), (16.0, -86.25), (16.0, -86.5), (16.0, -86.75), (16.0, -87.0), (16.0, -87.25), (16.0, -87.5), (16.25, -87.75), (16.25, -88.0), (16.25, -88.25), (16.25, -88.5), (16.5, -88.5), (16.5, -88.75), (16.5, -89.0), (16.5, -89.25), (16.5, -89.5), (16.5, -89.75), (16.5, -90.0), (16.5, -90.25), (16.75, -90.25), (16.75, -90.5), (17.0, -90.5), (17.0, -90.75), (17.25, -90.75), (17.5, -90.75), (17.75, -90.75), (18.0, -90.75), (18.0, -91.0), (18.25, -91.0), (18.5, -91.0), (18.75, -91.0), (19.0, -91.0), (19.25, -91.0), (19.25, -91.25), (19.5, -91.25), (19.75, -91.25), (20, -91.25)]
    path = []
    for tup in LatLongInput:
        latx = tup[0]
        laty = tup[1]
        xpoint = start_coords["x"] + (latx - start_lats["lat"]) * scale_x
        ypoint = start_coords["y"] + (laty - start_lats["lon"]) * scale_y
        path.append({"x": xpoint, "y": ypoint})


    # path = [{"x": random.randint(100, 1000), "y": random.randint(100, 1000)} for _ in range(50)]
    # Pass the coordinates to the template
    return render_template('simulation.html', start_city=start_city, end_city=end_city, start_coords=start_coords, end_coords=end_coords, path=path)

if __name__ == '__main__':
    app.run(debug=True)
