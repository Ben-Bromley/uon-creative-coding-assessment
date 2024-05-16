# IMPORT LIBRARIES #
import wave
# import sys
# import time
import pyaudio
# import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import librosa.feature
from PIL import Image


# FUNCTION TO RECORD AUDIO FROM THE AUDIO STREAM [PYAUDIO] #
def record_audio(filename,
                 _duration,
                 _format=pyaudio.paInt24,
                 _channels=1, rate=44100,
                 _frames_per_buffer=1024):
    # create the audio stream to record on
    p = pyaudio.PyAudio()
    stream = p.open(format=_format,  # what to save the samples as
                    channels=_channels,  # the number of channels to use
                    rate=rate,  # how quick to sample at (bits recorded per second)
                    input=True,  # stream recieves audio
                    frames_per_buffer=_frames_per_buffer)  # number of samples per buffer

    print("Recording...")  # state that the stream is about to start recording
    frames = []  # array to store the recorded samples in

    for i in range(0, int(rate / _frames_per_buffer * _duration)):  # for each buffer
        data = stream.read(_frames_per_buffer)  # read in the frames from the buffer
        frames.append(data)  # add them on to the end of the frames array

    print("Recording complete.")  # state that the stream has stopped recording
    stream.stop_stream()  # close to save memory
    stream.close()  # close to save memory
    p.terminate()  # close to save memory

    wf = wave.open(filename, 'wb')  # create a new file to write to called filename
    wf.setnchannels(_channels)  # set the number of channels it uses
    wf.setsampwidth(p.get_sample_size(_format))  # set the sample size based on the format
    wf.setframerate(rate)  # set the sample rate
    wf.writeframes(b''.join(frames))  # write the frames to the file
    wf.close()  # close to save memory


# FUNCTION TO ANALYSE AND EXTRACT INFORMATION FROM THE AUDIO - AUDIO ANALYSIS [LIBROSA] #
def analyze_audio(file_path):
    y, sr = librosa.load(file_path)  # LOAD THE AUDIO FILE
    # EXTRACT TIME #
    # duration = librosa.get_duration(y=y, sr=sr)  # SAVE THE LENGTH OF THE FILE
    # EXTRACT FREQUENCY CONTENT #
    # get the spectral centroid (average frequency of the sound over time)
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    rms = librosa.feature.rms(y=y)[0]  # calculate the average amplitude for each sample change
    return y, sr, spectral_centroids, rms  # 'y' = DATATYPE, 'sr' = TARGET SAMPLE RATE


# COLOUR MAP/KEY ARRAY - USED TO TRANSLATE THE EXTRACTED DATA #
def create_colour_matrix():
    return np.array([
        [245, 100, 191],  # PINK   = SUB      values
        [191, 100, 245],  # PURPLE = BASS     values
        [100, 191, 245],  # BLUE   = LOW MID  values
        [191, 245, 100],  # GREEN  = MID      values
        [245, 251, 100],  # YELLOW = HIGH MID values
        [245, 191, 100]])  # ORANGE = HIGH     values


# FUNCTION TO CONVERT NUMERICAL VALUES TO COLOURS#
def value_to_colour(value, min_value, max_value, colour_matrix):
    log_values = np.log(np.clip(value, a_min=min_value, a_max=max_value)+ 1)
    log_min = np.log(min_value + 1)
    log_max = np.log(max_value + 1)

    norm_value = (log_values - log_min) / (log_max - log_min)
    color_idx = (norm_value * (len(colour_matrix) - 1)).astype(int)
    color_idx = np.clip(color_idx, 0, len(colour_matrix) - 1)  # Ensure the index is within valid range
    return colour_matrix[color_idx]

    # normalise the value to be between 0 and 1
    # norm_value = (value - min_value) / (max_value - min_value)
    # determine what colour it should equate to
    # colour_id = int(norm_value * (len(colour_matrix) - 1))    # -1 to select correct array position
    # return colour_matrix[colour_id]  # return that colour id


# FUNCTION TO CONVERT NUMERICAL VALUES TO AN RGBA ALPHA/TRANSPARENCY LEVEL
def value_to_alpha(value, min_value, max_value):
    # normalise the value to be between 0 and 1
    norm_value = (value - min_value) / (max_value - min_value)
    return int(norm_value * 255)


# CONVERT THE AUDIO INTO VISUALS - DATA CONVERSION #
def convert_audio_to_visuals(spectral_centroids,
                             rms,
                             colour_matrix):
    width, height = 800, 800  # the sizes of the image
    visual = Image.new("RGBA", (width, height))  # create a new image file
    pixels = visual.load()  # create a place to store the pixel data

    num_frames = len(spectral_centroids)
    colours = value_to_colour(spectral_centroids,
                              np.min(spectral_centroids),
                              np.max(spectral_centroids),
                              colour_matrix)
    min_rms, max_rms = np.min(rms), np.max(rms)

    # for every pixel in the image
    # Map spectral centroids and RMS to pixels
    for x in range(width):  # for the length of the image
        # determine the time period associated with the x position
        idx = int(x / width * num_frames)
        colour = colours[idx]  # get the colour for that pixel

        # convert the amplitude value into it's appropriate alpha value
        alpha = value_to_alpha(rms[idx], min_rms, max_rms)

        for y in range(height):
            pixels[x, y] = (colour[0], colour[1], colour[2] , alpha)

    return visual


# FUNCTION THAT ENCAPSULATES THE PROCESS OF CREATING ART FROM AUDIO #
def create_artwork(file_path):
    y, sr, spectral_centroids, rms = analyze_audio(file_path)  # obtain the audio to be analysed
    #
    # duration, spectral_centroids, spectral_centroids_time, rms, rms_time = extract_audio_features(y, sr)
    # instantiate the colour matrix
    colour_matrix = create_colour_matrix()
    # perform the conversion
    artwork = convert_audio_to_visuals(spectral_centroids, rms, colour_matrix)
    return artwork


# FUNCTION TO SAVE THE ARTWORK AS AN IMAGE FILE #
def save_artwork(artwork, filename):
    artwork.save(filename)


# main operation
if __name__ == "__main__":
    audio_filename = "recorded_audio.wav"  # name to save the recorded audio file as
    artwork_filename = "audio_artwork.png"  # name to save the created artwork file as


    choice = input("Would you like to (R)ecord a new audio file or use an (E)xisting one? (R/E): ").strip().lower()

    if choice == 'r':
        length = int(input("Enter the length of the recording in seconds: ").strip())
        record_audio(audio_filename, length)
        print(f"Recording saved as {audio_filename}")  # display after saving artwork
    elif choice == 'e':
        audio_filename = (input("Enter the path to the existing audio file: ").strip())

    image = create_artwork(audio_filename)  # create the image of art made by the recorded file
    save_artwork(image, artwork_filename)  # save the image with the given file name
    print(f"Artwork saved as {artwork_filename}")  # display after saving artwork
