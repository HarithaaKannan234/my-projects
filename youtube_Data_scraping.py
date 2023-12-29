pip install google-api-python-client
pip install pandas
get_ipython().system('pip install google-api-python-client pymongo')
import os
from googleapiclient.discovery import build
from pprint import pprint
from pymongo import MongoClient

api_key = "AIzaSyCaBIl9bWM_a30SqNs9IeH1Jx34JU6shH4"  
api_service_name = "youtube"
api_version = "v3"
channels = ["UCLpovxJVLBZrXJGCymB6LYw", "UC9anh3Cs_tqMkKHxVFAqeQA", "UC0cyuNScmlQ8oyMpTvv4YSQ","UC9s5vcA1shZGHx3O1__UyVA","UCL3bXmDdBadWGBLvP52T9lg"," UCC4P0TtsS2tBOwsLnvjrgwQ","UC8p3oT98Gb9VwzhMjHlWJEQ","UCqVEHtQoXHmUCfJ-9smpTSg","UCKjFW3fLTteXH4p6pir1H2Q ","UCMAwZx4IV9RYrN4CYaZyaSw "]



client = MongoClient("mongodb://localhost:27017")
db = client["Youtube_Assignment"]
collection = db["Youtube_data"]

def get_youtube_service(api_key):
    return build(api_service_name, api_version, developerKey=api_key)

def get_playlist_id(channel_id, youtube):
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()
    playlists = response['items'][0]['contentDetails']['relatedPlaylists']
    playlist_id = playlists['uploads']
    return playlist_id

def youtube_channel(channel_id, youtube):
    final_data = []
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics,topicDetails,status",
        id=channel_id
    )
    response = request.execute()
    
    if 'items' in response:
    
    
        for item in response['items']:
            channel_info = {
                "Channel_Id": item["id"],
                "Channel_Name": item["snippet"]["title"],
                "Subscription_Count": item["statistics"]["subscriberCount"],
                "Channel_Views": item["statistics"]["viewCount"],
                "Channel_Description": item["snippet"]["description"],
                "Playlist_Id": get_playlist_id(channel_id, youtube),
                "Videos": [] 
            final_data.append(channel_info)

    return final_data

def youtube_get_video_id(playlist_id, youtube):
    video_list = []
    
    request = youtube.playlistItems().list(
        part="contentDetails",
        maxResults=50,
        playlistId=playlist_id
    )
    response = request.execute()
    
    for item in response["items"]:
        video_list.append(item["contentDetails"]["videoId"])
    
    next_page_token = response.get('nextPageToken')
    while next_page_token:
        request = youtube.playlistItems().list(
            part="contentDetails",
            maxResults=50,
            playlistId=playlist_id,
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response["items"]:
            video_list.append(item["contentDetails"]["videoId"])
        
        next_page_token = response.get('nextPageToken')
    
    return video_list

def video_details(video_ids, youtube):
    video_details_list = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i + 50])
        )
        response = request.execute()

        for item in response["items"]:
            video_data = {
                "Video_Id": item["id"],
                "Video_Name": item["snippet"]["title"],
                "Video_Description": item["snippet"].get("description", ""),
                "PublishedAt": item["snippet"]["publishedAt"],
                "View_Count": item["statistics"].get("viewCount", 0),
                "Like_Count": item["statistics"].get("likeCount", 0),
                "Dislike_Count": item["statistics"].get("dislikeCount", 0),
                "Favorite_Count": item["statistics"].get("favoriteCount", 0),
                "Comment_Count": 0,  
                "Duration": item["contentDetails"]["duration"],
                "Thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                "Caption_Status": item["contentDetails"]["caption"],
                "Comments": [] 
            }

            try:
               
                comments_request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=item["id"],
                    textFormat="plainText",
                    maxResults=100
                )
                comments_response = comments_request.execute()

              
                video_data["Comment_Count"] = len(comments_response.get("items", []))

                for comment_item in comments_response.get("items", []):
                    comment_data = {
                        "Comment_Id": comment_item["id"],
                        "Comment_Text": comment_item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                        "Comment_Author": comment_item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                        "Comment_PublishedAt": comment_item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                    }
                    video_data["Comments"].append(comment_data)

            except Exception as e:
               
                print(f"Error fetching comments for video {item['id']}: {str(e)}")

            video_details_list.append(video_data)

    return video_details_list


for channel_id in channels:
    youtube = get_youtube_service(api_key)

    channel_data = youtube_channel(channel_id, youtube)
 
    
    if channel_data:
 
        collection.insert_many(channel_data)

        playlist_id = channel_data[0]["Playlist_Id"]
        playlist_video_ids = youtube_get_video_id(playlist_id, youtube)

        video_data = video_details(playlist_video_ids, youtube)
    
    
    if channel_data:
        for video in video_data:
            collection.update_one({"Channel_Id": channel_data[0]["Channel_Id"]}, {"$push": {"Videos": video}})

        print("done")


client.close()
pip install streamlit
import streamlit as st

st.text('Fixed width text')
st.markdown('_Markdown_') 



