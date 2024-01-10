import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import folium
from streamlit_folium import folium_static

def fetch_data():
    conn = psycopg2.connect(
        host="localhost",
        database="Air",
        user="postgres",
        password="Sukan@01"
    )

    address_query = "select listing_id, name, street, country, country_code, latitude, longitude from address_details"
    address_data = pd.read_sql(address_query, conn)

    price_query = "select listing_id , name , price from price_details"
    price_data = pd.read_sql(price_query, conn)

    amenities_query = """
    SELECT 
        listing_id, 
        tv, 
        wifi, 
        "Air Conditioning" AS air_conditioning, 
        pool, 
        kitchen, 
        refrigerator, 
        gym, 
        "24-hour Check-in" AS "24-hour_check_in", 
        "Pets Allowed" AS pets_allowed, 
        "Wheelchair Accessible" AS wheelchair_accessible 
    FROM amenities_details
    """
    amenities_data = pd.read_sql(amenities_query, conn)

    review_query = """
        SELECT 
    listing_id, 
    number_of_reviews,
    review_scores_accuracy AS accuracy,
    review_scores_cleanliness AS cleanliness,
    review_scores_checkin AS checkin,
    review_scores_communication AS communication,
    review_scores_location AS location,
    review_scores_value AS value,
    review_scores_rating AS rating
FROM review_details

        """
    review_data = pd.read_sql(review_query, conn)
    data = pd.merge(address_data, price_data, on='listing_id', how='left')
    data = pd.merge(data, amenities_data, on='listing_id', how='left')
    data = pd.merge(data, review_data, on='listing_id', how='left')
    data['price_name'] = data['name_y'].combine_first(data['name_x'])

    conn.close()
    return data

def main():
    st.title(" Find Your AirBnB ")

    # Fetch data from PostgreSQL
    df = fetch_data()

    # Extract country from location
    countries = df['country'].unique()
    selected_country = st.selectbox("Select your desired country", countries)

    # Filter data based on selected country
    filtered_data = df[df['country'] == selected_country]

    # Exclude specific columns from amenities_columns
    exclude_columns = ['country', 'street', 'country_code']
    amenities_columns = [col for col in df.columns if col not in exclude_columns and col not in ['listing_id', 'name_x', 'name_y', 'price', 'price_name', 'latitude', 'longitude']]

    # Multi-select for amenities
    selected_amenities = st.multiselect("Select your desired amenities", amenities_columns, default=[])

    # Price filter
   
    max_price = st.slider("Select maximum price", min_value=df['price'].min(), max_value=df['price'].max(), value=df['price'].max())

    # Filter data based on selected amenities and price
    for amenity in selected_amenities:
        if amenity in filtered_data.columns:
            filtered_data = filtered_data[filtered_data[amenity]]

    filtered_data = filtered_data[ (filtered_data['price'] <= max_price)]

    # Filter out rows with NaN values in latitude and longitude
    filtered_data = filtered_data.dropna(subset=['latitude', 'longitude'])

    # Check if filtered_data is empty
    if filtered_data.empty:
        st.warning("No hotels match the selected criteria.")
    else:
        # Continue with the rest of the code
        center_latitude = filtered_data['latitude'].mean()
        center_longitude = filtered_data['longitude'].mean()
        m = folium.Map(location=[center_latitude, center_longitude], zoom_start=5)

        # Add markers to the map
        for index, row in filtered_data.iterrows():
            
            marker = folium.Marker([row['latitude'], row['longitude']],
                          
                          icon=folium.Icon(color="grey", icon='glyphicon glyphicon-home')).add_to(m)
            marker.add_child(folium.Popup(f"<b>Name:</b> {row['price_name']}"))


        # Display the Folium map in Streamlit
        folium_static(m)

if __name__ == "__main__":
    main()