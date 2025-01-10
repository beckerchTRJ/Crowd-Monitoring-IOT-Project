Youtube Link: https://www.youtube.com/watch?v=LbNKR4wWQQg

Canva Link: https://www.canva.com/design/DAGYj7B1vYY/lTZDWgvlLEK3cPX3bxsgMw/edit?utm_content=DAGYj7B1vYY&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton 

# Crowd Monitoring IOT Project

## Overview
A comprehensive IoT-based crowd monitoring system that combines real-time sensor data collection with an interactive web dashboard. The system monitors crowd density through multiple sensors and provides real-time alerts and visualizations.

## Components

### Backend Sensor Scripts

#### `new_density_sensor.py`
Core sensor data collection script that:
- Collects data from multiple sensors:
  - Light level monitoring (lux)
  - Sound level detection (dB)
  - Proximity sensing
- Processes and analyzes raw sensor data
- Integrates with ThingsBoard for data visualization
- Stores data in MySQL database
- Configurable thresholds for different environments
- Handles audio recording and analysis
- Manages data transmission to cloud services

#### `new_detection.py`
Monitoring and alert system that:
- Implements real-time crowd density detection
- Calculates moving averages for sensor data
- Triggers alerts based on configurable thresholds:
  - Noise spikes above 45 dB
  - Light level drops greater than 10%
  - Proximity changes beyond 3%
- Sends email alerts when dangerous conditions detected
- Provides continuous monitoring with status updates
- Integrates with ThingsBoard for real-time visualization

### Frontend Dashboard

#### `index.html` & `script.js`
Interactive web dashboard that provides:
- Real-time crowd density heat map
- Dynamic metrics display:
  - Light levels
  - Sound levels
  - Proximity data
  - Safety score
- Interactive map features:
  - Custom markers for key locations
  - Risk level indicators
  - Population density overlays
- Crowd trend analysis charts
- Risk assessment grid
- Location-based monitoring controls

#### `styles.css`
Custom styling that implements:
- Modern dark theme interface
- Responsive grid layouts
- Interactive animations
- Custom gradients and color schemes
- Dynamic card layouts
- Responsive design for various screen sizes

## Setup

### Backend Setup
1. Install required Python packages:
bash
pip install pydub pymysql requests

2. Configure email settings in `new_density_sensor.py`:
python
"email": {
"sender": "your.email@gmail.com",
"password": "your-app-specific-password",
"recipients": ["recipient@email.com"],
"smtp_server": "smtp.gmail.com",
"smtp_port": 587
}

3. Configure ThingsBoard and MySQL settings

### Frontend Setup
1. Host the web files on a web server
2. Ensure all dependencies are loaded:
   - Leaflet.js for maps
   - Chart.js for visualizations
   - Custom fonts (Rajdhani, Audiowide)

## Usage

### Running the Monitoring System
bash
Start the sensor monitoring
python new_detection.py

### Accessing the Dashboard
- Open `index.html` in a web browser
- Dashboard will automatically update every 5 seconds
- Monitor real-time metrics and alerts
- View crowd density heat maps
- Track historical trends

## Thresholds and Alerts
- Noise Level: > 45 dB triggers alert
- Light Level: -10% change triggers alert
- Proximity: -3% change triggers alert
- Window Size: 10 readings for moving average

## Data Flow
1. Sensors collect raw data
2. Data processed by density sensor script
3. Detection script analyzes patterns
4. Alerts triggered if thresholds exceeded
5. Data visualized on web dashboard
6. Email alerts sent to configured recipients

## Technologies Used
- Python for backend processing
- JavaScript for frontend interactivity
- Leaflet.js for mapping
- Chart.js for data visualization
- ThingsBoard for IoT data platform
- MySQL for data storage
