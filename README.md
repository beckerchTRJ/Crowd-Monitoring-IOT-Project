# Crowd Monitoring IOT Project

## Overview
Real-time crowd density monitoring system using IoT sensors and web dashboard.

## Features
- Light level monitoring
- Sound level detection
- Proximity sensing
- Email alerts for dangerous conditions
- Web dashboard visualization
- ThingsBoard integration

## Components
- `density.py`: Original sensor data collection
- `new_density_sensor.py`: Updated sensor data collection with email configuration
- `new_detection.py`: Monitoring and alert system
- `index.html`: Web dashboard interface
- `script.js`: Dashboard functionality
- `styles.css`: Dashboard styling

## Setup
1. Install required Python packages
2. Configure email settings in new_density_sensor.py
3. Set up ThingsBoard credentials
4. Run new_detection.py for monitoring

## Usage
```bash
python new_detection.py
```
