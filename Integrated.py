import pandas as pd
from geopy.distance import geodesic
from sklearn.linear_model import Ridge
from math import pi

def create_predictions(weather, reg):
    predictors = ["tempmax", "tempmin", "dew", "humidity", "moonphase"]
    weather = weather.sort_index()
    train = weather.loc[:'31-05-2023']
    test = weather.loc['01-06-2023':]
    reg.fit(train[predictors], train["target"])
    predictions = reg.predict(test[predictors])
    combined = pd.concat([test["target"], pd.Series(predictions, index=test.index)], axis=1)
    combined.columns = ["actual", "predictions"]
    return combined.max().max()

df1 = pd.read_csv('bbmp_lakes_masterlist-final.csv')
df2 = pd.read_csv('flooding_vulnerable_locations.csv')
df3 = pd.read_csv('stp_locations.csv')  # Load the new CSV file

df2[['Longitude', 'Latitude']] = df2['WKT'].str.extract(r'POINT \((.*?) (.*?)\)')

# Convert the Longitude and Latitude columns to numeric
df2['Longitude'] = pd.to_numeric(df2['Longitude'])
df2['Latitude'] = pd.to_numeric(df2['Latitude'])

# Ensure the dataframes have 'Latitude' and 'Longitude' columns
assert 'Latitude' in df1.columns and 'Longitude' in df1.columns
assert 'Latitude' in df2.columns and 'Longitude' in df2.columns
assert 'Latitude' in df3.columns and 'Longitude' in df3.columns

# Create an empty dataframe to store the results
result_df = pd.DataFrame(columns=['average_latitude', 'average_longitude', 'Name_of_th', 'LocationName'])

# Compare each pair of coordinates
for index1, row1 in df1.iterrows():
    for index2, row2 in df2.iterrows():
        coord1 = (row1['Latitude'], row1['Longitude'])
        coord2 = (row2['Latitude'], row2['Longitude'])

        # If the distance is less than or equal to 10km
        if geodesic(coord1, coord2).km <= 10:
            # Calculate the average coordinates
            avg_latitude = (row1['Latitude'] + row2['Latitude']) / 2
            avg_longitude = (row1['Longitude'] + row2['Longitude']) / 2

            # Create a temporary DataFrame for the new row
            new_row = pd.DataFrame({
                'average_latitude': [avg_latitude],
                'average_longitude': [avg_longitude],
                'Name_of_th': [row1['Name_of_th']],
                'LocationName': [row2['LocationName']]
            })

            # Add the new row to the DataFrame if it's not empty
            if not new_row.empty:
                if result_df.empty:
                    result_df = new_row
                else:
                    result_df = pd.concat([result_df, new_row], ignore_index=True)

# After all rows have been added to result_df, remove duplicates
result_df = result_df.drop_duplicates(subset=['Name_of_th', 'LocationName'])

# Add a new column for the closest STP
result_df['Closest_STP'] = None

# Calculate maximum value
weather = pd.read_csv("2020-2024.csv", index_col="datetime")
weather.drop(columns=["windgust", "visibility", "winddir", "solarenergy", "sunrise", "sunset", "windspeed", "sealevelpressure", "solarradiation", "cloudcover", "uvindex", "severerisk", "description", "conditions", "icon"], axis=1, inplace=True)
weather.index = pd.to_datetime(weather.index, format="mixed")
weather["target"] = weather.shift(-1)["precip"]
weather = weather.iloc[:-1, :].copy()
reg = Ridge(alpha=.1)
a = create_predictions(weather, reg)

if (a>=3):  # Compare each pair of coordinates between the result_df and df3
    for index1, row1 in result_df.iterrows():
        closest_stp = None
        closest_distance = None

        for index3, row3 in df3.iterrows():
            coord1 = (row1['average_latitude'], row1['average_longitude'])
            coord3 = (row3['Latitude'], row3['Longitude'])

            # Calculate the distance
            distance = geodesic(coord1, coord3).km

            # If this is the closest STP so far, save it
            if closest_distance is None or distance < closest_distance:
                closest_stp = row3['STPName']
                closest_distance = distance

        # Add the closest STP to the result_df
        result_df.loc[index1, 'Closest_STP'] = closest_stp

    # Write result_df to a CSV file
    result_df.to_csv('output.csv', index=False)

# Now you can use 'a' anywhere in your code as needed
print("Maximum Combined Value:", a)
