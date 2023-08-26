from facebook_uploader.uploader import FacebookReelsUploader, VideoSpecificationsChecker
import os

# Provide the file path of the video you want to check
video_file_path = "../assets/test_vid (4).mp4"
result = VideoSpecificationsChecker().check(video_file_path)
print(result)
