import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import folium
from streamlit_folium import folium_static
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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
    
    tab1 , tab2 = st.tabs(["Find your AirBnB", "More Insights"])
    with tab1:
        st.title(" Find Your AirBnB ")

     
        df = fetch_data()

     
        countries = df['country'].unique()
        selected_country = st.selectbox("Select your desired country", countries)

       
        filtered_data = df[df['country'] == selected_country]

      
        exclude_columns = ['country', 'street', 'country_code']
        amenities_columns = [col for col in df.columns if col not in exclude_columns and col not in ['listing_id', 'name_x', 'name_y', 'price', 'price_name', 'latitude', 'longitude']]

     
        selected_amenities = st.multiselect("Select your desired amenities", amenities_columns, default=[])

       
    
        max_price = st.slider("Select maximum price", min_value=df['price'].min(), max_value=df['price'].max(), value=df['price'].max())

      
        for amenity in selected_amenities:
            if amenity in filtered_data.columns:
                filtered_data = filtered_data[filtered_data[amenity]]

        filtered_data = filtered_data[ (filtered_data['price'] <= max_price)]

        
        filtered_data = filtered_data.dropna(subset=['latitude', 'longitude'])

        
        if filtered_data.empty:
            st.warning("No hotels match the selected criteria.")
        else:
          
            center_latitude = filtered_data['latitude'].mean()
            center_longitude = filtered_data['longitude'].mean()
            m = folium.Map(location=[center_latitude, center_longitude], zoom_start=5)

            for index, row in filtered_data.iterrows():
                popup_html = f"<b>Name:</b> {row['price_name']}<br><b>Price:</b> {row['price']}"
                marker = folium.Marker([row['latitude'], row['longitude']],
                                        icon=folium.Icon(color="grey", icon='glyphicon glyphicon-home')).add_to(m)
                marker.add_child(folium.Popup(popup_html))

         
            folium_static(m)
    with tab2:
        st.title("More Insights")

      
        df = fetch_data()

        st.subheader("Price Distribution")
        fig = px.histogram(df, x='price', title='Price Distribution',color_discrete_sequence=px.colors.qualitative.Alphabet)
        st.plotly_chart(fig)

     
        st.subheader("Number of Listings per Country")
        country_counts = df['country'].value_counts()
        fig = px.bar(country_counts, x=country_counts.index, y=country_counts.values, labels={'x':'Country', 'y':'Number of Listings'}, title='Number of Listings per Country',color=country_counts.index)
        st.plotly_chart(fig)

       
        st.subheader("Amenities Analysis")
        amenities_counts = df[amenities_columns].sum()
        fig = px.bar(amenities_counts, x=amenities_counts.index, y=amenities_counts.values, labels={'x':'Amenity', 'y':'Count'}, title='Amenities Analysis',color=amenities_counts.index)
        st.plotly_chart(fig)

    
        st.subheader("Word Cloud of AirBnB Names")
        wordcloud_text = ' '.join(df['price_name'].dropna().astype(str))
        wordcloud = WordCloud(width=800, height=400, background_color ='white', stopwords = None, min_font_size = 10).generate(wordcloud_text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        st.subheader("Price Fluctuation Analysis")
        fig = px.line(df, x=df.index, y='price', title='Price Fluctuation Over Time',color_discrete_sequence= ["green"])
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
