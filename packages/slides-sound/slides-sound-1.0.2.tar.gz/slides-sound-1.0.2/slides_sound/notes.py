#!/usr/bin/python -u
import re
import os
import wave
import math
import fluidsynth as fl

notes = {
"C0":16.35,
"C#0":17.32,
"Db0":17.32,
"D0":18.35,
"D#0":19.45,
"Eb0":19.45,
"E0":20.60,
"F0":21.83,
"F#0":23.12,
"Gb0":23.12,
"G0":24.50,
"G#0":25.96,
"Ab0":25.96,
"A0":27.50,
"A#0":29.14,
"Bb0":29.14,
"B0":30.87,
"C1":32.70,
"C#1":34.65,
"Db1":34.65,
"D1":36.71,
"D#1":38.89,
"Eb1":38.89,
"E1":41.20,
"F1":43.65,
"F#1":46.25,
"Gb1":46.25,
"G1":49.00,
"G#1":51.91,
"Ab1":51.91,
"A1":55.00,
"A#1":58.27,
"Bb1":58.27,
"B1":61.74,
"C2":65.41,
"C#2":69.30,
"Db2":69.30,
"D2":73.42,
"D#2":77.78,
"Eb2":77.78,
"E2":82.41,
"F2":87.31,
"F#2":92.50,
"Gb2":92.50,
"G2":98.00,
"G#2":103.83,
"Ab2":103.83,
"A2":110.00,
"A#2":116.54,
"Bb2":116.54,
"B2":123.47,
"C3":130.81,
"C#3":138.59,
"Db3":138.59,
"D3":146.83,
"D#3":155.56,
"Eb3":155.56,
"E3":164.81,
"F3":174.61,
"F#3":185.00,
"Gb3":185.00,
"G3":196.00,
"G#3":207.65,
"Ab3":207.65,
"A3":220.00,
"A#3":233.08,
"Bb3":233.08,
"B3":246.94,
"C4":261.63,
"C#4":277.18,
"Db4":277.18,
"D4":293.66,
"D#4":311.13,
"Eb4":311.13,
"E4":329.63,
"F4":349.23,
"F#4":369.99,
"Gb4":369.99,
"G4":392.00,
"G#4":415.30,
"Ab4":415.30,
"A4":440.00,
"A#4":466.16,
"Bb4":466.16,
"B4":493.88,
"C5":523.25,
"C#5":554.37,
"Db5":554.37,
"D5":587.33,
"D#5":622.25,
"Eb5":622.25,
"E5":659.26,
"F5":698.46,
"F#5":739.99,
"Gb5":739.99,
"G5":783.99,
"G#5":830.61,
"Ab5":830.61,
"A5":880.00,
"A#5":932.33,
"Bb5":932.33,
"B5":987.77,
"C6":1046.50,
"C#6":1108.73,
"Db6":1108.73,
"D6":1174.66,
"D#6":1244.51,
"Eb6":1244.51,
"E6":1318.51,
"F6":1396.91,
"F#6":1479.98,
"Gb6":1479.98,
"G6":1567.98,
"G#6":1661.22,
"Ab6":1661.22,
"A6":1760.00,
"A#6":1864.66,
"Bb6":1864.66,
"B6":1975.53,
"C7":2093.00,
"C#7":2217.46,
"Db7":2217.46,
"D7":2349.32,
"D#7":2489.02,
"Eb7":2489.02,
"E7":2637.02,
"F7":2793.83,
"F#7":2959.96,
"Gb7":2959.96,
"G7":3135.96,
"G#7":3322.44,
"Ab7":3322.44,
"A7":3520.00,
"A#7":3729.31,
"Bb7":3729.31,
"B7":3951.07,
"C8":4186.01,
"C#8":4434.92,
"Db8":4434.92,
"D8":4698.64,
"D#8":4978.03,
"Eb8":4978.03,
}

