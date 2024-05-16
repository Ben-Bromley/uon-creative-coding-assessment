from library.audio import Audio
from library.converter import Converter


# This class is used to abstract the mathematical process of converting audio into art
class Artist:

    def __init__(self):
        self.audio_manager = Audio()
        self.audio_converter = Converter()

    def create_artwork(self, file_path):
        """
          1. Use our audio manager to get the stats we need
          2. Use our audio converter to tranlsate those stats into an image
        """

        # obtain the audio to be analysed
        average_freq, average_amp = self.audio_manager.analyze_audio(file_path)

        # given the freq & amp stats, produce an image and return it
        artwork = self.audio_converter.convert_audio_to_visuals(
            average_freq, average_amp)
        return artwork

    def save_artwork(self, artwork, filename):
        """
          accepts a PIL module "Image" object
          Uses the inbuilt save function to 
        """
        artwork.save(filename)
