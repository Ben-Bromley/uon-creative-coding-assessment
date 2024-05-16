from PIL import Image
import numpy as np
from library.matrix import Matrix

#


class Converter:

    #
    def get_colour_matrix(self):
        matrix_generator = Matrix()
        return matrix_generator.generate()

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

        # return given colour
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

    def convert_audio_to_visuals(self, average_freq, average_amp):
        width, height = 800, 800  # image dimensions
        # instantiate image object 800x800px
        visual = Image.new("RGBA", (width, height))
        pixels = visual.load()  # load pixel data, allocate memory for image

        # get total number of samples captured
        num_frames = len(average_freq)
        colours = self.value_to_colour(average_freq,
                                       np.min(average_freq),
                                       np.max(average_freq))
        min_amplitude, max_amplitude = np.min(average_amp), np.max(average_amp)

        # for each column of pixels in the image, assign a colour
        for x in range(width):
            # determine the time period associated with the x position
            idx = int(x / width * num_frames)
            colour = colours[idx]  # get the colour for that pixel

            # convert the amplitude value into it's appropriate alpha value
            alpha = self.value_to_alpha(
                average_amp[idx], min_amplitude, max_amplitude)

            # go down the height of the image and fill in the pixels
            for y in range(height):
                pixels[x, y] = (colour[0], colour[1], colour[2])

        return visual
