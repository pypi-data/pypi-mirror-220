#!/usr/bin/python -u
import math
import wave
from .notes import notes, scale, chord, C, N, S, Song, duration, chord2scales, split_chord, join_chord, init_sample_cache, init_sample_cache_sf, find_default_soundfont, get_cached_sample, closest_index_in_scale, total_time
import time
import re
import random
import sys

# Tempo in bpm
tempo = 120
global_max_amp = 15386.00
phrase_measures = random.choice([2,4,8])
verbose = False
debug = False
random.seed()

value_to_eighths = {
    1.5:12,
    1:8,
    2.5:6,
    2:4,
    4.5:3,
    4:2,
    8:1
    }

eighths_to_value = {
    12:1.5,
    8:1,
    6:2.5,
    4:2,
    3:4.5,
    2:4,
    1:8
    }

note_lengths = [0,8,8,8,4,4,4,2,1]
times = [0,1,1,1,2,2,2,4,8]
bass_note_lengths = [0,8,4,4,4,2,2,2,1]
bass_times = [0,1,2,2,2,4,4,4,8]


class DeltaGenerator:
    def __init__(self, deltas = [] ):
        self.deltas = deltas
        self.didx = 0

    def getDelta( self ):
        delta = 0
        if self.deltas:
            delta = self.deltas[self.didx]
            self.didx = self.didx + 1
            if self.didx >= len(self.deltas):
                self.didx = 0
        return delta

def sum_eighths( line ):
    eighths = 0
    for s in line:
        eighths += value_to_eighths[s.value]
    return eighths

def load_music( music_file ):
    s = open(music_file,"r").read()
    return eval(s)

def set_verbose( vb ):
    global verbose
    verbose = vb

def set_debug( db ):
    global debug
    debug = db

