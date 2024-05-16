from PIL import Image
import numpy as np
import colorsys

#


class Converter:

    def pitches_to_hues(self, average_freqs):
        """
            convert the list of average pitches into a list of hue values
        """
        # create a list of values 0-255 to select from
        hue_range = np.array(range(255))

        # get min & max values
        min_freq, max_freq = np.min(average_freqs), np.max(average_freqs)

        # use log values to simplify numbers
        log_values = np.log(average_freqs + 1)
        log_min = np.log(min_freq + 1)
        log_max = np.log(max_freq + 1)

        # a list of how high notes are within the range, represented as a number between 0-1
        pitch_percentages = (log_values - log_min) / (log_max - log_min)
        # convert percent into an index of hue_range
        color_idx = (pitch_percentages * (len(hue_range) - 1)).astype(int)

        # Ensure index is within valid range
        color_idx = np.clip(color_idx, 0, len(hue_range) - 1)

        # return given colour
        return hue_range[color_idx]

    def amplitude_to_saturation(self, current_avg_amp, average_amps):
        """
            Calculate a percentage saturation based on how high the current avg amp is
            use the minimum average amplitude to adjust incase of non-zero minimums
        """
        min_amplitude, max_amplitude = np.min(
            average_amps), np.max(average_amps)
        saturation = int(((current_avg_amp - min_amplitude) /
                         (max_amplitude - min_amplitude)) * 100)
        return saturation

    def hsl_to_rgb(self, hue, saturation, lightness=100):
        """
            accept typical 0-255 hue, 0-100 saturation, and 0-100 lightness
            return an RGB value
        """
        # normalise values, colorsys expects 0-1
        hue = hue / 255
        saturation = saturation / 100
        lightness = lightness / 100

        # 
        decimal_rgb = colorsys.hls_to_rgb(hue, lightness, saturation)

        # 
        rgb_list = []
        for value in decimal_rgb:
            rgb_list.append(int(value * 255))
        
        return tuple(rgb_list)

    def convert_audio_to_visuals(self, average_freqs, average_amps):
        """
            initialise a PIL image, calculate colours based on amp & freq,
            then add those colours to 2d pixel array
        """
        width, height = 800, 800  # image dimensions
        # instantiate image object 800x800px
        visual = Image.new("RGBA", (width, height))
        pixels = visual.load()  # load pixel data, allocate memory for image

        # get total number of samples captured
        num_frames = len(average_freqs)

        # for each column of pixels in the image, assign a colour
        for x in range(width):
            # determine the time period associated with the x position
            idx = int(x / width * num_frames)
            # convert the amplitude into a saturation
            saturation = self.amplitude_to_saturation(
                average_amps[idx], average_amps)
            hues = self.pitches_to_hues(average_freqs)
            hue = hues[idx]  # get the colour for that pixel

            # convert to rgb for pixel map
            rgb = self.hsl_to_rgb(hue, saturation, lightness=50)

            # go down the height of the image and fill in the pixels
            for y in range(height):
                pixels[x, y] = rgb

        return visual
