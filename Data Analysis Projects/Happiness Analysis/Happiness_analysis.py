# Importing data and creating one usable dataset

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Intializing the dataframe
df = pd.DataFrame()

# Creating a year column and merging the data to one dataset
for year in range(2015, 2024):
    filename = f'...\\Happiness_analysis\\WHR_{year}.csv'
    data = pd.read_csv(filename)
    data['year'] = year
    df = pd.concat([df, data], ignore_index=True)

print(df.head())

# Converting to a new excel file
df.to_csv("Happiness_Data(2015-2023).csv", index=False)


# Renaming the data for readability purposes
happy_data = pd.read_csv(r"...\Happiness_Data(2015-2023).csv")
print(happy_data.head())


# Size of the data
print(happy_data.shape)


# Types of data
print(happy_data.info())


# Checking for Null values
print(happy_data.isnull().sum())


# Distribution of Happiness Score

plt.figure(figsize=(10,6))
sns.histplot(data=happy_data, x='happiness_score', bins=20, kde=True)
plt.title("Distribution of happiness score")
plt.xlabel("Happiness Score")
plt.ylabel("Frequency")
plt.show()


# Average rating over the years

avg_score_yearly = happy_data.groupby(['year']).agg(happiness_score_mean=('happiness_score', 'mean')).reset_index()

fig = px.line(
    avg_score_yearly,
    x='year',
    y='happiness_score_mean',
    markers=True
)

fig.update_layout(
    yaxis_range =[4,7],
    title={
        'text': 'Mean Happiness Change Over Years',
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title ='Years',
    yaxis_title ='Mean Happiness Score'
)

fig.show()


# Countries with the highest average happiness score

happiness_by_country =  happy_data.groupby(['country']).agg(happiness_score_mean=("happiness_score", "mean")).reset_index()
sorted_country = happiness_by_country.sort_values(by='happiness_score_mean', ascending=False).head(20)

fig = px.bar(
    sorted_country,
    x='country',
    y='happiness_score_mean',
    color='happiness_score_mean'
)

fig.update_layout(
        yaxis_range = (0,10),
    title={
        'text': 'Top 20 Happiest Countries(average)',
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title ='Country',
    yaxis_title ='Mean Happiness Score'
)


# Region with the highest average happiness score

happiness_by_region = happy_data.groupby(['region']).agg(happiness_score_mean=('happiness_score', 'mean')).reset_index()
sorted_region = happiness_by_region.sort_values(by='happiness_score_mean', ascending=False)

fig = px.bar(
    sorted_region,
    x='region',
    y='happiness_score_mean',
    color="happiness_score_mean"
)

fig.update_layout(
    yaxis_range = (0,10),
    title={
        'text': 'Average Happiness by Region',
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title ='Region',
    yaxis_title ='Mean Happiness Score'
)
fig.show()


# Change of Happiness Over Time
region_happiness_over_time = happy_data.groupby(['region', 'year'])['happiness_score'].mean().reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(
    data=region_happiness_over_time,
    x='year',
    y='happiness_score',
    hue='region',
    markers='o',
    linewidth=2.5,
)

plt.title('Average Happiness Score by Region Over Time')
plt.xlabel('Year')
plt.ylabel('Average Happiness Score')
plt.legend(title='region')
plt.grid(True)

plt.legend(
    title='Region',
    loc='upper left',
    bbox_to_anchor=(1,1),
    fontsize='small',
    title_fontsize='medium'
)

plt.show()


# Finding correlation between the different variables and Happiness

happy_correlation = happy_data.drop(['year'], axis=1, inplace=True)

plt.figure(figsize=(10,10))
sns.heatmap(happy_data.corr(numeric_only=True),cmap= 'viridis', annot=True, cbar=False)
plt.show()


# Individual Factors of Happiness

sns.pairplot(happy_data, hue='region', 
             x_vars=['gdp_per_capita', 
                     'social_support', 
                     'healthy_life_expectancy',
                    'freedom_to_make_life_choices', 
                    'generosity', 
                    'perceptions_of_corruption'], 
            y_vars=['happiness_score'],
            kind='scatter'
)

plt.suptitle='Correlation Among Factors by Region'
plt.show()


# Contribution each factor has on happiness

happy_factor_columns= ['gdp_per_capita', 'social_support', 'healthy_life_expectancy', 'freedom_to_make_life_choices','generosity', 'perceptions_of_corruption']
happy_factor_contributions = happy_data[happy_factor_columns].mean().sort_values(ascending=False)
happy_factor_contributions.plot(kind='bar', color='red')
plt.title("Average FActor Contributions to Happiness")
plt.xlabel("Factors")
plt.ylabel("Average Value")
plt.show()
