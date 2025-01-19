import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Or 'Agg', 'Qt5Agg', depending on your system
import matplotlib.pyplot as plt

# Original data for Building A
data = {
    'month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'generated_kwh': [
        1245.8249984400027, 2716.2750007499853, 5206.800000069998, 8563.500009900017,
        12422.250011630022, 13765.57499645, 13237.64997920995, 8970.074988159933,
        7299.900001130009, 3633.22499632003, 1635.0750044900342, 821.2499997699633
    ],
    'consumption_kwh': [
        20692.552058400062, 17757.562031700043, 19765.793057489907, 12843.537025180063,
        11116.710010960058, 18039.977001239953, 12436.120971489872, 9014.50597754016,
        15779.806990099954, 11757.95300706994, 18861.22905676003, 16967.646026179893
    ]
}

# Convert original data to a DataFrame
df = pd.DataFrame(data)

# Calculate total consumption and generation for Building A
total_consumption_A = df['consumption_kwh'].sum()
total_generation_A = df['generated_kwh'].sum()

# Total consumption and generation for Building B (given)
total_consumption_B = 289000
total_generation_B = 90920

# Calculate estimated monthly consumption for Building B
df['estimated_consumption_B'] = (df['consumption_kwh'] / total_consumption_A) * total_consumption_B

# Calculate estimated monthly generation for Building B
df['estimated_generation_B'] = (df['generated_kwh'] / total_generation_A) * total_generation_B

# Load data from CSV
csv_file = """time;Elektra Gebouwgebonden;PV Opgewekte energie totaal
"01/2024";0;0
"02/2024";0;0
"03/2024";0;0
"04/2024";2064;0
"05/2024";8611;23753,04734010001
"06/2024";11127;27095,851122600012
"07/2024";10066;18504,712281899978
"08/2024";5687;10496,84760930005
"09/2024";10341;16528,858819200017
"10/2024";9814;12145,381665299967
"11/2024";15287;5113,950433800041
"12/2024";17633;2862,7354859999905
"""

from io import StringIO

csv_df = pd.read_csv(StringIO(csv_file), sep=';', decimal=',', quotechar='"')

# Process the CSV data
csv_df['month'] = csv_df['time'].str[:2].replace({
    '01': 'January', '02': 'February', '03': 'March', '04': 'April',
    '05': 'May', '06': 'June', '07': 'July', '08': 'August',
    '09': 'September', '10': 'October', '11': 'November', '12': 'December'
})
csv_df.rename(columns={
    'Elektra Gebouwgebonden': 'consumption_kwh',
    'PV Opgewekte energie totaal': 'generated_kwh'
}, inplace=True)

# Sort the DataFrame by month (to match plotting order)
csv_df['month_order'] = pd.Categorical(csv_df['month'], categories=data['month'], ordered=True)
csv_df.sort_values(by='month_order', inplace=True)

# Plotting
plt.figure(figsize=(10, 6))

# Original Building A and B data
#plt.plot(df['month'], df['consumption_kwh'], marker='o', color='tab:red', label='Consumption (kWh) - Citadel 2023')
#plt.plot(df['month'], df['generated_kwh'], marker='o', color='tab:blue', label='Generation (kWh) - Citadel 2023')
plt.plot(df['month'], df['estimated_consumption_B'], marker='o', color='tab:orange', linestyle='--', label='Estimated Consumption (kWh) - Passie')
plt.plot(df['month'], df['estimated_generation_B'], marker='o', color='tab:green', linestyle='--', label='Estimated Generation (kWh) - Passie')

# CSV data
plt.plot(csv_df['month'], csv_df['consumption_kwh'], marker='o', color='tab:red', label='Consumption (kWh) - De Passie 2024')
plt.plot(csv_df['month'], csv_df['generated_kwh'], marker='o', color='tab:blue', label='Generation (kWh) - De Passie 2024')

# Labels and title
plt.xlabel('Month')
plt.ylabel('Energy (kWh)')
plt.title('Actual and estimated consumption and generation of De Passie')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Add legend
plt.legend()

# Grid for easier interpretation
plt.grid(True)

# Layout adjustment to ensure everything fits
plt.tight_layout()

# Show the plot
plt.show()
