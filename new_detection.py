from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from collections import deque
import time
from new_density_sensor import (
    CONFIG, record_audio, convert_to_wav, analyze_audio, 
    get_sensor_data, send_data_to_thingsboard
)

def calculate_moving_average(values):
    if not values:
        return None
    return sum(values) / len(values)

def send_email_alert(subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = CONFIG["email"]["sender"]
        msg['To'] = ", ".join(CONFIG["email"]["recipients"])
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP(CONFIG["email"]["smtp_server"], CONFIG["email"]["smtp_port"])
        server.starttls()
        server.login(CONFIG["email"]["sender"], CONFIG["email"]["password"])
        server.send_message(msg)
        server.quit()
        print("Alert email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def monitor_sensors():
    # Initialize moving average queues
    light_values = deque(maxlen=CONFIG["thresholds"]["window_size"])
    proximity_values = deque(maxlen=CONFIG["thresholds"]["window_size"])
    last_status_time = time.time()
    danger_detected = False
    
    try:
        while True:
            current_time = time.time()
            
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

                # Update moving averages
                light_values.append(light_level)
                proximity_values.append(proximity_value)
                
                # Prepare data for ThingsBoard
                sensor_data = {
                    "light_level": light_level,
                    "proximity_value": proximity_value
                }
                if noise_level:
                    sensor_data["noise_level"] = noise_level
                
                # Send to ThingsBoard
                send_data_to_thingsboard(sensor_data)
                
                # Check for alerts if we have enough data points
                if len(light_values) == CONFIG["thresholds"]["window_size"]:
                    light_avg = calculate_moving_average(light_values)
                    proximity_avg = calculate_moving_average(proximity_values)
                    
                    # Calculate percentage changes
                    light_change = ((light_level - light_avg) / light_avg) * 100
                    proximity_change = ((proximity_value - proximity_avg) / proximity_avg) * 100
                    
                    # Check for alert conditions
                    danger_detected = (
                        noise_level and 
                        noise_level > CONFIG["thresholds"]["noise_spike"] and 
                        light_change < CONFIG["thresholds"]["light_drop"] and 
                        proximity_change < CONFIG["thresholds"]["proximity_drop"]
                    )
                    
                    # Send additional status to ThingsBoard
                    send_data_to_thingsboard({
                        "danger_detected": danger_detected,
                        "light_change": light_change,
                        "proximity_change": proximity_change
                    })
                    
                    if danger_detected:
                        alert_message = f"""
                        Alert: Large Crowd Detected!Avoid if possible
                        
                        Noise Level: {noise_level:.2f} dB
                        Light Level Change: {light_change:.2f}%
                        Proximity Change: {proximity_change:.2f}%
                        
                        Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
                        """
                        
                        send_email_alert("Sensor Alert - Suspicious Activity", alert_message)
            
            # Print status every 5 seconds
            if current_time - last_status_time >= 5:
                status_message = (
                    "\n🚨 DANGER DETECTED! 🚨" if danger_detected 
                    else "\n✅ Status: Normal - No Danger Detected"
                )
                print(f"{status_message}")
                print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                if noise_level:
                    print(f"Current Noise Level: {noise_level:.2f} dB")
                print("-" * 50)
                last_status_time = current_time

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nGracefully shutting down...")
    except Exception as e:
        print(f"Error in monitoring loop: {e}")

if __name__ == "__main__":
    monitor_sensors()

