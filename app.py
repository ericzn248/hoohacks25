from flask import Flask, jsonify, request, send_from_directory, redirect, url_for, render_template
from flask_cors import CORS
import os
import time
import threading

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

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

    # Pass the coordinates to the template
    return render_template('simulation.html', start_city=start_city, end_city=end_city, start_coords=start_coords, end_coords=end_coords)

if __name__ == '__main__':
    app.run(debug=True)
