#
from music21 import converter

#
def get_midi_lists(mf: str) -> list:
    """INSERT DOCSTRING HERE"""

    # parses a midi file when given the filepath
    score_in = converter.parseFile(mf)

    #
    components = []

    # loops over all of the messages for the notes and rests in the midi score
    for msg in score_in.recurse().notesAndRests:

        # if the note is a quarter note
        if msg.duration.quarterLength != 0:

            # attempt to run the contained code, with a fallback (see "except")
            try:
                pitchlist = msg.pitches

                # for all pitches in the current message
                for pitch in pitchlist:
                    #
                    neopitch = make_neonote(pitch)

                    #
                    if not None:
                        components.append(neopitch)

            # If the above code encounters an error, print an error, alongside the current message we're looking at
            except:
                print("error:", msg)

    return components

def make_neonote(pitch):
    neopitch = pitch.name.lower()
    neooctave = pitch.octave

    if neopitch[-1] == "#":
        neopitch = f"{neopitch[0]}s"
    elif neopitch[-1] == "-":
        neopitch = f"{neopitch[0]}f"

    #
    if 2 <= neooctave <= 6:

        #
        if neooctave > 4:
            ticks = neooctave - 4
            for tick in range(ticks):
                neopitch += "'"

        #
        elif neooctave < 4:
            if neooctave == 3:
                neopitch += ","
            elif neooctave == 2:
                neopitch += ",,"

        return neopitch


if __name__ == "__main__":
    component_list = get_midi_lists("media/A_Sleepin_Bee.mid")
    for c in component_list:
        print(c)
