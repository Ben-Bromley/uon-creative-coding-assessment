import librosa
import wave
import pyaudio

# 
class Audio:
    # FUNCTION TO RECORD AUDIO FROM THE AUDIO STREAM [PYAUDIO] #
    def record_audio(self, filename,
                     _duration,
                     _format=pyaudio.paInt24,
                     _channels=1, rate=44100,
                     _frames_per_buffer=1024):
        # create the audio stream to record on
        p = pyaudio.PyAudio()
        stream = p.open(format=_format,  # what to save the samples as
                        channels=_channels,  # the number of channels to use
                        # how quick to sample at (bits recorded per second)
                        rate=rate,
                        input=True,  # stream recieves audio
                        frames_per_buffer=_frames_per_buffer)  # number of samples per buffer

        # state that the stream is about to start recording
        print("Recording...")
        frames = []  # array to store the recorded samples in

        for i in range(0, int(rate / _frames_per_buffer * _duration)):  # for each buffer
            # read in the frames from the buffer
            data = stream.read(_frames_per_buffer)
            frames.append(data)  # add them on to the end of the frames array

        # state that the stream has stopped recording
        print("Recording complete.")
        stream.stop_stream()  # close to save memory
        stream.close()  # close to save memory
        p.terminate()  # close to save memory

        # create a new file to write to called filename
        wf = wave.open(filename, 'wb')
        wf.setnchannels(_channels)  # set the number of channels it uses
        # set the sample size based on the format
        wf.setsampwidth(p.get_sample_size(_format))
        wf.setframerate(rate)  # set the sample rate
        wf.writeframes(b''.join(frames))  # write the frames to the file
        wf.close()  # close to save memory

    # FUNCTION TO ANALYSE AND EXTRACT INFORMATION FROM THE AUDIO - AUDIO ANALYSIS [LIBROSA] #

    def analyze_audio(self, file_path):
        y, sr = librosa.load(file_path)  # LOAD THE AUDIO FILE

        # EXTRACT TIME #
        # duration = librosa.get_duration(y=y, sr=sr)  # SAVE THE LENGTH OF THE FILE

        # EXTRACT FREQUENCY CONTENT #
        # get the spectral centroid (average frequency of the sound over time)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        # calculate the average amplitude for each sample change
        rms = librosa.feature.rms(y=y)[0]
        # 'y' = DATATYPE, 'sr' = TARGET SAMPLE RATE
        return y, sr, spectral_centroids, rms
