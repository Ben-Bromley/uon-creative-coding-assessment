from time import sleep
from random import random
import pyaudio
import numpy as np
import math
from threading import Thread


class Listener:
    def __init__(self):
        """Initialise the Listener object with the required attributes"""

        # sets running to true which maintains the while loop in audio_analyser()
        self.running = True

        #
        self.CHUNK = 2 ** 11
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        # array of notes names to be stored in neonote
        self.list_of_notes = ['a', 'bf', 'b', 'c',
                              'df', 'd', 'ef', 'e', 'f', 'gf', 'g', 'af']
        self.amplitude = 0,
        self.freq = 0
        self.neonote = 'a'

    def start(self):
        print("mic listener: started!")

        # creates a new thread for running the analysis function
        audio_thread = Thread(target=self.audio_analyser)
        audio_thread.start()

    def audio_analyser(self):
        while self.running:
            data = np.frombuffer(self.stream.read(self.CHUNK,
                                                  exception_on_overflow=False),
                                 dtype=np.int16)
            peak = np.average(np.abs(data)) * 2
            if peak > 1000:
                bars = "#" * int(50 * peak / 2 ** 16)

                #
                data = data * np.hanning(len(data))
                fft = abs(np.fft.fft(data).real)
                fft = fft[:int(len(fft) / 2)]
                frq = np.fft.fftfreq(self.CHUNK, 1.0 / self.RATE)
                frq = frq[:int(len(frq) / 2)]
                self.freq = frq[np.where(fft == np.max(fft))[0][0]] + 1

                # assign to neonote, a note name, calculated by freq_to_note, based on the frequency of the note
                self.neonote = self.freq_to_note(self.freq)

                # Shows the peak frequency and the bars for the amplitude
                print(
                    f"peak frequency: {self.freq} Hz, mididnote {self.neonote}:\t {bars}")

            self.amplitude = peak

    def freq_to_note(self, freq: float) -> list:
        """
        Convert a given frequency to a neoscore compatible note name
        
        It retrieves the note name by following an algorithm
        which converts a frequence in Hertz, to an array index 0-11

        It appends notation to dictate octave by calculating the octave number
        and adding the corresponding amount of commas or inverted commas to the note name
        """

        # converts frequency into a note name and octave number
        note_number = 12 * math.log2(freq / 440) + 49 #
        note_number = round(note_number) # 
        note_position = (note_number - 1) % len(self.list_of_notes)
        neonote = self.list_of_notes[note_position]
        octave = (note_number + 8) // len(self.list_of_notes)

        # if the octave of the pitch is between 2-6 (inclusive)
        if 2 <= octave <= 6:

            # if the octave is greater than 4 (middle C)
            if octave > 4:
                # find the remaining octaves difference
                ticks = octave - 4
                # add that number of inverted commas to the note, to ensure the note is displayed in the correct octave above middle C
                for tick in range(ticks):
                    neonote += "'"

            # if the octave is less than 4 (middle C octave)
            elif octave < 4:
                if octave == 3:
                    #  for octave 3, add a single comma to ensure the note is displayed 1 octave below middle C
                    neonote += ","
                elif octave == 2:
                    #  for octave 3, add two commas to ensure the note is displayed 2 octaves below middle C
                    neonote += ",,"

        return [neonote]

    def terminate(self):
        """safely terminates all streams"""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


if __name__ == "__main__":
    mic = Listener()
    mic.start()
    while True:
        print(mic.freq,
              mic.amplitude,
              mic.neonote
              )
        sleep(1)
