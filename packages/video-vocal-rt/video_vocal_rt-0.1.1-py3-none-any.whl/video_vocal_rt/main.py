import os
import random
import time
import cv2
from sounddevice import rec, wait
from scipy.io.wavfile import write
from openpyxl import Workbook

VIDEO_DIRECTORY = "VIDEO_FILES"
AUDIO_DIRECTORY = "AUDIO_RECORDINGS"
DATA_DIRECTORY  = "DATA_FOLDER"
PARTICIPANT_ID  = "test"            # Chosen by the experimenter
PARTICIPANT_ID2 = str(time.time())  # Random to avoid collisions

sample_rate     = 44100
audio_duration  = 6

video_files = [f for f in os.listdir(VIDEO_DIRECTORY) if f.endswith('.avi')]
random.shuffle(video_files)

# Set up excel file
wb = Workbook()
ws = wb.active
ws.append(['ID', 'Order', 'Video', 'Audio_path'])

# Set up full screen display
cv2.namedWindow('main_window', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('main_window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Display blank screen and wait for key press
blank = cv2.imread('white_background.png')
cv2.imshow('main_window', blank)
cv2.waitKey(0)

for i, video_file in enumerate(video_files):

    video_path = os.path.join(VIDEO_DIRECTORY, video_file)
    video      = cv2.VideoCapture(video_path)
    fps        = video.get(cv2.CAP_PROP_FPS)
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    
    # Fixation screen display
    fixation = cv2.imread('fixation.png')
    cv2.imshow('main_window', fixation)
    cv2.waitKey(1000)

    recording    = rec(int(audio_duration * sample_rate), samplerate=sample_rate, channels=1)
    
    while True: # Video playing loop
        
        ret, frame = video.read()
        if not ret:
            break
        
        cv2.imshow('main_window', frame)
        cv2.waitKey(int(1000/(fps*2)))  # I don't really understand why

    # white screen display
    white = cv2.imread('white_background.png')
    cv2.imshow('main_window', white)
    cv2.waitKey(1000)

    wait() # wait for recording to finish
    audio_file = f"{video_file[:-4]}_{PARTICIPANT_ID}_{PARTICIPANT_ID2}.wav"
    audio_path = os.path.join(AUDIO_DIRECTORY, audio_file)
    write(audio_path, sample_rate, recording)

    ws.append([PARTICIPANT_ID, i+1, video_file, audio_path])

    video.release()
cv2.destroyAllWindows()

data_file = f"{PARTICIPANT_ID}_{PARTICIPANT_ID2}.xlsx"
data_path = os.path.join(DATA_DIRECTORY, data_file)
wb.save(data_path)

