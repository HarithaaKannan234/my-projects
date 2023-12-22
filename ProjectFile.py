import streamlit as st
from googleapiclient.discovery import build
import pandas as pd


question_files = {
    "What are the names of all the videos and their corresponding channels?": "query1.csv",
    "Which channels have the most number of videos and how many videos do they have?": "query2.csv",
    "What are the top 10 most viewed videos and their respective channels?": "query3.csv",
    "How many comments were made on each video, and what are their corresponding video names?": "query4.csv",
    "Which videos have the highest number of likes, and what are their corresponding channel names?": "query5.csv",
    "What is the total number of likes and dislikes for each video, and what are their corresponding video names?": "query6.csv",
    "What is the total number of views for each channel, and what are their corresponding channel names?": "query7.csv",
    "What are the names of all the channels that have published videos in the year 2022?": "query8.csv",
    "What is the average duration of all videos in each channel, and what are their corresponding channel names?": "query9.csv",
    "Which videos have the highest number of comments, and what are their corresponding channel names?": "query10.csv",
}


st.title("Youtube Channel - Analysed data")


selected_question = st.selectbox("Select a question from the dropdown below to view analysed data", list(question_files.keys()))


df = pd.read_csv(question_files[selected_question])


st.table(df)

st.write("by Harithaa Kannan")

