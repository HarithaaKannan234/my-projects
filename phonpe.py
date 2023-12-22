import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static
import plotly.express as px


json_file_path = "C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\PhonePeHK\\states_india.geojson"


transaction_data = pd.read_csv("C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\PhonePeHK\\aggtrans.csv")
aggregated_users_csv = pd.read_csv('C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\PhonePeHK\\agguser.csv')
map_user_csv = pd.read_csv('C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\PhonePeHK\\mapuser.csv')
map_user_csv['registereduser'] = pd.to_numeric(map_user_csv['registereduser'])
map_user_csv['appopens'] = pd.to_numeric(map_user_csv['appopens'])
map_trans_csv = pd.read_csv("C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\PhonePeHK\\maptrans.csv")




st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
tab1, tab2 = st.tabs(["***India Transaction Map***", "***More Insights***",])
with tab1:
   
    choice = st.sidebar.selectbox("Select Metric", ["Transaction_Count", "Transaction_Amount"])

    
    selected_year = st.sidebar.selectbox("Select Year", transaction_data['years'].unique())
    selected_quarter = st.sidebar.selectbox("Select Quarter", transaction_data['quarter'].unique())

    
    filtered_data = transaction_data[(transaction_data['years'] == selected_year) & (transaction_data['quarter'] == selected_quarter)]

    
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

  
    folium.Choropleth(
        geo_data=json_file_path,
        name="choropleth",
        data=filtered_data,
        columns=["states", choice.lower()],  
        key_on="feature.properties.st_nm",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=choice
    ).add_to(m)

    
    folium.features.GeoJson(json_file_path, name="States",
                            popup=folium.features.GeoJsonPopup(fields=["st_nm"])).add_to(m)

    
    folium_static(m, width=1000, height=600)
