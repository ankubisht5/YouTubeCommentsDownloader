from flask import Flask, render_template, request, send_from_directory
from flask import Response
from googleapiclient.discovery import build
import json
import os
import csv
import re

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    youtube_url = request.form.get('youtube_url')
    remove_duplicates = request.form.get('remove_duplicates')
    keyword_filter = request.form.get('keyword_filter')
    num_comments = request.form.get('num_comments')
    comment_format = request.form.get('comment_format')
    # Process the form
    result = process_form(youtube_url, remove_duplicates, keyword_filter, num_comments, comment_format)
    if result == 100:
        return "Invalid Link"
    elif result == 101:
        return "Video does not exist"
    elif result == 103:
        if comment_format == 'csv':
            filename = 'comments.csv'
            return send_csv(filename)
        else:
            filename = 'comments.json'
            return send_json(filename)
    else:
        return "Error Occurred"


def extract_video_id(link):
    video_id = None
    if "youtu.be/" in link:
        video_id = link.split("youtu.be/")[-1]
    elif "youtube.com/watch?v=" in link:
        video_id = link.split("youtube.com/watch?v=")[-1].split("&")[0]
    else:
        return None
    return video_id


def process_form(video_link, remove_duplicates, keyword_filter, num_comments, comment_format):
    print(video_link, remove_duplicates, keyword_filter, num_comments, comment_format)
    api_key = "AIzaSyC2DZA3LFIfGwLoxHHYvnQLzY7t-xWS7Dg"  # Replace with your own YouTube Data API key
    youtube = build('youtube', 'v3', developerKey=api_key)
    # Extract the video ID from the link
    video_id = extract_video_id(video_link)
    if video_id is None:
        print("Invalid YouTube video link.")
        return 100
    try:
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        if not video_response['items']:
            print("Invalid Video ID.")
            return 101
        # Retrieve the comments from the video
        all_comments = download_all_comments(youtube,video_id)
        comments = filter_comments(all_comments,keyword_filter)
        filename = 'comments.json'
        # Save the comments to a JSON file
        with open(filename, 'w') as file:
            json.dump(comments, file, indent=4)

        print("Comments scraped successfully and saved to comments.json.")
        directory = os.path.dirname(os.path.abspath(__file__))
        convert_json_to_csv('comments.json','comments.csv')
        # Return the file as a download response
        return 103

    except Exception as e:
        print("An error occurred:", str(e))
        return str(e)

def convert_json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as file:
        comments = json.load(file)

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Likes', 'Date', 'Text'])

        for comment in comments:
            writer.writerow([comment['username'], comment['likes'], comment['date'], comment['text']])

    print(f"JSON file '{json_file}' converted to CSV file '{csv_file}' successfully.")
def send_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        contents = file.read()

    return Response(
        contents,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )

def send_json(filename):
    with open(filename, 'r') as file:
        contents = file.read()

    return Response(
        contents,
        mimetype="application/json",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )
def filter_comments(data,keyword_filter):
        filtered_comments = [comment for comment in data if keyword_filter.lower() in comment['text'].lower()]
        return filtered_comments

# Assuming you have already set up the YouTube Data API client (not shown here)
# and have a video ID for which you want to download all the comments.

def download_all_comments(youtube,video_id):
    try:
        all_comments = []

        next_page_token = None
        while True:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,  # Maximum value allowed for maxResults is 100
                pageToken=next_page_token
            ).execute()

            for item in response.get("items", []):
                comment = item['snippet']['topLevelComment']['snippet']
                comment_data = {
                    'username': comment['authorDisplayName'],
                    'likes': comment['likeCount'],
                    'date': comment['publishedAt'],
                    'text': comment['textDisplay']
                }
                all_comments.append(comment_data)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break  # No more pages, exit the loop

        return all_comments
    except Exception as e:
        print("Error:", e)
        return []
if __name__ == '__main__':
    app.run(debug=True)
