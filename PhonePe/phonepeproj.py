import json
import folium
import streamlit as st
import pandas as pd
import requests
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
json_file_path = "C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\PhonePeHK\\states_india.geojson"
#CREATE DATAFRAMES FROM SQL
#sql connection
mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        password = "Sukan@01",
                        database = "PhonePe",
                        port = "5432"
                        )
cursor = mydb.cursor()
cursor.execute("select * from aggregated_transaction;")
mydb.commit()
table1 = cursor.fetchall()
Aggre_transaction = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

cursor.execute("select * from aggregated_users")
mydb.commit()
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

cursor.execute("select * from map_transaction")
mydb.commit()
table3 = cursor.fetchall()
Map_transaction = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

cursor.execute("select * from map_user")
mydb.commit()
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

cursor.execute("select * from top_transaction")
mydb.commit()
table5 = cursor.fetchall()
Top_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

cursor.execute("select * from top_user")
mydb.commit()
table6 = cursor.fetchall()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))


st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
tab1 , tab2= st.tabs([ "***More Insights***","bruh"])

with tab1:
    st.write("### Choose a Question")
    selected_question = st.selectbox("Select Question", [
        "Top Brands Of Mobiles Used",
        "8 States With Highest Total Registered Users",
        "States With Lowest Transaction Amount",
        "Top 8 Districts With Highest Transaction Amount",
        "Top 8 Districts With Lowest Transaction Amount",
        "Total Transaction Count and Amount",
        "States With Highest Transaction Count",
        "States With Lowest Transaction Count",
        "8 States With Lowest Total Registered Users",
        "Most Used Brands in Each State"
    ])

    st.write(f"### {selected_question}")

    if selected_question == "Top Brands Of Mobiles Used":
        # Execute SQL query to get top brands from PostgreSQL database
        cursor.execute("SELECT brands, SUM(transaction_count) AS total_count FROM aggregated_users GROUP BY brands ORDER BY total_count DESC LIMIT 5")
        top_brands_data = cursor.fetchall()
        top_brands = pd.DataFrame(top_brands_data, columns=["brands", "transaction_count"])

        # Create donut chart for Top Brands Of Mobiles Used using data from PostgreSQL database
        fig_brands = px.pie(top_brands, names='brands', values='transaction_count',
                            title='Top 5 Brands Of Mobiles Used', hole=0.5,
                            color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_brands)

    if selected_question == "8 States With Highest Total Registered Users":
            selected_year = st.slider("Select Year", min_value=Map_user['Years'].min(),
                                    max_value=Map_user['Years'].max(), value=Map_user['Years'].max())

            filtered_data = Map_user[Map_user['Years'] == selected_year]

            top_states = filtered_data.groupby('States')['RegisteredUser'].sum().nlargest(8).reset_index()

            fig_states = px.bar(top_states, x='States', y='RegisteredUser',
                                title=f'Top 8 States With Highest Total Registered Users ({selected_year})',
                                color='RegisteredUser', color_continuous_scale='Viridis')
            st.plotly_chart(fig_states)

    if selected_question == "States With Lowest Transaction Amount":
        selected_year_bar = st.selectbox("Select Year", Map_transaction['Years'].unique(), key='year_bar')
        selected_quarter_bar = st.selectbox("Select Quarter", Map_transaction['Quarter'].unique(), key='quarter_bar')

        filtered_data_bar = Map_transaction[
            (Map_transaction['Years'] == selected_year_bar) & (Map_transaction['Quarter'] == selected_quarter_bar)]

        lowest_transaction_states_bar = filtered_data_bar.groupby('States')['Transaction_amount'].sum().nsmallest(8).reset_index()

        fig_states_bar = px.bar(lowest_transaction_states_bar, x='States', y='Transaction_amount',
                                title=f'8 States With Lowest Transaction Amount ({selected_year_bar} - {selected_quarter_bar})',
                                color='Transaction_amount', color_continuous_scale='Viridis')
        st.plotly_chart(fig_states_bar)

    if selected_question == "Top 8 Districts With Highest Transaction Amount":
        selected_year_bar_districts = st.selectbox("Select Year", Map_transaction['Years'].unique(), key='year_bar_districts')
        selected_quarter_bar_districts = st.selectbox("Select Quarter", Map_transaction['Quarter'].unique(), key='quarter_bar_districts')

        filtered_data_bar_districts = Map_transaction[
        (Map_transaction['Years'] == selected_year_bar_districts) & 
        (Map_transaction['Quarter'] == selected_quarter_bar_districts)]

        highest_transaction_district = filtered_data_bar_districts.groupby('Districts')['Transaction_amount'].sum().nlargest(8).reset_index()

        fig_districts = px.bar(highest_transaction_district, x='Districts', y='Transaction_amount',
                                title=f'Top 8 Districts With Highest Transaction Amount ({selected_year_bar_districts} - {selected_quarter_bar_districts})',
                                color='Transaction_amount', color_continuous_scale='Viridis')
        st.plotly_chart(fig_districts)
    if selected_question == "Top 8 Districts With Lowest Transaction Amount":
        selected_year_bar_districts = st.selectbox("Select Year", Map_transaction['Years'].unique(), key='year_bar_districts')
        selected_quarter_bar_districts = st.selectbox("Select Quarter", Map_transaction['Quarter'].unique(), key='quarter_bar_districts')

        filtered_data_bar_districts = Map_transaction[
            (Map_transaction['Years'] == selected_year_bar_districts) & 
            (Map_transaction['Quarter'] == selected_quarter_bar_districts)]

        lowest_transaction_districts = filtered_data_bar_districts.groupby('Districts')['Transaction_amount'].sum().nsmallest(8).reset_index()

        fig_districts_top = px.bar(lowest_transaction_districts, x='Districts', y='Transaction_amount',
                                    title=f'Top 8 Districts With Lowest Transaction Amount ({selected_year_bar_districts} - {selected_quarter_bar_districts})',
                                    color='Transaction_amount', color_continuous_scale='Viridis')
        st.plotly_chart(fig_districts_top)
    if selected_question == "Total Transaction Count and Amount":
        selected_year_cards = st.slider("Select Year", min_value=Aggre_transaction['Years'].min(),
                                        max_value=Aggre_transaction['Years'].max(), value=Aggre_transaction['Years'].max())

        filtered_data_cards = Aggre_transaction[Aggre_transaction['Years'] == selected_year_cards]

        total_transaction_count_cards = filtered_data_cards['Transaction_count'].sum()
        total_transaction_amount_cards = filtered_data_cards['Transaction_amount'].sum()

        st.info(f"**Total Transaction Count in {selected_year_cards}:** {total_transaction_count_cards}")
        st.success(f"**Total Transaction Amount in {selected_year_cards}:** {total_transaction_amount_cards}")
    if selected_question == "States With Highest Transaction Count":
        selected_year_bar = st.selectbox("Select Year", Aggre_transaction['Years'].unique(), key='year_bar')
        selected_quarter_bar = st.selectbox("Select Quarter", Aggre_transaction['Quarter'].unique(), key='quarter_bar')

        filtered_data_bar = Aggre_transaction[
            (Aggre_transaction['Years'] == selected_year_bar) & (Aggre_transaction['Quarter'] == selected_quarter_bar)]

        highest_transaction_states = filtered_data_bar.groupby('States')['Transaction_count'].sum().nlargest(5).reset_index()

        fig_states_highest_count = px.bar(highest_transaction_states, x='States', y='Transaction_count',
                                        title=f'Top 5 States With Highest Transaction Count ({selected_year_bar} - {selected_quarter_bar})',
                                        color='Transaction_count', color_continuous_scale='Viridis')
        st.plotly_chart(fig_states_highest_count)
    if selected_question == "States With Lowest Transaction Count":
        selected_year_bar = st.selectbox("Select Year", Aggre_transaction['Years'].unique(), key='year_bar')
        selected_quarter_bar = st.selectbox("Select Quarter", Aggre_transaction['Quarter'].unique(), key='quarter_bar')

        filtered_data_bar = Aggre_transaction[
            (Aggre_transaction['Years'] == selected_year_bar) & (Aggre_transaction['Quarter'] == selected_quarter_bar)]

        lowest_transaction_states = filtered_data_bar.groupby('States')['Transaction_count'].sum().nsmallest(5).reset_index()

        fig_states_lowest_count = px.bar(lowest_transaction_states, x='States', y='Transaction_count',
                                        title=f'Top 5 States With Lowest Transaction Count ({selected_year_bar} - {selected_quarter_bar})',
                                        color='Transaction_count', color_continuous_scale='Viridis')
        st.plotly_chart(fig_states_lowest_count)
    if selected_question == "8 States With Lowest Total Registered Users":
        selected_year = st.selectbox("Select Year", Map_user['Years'].unique(), key='unique_key_for_selectbox')

        filtered_data = Map_user[Map_user['Years'] == selected_year]

        lowest_registered_users_states = filtered_data.groupby('States')['RegisteredUser'].sum().nsmallest(8).reset_index()

        fig_states_lowest_registered_users = px.bar(lowest_registered_users_states, x='States', y='RegisteredUser',
                                                    title=f'Top 8 States With Lowest Total Registered Users ({selected_year})',
                                                    color='RegisteredUser', color_continuous_scale='Viridis')

        st.plotly_chart(fig_states_lowest_registered_users)
    if selected_question == "Most Used Brands in Each State":
        most_used_brands = Aggre_user.groupby(['States', 'Brands'])['Transaction_count'].sum().reset_index()
        most_used_brands = most_used_brands.loc[most_used_brands.groupby('States')['Transaction_count'].idxmax()]

        st.write("Most Used Brands in Each State:")
        st.write(most_used_brands)

        fig_most_used_brands = px.bar(most_used_brands, x='States', y='Transaction_count', color='Brands',
                                    title='Most Used Brands in Each State', 
                                    labels={'Transaction_count': 'Transaction Count'},
                                    color_discrete_sequence=px.colors.qualitative.Set3)

        st.plotly_chart(fig_most_used_brands)


