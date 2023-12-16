import streamlit as st
from googleapiclient.discovery import build
import pandas as pd


question_files = {
    "What are the names of all the videos and their corresponding channels?": "query1.csv",
    "Which channels have the most number of videos and how many videos do they have?": "C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\YoutubeHK\\query2.csv",
    "What are the top 10 most viewed videos and their respective channels?": "C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\YoutubeHK\\query3.csv",
    "How many comments were made on each video, and what are their corresponding video names?": "C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\YoutubeHK\\query4.csv",
    "Which videos have the highest number of likes, and what are their corresponding channel names?": "C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\YoutubeHK\\query5.csv",
    "What is the total number of likes and dislikes for each video, and what are their corresponding video names?": "C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\YoutubeHK\\query6.csv",
    "What is the total number of views for each channel, and what are their corresponding channel names?": "C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\YoutubeHK\\query7.csv",
    "What are the names of all the channels that have published videos in the year 2022?": "C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\YoutubeHK\\query8.csv",
    "What is the average duration of all videos in each channel, and what are their corresponding channel names?": "C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\YoutubeHK\\query9.csv",
    "Which videos have the highest number of comments, and what are their corresponding channel names?": "C:\\Users\\Admin\\Desktop\\Murdoch\\guvi\\projects\\YoutubeHK\\query10.csv",
}

# Title of the Streamlit app
st.title("Youtube Channel - Analysed data")

# Dropdown to select a question
selected_question = st.selectbox("Select a question from the dropdown below to view analysed data", list(question_files.keys()))

# Load the selected CSV file into a DataFrame
df = pd.read_csv(question_files[selected_question])

# Display the DataFrame as a table
st.table(df)

st.write("by Harithaa Kannan")

