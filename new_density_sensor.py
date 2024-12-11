from pydub import AudioSegment
import pymysql
import json
import subprocess
import requests
import time
import os
from math import log10

# Configuration
CONFIG = {
    "thingsboard": {
        "url": "http://18.207.96.176:8080/api/v1/OtNrLFgKUauDVNTQa7cW/telemetry",
        "headers": {"Content-Type": "application/json"}
    },
    "mysql": {
        "host": "3.94.116.31",
        "user": "sensor_user",
        "password": "wangshihaoW721@",
        "db": "sensor_data"
    },
    "audio": {
        "raw_file": "/data/data/com.termux/files/home/noise_sample.mp4",
        "wav_file": "/data/data/com.termux/files/home/noise_sample.wav"
    },
       "email": {
        "sender": "youremail@gmail.com",
        "password": "",  # Generate this from Google Account settings
        "recipients": ["youremail@gmail.com"],
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 
    },
    "thresholds": {
        "noise_spike": 45,  # dB threshold for noise spike
        "light_drop": -10,  # percentage drop threshold
        "proximity_drop": -3,  # percentage drop threshold
        "window_size": 10  # size of moving average window
    }
    
}

# MySQL Connection
def connect_to_mysql():
    try:
        return pymysql.connect(
            host=CONFIG["mysql"]["host"],
            user=CONFIG["mysql"]["user"],
            password=CONFIG["mysql"]["password"],
            db=CONFIG["mysql"]["db"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
    except Exception as e:
        print(f"Failed to connect to MySQL: {e}")
        return None

# Insert data into MySQL
def insert_data_into_mysql(light_level, proximity_value, noise_level=None):
    try:
        connection = connect_to_mysql()
        if connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO sensor_data (light_level, proximity_value, noise_level) VALUES (%s, %s, %s)"
                cursor.execute(query, (light_level, proximity_value, noise_level))
                connection.commit()
                print("Data inserted into MySQL successfully!")
            connection.close()
    except Exception as e:
        print(f"Error inserting data into MySQL: {e}")

# Send data to ThingsBoard
def send_data_to_thingsboard(data):
    try:
        response = requests.post(
            CONFIG["thingsboard"]["url"], 
            headers=CONFIG["thingsboard"]["headers"], 
            json=data,
            timeout=5
        )
        response.raise_for_status()
        print("Data sent to ThingsBoard successfully!")
    except requests.Timeout:
        print("Timeout while sending data to ThingsBoard")
    except requests.RequestException as e:
        print(f"Error sending data to ThingsBoard: {e}")

# Audio Recording Functions
def record_audio(duration=5):
    try:
        raw_file = CONFIG["audio"]["raw_file"]
        
        # Clean up any existing recording
        subprocess.run(["termux-microphone-record", "-q"], check=False)
        
        if os.path.exists(raw_file):
            os.remove(raw_file)
            
        # Start recording
        subprocess.run(["termux-microphone-record", "-f", raw_file, "-l", str(duration)], check=True)
        
        # Wait for recording to complete
        time.sleep(duration + 1)
        
        # Stop recording
        subprocess.run(["termux-microphone-record", "-q"], check=True)
        
        if os.path.exists(raw_file):
            return raw_file
        else:
            print("Recording file not created")
            return None
            
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None
def convert_to_wav(input_file, output_file):
    try:
        if os.path.exists(output_file):
            os.remove(output_file)
        subprocess.run([
            "ffmpeg", "-y", "-i", input_file, "-ar", "44100", "-ac", "2",
            "-c:a", "pcm_s16le", output_file
        ], check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error converting to WAV: {e}")
        return None
def analyze_audio(file_path):
    try:
        audio = AudioSegment.from_file(file_path, format="wav")
        # Get raw audio data
        samples = audio.get_array_of_samples()
        
        # Calculate RMS without numpy
        squared_sum = sum(float(sample * sample) for sample in samples)
        mean_squared = squared_sum / len(samples)
        rms = (mean_squared ** 0.5)
        
        # Calculate decibels
        decibels = 20 * log10(rms + 1e-6)
        return decibels
    except Exception as e:
        print(f"Error analyzing audio: {e}")
        return None
def get_sensor_data(sensor_type):
    try:
        result = subprocess.run(
            ["termux-sensor", "-s", sensor_type, "-n", "1"],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing sensor command: {e}")
        return None

def main():
    try:
        while True:
            # Record and analyze audio
            print("Recording audio...")
            recorded_file = record_audio(duration=5)
            noise_level = None
            
            if recorded_file:
                print("Converting to WAV...")
                time.sleep(10)  # Wait for recording to complete
                wav_file = CONFIG["audio"]["wav_file"]
                converted_file = convert_to_wav(recorded_file, wav_file)
                
                if converted_file:
                    print("Analyzing audio...")
                    noise_level = analyze_audio(converted_file)
                    print(f"Noise Level: {noise_level:.2f} dB")

            # Get Light and Proximity Sensor Data
            light_data = get_sensor_data('stk33562_l')
            proximity_data = get_sensor_data('stk33562_p')

            if light_data and proximity_data:
                light_level = light_data["stk33562_l"]["values"][0]
                proximity_value = proximity_data["stk33562_p"]["values"][0]

                # Prepare data payload
                sensor_data = {
                    "light_level": light_level,
                    "proximity_value": proximity_value
                }
                if noise_level:
                    sensor_data["noise_level"] = noise_level

                # Send to ThingsBoard
                send_data_to_thingsboard(sensor_data)
                
                # Insert into MySQL
                insert_data_into_mysql(light_level, proximity_value, noise_level)
            
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nGracefully shutting down...")
    except Exception as e:
        print(f"Error in main loop: {e}")

if __name__ == "__main__":
    main()





