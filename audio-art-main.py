# IMPORT OUR CUSTOM LIBRARIES #
from library.artist import Artist
from library.audio import Audio

# main thread
if __name__ == "__main__":
    audio_filename = "recorded_audio.wav"  # name to save the recorded audio file as
    artwork_filename = "audio_artwork.png"  # name to save the created artwork file as
    
    artist = Artist()  # create an instance of the Artist class
    recorder = Audio()  # create an instance of the Audio class

    choice = input("Would you like to (R)ecord a new audio file or use an (E)xisting one? (R/E): ").strip().lower()

    if choice == 'r':
        length = int(input("Enter the length of the recording in seconds: ").strip())
        recorder.record_audio(audio_filename, length)
        print(f"Recording saved as {audio_filename}")  # display after saving artwork
    elif choice == 'e':
        audio_filename = (input("Enter the path to the existing audio file: ").strip())
    else: 
        print("Invalid choice. Exiting...")
        exit()

    image = artist.create_artwork(audio_filename)  # create the image of art made by the recorded file
    artist.save_artwork(image, artwork_filename)  # save the image with the given file name
    print(f"Artwork saved as {artwork_filename}")  # display after saving artwork
