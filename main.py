from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__,template_folder='template')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    url = f"https://api.weatherapi.com/v1/current.json?key=8aed93a5edcb41e1b2485731242703&q={city}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

    weather_data = response.json()
    current_weather = weather_data.get('current', {})
    location = weather_data.get('location', {})
    
    weather_report = {
        'city': location.get('name'),
        'country': location.get('country'),
        'temperature': current_weather.get('temp_c'),
        'condition': current_weather.get('condition', {}).get('text'),
        'wind_speed': current_weather.get('wind_kph'),
        'humidity': current_weather.get('humidity'),
        # Add more weather parameters as needed
    }

    return jsonify(weather_report)

if __name__ == '__main__':
    app.run(debug=True)