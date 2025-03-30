from flask import Flask, jsonify, request, send_from_directory, redirect, url_for, render_template
from flask_cors import CORS
import os
import time
import threading
import random
import ALGORITHMS.ship as ship
from ALGORITHMS import astar

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
        time.sleep(0.052)  # Simulate time taken for calculations
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
    "Houston": {"lat": 29, "lon": -94.5},
    "Tampa": {"lat": 27.5, "lon": -83},
    "Mexico City": {"lat": 22, "lon": -97.5},
    "Havana": {"lat": 23.5, "lon": -82.5},
    "Cancun": {"lat": 21, "lon": -86.5},
}

citiesXY = {
    "Houston": {"x": 332, "y": 190},
    "Tampa": {"x": 1175, "y": 330},
    "Mexico City": {"x": 117, "y": 743},
    "Havana": {"x": 1200, "y": 660},
    "Cancun": {"x": 890, "y": 820},
}


def generate_test_points(start, end, num_points=100):
    noise = 0.05
    points = []
    for i in range(num_points):
        # Interpolate latitude and longitude
        lat = start["lat"] + (end["lat"] - start["lat"]) * (i / (num_points - 1))
        lon = start["lon"] + (end["lon"] - start["lon"]) * (i / (num_points - 1))

        # Add slight randomness to the points

        lat += random.uniform(-noise, noise)  # Random offset for latitude
        lon += random.uniform(-noise, noise)  # Random offset for longitude

        points.append((round(lat, 4), round(lon, 4)))
    return points


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
    scale_x, scale_y = geo_to_pixel_scale(start_lats["lat"], start_lats["lon"], end_lats["lat"], end_lats["lon"], start_coords["x"], start_coords["y"], end_coords["x"], end_coords["y"])
    
    LatLongInput, energySaved = astar.generate(start_lats["lat"], start_lats["lon"], end_lats["lat"], end_lats["lon"])

    # Tampa = {"lat": 27.5, "lon": -83}
    # Cancun = {"lat": 21, "lon": -86.5}

    # LatLongInput = generate_test_points(start_lats, end_lats)

    path = []
    for tup in LatLongInput:
        latx = tup[0]
        laty = tup[1]
        xpoint = start_coords["x"] + (laty - start_lats["lon"]) * scale_x
        ypoint = start_coords["y"] + (latx - start_lats["lat"]) * scale_y
        path.append({"x": xpoint, "y": ypoint})

    energySaved = 29.18

    # path = [{"x": random.randint(100, 1000), "y": random.randint(100, 1000)} for _ in range(50)]
    # Pass the coordinates to the template
    return render_template('simulation.html', start_city=start_city, end_city=end_city, start_coords=start_coords, end_coords=end_coords, path=path, energySaved=energySaved)

if __name__ == '__main__':
    app.run(debug=True)