note_table = [
("C0",16.35),
("C#0",17.32),
("Db0",17.32),
("D0",18.35),
("D#0",19.45),
("Eb0",19.45),
("E0",20.60),
("F0",21.83),
("F#0",23.12),
("Gb0",23.12),
("G0",24.50),
("G#0",25.96),
("Ab0",25.96),
("A0",27.50),
("A#0",29.14),
("Bb0",29.14),
("B0",30.87),
("C1",32.70),
("C#1",34.65),
("Db1",34.65),
("D1",36.71),
("D#1",38.89),
("Eb1",38.89),
("E1",41.20),
("F1",43.65),
("F#1",46.25),
("Gb1",46.25),
("G1",49.00),
("G#1",51.91),
("Ab1",51.91),
("A1",55.00),
("A#1",58.27),
("Bb1",58.27),
("B1",61.74),
("C2",65.41),
("C#2",69.30),
("Db2",69.30),
("D2",73.42),
("D#2",77.78),
("Eb2",77.78),
("E2",82.41),
("F2",87.31),
("F#2",92.50),
("Gb2",92.50),
("G2",98.00),
("G#2",103.83),
("Ab2",103.83),
("A2",110.00),
("A#2",116.54),
("Bb2",116.54),
("B2",123.47),
("C3",130.81),
("C#3",138.59),
("Db3",138.59),
("D3",146.83),
("D#3",155.56),
("Eb3",155.56),
("E3",164.81),
("F3",174.61),
("F#3",185.00),
("Gb3",185.00),
("G3",196.00),
("G#3",207.65),
("Ab3",207.65),
("A3",220.00),
("A#3",233.08),
("Bb3",233.08),
("B3",246.94),
("C4",261.63),
("C#4",277.18),
("Db4",277.18),
("D4",293.66),
("D#4",311.13),
("Eb4",311.13),
("E4",329.63),
("F4",349.23),
("F#4",369.99),
("Gb4",369.99),
("G4",392.00),
("G#4",415.30),
("Ab4",415.30),
("A4",440.00),
("A#4",466.16),
("Bb4",466.16),
("B4",493.88),
("C5",523.25),
("C#5",554.37),
("Db5",554.37),
("D5",587.33),
("D#5",622.25),
("Eb5",622.25),
("E5",659.26),
("F5",698.46),
("F#5",739.99),
("Gb5",739.99),
("G5",783.99),
("G#5",830.61),
("Ab5",830.61),
("A5",880.00),
("A#5",932.33),
("Bb5",932.33),
("B5",987.77),
("C6",1046.50),
("C#6",1108.73),
("Db6",1108.73),
("D6",1174.66),
("D#6",1244.51),
("Eb6",1244.51),
("E6",1318.51),
("F6",1396.91),
("F#6",1479.98),
("Gb6",1479.98),
("G6",1567.98),
("G#6",1661.22),
("Ab6",1661.22),
("A6",1760.00),
("A#6",1864.66),
("Bb6",1864.66),
("B6",1975.53),
("C7",2093.00),
("C#7",2217.46),
("Db7",2217.46),
("D7",2349.32),
("D#7",2489.02),
("Eb7",2489.02),
("E7",2637.02),
("F7",2793.83),
("F#7",2959.96),
("Gb7",2959.96),
("G7",3135.96),
("G#7",3322.44),
("Ab7",3322.44),
("A7",3520.00),
("A#7",3729.31),
("Bb7",3729.31),
("B7",3951.07),
("C8",4186.01),
("C#8",4434.92),
("Db8",4434.92),
("D8",4698.64),
("D#8",4978.03),
("Eb8",4978.03),
]

idx_to_note = {}
note_to_idx = {}
note_idx = 0
interval = 0
for idx in range(len(note_table)):
    if note_table[idx][1] != note_table[note_idx][1]:
        note_idx = idx
        interval += 1
    idx_to_note[interval] = note_table[idx][0]
    note_to_idx[note_table[idx][0]] = interval

max_note_idx = interval

