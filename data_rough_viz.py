# Name: Dong Han
# Student ID: 202111878
# Mail: dongh@mun.ca
import re

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#############################################    DATA ROUGH VIZ    #############################################
## Generate a Image consisted of Job tiles with different frequency
## Also generate the Job Density map
def ciyun(dataPath):
    from wordcloud import WordCloud
    import stylecloud

    df = pd.read_csv(dataPath)
    text = ' '.join(df['Title'].dropna().tolist())

    # Generate a word cloud image
    wordcloud = WordCloud(background_color='white').generate(text)

    # Display the generated image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Hide the axes
    plt.show()

    stylecloud.gen_stylecloud(text=text,
                              icon_name='fas fa-frown', # Choose an icon from FontAwesome
                              palette='colorbrewer.diverging.Spectral_11',  # Color palette
                              background_color='white',
                              gradient='horizontal',  # Gradient direction
                              size=1024)  # Image size

def add_coord(dataPath):
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
    # Initialize the geocoder
    geolocator = Nominatim(user_agent="jobAreaDemandAnalysis", timeout=10)

    # Use rate limiter to avoid overloading the API service
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    df = pd.read_csv(dataPath)

    # Define a function to apply geocoding
    def geocode_location(location, geocode_cache):

        if "remote" in location or "Remote" in location:
            match = re.search(r'in\s+([A-Za-z\s\'.]+,\s+[A-Z]{2})', location)
            location = match.group(1).strip() if match else "St.John's"

        # Check the cache first
        if location in geocode_cache:
            return geocode_cache[location]

        try:
            location_result = geocode(location)
            if location_result:
                geocode_cache[location] = (location_result.latitude, location_result.longitude)
                return location_result.latitude, location_result.longitude
        except Exception as e:
            print(f"Error geocoding {location}: {e}")
            # If geocoding fails, return NaN values
        geocode_cache[location] = (pd.NA, pd.NA)
        return pd.NA, pd.NA

    geocode_cache = {}
    # Apply the function to your 'Location' column
    df['Latitude'], df['Longitude'] = zip(*df['Location'].apply(lambda loc: geocode_location(loc, geocode_cache)))

    # Save the DataFrame with the new latitude and longitude data
    df.to_csv('jobs_with_coordinates.csv', index=False)
    return 'jobs_with_coordinates.csv'

def city_job_density(dataPath):
    df = pd.read_csv(dataPath)

    # Aggregate job counts by location
    job_counts = df.groupby(['Latitude', 'Longitude']).size().reset_index(name='Job Count')

    # Create a weighted map where the circle size and color intensity depend on the job count
    fig = px.density_mapbox(job_counts, lat='Latitude', lon='Longitude', z='Job Count',
                            radius=40,  # This sets the radius of influence of each point
                            center=dict(lat=0, lon=180), zoom=0,
                            mapbox_style="open-street-map"
                            )

    fig.show()

#############################################    MAIN    #############################################
def main():
    # # Visulization
    dataPath = "cleaned_xx_jobs.csv"
    ciyun(dataPath)

    newDataWcoord = add_coord(dataPath) #'jobs_with_coordinates.csv'
    city_job_density('jobs_with_coordinates.csv')

if __name__ == '__main__':
    main()