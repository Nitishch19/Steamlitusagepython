# Create complete Arduino sensor monitoring Streamlit app
# This will create a comprehensive dashboard for monitoring LDR and DHT11 sensor data

import pandas as pd
import numpy as np

# Create sample sensor data to simulate what would come from Arduino
np.random.seed(42)

# Generate sample data for demonstration (in real scenario this would come from serial communication)
timestamps = pd.date_range('2024-10-15 14:00:00', periods=100, freq='10S')
light_values = np.random.randint(0, 1023, 100)  # LDR values (0-1023)
temperature = 20 + 10 * np.random.random(100)  # DHT11 temperature (20-30°C)
humidity = 40 + 20 * np.random.random(100)  # DHT11 humidity (40-60%)

# Create sample data
sample_data = pd.DataFrame({
    'timestamp': timestamps,
    'light_intensity': light_values,
    'temperature': temperature,
    'humidity': humidity
})

# Save sample data for the Streamlit app to use
sample_data.to_csv('sensor_data.csv', index=False)
print("Sample sensor data created and saved to sensor_data.csv")
print(sample_data.head())