Scales = {
"Maj":[2,2,1,2,2,2,1],
"Min":[2,1,2,2,1,2,2],
"MMin":[2,1,2,2,2,2,2],
"Blues":[3,2,1,1,3,2],
"Mix":[2,2,1,2,2,1,2],
"Dor":[2,1,2,2,2,1,2],
"Lyd":[2,2,2,1,2,2,1],
"LydM":[2,2,2,1,1,2,2],
"Who":[2,2,2,2,2,2,2],
"Dim":[1,2,1,2,1,2,1]
}
scale_pat = "([A-G]+[b#]*[0-8])(Maj|MMin|Min|Blues|Mix|Dor|LydM|Lyd|Who|Dim)"

Chords = {
"Maj":[4,3],
"Min":[3,4],
"7":[4,3,3],
"Maj7":[4,3,4],
"Min6":[3,4,2],
"Min7":[3,4,3],
"-Maj7":[3,4,4],
"Min7b5":[3,3,4],
"7b9": [4,3,3,3],
"7#11":[4,3,3,8]
}
chord_pat = "([A-G]+[b#]*[0-8])(\-Maj7|Maj7|Maj|Min6|Min7b5|Min7|Min|7b9|7#11|7)"
chord_pat_octave = "([A-G]+[b#]*)([0-8])(\-Maj7|Maj7|Maj|Min6|Min7b5|Min7|Min|7b9|7#11|7)"

Chord_Scale_Map = {
"Maj":("Maj",),
"Min":("Min",),
"7":("Mix","Blues"),
"Maj7":("Lyd",),
"Min7":("Dor",),
"Min6":("Dor","MMin"),
"Min7b5":("Dim",),
"-Maj7":("MMin",),
"7b9":("Dim",),
"7#11":("LydM",)
}

def chord2scales( name ):
    m = re.match(chord_pat,name)
    if m:
        return [m.group(1)+f for f in Chord_Scale_Map[m.group(2)]]
    else:
        return None

def split_chord( name ):
    m = re.match(chord_pat_octave, name)
    if m:
        root = m.group(1)
        octave = int(m.group(2))
        type = m.group(3)
        return (root,octave,type)
    else:
        return None

def join_chord( root, octave, type ):
    return root+str(octave)+type

def scale( name, transpose = 0, octaves = 1 ):
    m = re.match(scale_pat,name)
    if m:
        root = note_to_idx[m.group(1)]
        nroot = root + (transpose*12)
        if nroot >= 0 and nroot < max_note_idx:
            root = nroot
        pattern = Scales[m.group(2)]
        s = [idx_to_note[root]]
        while (octaves):
            for i in pattern:
                root += i
                s.append(idx_to_note[root % max_note_idx])
            octaves -= 1
        return s
    else:
        return []

def closest_index_in_scale( note, scl ):
    idx = note_to_idx[note]
    sidx = 0
    while sidx < len(scl):
        if note_to_idx[scl[sidx]] >= idx:
            return sidx
        sidx += 1
    return len(scl) / 2

def chord( name ):
    if name[0] == "[":
        return tuple(name[1:-1].split(","))

    m = re.match(chord_pat,name)
    if m:
        root = note_to_idx[m.group(1)]
        pattern = Chords[m.group(2)]
        s = [idx_to_note[root]]
        for i in pattern:
            root += i
            s.append(idx_to_note[root % max_note_idx])
        return tuple(s)
    else:
        return ()

value_to_beats = { 1.0:4.0, 1.5:6.0, 2.0:2.0, 2.5:3.0, 4.0:1.0, 4.5:1.5, 8.0:0.5, 8.5:0.75 }

def duration( tempo, value ):
    bps = (60.0 / tempo)
    return bps * value_to_beats[float(value)]

# name can be either a chord name like "C4Maj7" or
# a list of notes [ "C4","E4","G4" ] or
# a string formatted as "[C4,E4,G4]"
class C:
    def __init__(self, name, value ):
        if isinstance(name,list):
            self.name = "["+",".join(name)+"]"
        else:
            self.name = name
        self.value = value

    def __repr__(self):
        return "C(\"%s\",%d)"%(self.name,self.value)

    def notes( self ):
        return chord(self.name)

