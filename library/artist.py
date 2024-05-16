from library.audio import Audio
from library.converter import Converter


# This class is used to abstract the mathematical process of converting audio into art
class Artist:

    def __init__(self):
        self.audio_manager = Audio()
        self.audio_converter = Converter()

    # FUNCTION THAT ENCAPSULATES THE PROCESS OF CREATING ART FROM AUDIO #
    def create_artwork(self, file_path):
        y, sr, spectral_centroids, rms = self.audio_manager.analyze_audio(
            file_path)  # obtain the audio to be analysed
        artwork = self.audio_converter.convert_audio_to_visuals(
            spectral_centroids, rms)  # perform the conversion
        return artwork

    # FUNCTION TO SAVE THE ARTWORK AS AN IMAGE FILE #
    def save_artwork(self, artwork, filename):
        artwork.save(filename)
