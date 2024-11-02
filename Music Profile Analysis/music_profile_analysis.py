import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Importing the Data
df = pd.read_csv(r'C:\Users\ebello\OneDrive - United Against Poverty\Desktop\D.A.P\FuckItMusic-music-export.csv')
print(df.head())

# Columns and Objects
print(df.shape)

# Types of Data
print(df.dtypes)

# More descriptions of the data
print(df.info())

# Checking if any values are null
df.isnull().sum()

# Dropping columns with empty values
df.drop(columns=['Ownership', 'Purchase Date', 'Media Type'], inplace=True)
df.head()


# Data Cleaning #


# Creating a new column "Artist Name"
df['Artist Name'] = df[' First Name'].astype(str) + ' ' +  df['Last Name']

# Creating a new column " Localized Name" for special cases
df['Localized Name'] = df['First Name localized'] + ' ' + df[' Last Name localized']

# Dropping null columns
df.drop(columns=[' First Name', 'Last Name', 'First Name localized', ' Last Name localized'],inplace=True)

# Renaming column for clarity
df.rename(columns= {'Release_Date': 'Year_Of_Release'}, inplace=True)

# Clearing spaces and NaN values in Artist Name column
df['Artist Name'] = df['Artist Name'].str.lstrip('nan')
df['Artist Name'] = df['Artist Name'].str.strip()

# Replacing special characters with their appropriate replacement for readability
df['Artist Name'].replace('&amp;', 'and', regex=True, inplace=True)
df['Artist Name'] = df['Artist Name'].apply(lambda x: x.replace('$', 's') if '$' in x else x)

# Replacing odd names with their appropriate replacement
df['Artist Name'].replace('Илья Рачковский', 'Ilya Rachkovsky', regex=True, inplace=True)
df['Artist Name'].replace('AsAp Ferg', 'ASAP Ferg', regex=True, inplace=True)

# Finally, dropping the Localized Name column for being redundant
df.drop(columns=['Localized Name'],inplace=True)

# Viewing the cleaned dataset
df.head()

# Pie Chart for distribution of ratings
fig = px.pie(
    df, 
    names='Rating',
    height=600,
    width=1000,
    title="Distribution of Ratings",)
fig.update_traces(textposition = 'inside', textinfo = 'percent+label')
fig.show()

# The mean rating of the dataset
mean_rating = df['Rating'].mean()
print(mean_rating)

# Finding the mean rating by decade
avg_by_decade = df.groupby((df.Year_Of_Release//10)*10)['Rating'].mean().reset_index()
fig = px.bar(
    x=avg_by_decade['Year_Of_Release'], 
    y=avg_by_decade['Rating'],
    labels={'y':'Rating Scale', 'x':'Decade'}, 
    title='Average Rating By Decade'
)
fig.show()


# Scatter Plot Creation #


# Defining a threshold 
rating_threshold = 1

# Grouping Artist by the amount of ratings they have
total_ratings = df.groupby(['Artist Name']).agg(Rating_count=('Rating', 'count')).reset_index()

# Eliminating artist that fall below the threshold
sorted_ratings = total_ratings[total_ratings['Rating_count'] > rating_threshold]

# Creating custom hover text
sorted_ratings['hover text'] = sorted_ratings.apply(
    lambda row: f'Artist: {row['Artist Name']}<br>Rating Count: {row['Rating_count']}', axis=1
)

# Graphing the data
fig = go.Figure(go.Scatter(
    mode='markers',
    x=sorted_ratings.index,
    y=sorted_ratings['Rating_count'],
    marker_color=sorted_ratings['Rating_count'],
    marker_size=10,
    text=sorted_ratings['hover text'],
    hoverinfo='text'

))

# Updating the labels for readability
fig.update_layout(
    title={
        'text': 'Total Artist Ratings',
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.9,
        'yanchor': 'top'    
    },
    xaxis_title = 'Artist',
    yaxis_title = 'Rating Count'
)

# Showing the graph
fig.show()


# Scatter Plot to show the Artist with the highest mean rating #


# Threshold based on the 5 album rule(Great artist at least have 5 good albums)
rating_threshold = 5

# Grouping Artist based on their mean rating and the total count of ratings
artist_average = df.groupby(['Artist Name']).agg(
    Rating_count=('Rating', 'count'),
    Rating_mean=('Rating', 'mean')
).reset_index()

# Filtering based on rating threshold
average_threshold = artist_average[artist_average['Rating_count'] >= rating_threshold]

# Sorting by Rating_mean in descending order
average_threshold_sorted = average_threshold.sort_values(by='Rating_mean', ascending=True)

# Creating custom hover text
average_threshold_sorted['hover_text'] = average_threshold_sorted.apply(
    lambda row: f"Artist: {row['Artist Name']}<br>Rating Mean: {row['Rating_mean']}", axis=1
)

# Creating the scatter plot
fig = go.Figure(go.Scatter(
    mode="markers",
    x=average_threshold_sorted.index, 
    y=average_threshold_sorted['Rating_mean'],  
    marker_symbol='circle',
    marker_color=average_threshold_sorted['Rating_mean'],  
    marker_size=12,
    text=average_threshold_sorted['hover_text'], 
    hoverinfo='text'
))

# Updating layout for readability
fig.update_layout(
    title={
        'text': 'Artist Rating Mean (Sorted)',
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.90,
        'yanchor': 'top'    
    },
    xaxis_title='Artists',
    yaxis_title='Rating Mean',
)
    
# Showing the graph
fig.show()


# Boxplot Creation for total visualization of the data #


# Grpuping data by the Decade of music
the_50s = df[(df['Year_Of_Release']>= 1950) & (df['Year_Of_Release'] < 1960)]
the_60s = df[(df['Year_Of_Release']>= 1960) & (df['Year_Of_Release'] < 1970)] 
the_70s = df[(df['Year_Of_Release']>= 1970) & (df['Year_Of_Release'] < 1980)]
the_80s = df[(df['Year_Of_Release']>= 1980) & (df['Year_Of_Release'] < 1990)]
the_90s = df[(df['Year_Of_Release']>= 1990) & (df['Year_Of_Release'] < 2000)]
the_00s = df[(df['Year_Of_Release']>= 2000) & (df['Year_Of_Release'] < 2010)]
the_10s = df[(df['Year_Of_Release']>= 2010) & (df['Year_Of_Release'] < 2020)]
the_20s = df[(df['Year_Of_Release']>= 2020) & (df['Year_Of_Release'] < 2030)]

# Grouping Data Together
decades_of_music = [the_50s, the_60s,the_70s, the_80s, the_90s, the_00s, the_10s, the_20s]

# Labels
decade_labels = ['1950\'s', '1960\'s', '1970\'s', '1980\'s', '1990\'s', '2000\'s', '2010\'s', '2020\'s']

# Graph the data
fig = go.Figure()

for data, label in zip(decades_of_music, decade_labels):
    fig.add_trace(go.Box(
        y=data['Rating'], 
        name=label,                
        boxmean='sd',                  
        line=dict(width=2),            
        marker=dict(size=6),          
        boxpoints='all',               
    ))

# Updating labels for readability
fig.update_layout(
    title_text = 'Distribution of Ratings(by Decade)',
    xaxis_title = 'Decades Of Music',
    yaxis_title = 'Rating Score',
)

# Showing the data
fig.show()
