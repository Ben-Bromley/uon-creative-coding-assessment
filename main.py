import midi
from random import choice, random
from listener import Listener
from neoscore.common import *

path_to_midi_file = "media/A_Sleepin_Bee.mid" #  <--- change this to your file

class UI:
    """INSERT DOCSTRING HERE
        This class is responsible for the creation
    """

    def __init__(self):
        """This function instantiates the class"""

        # 
        self.midilist = midi.get_midi_lists(path_to_midi_file)
        print(f"Midilist contents: {self.midilist}")

        # initialises the neoscore library, before it's used
        neoscore.setup()

        # Create some text to display on our score
        annotation = "DEMO digital score BLAH BLAH"
        RichText((Mm(1), Mm(1)), None, annotation, width=Mm(170))

        # creates a musical Staff, with the below specifications
        staff = Staff((ZERO, Mm(70)), None, Mm(180), line_spacing=Mm(5))
        unit = staff.unit
        clef = Clef(ZERO, staff, "treble")

        #
        self.center = unit(20)

        #
        self.n1 = Chordrest(self.center, staff, ["g"], Duration(1, 4))
        self.n2 = Chordrest(self.center, staff, ["b"], Duration(1, 4))
        self.n3 = Chordrest(self.center, staff, ["d'"], Duration(1, 4))
        self.n4 = Chordrest(self.center, staff, ["f'"], Duration(1, 4))

        #
        self.note_list = (self.n1, self.n2, self.n3, self.n4)

        #
        self.ear = Listener()
        self.ear.start()

    def refresh_func(self, time):
        """INSERT DOCSTRING HERE"""

        #
        rnd_note = choice(self.note_list)
        if random() >= 0.5:
            new_pitch = choice(self.midilist)
        else:
            new_pitch = self.ear.neonote

        #
        try:
            rnd_note.notes = [new_pitch]
        except:
            pass


if __name__ == "__main__":
    run = UI()
    neoscore.set_refresh_func(run.refresh_func, target_fps=1)
    neoscore.show(display_page_geometry=False,
                  auto_viewport_interaction_enabled=False
                  )