class N:
    def __init__(self, name, value ):
        self.name = name
        self.value = value

    def __repr__(self):
        return "N(\"%s\",%d)"%(self.name,self.value)

class S:
    def __init__(self, name, value ):
        self.name = name
        self.value = value

    def __repr__(self):
        return "S(\"%s\",%s)"%(self.name,str(self.value))

def total_time( chords, tempo ):
    """ return the total time to play chord progression """
    time = 0
    for c in chords:
        time += duration( tempo,c.value)
    return time

class Song:
    def __init__(self, swing, tempo, measure, beat, chords, melody=None, rhythm=None,
         song_time= 0, chord_voice = 0, melody_voice = 0, rhythm_voice = 0 ):
        self.swing = swing
        self.tempo = tempo
        self.measure = measure
        self.beat = beat
        self.chords = chords
        self.melody = melody
        self.rhythm = rhythm
        self.chord_voice = chord_voice
        self.melody_voice = melody_voice
        self.rhythm_voice = rhythm_voice
        self.song_time = song_time
        if self.song_time:
            while total_time(self.chords,self.tempo) > self.song_time+duration( self.tempo,1.0):
                self.chords.pop(-1)

            chorus = float(song_time) / float(total_time(self.chords,self.tempo))
            if chorus >= 2.0:
                chorus = int(chorus)
                self.chords = self.chords * chorus
                if self.melody:
                    self.melody = self.melody * chorus
                if self.rhythm:
                    self.rhythm = self.rhythm * chorus

# sample cache is keyed by (Note,Dynamic (p,mp,mf,f,ff)) and contains ( filename, sample ) if sample hasn't been loaded then sample is None
sample_cache = {}
voices =  {}

def load_sample_from_file( filename, verbose=False ):
    """ loads a sample directly from a wav file """
    wf =wave.open(filename,"r")
    samples = wf.readframes(wf.getnframes())
    wf.close()
    if verbose:
        print("load_sample_from_file:",filename)
    return samples

def midi_note_to_table_idx( midi_note, midi_offset = 21, table_offset = 13 ):
    """ compute the note table index of a midi note """
    note_idx = table_offset
    midi_note -= midi_offset
    while midi_note:
        note_idx += 1
        if note_idx < len(note_table)-1 and note_table[note_idx][1] == note_table[note_idx+1][1]:
            note_idx += 1
        midi_note -= 1
    return note_idx

def init_sample_cache( directory, voice = 0, midi_offset = 21, table_offset = 13, verbose = False ):
    """ init sample cache from samples on disk """
    min_note_idx = 10000
    max_note_idx = 0
    for f in os.listdir( directory ):
        if f.endswith(".wav"):
            l = f.split("_")
            r = l[-1].split(".")
            note_idx  = midi_note_to_table_idx(int(r[0]),midi_offset,table_offset)
            if note_idx < min_note_idx:
                min_note_idx = note_idx
            if note_idx > max_note_idx:
                max_note_idx = note_idx
            sample_cache[ (note_table[note_idx][0],l[2],voice) ] = ( lambda directory=directory,f=f,verbose=verbose : load_sample_from_file(os.path.join( directory, f),verbose), None )
            if verbose:
                print("stored",(note_table[note_idx][0],l[2],voice),( os.path.join( directory, f), None ))
            if note_idx < len(note_table)-1 and note_table[note_idx][1] == note_table[note_idx+1][1]:
                note_idx += 1
                sample_cache[ (note_table[note_idx][0],l[2],voice) ] = (lambda directory=directory,f=f,verbose=verbose : load_sample_from_file( os.path.join( directory, f),verbose), None )
                if note_idx < min_note_idx:
                    min_note_idx = note_idx
                if note_idx > max_note_idx:
                    max_note_idx = note_idx
                if verbose:
                    print("stored",(note_table[note_idx][0],l[2],voice),(os.path.join( directory, f), None ))
    voices[voice] = (min_note_idx, max_note_idx)