with tab2:
    st.sidebar.title("Choropleth Map Options")
    
    choice = st.sidebar.selectbox("Select Metric", ["Transaction_Count", "Transaction_Amount"])
    selected_year = st.sidebar.selectbox("Select Year", Aggre_transaction['Years'].unique())
    selected_quarter = st.sidebar.selectbox("Select Quarter", Aggre_transaction['Quarter'].unique())
    
    
    cursor.execute("SELECT States, Years, Quarter, Transaction_count, Transaction_amount FROM map_transaction;")
    map_data = cursor.fetchall()
    map_transaction_df = pd.DataFrame(map_data, columns=["States", "Years", "Quarter", "Transaction_Count", "Transaction_Amount"])
    
    
    filtered_data = map_transaction_df[(map_transaction_df['Years'] == selected_year) & (map_transaction_df['Quarter'] == selected_quarter)]
    
    
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    
    
    folium.Choropleth(
        geo_data=json_file_path,
        name="choropleth",
        data=filtered_data,
        columns=["States", choice],  
        key_on="feature.properties.st_nm",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=choice
    ).add_to(m)
    
  
    folium.features.GeoJson(json_file_path, name="States",
                            popup=folium.features.GeoJsonPopup(fields=["st_nm"])).add_to(m)
    
    
    folium_static(m, width=1000, height=600)