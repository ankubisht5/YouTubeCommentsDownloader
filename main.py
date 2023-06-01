from googleapiclient.discovery import build
import json
import re

def extract_video_id(link):
    video_id = None
    if "youtu.be/" in link:
        video_id = link.split("youtu.be/")[-1]
    elif "youtube.com/watch?v=" in link:
        video_id = link.split("youtube.com/watch?v=")[-1].split("&")[0]
    else:
        return None
    return video_id


def main():
    # Set up the YouTube Data API
    api_key = "YOUR_API"  # Replace with your own YouTube Data API key
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Specify the video link
    video_link = input("Enter the YouTube video link: ")

    # Extract the video ID from the link
    video_id = extract_video_id(video_link)
    if video_id is None:
        print("Invalid YouTube video link.")
        return

    try:
        # Retrieve the comments from the video
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,  # Adjust as needed to fetch more comments
            textFormat='plainText'
        ).execute()

        # Extract the relevant information from the comments
        comments = []
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comment_data = {
                'username': comment['authorDisplayName'],
                'likes': comment['likeCount'],
                'date': comment['publishedAt'],
                'text': comment['textDisplay']
            }
            comments.append(comment_data)

        # Save the comments to a JSON file
        with open('comments.json', 'w') as file:
            json.dump(comments, file, indent=4)

        print("Comments scraped successfully and saved to comments.json.")

    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == '__main__':
    main()