def load_sample_from_sf( bank, preset, sf_path, note, dyn, verbose = False ):
    """ load one sample from soundfont """
    fs = fl.Synth()
    fs.start()
    sf = fs.sfload( sf_path )
    fs.program_select(0,sf,bank,preset)
    fs.cc(0,7,127)
    time = duration( 120, 1 ) * 44100.0
    decay = int(time/4.0)
    attack = int(time) - decay
    dyn_to_velocity = {"p":48,"mp":64,"mf":80,"f":96,"ff":112}
    velocity = dyn_to_velocity[dyn]
    fs.noteon(0,note,velocity)
    attack_samples = fs.get_samples(attack)
    fs.noteoff(0,note)
    decay_samples = fs.get_samples(decay)
    output_sample = bytearray(attack_samples)+bytearray(decay_samples)
    fs.delete()
    if verbose:
        print("load_sample_from_sf:",bank,preset,sf_path,note,dyn)
    return output_sample

def find_default_soundfont():
    """ look through /usr/share for the first thing ending with *.sf[2,3] """
    for dirpath,dirnames,filenames in os.walk('/usr/share'):
            for f in filenames:
                if f.endswith(".sf2") or f.endswith(".sf3"):
                    return "0:0:%s"%os.path.join(dirpath,f)
    return ""

def init_sample_cache_sf( bank, preset, sf_path, voice, midi_offset = 21, table_offset = 13, verbose = False):
    """ init sample cache from soundfont """

    if verbose:
        print("initalizing cache for soundfont:",bank,preset,sf_path)

    min_note_idx = 10000
    max_note_idx = 0
    for midi_note in range(21,108):
        for dyn in ["p","mp","mf","f","ff"]:
            note_idx = midi_note_to_table_idx(midi_note,midi_offset,table_offset)
            sample_cache[ ( note_table[note_idx][0],dyn,voice ) ] = (lambda bank=bank,preset=preset,sf_path=sf_path,midi_note=midi_note,dyn=dyn,verbose=verbose: load_sample_from_sf( bank, preset, sf_path, midi_note, dyn, verbose ), None)
            if verbose:
                print("stored",(note_table[note_idx][0],dyn,voice),( "%d:%d:%d:%s"%(midi_note,bank,preset,sf_path), None ))
            if note_idx < min_note_idx:
                min_note_idx = note_idx
            if note_idx > max_note_idx:
                max_note_idx = note_idx
            if note_idx < len(note_table)-1 and note_table[note_idx][1] == note_table[note_idx+1][1]:
                note_idx += 1
                sample_cache[ (note_table[note_idx][0],dyn,voice) ] = (lambda bank=bank,preset=preset,sf_path=sf_path,midi_note=midi_note,dyn=dyn,verbose=verbose: load_sample_from_sf( bank, preset, sf_path, midi_note, dyn, verbose ), None )
                if verbose:
                    print("stored",(note_table[note_idx][0],dyn,voice),( "%d:%d:%d:%s"%(midi_note,bank,preset,sf_path), None ))
                if note_idx < min_note_idx:
                    min_note_idx = note_idx
                if note_idx > max_note_idx:
                    max_note_idx = note_idx
    voices[voice] = (min_note_idx,max_note_idx)

def get_cached_sample ( name, dynamic,voice= 0,verbose = False ):
    while note_to_idx[name] < voices[voice][0]:
        name = idx_to_note[note_to_idx[name]+12]
    while note_to_idx[name] > voices[voice][1]:
        name = idx_to_note[note_to_idx[name]-12]
    if (name,dynamic,voice) in sample_cache:
        if verbose:
            print("found",(name,dynamic,voice))
        ce = sample_cache[(name,dynamic,voice)]
        if ce[1] == None:
            samples = ce[0]()
            sample_cache[(name,dynamic,voice)] = (ce[0],samples)
            return samples
        else:
            return ce[1]
    else:
        if verbose:
            print("not found",(name,dynamic,voice))
        return None


if __name__ == '__main__':
    init_sample_cache( "/home/james/Downloads/ssamples" )
    print(sorted(sample_cache.items()))
