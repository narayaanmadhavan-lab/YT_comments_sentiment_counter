from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch
from urllib.parse import urlparse, parse_qs

# Constants
YOUTUBE_API_KEY = "AIzaSyAtZ7RMvC7Wu2M0KSsoP_eSaqIl0iALy-E"

# App setup
app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model = AutoModelForSequenceClassification.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment",
    local_files_only=True  # Make sure model is already downloaded
)

# Extract video ID from YouTube URL
def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
    return None

# Get comments using YouTube API
def get_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        next_page_token = response.get('nextPageToken')
        if not next_page_token or len(comments) >= 800:
            break
    return comments

def analyze_sentiment(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=512  # <= Ensure input fits model's limits
    )
    with torch.no_grad():
        logits = model(**inputs).logits
    scores = softmax(logits.numpy()[0])
    labels = ["negative", "neutral", "positive"]
    return labels[scores.argmax()]

@app.get("/analyze")
def analyze(youtube_url: str):
    try:
        video_id = extract_video_id(youtube_url)
        if not video_id:
            return {"error": "Invalid YouTube URL."}

        comments = get_comments(video_id)
        result = {"positive": 0, "neutral": 0, "negative": 0}

        for c in comments:
            label = analyze_sentiment(c)
            result[label] += 1

        result["total"] = sum(result.values())
        return result
    except Exception as e:
        return {"error": str(e)}

# Health check endpoint
@app.get("/")
def home():
    return {"message": "FastAPI is working!"}

@app.get("/ping")
def ping():
    return {"message": "pong"}
