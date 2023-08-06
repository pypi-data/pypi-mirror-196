import os
import random
import time
import cv2
import PySimpleGUI as sg
from sounddevice import rec, wait
from scipy.io.wavfile import write
from openpyxl import Workbook

class Parameters:
    def __init__(self):
        self.participant_ID = None
        self.fixation_duration = None
        self.white_duration = None
        self.audio_duration = None
        self.video_dir = None
        self.audio_dir = None
        self.data_dir = None
        self.sample_rate = 44100
        self.unique_key = str(time.time())
        

def gui():
    layout = [

        [
        sg.Column([
            [sg.Text("Participant ID:")],
            [sg.Text("Fixation Duration (ms):")],
            [sg.Text("White Duration (ms):")],
            [sg.Text("Audio Duration (s):")],
            ], element_justification="left", pad=(0, 5)),

        sg.Column([
            [sg.InputText(size = (35, 1), key = "-PARTICIPANT_ID-")],
            [sg.InputText(default_text="1000", key="-FIX-DURATION-", size=(10, 1))],
            [sg.InputText(default_text="1000", key="-WHITE-DURATION-", size=(10, 1))],
            [sg.InputText(default_text="6", key="-AUDIO-DURATION-", size=(10, 1))],
            ], element_justification="left", pad=(0, 5))
        ],

        [
        sg.Column([
            [sg.Text("Video Directory:")],
            [sg.Text("Audio Directory:")],
            [sg.Text("Data Directory:")],
            ], element_justification="left", pad=(0, 5)),

        sg.Column([
            [sg.InputText(default_text="VIDEO_FILES", key="-VIDEO-DIR-", size=(40, 1)), sg.FolderBrowse()],
            [sg.InputText(default_text="AUDIO_RECORDINGS", key="-AUDIO-DIR-", size=(40, 1)), sg.FolderBrowse()],
            [sg.InputText(default_text="DATA_FOLDER", key="-DATA-DIR-", size=(40, 1)), sg.FolderBrowse()],
            ], element_justification="left", pad=(0, 5))
        ],
        
        [
        sg.Column([ 
            [sg.Button("Start Experiment", size=(20,1))]
            ], expand_x=True, element_justification="left", pad=(0, 5)),
        
        sg.Column([ 
            [sg.Button("Reset", size=(10,1)), sg.Button("Cancel", size=(10,1))] 
            ], expand_x=True, element_justification="right", pad=(0, 5))
        ],
    ]
    
    window = sg.Window("Experiment Setup", layout)
    parameters = Parameters()
    
    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            exit()
        if event == "Start Experiment":
            parameters.participant_id = str(values["-PARTICIPANT_ID-"])
            parameters.fixation_duration = int(values["-FIX-DURATION-"])
            parameters.white_duration = int(values["-WHITE-DURATION-"])
            parameters.audio_duration = int(values["-AUDIO-DURATION-"])
            parameters.video_dir = values["-VIDEO-DIR-"]
            parameters.audio_dir = values["-AUDIO-DIR-"]
            parameters.data_dir = values["-DATA-DIR-"]
            window.close()
            break
        if event == "Reset":
            window["-PARTICIPANT_ID-"].update("")
            window["-FIX-DURATION-"].update("1000")
            window["-WHITE-DURATION-"].update("1000")
            window["-AUDIO-DURATION-"].update("6")
            window["-VIDEO-DIR-"].update("VIDEO_FILES")
            window["-AUDIO-DIR-"].update("AUDIO_RECORDINGS")
            window["-DATA-DIR-"].update("DATA_FOLDER")

    window.close()
    return parameters

def main():
    # Create the GUI to enter experiment parameters, returns a parameters object
    parameters = gui()
    video_files = [f for f in os.listdir(parameters.video_dir) if f.endswith('.avi')]
    print(parameters.participant_id)
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

        video_path = os.path.join(parameters.video_dir, video_file)
        video      = cv2.VideoCapture(video_path)
        fps        = video.get(cv2.CAP_PROP_FPS)
        num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Fixation screen display
        fixation = cv2.imread('fixation.png')
        cv2.imshow('main_window', fixation)
        cv2.waitKey(parameters.fixation_duration)

        recording    = rec(int(parameters.audio_duration * parameters.sample_rate), 
                        samplerate=parameters.sample_rate, channels=1)
        
        while True: # Video playing loop
            ret, frame = video.read()
            if not ret:
                break
            
            cv2.imshow('main_window', frame)
            cv2.waitKey(int(1000/(fps*2)))  # I don't really understand why

        # white screen display
        white = cv2.imread('white_background.png')
        cv2.imshow('main_window', white)
        cv2.waitKey(parameters.white_duration)
        

        wait() # wait for recording to finish
        audio_file = f"{video_file[:-4]}_{parameters.participant_id}_{parameters.unique_key}.wav"
        audio_path = os.path.join(parameters.audio_dir, audio_file)
        write(audio_path, parameters.sample_rate, recording)

        ws.append([parameters.participant_id, i+1, video_file, audio_path])

        video.release()

    cv2.destroyAllWindows()

    data_file = f"{parameters.participant_id}_{parameters.unique_key}.xlsx"
    wb.save(os.path.join(parameters.data_dir, data_file))

if __name__ == "__main__":
    main()