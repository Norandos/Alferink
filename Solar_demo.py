import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Or 'Agg', 'Qt5Agg', depending on your system
import matplotlib.pyplot as plt

# Solar Panel Parameters
P_max = 321  # Nominal power in Watts (NOCT)
I_NOCT = 800  # Light intensity at NOCT in W/m^2
temperature_coefficient = -0.0029  # Temperature coefficient (per °C)
T_ref = 20  # Reference temperature in °C (NOCT)
amount_of_panels = 385  # Amount of solar panels

# Preprocess CSV
def preprocess_csv(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Replace commas with dots and empty fields with NaN
            line = line.replace(',', '.').replace('""', 'NaN')
            outfile.write(line)

# File paths
input_file = 'report.csv'
processed_file = 'processed_report.csv'

# Preprocess the CSV file
preprocess_csv(input_file, processed_file)

# Demo file for export limit
export_limit_file = 'report(1).csv'
preprocess_csv(export_limit_file, 'processed_report(1).csv')

# Load export limit data
dg = pd.read_csv('processed_report(1).csv', delimiter=';', parse_dates=['time'], dayfirst=True)
export_limit = pd.to_numeric(dg['Export beperking'], errors='coerce')  # Export limit as percentage
export_limit.fillna(100, inplace=True)  # Replace missing export limits with 100%

# Load light intensity and temperature data
df = pd.read_csv(processed_file, delimiter=';', parse_dates=['time'], dayfirst=True)
light_intensity = pd.to_numeric(df['Lichtintensiteit zuid'], errors='coerce')  # Light intensity
T_actual = pd.to_numeric(df['Buitentemperatuur'], errors='coerce')  # Outdoor temperature

# Handle missing data
light_intensity.fillna(0, inplace=True)  # Replace missing light intensity with 0
T_actual.fillna(method='ffill', inplace=True)  # Fill temperature NaNs with the previous value

# Truncate to the smallest dataset length
n_points = min(len(light_intensity), len(export_limit))
light_intensity = light_intensity[:n_points]
T_actual = T_actual[:n_points]
export_limit = export_limit[:n_points]

# Convert light intensity from kilolux to W/m^2 and scale by number of panels
light_intensity = light_intensity * 0.0079 * 1000 * amount_of_panels # 1 lux = 0.0079 W/m^2

# Calculate Power Output
P_raw = P_max * (light_intensity / I_NOCT)  # Power generated at each time interval
P_raw = P_raw * (1 + temperature_coefficient * (T_actual - T_ref))  # Adjust for temperature
P_raw = np.clip(P_raw, 0, None)  # Set negative values to 0

# Adjust Power Output for Export Limit
export_factor = export_limit / 100.0  # Convert percentage to a multiplier
P_adjusted = P_raw * export_factor  # Apply export limit

# Calculate Energy Outputs
dt = 1 / 12  # Time interval in hours (5-minute intervals = 1/12 hour)
E_raw = np.sum(P_raw) * dt  # Total energy without export limit
E_adjusted = np.sum(P_adjusted) * dt  # Total missed energy output after export limit

# Display Results
print(f"Total Energy Output: {E_raw:.2f} Wh")
print(f"Total Energy Lost (Due to Export Limit): {E_adjusted:.2f} Wh")

# Plot Results
time = np.arange(0, n_points)  # Generate time indices as absolute numbers

plt.figure(figsize=(12, 6))
plt.plot(time, P_adjusted, '-o', label="Adjusted Power Output", markersize=4, color='green')
#plt.plot(time, P_raw, '-o', label="Raw Power Output", markersize=4, color='red')
plt.xlabel('Data Points')
plt.ylabel('Power (W)')
plt.title('Solar Panel Power Output and Energy Losses')
plt.text(time[0], P_adjusted.max(), f"Misgelopen Energie: {E_adjusted:.2f} Wh", fontsize=12, color='green')


plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
