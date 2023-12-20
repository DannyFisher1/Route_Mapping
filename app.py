from flask import Flask, render_template
import requests
import random
import math

app = Flask(__name__)

# Define the exponential sampling function with a mean of 10 minutes
lambda_rate = 1/10
wait_time = 0;  
def sample_exponential_wait_time():
    sample = int(random.expovariate(lambda_rate)) 
    if(sample >30): return 30 #max time per person drop off
    if(sample<5): return 5 #min time per person drop off
    return sample

hospital_abbreviations = {
    "GWU HOSPITAL, Washington, DC": "GWU",
    "MedStar Washington Hospital Center, Washington, DC": "MWHC",
    "MedStar Georgetown University Hospital, Washington, DC": "MGUH",
    "VHC Arlington, VA": "VHC"
}

@app.route('/')
def index():
    hospitals = [
        "GWU HOSPITAL, Washington, DC",
        "MedStar Washington Hospital Center, Washington, DC",
        "MedStar Georgetown University Hospital, Washington, DC",
        "VHC Arlington, VA"
    ]
    api_key = "AIzaSyD3ZfT6ELW3-J0IIidWaOrXHtvZlwbiALw"
    base = "38.8033,-76.8719"  # Joint Base Andrews

    # Calculate total travel times
    travel_times = {}
    for hospital in hospitals:
        directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={base}&destination={base}&waypoints={hospital}&key={api_key}"
        response = requests.get(directions_url).json()
        if response['status'] == 'OK':
            outbound_leg = response['routes'][0]['legs'][0]
            return_leg = response['routes'][0]['legs'][1]
            
            # Incorporate exponential wait time
            wait_time = sample_exponential_wait_time()
            
            total_duration = outbound_leg['duration']['value'] + wait_time + return_leg['duration']['value']
            travel_times[hospital] = total_duration

    # Sort hospitals by travel time in ascending order
    sorted_hospitals = sorted(hospitals, key=lambda x: travel_times.get(x, 0), reverse=False)

    hospital_abbs = [hospital_abbreviations[hospital] for hospital in sorted_hospitals]
    mean = (wait_time)

    return render_template("index.html", hospitals=sorted_hospitals, api_key=api_key, hospital_abbs=hospital_abbs, mean = mean)

if __name__ == "__main__":
    app.run(debug=True)
