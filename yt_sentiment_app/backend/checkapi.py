from googleapiclient.discovery import build

youtube = build("youtube", "v3", developerKey="AIzaSyAtZ7RMvC7Wu2M0KSsoP_eSaqIl0iALy-E")

response = youtube.commentThreads().list(
    part="snippet",
    videoId="tLYc97GuTt0",  # Replace with any valid video ID
    maxResults=5
).execute()

print(response)