def save_sample ( output, fname, channels ):
    out_file = wave.open(fname,"w")
    out_file.setparams((channels,2,44100,len(output)//2,"NONE","noncompressed"))
    out_file.writeframes(output)
    out_file.close()

def unpack_sample( s ):
    sl = len(s)//2
    up = wave.struct.unpack_from('%dh'%sl,s,0)
    us = [float(sv) for sv in up]
    return us

def unpack_channels( s ):
    up = unpack_sample(s)
    left = []
    right = []
    idx = 0
    while idx < len(up)-1:
        left.append(up[idx])
        right.append(up[idx+1])
        idx += 2
    return left,right

def pack_channels( left, right ):
    idx = 0
    both = []
    while idx < len(left):
        both.append(left[idx])
        both.append(right[idx])
        idx += 1
    return pack_sample(both)

def pack_sample( s ):
    sample = bytearray(len(s)*2)
    wave.struct.pack_into('%dh'%len(s),sample,0,*[int(sv) for sv in s])
    return sample

def max_sample( sa ):
    m = 0.0000001
    for s in sa:
        if math.fabs(s) > m:
            m = math.fabs(s)
    return m

def scale_sample( sa, scale ):
    ss = []
    for s in sa:
        ss.append(s*scale)
    return ss

def sum_samples( sa, sb ):
    ss = []
    ll = max(len(sa), len(sb))
    for idx in range(ll):
        if idx < len(sa) and idx < len(sb):
            ss.append(sa[idx]+sb[idx])
        elif idx < len(sa):
            ss.append(sa[idx])
        elif idx < len(sb):
            ss.append(sb[idx])
    return ss

def mix_sample( sa, sb, max_amp = global_max_amp):
    ua = unpack_sample(sa)
    ub = unpack_sample(sb)
    ss = sum_samples(ua,ub)
    mx = max_sample(ss)
    return pack_sample(scale_sample(ss,max_amp/mx))

def balance( sa, lpa, rpa, sb, lpb, rpb, max_amp = global_max_amp ):
    ua = unpack_sample(sa)
    ub = unpack_sample(sb)
    out_len = min(len(ua)-1,len(ub)-1)
    idx = 0
    while idx < out_len:
        ua[idx] = ua[idx] * lpa
        ua[idx+1] = ua[idx+1] * rpa
        idx += 2
    idx = 0
    while idx < out_len:
        ub[idx] = ub[idx] * lpa
        ub[idx+1] = ub[idx+1] * rpa
        idx += 2
    idx = 0
    ml = 0
    mr = 0
    while idx < out_len:
        ua[idx] = ua[idx] + ub[idx]
        ua[idx+1] = ua[idx+1] + ub[idx+1]
        if math.fabs(ua[idx]) > ml:
            ml = math.fabs(ua[idx])
        if math.fabs(ua[idx+1]) > mr:
            mr = math.fabs(ua[idx+1])
        idx += 2
    idx = 0
    while idx < out_len:
        ua[idx] = ua[idx] * max_amp/ml
        ua[idx+1] = ua[idx+1] * max_amp/mr
        idx += 2
    return pack_sample(ua)

def reverb( sa, delay = 0.05, sr = 44100.0, max_amp = global_max_amp ):
    delay_samples = int(sr*delay)

    ua = unpack_sample(sa)
    output = ua[:delay_samples]
    for idx in range(delay_samples,len(ua)):
        output.append(ua[idx]+ua[idx-delay_samples]*0.125+ua[idx-int(delay_samples*0.75)]*0.25+ua[idx-int(delay_samples*0.50)]*0.5+ua[idx-int(delay_samples*0.25)]*1.0)
    mx = max_sample(output)

    return pack_sample(scale_sample(output,max_amp/mx))

def gen_envelope( max_amp = global_max_amp, sr = 44100.0, t = 5.0 ):
    total_samples = int(sr*t)
    cur_amp = max_amp
    attack_slope = 0.0
    decay_slope = ((max_amp*0.75) - max_amp) / (total_samples/2.0 - total_samples/4.0)
    sustain_slope = 0.0
    release_slope = (0.0 - (max_amp*0.75)) / (total_samples - ((total_samples/4.0)*3.0))
    envelope = []
    for idx in range(total_samples):
        envelope.append(cur_amp)
        if idx < total_samples/4.0:
            cur_amp += attack_slope
        elif idx < total_samples/2.0:
            cur_amp += decay_slope
        elif idx < (total_samples/4.0)*3.0:
            cur_amp += sustain_slope
        elif idx < total_samples:
            cur_amp += release_slope
    return envelope

def smooth_decay( sample ):
    us = unpack_sample(sample)
    quarter = len(us)//4
    scale = slope = 1.0 / float(quarter)
    idx = -quarter
    while idx < 0:
        us[idx] = us[idx] - us[idx]*scale
        scale = scale + slope
        idx += 1
    return pack_sample(us)

note_cache = {}
def gen_note( note = "C4", sr = 44100.0, t = 5.0, max_amp = global_max_amp, dyn = "f", voice = 0 ):

    freq = notes[note]
    total_samples = (sr*t)
    period = sr / freq
    natural_freq = 2.0*math.pi/period

    key = ( note, int(total_samples), max_amp, dyn, voice )
    if key in note_cache:
        if verbose:
            print("Using cached note",key)
        return note_cache[key]

    if max_amp > 0.0:
        cs = get_cached_sample( note, dyn, voice, verbose )
        if cs:
            nc = int(total_samples)*4
            ls = len(cs)
            if nc > ls:
                output_signal = cs + (wave.struct.pack('h',0) * ((nc-ls)//2))
            else:
                output_signal = smooth_decay(cs[:nc])
        else:
            envelope = gen_envelope( max_amp, sr, t )
            #evaluate x-axis / time-axis positions
            time_axis = [float(x)*natural_freq for x in range(int(period))]
            #evaluate singal amplitudes for the period
            period_amp_data = [math.sin(x) for x in time_axis]
            #repeat the singal, and pack as short, 16 bit values
            output_signal = b''
            for i in range(int(total_samples/period)):
                for j in range(len(period_amp_data)):
                    output_signal += wave.struct.pack('h', int(period_amp_data[j]*envelope[i*j]))
    else:
        output_signal = wave.struct.pack('h',0)*int(total_samples)

    if verbose:
        print("Missed note cache",key)
    note_cache[key] = output_signal
    return output_signal

chord_cache = {}
def gen_chord( name = "C4Maj", sr = 44100.0, t = 5.0, max_amp = global_max_amp, dyn = "f",voice=0 ):
    key = ( name, int(sr*t), max_amp, dyn, voice )
    if key in chord_cache:
        if verbose:
            print("Using cached chord",key)
        return chord_cache[key]
    tones = chord(name)
    signal = b''
    for tn in tones:
        if not signal:
            signal = gen_note(tn,sr,t,max_amp,dyn,voice)
        else:
            signal = mix_sample(signal,gen_note(tn,sr,t,max_amp,dyn,voice))

    if verbose:
        print("Missed chord cache",key)
    chord_cache[key] = signal
    return signal

def gen_line( line, tempo = 120, add_swing = False, dyn = "f",voice=0 ):
    tt_time = 0.0
    output = b''
    swing = 0.0
    dyns = [ "ff","f","mf","f","ff"]
    if add_swing:
        swing = (duration(tempo, 8)/8.0)
    dyn_idx = dyns.index(dyn)
    eidx = 0
    while eidx < len(line):
        cur_dyn = dyns[dyn_idx]
        event = line[eidx]
        tn = duration(tempo, event.value)+swing
        if event.name == "R":
            output += gen_note( note="C4", t=tn, max_amp = 0.0, voice = voice)
            eidx += 1
        else:
            nn = event.name
            is_chord = isinstance(event,C)
            while eidx+1 < len(line) and line[eidx+1].name == "R":
                tn += duration(tempo, line[eidx+1].value)+swing
                swing = -swing
                eidx += 1
            if is_chord:
                output += gen_chord( name=nn, t = tn, dyn=cur_dyn, voice = voice)
            else:
                output += gen_note( note=nn, t = tn, dyn=cur_dyn, voice = voice)
            eidx += 1

        tt_time += tn
        swing = -swing
        if random.randint(1,10) <= 4:
            dyn_idx += 1
            if dyn_idx >= len(dyns):
                dyn_idx = 0
    if verbose:
        print("gen_line, total_time",tt_time)
        print("calculated total_time",total_time(line,tempo))
    return output

def improvise_scale_phrase( chords, note_idx=8, note_dir=1, harm=False, transpose = 1, delta_gen = None, ending = False ):
    melody = []
    cidx = 0

    if delta_gen:
        note_dir = delta_gen.getDelta()
    elif random.randint(1,10) <= 2:
        note_dir = -note_dir
    note_len = 0
    if random.randint(1,10) <= 4:
        nl = bass_note_lengths
        nt = bass_times
    else:
        nl = note_lengths
        nt = times

    while cidx < len(chords):
        root,octave,type = split_chord(chords[cidx].name)
        cname = join_chord(root,octave+transpose,type)

        scl_name = random.choice(chord2scales(cname))
        scl = scale(scl_name,transpose=-1,octaves=3)
        if note_idx >= len(scl):
            note_idx = len(scl)-2
            note_dir = -1

        eighths = value_to_eighths[chords[cidx].value]

        while ( eighths > 0 ):
            if (not note_len) or (note_len > eighths):
                if ending:
                    note_len = random.randint(min(eighths,4),eighths)
                else:
                    note_len = random.randint(1,eighths)

            rest = ( random.randint(1,20) <= 2) and not ending
            if rest:
                nn = N('R',nl[note_len])
            elif harm:
                chord = []
                chord_len = random.randint(2,3)
                cn_idx = note_idx
                while chord_len >= 0 and cn_idx >= 0:
                    chord.append(scl[cn_idx])
                    chord_len -= 1
                    cn_idx -= 2
                nn = C(chord,nl[note_len])
            else:
                nn = N(scl[note_idx],nl[note_len])
            melody.append(nn)
            eighths -= nt[note_len]
            note_idx += note_dir
            if note_idx < 0:
                note_idx = 1
                note_dir = 1
            elif note_idx >= len(scl):
                note_idx = len(scl)-2
                note_dir = -1

            if delta_gen:
                note_dir = delta_gen.getDelta()
            elif not eighths:
                note_dir = -note_dir
        cidx += 1
    return((melody,note_idx,note_dir))

def improvise_melody_phrase( chords, melody, transpose=1, harm = False ):
    cidx = 0
    midx = 0
    phrase = []
    total_eighths = 0
    chord_total_eighths = 0
    while midx < len(melody):
        scl_name = random.choice(chord2scales(chords[cidx].name))
        scl = scale(scl_name,transpose=transpose,octaves=3)
        if melody[midx].name == 'R':
            phrase.append(melody[midx])
        elif harm:
            cn_idx = closest_index_in_scale( melody[midx].name, scl) + 12
            chord = []
            chord_len = random.randint(2,3)
            while chord_len >= 0 and cn_idx >= 0:
                chord.append(scl[cn_idx])
                chord_len -= 1
                cn_idx -= 2
            phrase.append(C(chord,melody[midx].value))
        elif random.randint(1,10) < 4 and midx < len(melody)-1 and melody[midx+1].name != 'R':
            cn_idx = closest_index_in_scale( melody[midx].name, scl)
            en_idx = closest_index_in_scale( melody[midx+1].name, scl)
            inc = 1
            if en_idx < cn_idx:
                inc = -1
            eighths = value_to_eighths[melody[midx].value]
            while eighths:
                phrase.append(N(scl[cn_idx],8))
                eighths -= 1
                cn_idx += inc
                if cn_idx < 0 or cn_idx >= len(scl):
                    inc = -inc
                    cn_idx += inc
        else:
            phrase.append(melody[midx])

        total_eighths += value_to_eighths[melody[midx].value]
        while chord_total_eighths < total_eighths:
            chord_total_eighths += value_to_eighths[chords[cidx].value]
            cidx += 1
        cidx = min(cidx,len(chords)-1)
        midx += 1
    return phrase

def improvise_ex( song, transpose = 1, delta_gen = None ):
    phrase_eighths = (value_to_eighths[song.beat] * song.measure) * phrase_measures
    cidx = 0
    midx = 0
    melody = []
    note_idx = 8
    note_dir = 1
    harm = False

    line_time = 0
    cidx = 0

    while cidx < len(song.chords) and line_time < song.song_time:
        chord_phrase = []
        chord_phrase_eighths = 0
        chord_phrase_time = 0
        while cidx < len(song.chords) and chord_phrase_eighths < phrase_eighths and line_time+chord_phrase_time < song.song_time:
            chord_phrase.append(song.chords[cidx])
            chord_phrase_eighths += value_to_eighths[song.chords[cidx].value]
            chord_phrase_time = total_time(chord_phrase,song.tempo)
            cidx += 1
        melody_phrase = []
        melody_phrase_eighths = 0
        melody_phrase_time = 0
        if song.melody:
            while midx < len(song.melody) and melody_phrase_eighths < phrase_eighths and line_time+melody_phrase_time < song.song_time:
                melody_phrase.append(song.melody[midx])
                melody_phrase_eighths += value_to_eighths[song.melody[midx].value]
                melody_phrase_time = total_time(melody_phrase)
                midx += 1

        phrase = []
        harm = (random.randint(1,10) < 5)
        if melody_phrase and (random.randint(1,10) < 5):
            phrase = improvise_melody_phrase( chord_phrase, melody_phrase,transpose, harm )
        elif chord_phrase:
            phrase,note_idx,note_dir = improvise_scale_phrase( chord_phrase, note_idx, note_dir, harm, transpose, delta_gen, ending = ( cidx >= (len(song.chords)-8)) )

        melody += phrase
        line_time = total_time(melody,song.tempo)

    if verbose:
        print("improvise_ex:",melody)
    return melody

def arpegiate_ex( song, transpose = -1 ):
    phrase_eighths = value_to_eighths[song.beat] * song.measure * phrase_measures
    phrase_index = 0
    phrase = []
    eighths = phrase_eighths
    while ( eighths > 0 ):
        note_len = min(eighths,random.choice([1,2,4]))
        phrase.append(note_len)
        eighths -= bass_times[note_len]

    line = []
    note_idx = 8
    note_dir = 1
    cidx = 0
    lay_out = False
    punch_chord = False
    play_chord = False
    phrase_time = 0
    line_time = 0
    cidx = 0

    while cidx < len(song.chords) and line_time < song.song_time:
        c = song.chords[cidx]
        cc = c.name
        root,octave,type = split_chord(cc)
        cp = join_chord(root,octave+transpose,type)
        eighths = value_to_eighths[c.value]

        if not phrase_time:
            play_chord = (random.randint(1,10) <= 2)
            punch_chord = (random.randint(1,10) <= 2)
            lay_out = (random.randint(1,10) <= 2)

        phrase_time += eighths
        if phrase_time >= phrase_eighths:
            phrase_time = 0

        cn = chord(cp)
        if (play_chord):
            line.append(c)
        elif (lay_out):
            line.append(N("R",c.value))
        elif (punch_chord):
            while ( eighths > 0 ):
                if phrase_index >= len(phrase):
                    phrase_index = 0

                note_len = phrase[phrase_index]
                if note_len < 0:
                    note_len = -note_len
                    nn = "R"
                note_len = min(eighths, note_len)
                line.append(C(cc,bass_note_lengths[note_len]))
                cc = "R"
                eighths -= bass_times[note_len]
                phrase_index += 1
        else:
            idx = 0
            while ( eighths > 0 ):
                if idx >= len(cn):
                    idx = 0

                if phrase_index >= len(phrase):
                    phrase_index = 0

                note_len = phrase[phrase_index]
                nn = cn[idx]
                if note_len < 0:
                    note_len = -note_len
                    nn = "R"

                if lay_out:
                    nn = "R"

                note_len = min(eighths, note_len)
                if punch_chord and not lay_out:
                    line.append(C(cc,bass_note_lengths[note_len]))
                    cc = "R"
                else:
                    line.append(N(nn,bass_note_lengths[note_len]))
                eighths -= bass_times[note_len]
                idx += 1
                phrase_index += 1
        line_time = total_time(line,song.tempo)
        cidx += 1
    if verbose:
        print("arpegiate_ex:",line)
    return line

def play_song( s, out_file = "soundgen.wav" ):
    if verbose:
        print("Phrase measures",phrase_measures)

    if verbose:
        print("Synthesizing Melody")
        print("melody eighths =",sum_eighths(s.melody))
    melody_line = gen_line( s.melody,s.tempo,s.swing,"f",s.melody_voice)
    if debug:
        save_sample(melody_line,"melody.wav",1)
    melody_line = reverb(melody_line)
    if debug:
        save_sample(melody_line,"melodyrv.wav",1)

    if verbose:
        print("Synthesizing Bass")
        print("bass eighths = ",sum_eighths(s.rhythm))
    bass_line = gen_line( s.rhythm,s.tempo,s.swing,"f",s.rhythm_voice)
    if debug:
        save_sample(bass_line,"bass.wav",1)
    bass_line = reverb(bass_line)
    if debug:
        save_sample(bass_line,"bassrv.wav",1)
    if verbose:
        print("Balancing Channels")
    output = balance( bass_line, 0.60, 0.40, melody_line, 0.40, 0.60 )
    if verbose:
        print("Saving song")
    save_sample(output,out_file,2)
