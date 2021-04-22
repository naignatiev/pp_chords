from scipy.io.wavfile import write
import numpy as np
from dataclasses import dataclass
from itertools import product


NOTES = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']


class ChordMaker:
    def __init__(self, sample_rate=44100, during=30):
        """
        :param sample_rate: Hz
        :param during: in seconds
        """
        self.sample_rate = sample_rate
        self.during = during
        self.amplitude = np.iinfo(np.int16).max

    def save_chord(self, notes: list, wav_name):
        """
        :param notes: list of notes in Hz
        :return:
        """
        sins = []
        for note_hz in notes:
            sins.append(self.amplitude * np.cos(self.__get_t() * 2 * np.pi * note_hz))
        resulting_data = np.sum(sins, axis=0) / len(sins)
        write(wav_name, self.sample_rate, resulting_data.astype(np.int16))

    def __get_t(self):
        return np.linspace(0., self.during, self.sample_rate * self.during)


class NoteSystem:

    def __init__(self, tuning='12TET', a4_hz=440):
        self.a4_hz = a4_hz
        if tuning == '12TET':
            self.__init_12tet(a4_hz)
        self.tuning = tuning

    def __init_12tet(self, a4_hz):
        for note, octave in product(NOTES, (2, 3, 4, 5)):
            self.__setattr__(f'{note}{octave}', a4_hz * np.power(2, self._get_dist(note, octave) / 12))

    def _get_dist(self, _note, _octave):
        _octave = int(_octave)
        return (NOTES.index(_note) - NOTES.index('a')) + (_octave - 4) * 12


class Guitar(NoteSystem):
    def __init__(self, tuning='12TET', a4_hz=440):
        super().__init__(tuning, a4_hz)
        self.opened = ('e2', 'a2', 'd3', 'g3', 'b3', 'e4')

    def get_hzs_by_tabs(self, tabs=(None, None, None, None, None, None)):
        hzs = []
        for i, t in enumerate(tabs):
            if t:
                hzs.append(
                    self.a4_hz * np.power(2, (self._get_dist(*self.opened[i]) + t) / 12))
        return hzs


if __name__ == '__main__':
    chords = {
        'Em6': (0, 4, 5, 5, 5, None),
        'E7sus2|D': (None, 2, 0, 2, 2, 0),
        'F#aug': (2, None, None, 3, 3, 2),
        'Bm6': (2, None, 1, 2, 2, None),
        'Fsus2|D#': (None, None, 13, 12, 13, 13),
        'Fadd9': (None, 8, 7, 5, 8, None),
        'Gmaj7': (3, 5, 5, 7, 7, 7),
        'G|B': (None, 2, 0, 0, 3, None),
        'Amaj9': (None, 0, 11, 13, 12, 0),
        'Dmadd9|A': (None, 0, 3, 2, 3, 0),
        'Am': (5, None, None, 5, 5, 5),
        'G#m7': (4, 6, 4, 4, None, None),
        'Am|C': (8, 7, 7, 9, None, None),
        'D#maj7|A#': (6, 6, 5, 7, None, None),
        'Am9(no5)': (5, 3, 5, 4, None, None),
        'Cadd11': (None, 3, 3, 0, 1, 0),
        'G6add9': (3, 2, 2, 2, 3, None),
        'Ebmaj7|G#': (4, 6, 5, 7, None, None),
        'Dmaj7|C#': (9, 9, 0, 7, 7, None),
        'Fm|Ab': (4, None, 6, 5, 6, None),
        'Dm|A': (None, 0, 3, 2, 3, 1),
        'Amadd9(no5)': (None, 0, 7, 5, 0, None),
        'Bm9|F#': (2, 2, 0, 2, 2, None)
    }
    for name, chord in chords.items():
        ChordMaker(during=10).save_chord(notes=Guitar().get_hzs_by_tabs(
            chord), wav_name=f'chords/{name}.wav')