with tab2:
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
      
        top_brands = aggregated_users_csv.groupby('brands')['transaction_count'].sum().nlargest(5).reset_index()

       
        fig_brands = px.pie(top_brands, names='brands', values='transaction_count',
                            title='Top 5 Brands Of Mobiles Used', hole=0.5,
                            color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_brands)

    if selected_question == "8 States With Highest Total Registered Users":
           
            selected_year = st.slider("Select Year", min_value=map_user_csv['years'].min(),
                                    max_value=map_user_csv['years'].max(), value=map_user_csv['years'].max())

            filtered_data = map_user_csv[map_user_csv['years'] == selected_year]

            top_states = filtered_data.groupby('states')['registereduser'].sum().nlargest(8).reset_index()

            
            fig_states = px.bar(top_states, x='states', y='registereduser',
                                title=f'Top 8 States With Highest Total Registered Users ({selected_year})',
                                color='registereduser', color_continuous_scale='Viridis')
            st.plotly_chart(fig_states)
    
    if selected_question == "States With Lowest Transaction Amount":
        
        selected_year_bar = st.selectbox("Select Year", transaction_data['years'].unique(), key='year_bar')
        selected_quarter_bar = st.selectbox("Select Quarter", transaction_data['quarter'].unique(), key='quarter_bar')

        
        filtered_data_bar = transaction_data[
            (transaction_data['years'] == selected_year_bar) & (transaction_data['quarter'] == selected_quarter_bar)]

        
        lowest_transaction_states_bar = filtered_data_bar.groupby('states')[choice.lower()].sum().nsmallest(8).reset_index()

       
        fig_states_bar = px.bar(lowest_transaction_states_bar, x='states', y=choice.lower(),
                                title=f'8 States With Lowest {choice} ({selected_year_bar} - {selected_quarter_bar})',
                                color=choice.lower(), color_continuous_scale='Viridis')
        st.plotly_chart(fig_states_bar)
    if selected_question == "Top 8 Districts With Highest Transaction Amount":
        
        selected_year_bar_districts = st.selectbox("Select Year", map_trans_csv['years'].unique(), key='year_bar_districts')
        selected_quarter_bar_districts = st.selectbox("Select Quarter", map_trans_csv['quarter'].unique(), key='quarter_bar_districts')

        
        filtered_data_bar_districts = map_trans_csv[
           (map_trans_csv['years'] == selected_year_bar_districts) & 
           (map_trans_csv['quarter'] == selected_quarter_bar_districts)
]


        highest_transaction_district = filtered_data_bar_districts.groupby('district')[choice.lower()].sum().nlargest(8).reset_index()

        
        
        
        fig_districts = px.bar(highest_transaction_district, x='district', y=choice.lower(),
                                title=f'District With Highest {choice} ({selected_year_bar_districts} - {selected_quarter_bar_districts})',
                                color=choice.lower(), color_continuous_scale='Viridis')
        st.plotly_chart(fig_districts)


    if selected_question == "Top 8 Districts With Lowest Transaction Amount":
            
            selected_year_bar_districts = st.selectbox("Select Year", map_trans_csv['years'].unique(), key='year_bar_districts')
            selected_quarter_bar_districts = st.selectbox("Select Quarter", map_trans_csv['quarter'].unique(), key='quarter_bar_districts')

           
            filtered_data_bar_districts = map_trans_csv[
            (map_trans_csv['years'] == selected_year_bar_districts) & 
            (map_trans_csv['quarter'] == selected_quarter_bar_districts)]
            
            top_districts = filtered_data_bar_districts.groupby('district')[choice.lower()].sum().nsmallest(8).reset_index()

           
            fig_districts_top = px.bar(top_districts, x='district', y=choice.lower(),
                                        title=f'Top 8 Districts With Lowest {choice} ({selected_year_bar_districts} - {selected_quarter_bar_districts})',
                                        color=choice.lower(), color_continuous_scale='Viridis')
            st.plotly_chart(fig_districts_top)
    if selected_question == "Total Transaction Count and Amount":
        
        selected_year_cards = st.slider("Select Year", min_value=transaction_data['years'].min(),
                                         max_value=transaction_data['years'].max(), value=transaction_data['years'].max())

       
        filtered_data_cards = transaction_data[transaction_data['years'] == selected_year_cards]

       
        total_transaction_count_cards = filtered_data_cards['transaction_count'].sum()
        total_transaction_amount_cards = filtered_data_cards['transaction_amount'].sum()

        st.info(f"**Total Transaction Count in {selected_year_cards}:** {total_transaction_count_cards}")
        st.success(f"**Total Transaction Amount in {selected_year_cards}:** {total_transaction_amount_cards}")

    if selected_question == "States With Highest Transaction Count":
        
        selected_year_bar = st.selectbox("Select Year", transaction_data['years'].unique(), key='year_bar')
        selected_quarter_bar = st.selectbox("Select Quarter", transaction_data['quarter'].unique(), key='quarter_bar')

        
        filtered_data_bar = transaction_data[
            (transaction_data['years'] == selected_year_bar) & (transaction_data['quarter'] == selected_quarter_bar)]

       
        highest_transaction_states = filtered_data_bar.groupby('states')['transaction_count'].sum().nlargest(5).reset_index()

        
        fig_states_highest_count = px.bar(highest_transaction_states, x='states', y='transaction_count',
                                          title=f'Top 5 States With Highest Transaction Count ({selected_year_bar} - {selected_quarter_bar})',
                                          color='transaction_count', color_continuous_scale='Viridis')
        st.plotly_chart(fig_states_highest_count)
    if selected_question == "States With Lowest Transaction Count":
        
        selected_year_bar = st.selectbox("Select Year", transaction_data['years'].unique(), key='year_bar')
        selected_quarter_bar = st.selectbox("Select Quarter", transaction_data['quarter'].unique(), key='quarter_bar')

        
        filtered_data_bar = transaction_data[
            (transaction_data['years'] == selected_year_bar) & (transaction_data['quarter'] == selected_quarter_bar)]

        
        lowest_transaction_states = filtered_data_bar.groupby('states')['transaction_count'].sum().nsmallest(5).reset_index()

        
        fig_states_lowest_count = px.bar(lowest_transaction_states, x='states', y='transaction_count',
                                         title=f'Top 5 States With Lowest Transaction Count ({selected_year_bar} - {selected_quarter_bar})',
                                         color='transaction_count', color_continuous_scale='Viridis')
        st.plotly_chart(fig_states_lowest_count)
    if selected_question == "8 States With Lowest Total Registered Users":
        
        selected_year = st.sidebar.selectbox("Select Year", map_user_csv['years'].unique(), key='unique_key_for_selectbox')


        
        filtered_data = map_user_csv[map_user_csv['years'] == selected_year]

        
        lowest_registered_users_states = filtered_data.groupby('states')['registereduser'].sum().nsmallest(8).reset_index()

        
        fig_states_lowest_registered_users = px.bar(lowest_registered_users_states, x='states', y='registereduser',
                                                    title=f'Top 8 States With Lowest Total Registered Users ({selected_year})',
                                                    color='registereduser', color_continuous_scale='Viridis')

        
        st.plotly_chart(fig_states_lowest_registered_users)
    if selected_question == "Most Used Brands in Each State":
        
        most_used_brands = aggregated_users_csv.groupby(['states', 'brands'])['transaction_count'].sum().reset_index()
        most_used_brands = most_used_brands.loc[most_used_brands.groupby('states')['transaction_count'].idxmax()]

        
        st.write("Most Used Brands in Each State:")
        st.write(most_used_brands)
        
        
        fig_most_used_brands = px.bar(most_used_brands, x='states', y='transaction_count', color='brands',
                                    title='Most Used Brands in Each State', 
                                    labels={'transaction_count': 'Transaction Count'},
                                    color_discrete_sequence=px.colors.qualitative.Set3)
        
        st.plotly_chart(fig_most_used_brands)
