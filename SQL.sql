/*

channel - channel_id , channel_name , channel_type ,channel_views, channel_description , channel_status
playlist - playlist_id , channel_id 
comment - comment_id , video_id , comment_text , comment_author , comment_published_date
video - video_id, playlist_id , video_name , video_description,published_date , view_count , like_count ,deslike_count , favourite_count , comment_count , duration , thumbnail , caption_status

*/

CREATE TABLE Channel (
    channel_id VARCHAR(255) ,
    channel_name VARCHAR(255),
    channel_views INT,
    channel_description VARCHAR(MAX),
    playlist_id VARCHAR(255) -- You need to define the appropriate data type
);

CREATE TABLE Video (
 
    Video_Id varchar(255),
    Playlist_Id varchar(255),
    Video_Name varchar(255),
    Video_Description varchar(max),
    PublishedAt datetime,
    View_Count int,
    Like_Count int,
    Dislike_Count int,
    Favorite_Count int,
    Comment_Count int,
    Duration varchar(255),
    Thumbnail varchar(max),
    Caption_Status varchar(255)
);

create table playlist (
playlist_id varchar(255),
channel_id varchar(255))


CREATE TABLE Comment (
   
    Comment_Id varchar(255),
    Video_Id varchar(255),
    Comment_Text varchar(max),
    Comment_Author varchar(255),
    Comment_PublishedAt datetime
);

DECLARE @json_table nvarchar(max);


SELECT @json_table = BulkColumn
FROM OPENROWSET(BULK 'C:\Users\Admin\Desktop\Murdoch\guvi\projects\youtube\Youtube_Assignment.Youtube_data.json', SINGLE_CLOB) AS t;

INSERT INTO Channel
SELECT
    
    Channel_Id,
    Channel_Name,
    Channel_Views,
    Channel_Description,
    Playlist_Id
FROM OPENJSON(@json_table)
WITH (
   
    Channel_Id varchar(255),
    Channel_Name varchar(255),
    Channel_Views int,
    Channel_Description varchar(max),
    Playlist_Id varchar(255)
);


INSERT INTO Video
SELECT
    
    Video_Id,
    Playlist_Id,
    Video_Name,
    Video_Description,
    PublishedAt,
    View_Count,
    Like_Count,
    Dislike_Count,
    Favorite_Count,
    Comment_Count,
    Duration,
    Thumbnail,
    Caption_Status
FROM OPENJSON(@json_table)
WITH (
    Playlist_Id varchar(255),
    Channel_Id varchar(255),
    Videos nvarchar(max) AS JSON
) AS tableA
CROSS APPLY OPENJSON(tableA.Videos)
WITH (
    Video_Id varchar(255),
    
    Video_Name varchar(255),
    Video_Description varchar(max),
    PublishedAt datetime,
    View_Count int,
    Like_Count int,
    Dislike_Count int,
    Favorite_Count int,
    Comment_Count int,
    Duration varchar(255),
    Thumbnail varchar(max),
    Caption_Status varchar(255)
    
) AS Videos;


INSERT INTO Comment
SELECT
   
    Comment_Id,
    Video_Id,
    Comment_Text,
    Comment_Author,
    Comment_PublishedAt
FROM OPENJSON(@json_table)
WITH (
    
    Channel_Id varchar(255),
    Videos nvarchar(max) AS JSON
) AS tableA
CROSS APPLY OPENJSON(tableA.Videos)
WITH (
    Video_Id varchar(255),
    Comments nvarchar(max) AS JSON
) AS Videos
CROSS APPLY OPENJSON(Videos.Comments)
WITH (
    Comment_Id varchar(255),
    Comment_Text varchar(max),
    Comment_Author varchar(255),
    Comment_PublishedAt datetime
) AS Comments;


INSERT INTO Playlist (Playlist_Id, Channel_Id)
SELECT
    Playlist_Id,
    Channel_Id
FROM OPENJSON(@json_table)
WITH (
    Playlist_Id varchar(255),
    Channel_Id varchar(255),
    Videos nvarchar(max) AS JSON
) AS tableA;


select * from Comment
select * from playlist
select * from Video
select * from Channel
 ----------------queries-------------------------------
 --1)--
 select Video_name , channel_name
 from Video join  Channel on (video.Playlist_Id = Channel.playlist_id)

 --2)--
