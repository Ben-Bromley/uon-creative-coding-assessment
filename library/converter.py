from PIL import Image
import numpy as np


class Converter:

    def get_colour_matrix(self):
        return np.array([
            [245, 100, 191],  # PINK   = SUB      values
            [191, 100, 245],  # PURPLE = BASS     values
            [100, 191, 245],  # BLUE   = LOW MID  values
            [191, 245, 100],  # GREEN  = MID      values
            [245, 251, 100],  # YELLOW = HIGH MID values
            [245, 191, 100]])  # ORANGE = HIGH     values

    # FUNCTION TO CONVERT NUMERICAL VALUES TO COLOURS#
    def value_to_colour(self, value, min_value, max_value):
        colour_matrix = self.get_colour_matrix()

        log_values = np.log(
            np.clip(value, a_min=min_value, a_max=max_value) + 1)
        log_min = np.log(min_value + 1)
        log_max = np.log(max_value + 1)

        norm_value = (log_values - log_min) / (log_max - log_min)
        color_idx = (norm_value * (len(colour_matrix) - 1)).astype(int)
        # Ensure the index is within valid range
        color_idx = np.clip(color_idx, 0, len(colour_matrix) - 1)
        return colour_matrix[color_idx]

        # normalise the value to be between 0 and 1
        # norm_value = (value - min_value) / (max_value - min_value)
        # determine what colour it should equate to
        # colour_id = int(norm_value * (len(colour_matrix) - 1))    # -1 to select correct array position
        # return colour_matrix[colour_id]  # return that colour id

    # FUNCTION TO CONVERT NUMERICAL VALUES TO AN RGBA ALPHA/TRANSPARENCY LEVEL

    def value_to_alpha(self, value, min_value, max_value):
        # normalise the value to be between 0 and 1
        norm_value = (value - min_value) / (max_value - min_value)
        return int(norm_value * 255)

    # CONVERT THE AUDIO INTO VISUALS - DATA CONVERSION #

    def convert_audio_to_visuals(self, spectral_centroids,
                                 rms):
        width, height = 800, 800  # the sizes of the image
        visual = Image.new("RGBA", (width, height))  # create a new image file
        pixels = visual.load()  # create a place to store the pixel data

        num_frames = len(spectral_centroids)
        colours = self.value_to_colour(spectral_centroids,
                                       np.min(spectral_centroids),
                                       np.max(spectral_centroids))
        min_rms, max_rms = np.min(rms), np.max(rms)

        # for every pixel in the image
        # Map spectral centroids and RMS to pixels
        for x in range(width):  # for the length of the image
            # determine the time period associated with the x position
            idx = int(x / width * num_frames)
            colour = colours[idx]  # get the colour for that pixel

            # convert the amplitude value into it's appropriate alpha value
            alpha = self.value_to_alpha(rms[idx], min_rms, max_rms)

            for y in range(height):
                pixels[x, y] = (colour[0], colour[1], colour[2], alpha)

        return visual
