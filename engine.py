import mingus
import mingus.core.chords as chords
from mingus.containers import NoteContainer, Note
from mingus.midi import midi_file_out as MidiFileOut
from midiutil.MidiFile import MIDIFile

class Engine:
    prior_chord_root = []
    prior_voice_led_chord = None

    def __init__(self, chord_seq):

        with open(chord_seq) as inp:
            lines = inp.read().split(',')

        lines = list(filter((lambda x: False if x == '' else True), lines))
        self.chord_seq = lines
        self.voice_led_chords = []

        #write midi file
        time = 0
        midi = MIDIFile(1)
        midi.addTempo(0, time, 120)
        midi.addTrackName(0, time, "ss")
        for chord in self.chord_seq:
            root_pos = self.construct_chord(chord)
            vl = self.voice_led_chord(root_pos)
            for note in vl:
                midi.addNote(track=0, channel=0, pitch=int(note), time=time, duration=3, volume=100)

            time += 3
        binfile = open("./Lateef/output.mid", 'wb')
        midi.writeFile(binfile)
        binfile.close()

    def construct_chord(self, chord):
        space_ind = chord.index(" ")
        chord_qual_ind = space_ind + 1
        tension_ind = chord_qual_ind + 3
        note_name = chord[:space_ind]
        if '/' in note_name:
            i = note_name.index('/')
            note_name = note_name[:i]

        chord_type = chord[chord_qual_ind: tension_ind]
        if chord_type == 'Min':
            chord_type = 'm'
        elif chord_type == 'Dom':
            chord_type = ''
        else:
            chord_type = 'M'

        tension_level = chord[tension_ind:]
        if tension_level == '11/13':
            tension_level = '13' if chord_type != 'm' else '11'

        chord = note_name + chord_type + tension_level
        return chords.from_shorthand(chord)

    def generate_chord_init_voicings(self, root_pos):
        n = NoteContainer()
        for note in root_pos:
            # select octave for each pitch of initial chord
            if root_pos.index(note) == 1:
                octave = 4
            elif root_pos.index(note) == 3:
                octave = 4 if note != 'C#' and note != 'D' and note != 'D#' and note != 'E' else 5
            elif root_pos.index(note) == 2:
                octave = 5
            elif root_pos.index(note) == 0:
                octave = 3
            else:
                octave = 6
            # add note to container
            n.add_note(Note(note, octave))
        return n

    def voice_led_chord(self, root_pos):
        n = NoteContainer()
        # if its the first chord in the sequence...
        if self.prior_voice_led_chord is None:
            n = self.generate_chord_init_voicings(root_pos)
        # if its not the first in the sequence
        else:
            old_voice_lead = self.prior_voice_led_chord
            new_root = self.generate_chord_init_voicings(root_pos)
            old_voice_lead_int = list(map(lambda x: int(x), old_voice_lead))
            new_root_int = list(map(lambda x: int(x), new_root))
            # given 2 list of ints, finds the mapping from one element in the old list to one of the new list closest to it
            new_voice_led_int = list(map(lambda y: min(new_root_int, key=lambda x: abs(x - y)), old_voice_lead_int))

            # list of notes, now voice led
            new_voice_led = list(map(lambda x: Note().from_int(x), new_voice_led_int))
            for notee in new_voice_led:
                n.add_note(notee)

            bass = (root_pos[0])
            n.add_note(Note(bass, 2))

        # update new prior root position chord, voice led chord, and add to list of chords
        self.prior_chord_root = root_pos
        self.prior_voice_led_chord = n
        self.voice_led_chords.append(n)
        return n