select channel_name , count(video_name) as video_count
from channel join video on (Channel.playlist_id = Video.Playlist_Id)
group by channel.channel_name
order by video_count desc

 --3)--
 select top 10 view_count , video_name , channel_name
 from Video join Channel on (video.Playlist_Id = Channel.playlist_id)
 order by view_count desc
 
 --4)--
 select video_name , count(comment_Id ) as comment_count
 from video join Comment on  (video.video_id = comment.video_id)
 group by video.video_id , video.video_name 
 order by 
 comment_count desc

 --5)--
select like_count ,video_id , channel_name 
from video join channel on (video.playlist_id = channel.playlist_id )
WHERE
   video.Like_Count = (select max(like_count) from video)

 --6)--
 select like_count, Dislike_Count , video_name
 from video 
 group by video_name,like_count, Dislike_Count
 order by Like_Count asc

 --7)--
 select channel_views , channel_name
 from channel
 order by channel_name

 --8)--
 select channel_name , PublishedAt
 from channel join video on (channel.playlist_id = video.Playlist_Id)
 where year(video.publishedAt) = 2022;

 --9)-

SELECT
  c.Channel_Id,
  c.Channel_Name,
  AVG(
    CASE
      WHEN CHARINDEX('H', v.Duration) > 0 AND CHARINDEX('M', v.Duration) > 0 AND CHARINDEX('S', v.Duration) > 0
        THEN CAST(SUBSTRING(v.Duration, CHARINDEX('H', v.Duration) + 1, CHARINDEX('M', v.Duration) - CHARINDEX('H', v.Duration) - 1) AS INT) * 3600
           + CAST(SUBSTRING(v.Duration, CHARINDEX('M', v.Duration) + 1, CHARINDEX('S', v.Duration) - CHARINDEX('M', v.Duration) - 1) AS INT) * 60
           + CAST(SUBSTRING(v.Duration, 3, CHARINDEX('H', v.Duration) - 3) AS INT)
      WHEN CHARINDEX('H', v.Duration) > 0 AND CHARINDEX('M', v.Duration) > 0
        THEN CAST(SUBSTRING(v.Duration, CHARINDEX('H', v.Duration) + 1, CHARINDEX('M', v.Duration) - CHARINDEX('H', v.Duration) - 1) AS INT) * 3600
           + CAST(SUBSTRING(v.Duration, 3, CHARINDEX('H', v.Duration) - 3) AS INT) * 60
      WHEN CHARINDEX('H', v.Duration) > 0 AND CHARINDEX('S', v.Duration) > 0
        THEN CAST(SUBSTRING(v.Duration, CHARINDEX('H', v.Duration) + 1, CHARINDEX('S', v.Duration) - CHARINDEX('H', v.Duration) - 1) AS INT) * 3600
           + CAST(SUBSTRING(v.Duration, 3, CHARINDEX('H', v.Duration) - 3) AS INT)
      WHEN CHARINDEX('H', v.Duration) > 0
        THEN CAST(SUBSTRING(v.Duration, 3, CHARINDEX('H', v.Duration) - 3) AS INT) * 3600
      WHEN CHARINDEX('M', v.Duration) > 0 AND CHARINDEX('S', v.Duration) > 0
        THEN CAST(SUBSTRING(v.Duration, CHARINDEX('M', v.Duration) + 1, CHARINDEX('S', v.Duration) - CHARINDEX('M', v.Duration) - 1) AS INT) * 60
           + CAST(SUBSTRING(v.Duration, 3, CHARINDEX('M', v.Duration) - 3) AS INT)
      WHEN CHARINDEX('M', v.Duration) > 0
        THEN CAST(SUBSTRING(v.Duration, 3, CHARINDEX('M', v.Duration) - CHARINDEX('H', v.Duration) - 1) AS INT) * 60
      WHEN CHARINDEX('S', v.Duration) > 0
        THEN CAST(SUBSTRING(v.Duration, 3, LEN(v.Duration) - 2) AS INT)
    END
  ) AS Average_Duration
FROM
  video v
JOIN
  channel c ON v.Playlist_Id = c.playlist_id
GROUP BY
  c.Channel_Id, c.Channel_Name;

 SELECT
 video_id , duration , channel_id , Channel_Name
 from video join channel on (video.Playlist_Id = channel.playlist_id)
 --10)--

 select video_name , comment_count , channel_name 
 from video join channel on(video.playlist_id = channel.playlist_id)
 order by Comment_count desc


 select * from Channel
