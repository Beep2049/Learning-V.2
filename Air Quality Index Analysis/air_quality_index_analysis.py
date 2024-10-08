import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default ='plotly_white'

# Importing the Dataset
data = pd.read_csv(r"C:\Users\ebello\OneDrive - United Against Poverty\Desktop\D.A.P\delhiaqi.csv")
print(data.head())


# Descriptive look at the Data
print(data.describe())


# Time Series for each Air Pollutant
fig = go.Figure()

for pollutant in ['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']:
    fig.add_trace(go.Scatter(x=data['date'], y=data[pollutant], mode='lines', name=pollutant))

fig.update_layout(title='Time Series Analysis of Air Pollutants in Delhi',
                  xaxis_title='Date', yaxis_title='Concentration (µg/m³)')
fig.show()


# Calculating Air Quality Index


# Define AQI Breakpoint and corresponding AQI values
aqi_breakpoints = [
    (0, 9.0, 50), (9.1, 35.4, 100),(35.5, 54.4, 150),
    (55.5, 125.4, 200), (125.5, 225.4, 300),(225.5, 325.4, 500),
    (325.5, 500.4, 500)
]


# Calculate AQI for each Row
def calculate_aqi(pollutant_name, concentration):
    for low, high, aqi in aqi_breakpoints:
        if low <= concentration <= high:
            return aqi
    return None


def calculate_overall_aqi(row):
    aqi_values = []
    pollutants = ['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']
    for pollutant in pollutants:
        aqi = calculate_aqi(pollutant, row[pollutant])
        if aqi is not None:
            aqi_values.append(aqi)
    return max(aqi_values)


# Define AQI Categories
data['AQI'] = data.apply(calculate_overall_aqi, axis=1)

aqi_categories = [
    (0, 50, 'Good'), (51, 100, 'Moderate'), (101, 150, 'Unhealthy for Sensitive Groups'),
    (151, 200, 'Unhealthy'), (201, 300, 'Very Unhealthy'), (301, 500, 'Hazardous')
]

def categorize_aqi(aqi_value):
    for low, high, category in aqi_categories:
        if low <= aqi_value <= high:
            return category
    return None


# Categorize AQI
data['AQI Category'] = data['AQI'].apply(categorize_aqi)
print(data.head())


# AQI over time
fig = px.bar(data, x='date', y='AQI',
             title='AQI of Delhi in January')
fig.update_xaxes(title='Date')
fig.update_yaxes(title='AQI')
fig.show()

# Category Distribution over time
fig = px.histogram(data, x='date',
                   color='AQI Category',
                   title='AQI Category Distribution Over Time')
fig.update_xaxes(title='Date')
fig.update_yaxes(title="Count")
fig.show()

# Define pollutants and assigning their colors
pollutants = ['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']
pollutant_colors = px.colors.qualitative.Plotly


# Calculating the sum of pollutant concentrations
total_concentrations = data[pollutants].sum()


# Create a DataFrame for the concentrations
concentration_data = pd.DataFrame({
    "Pollutant": pollutants,
    "Concentration": total_concentrations
})

# Creating a donut chart for pollutant concentrations
fig = px.pie(concentration_data, names="Pollutant", values="Concentration",
             title='Pollutant Concentration in Delhi',
             hole=0.4, color_discrete_sequence=pollutant_colors)


# Update layout for the donut chart
fig.update_traces(textinfo='percent+label')
fig.update_layout(legend_title='Pollutant')


# Show
fig.show()


# Correlation between pollutants
correlation_matrix = data[pollutants].corr()
fig = px.imshow(correlation_matrix, x=pollutants,
                y=pollutants, title='Correlation Between Pollutants')
fig.show()

# Extracting the hour from the date column
data['Hour'] = pd.to_datetime(data['date']).dt.hour


# Calculate hourly average AQI
hourly_avg_aqi = data.groupby('Hour')['AQI'].mean().reset_index()


# Create a line plot for hourly trends in AQI
fig = px.line(hourly_avg_aqi, x='Hour', y='AQI',
              title='Hourly Average AQI Trends in Delhi (Jan 2023)')
fig.update_xaxes(title='Hour of the Day')
fig.update_yaxes(title='Average AQI')
fig.show()


# Average AQI by Day of the Week
data['Day_of_week'] = data['date'].dt.day_name()
average_aqi_by_day = data.groupby('Day_of_week')['AQI'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday'])
fig = px.bar(average_aqi_by_day, x=average_aqi_by_day.index, y='AQI',
             title='Average AQI by the day of the week')
fig.update_xaxes(title='Day of the Week')
fig.update_yaxes(title='Average AQI')
fig.show()