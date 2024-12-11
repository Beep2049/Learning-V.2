import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Importing the data
data = pd.read_csv(r"....\u.s_gdp_percent_change_per_quarter.csv")
print(data.head())


# Learning the shape of the dataset
print(data.shape)


# Learning what oata types are in the dataset
print(data.info())


# Learning if there are any null values in the dataset
print(data.isnull().sum())

# Plotting the dataset in matplotlib
plt.plot(data['Time Period'], data['GDP Growth'],marker='o')
plt.xlabel('Time Period')
plt.ylabel('GDP Growth Rate')
plt.xticks(rotation = 75)
plt.title('GDP Growth Rate over Time(Monthly Data)')
plt.grid(True)

plt.show()


# Creating copy for further data analysis
quarterly_data = data.copy()


# Calculate recession based on quarterly GDP growth
quarterly_data['Recession'] = ((quarterly_data['GDP Growth'] < 0) & (quarterly_data['GDP Growth'].shift(1) < 0))


# Fill missing values with False (since the first quarter cannot be in a recession)
quarterly_data['Recession'].fillna(False, inplace=True)

quarterly_data.head()


# Determing where in the dataset a recession occurred
recession_period = quarterly_data.loc[quarterly_data['Recession'] == True, 'Time Period'].tolist()
print(recession_period)

# Visualizing where in the dataset the recession occurred
recession_period = quarterly_data.loc[quarterly_data['Recession'] == True]

plt.plot(quarterly_data['Time Period'],quarterly_data['GDP Growth'], label='GDP Growth',marker='o')
plt.plot(recession_period['Time Period'], recession_period['GDP Growth'], color='Red', label='Recession', marker='X')
plt.xlabel('Time Period')
plt.ylabel('GDP Growth')
plt.xticks(rotation=75)
plt.title('GDP Growth and Recession Over Time')
plt.grid(True)
plt.legend()

plt.show()


# Analyzing the severity and duration of the recession

# Creating variables that measure the severity and duration of a recession
quarterly_data['Recession Start'] = quarterly_data['Recession'].ne(quarterly_data['Recession'].shift()).cumsum()
recession_period = quarterly_data.groupby('Recession Start')
recession_duration = recession_period.size()
recession_severity = recession_period['GDP Growth'].sum()


# Plotting the graph for visualization
x = np.arange(len(recession_duration))
width = 0.40

plt.bar(x - width/2, recession_duration, width, label='Recession Duration', color='red')
plt.bar(x + width/2, recession_severity, width, label='Recession Serverity', color='green')
plt.xticks(x)
plt.xlabel('Recession Periods')
plt.ylabel('Duration/Serverity')
plt.title('Duration and Severity of Recession')
plt.legend(loc='lower right')
plt.show()
