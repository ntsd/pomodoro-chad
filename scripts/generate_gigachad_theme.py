#!/usr/bin/env python3
"""
Generate GigaChad Anthem ("Can You Feel My Heart" - Phonk / Synthwave Meme Edit)
Synthesizes a high-energy, seamless loop of the iconic GigaChad theme using numpy and wave,
then encodes with ffmpeg to public/vault/audio/gigachad_theme.mp3.
"""

import math
import wave
import struct
import subprocess
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "public" / "vault" / "audio"
OUTPUT_WAV = OUTPUT_DIR / "gigachad_theme.wav"
OUTPUT_MP3 = OUTPUT_DIR / "gigachad_theme.mp3"

SAMPLE_RATE = 44100
BPM = 128
BEAT_DUR = 60.0 / BPM  # ~0.46875s
STEP_DUR = BEAT_DUR / 4  # 16th note ~0.1171875s
BARS = 8  # 8 bars loop (2 cycles of Em - C - G - D)
TOTAL_DUR = BARS * 4 * BEAT_DUR
NUM_SAMPLES = int(SAMPLE_RATE * TOTAL_DUR)

t = np.linspace(0, TOTAL_DUR, NUM_SAMPLES, endpoint=False)
left = np.zeros(NUM_SAMPLES)
right = np.zeros(NUM_SAMPLES)

# --- NOTE TO FREQUENCY CONVERTER ---
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_to_freq(name: str) -> float:
    # Handles e.g. 'E1', 'F#3', 'Bb4'
    octave = int(name[-1])
    n = name[:-1]
    if n == 'Db': n = 'C#'
    elif n == 'Eb': n = 'D#'
    elif n == 'Gb': n = 'F#'
    elif n == 'Ab': n = 'G#'
    elif n == 'Bb': n = 'A#'
    semitone = NOTE_NAMES.index(n)
    midi = 12 + octave * 12 + semitone
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))

# --- 1. DRUMS ---
# Kick: 4-on-the-floor
kick_dur = 0.22
kick_samples = int(SAMPLE_RATE * kick_dur)
tk = np.linspace(0, kick_dur, kick_samples, endpoint=False)
kick_pitch = 160.0 * np.exp(-tk * 28.0) + 42.0
kick_env = np.exp(-tk * 14.0)
kick_wave = np.sin(2 * np.pi * np.cumsum(kick_pitch) / SAMPLE_RATE) * kick_env
click = np.random.uniform(-1, 1, int(SAMPLE_RATE * 0.01)) * np.exp(-np.linspace(0, 10, int(SAMPLE_RATE * 0.01)))
kick_wave[:len(click)] += click * 0.4
kick_wave = np.clip(kick_wave, -1.0, 1.0) * 0.85

# Snare / Clap: on beats 2 and 4
snare_dur = 0.25
snare_samples = int(SAMPLE_RATE * snare_dur)
tsn = np.linspace(0, snare_dur, snare_samples, endpoint=False)
snare_noise = np.random.uniform(-1, 1, snare_samples) * np.exp(-tsn * 16.0)
snare_tone = np.sin(2 * np.pi * 185 * tsn) * np.exp(-tsn * 22.0)
snare_wave = (snare_noise * 0.7 + snare_tone * 0.3) * 0.65

# Hi-hat: 16th note offbeats
hat_dur = 0.06
hat_samples = int(SAMPLE_RATE * hat_dur)
th = np.linspace(0, hat_dur, hat_samples, endpoint=False)
hat_wave = np.random.uniform(-1, 1, hat_samples) * np.exp(-th * 65.0) * 0.25

# Place drums across the track
for bar in range(BARS):
    bar_start_sample = int(bar * 4 * BEAT_DUR * SAMPLE_RATE)
    for beat in range(4):
        beat_sample = bar_start_sample + int(beat * BEAT_DUR * SAMPLE_RATE)
        # Kick on every beat
        if beat_sample + kick_samples <= NUM_SAMPLES:
            left[beat_sample:beat_sample + kick_samples] += kick_wave
            right[beat_sample:beat_sample + kick_samples] += kick_wave
        # Snare on 2 and 4 (beat indices 1 and 3)
        if beat in [1, 3]:
            if beat_sample + snare_samples <= NUM_SAMPLES:
                left[beat_sample:beat_sample + snare_samples] += snare_wave * 0.95
                right[beat_sample:beat_sample + snare_samples] += snare_wave * 1.05
        # Hats on 16th notes
        for step in range(4):
            step_sample = beat_sample + int(step * STEP_DUR * SAMPLE_RATE)
            if step in [1, 2, 3]:
                vol = 0.9 if step == 2 else 0.5
                if step_sample + hat_samples <= NUM_SAMPLES:
                    left[step_sample:step_sample + hat_samples] += hat_wave * vol * 0.8
                    right[step_sample:step_sample + hat_samples] += hat_wave * vol * 1.2

# --- 2. CHORD PROGRESSION & SUPERSAW STABS (Em - C - G - D) ---
chord_prog = [
    # Bar 1: Em
    {'root': 'E1', 'chord': ['E3', 'G3', 'B3', 'E4'], 'lead': 'E4'},
    # Bar 2: C
    {'root': 'C1', 'chord': ['C3', 'E3', 'G3', 'C4'], 'lead': 'G4'},
    # Bar 3: G
    {'root': 'G1', 'chord': ['G3', 'B3', 'D4', 'G4'], 'lead': 'D4'},
    # Bar 4: D
    {'root': 'D1', 'chord': ['D3', 'F#3', 'A3', 'D4'], 'lead': 'F#4'},
    # Bar 5: Em (higher octave energy)
    {'root': 'E1', 'chord': ['E3', 'G3', 'B3', 'E4'], 'lead': 'B4'},
    # Bar 6: C
    {'root': 'C1', 'chord': ['C3', 'E3', 'G3', 'C4'], 'lead': 'E5'},
    # Bar 7: G
    {'root': 'G1', 'chord': ['G3', 'B3', 'D4', 'G4'], 'lead': 'D5'},
    # Bar 8: D
    {'root': 'D1', 'chord': ['D3', 'F#3', 'A3', 'D4'], 'lead': 'F#4'},
]

# Iconic syncopated rhythm pattern per 16 steps in a bar:
# [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0]
stab_pattern = [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0]

def synth_supersaw(freq, duration, detune=0.015):
    """Generate wide detuned supersaw."""
    n_samp = int(SAMPLE_RATE * duration)
    tt = np.linspace(0, duration, n_samp, endpoint=False)
    detunes = [-detune * 1.5, -detune * 0.7, 0, detune * 0.7, detune * 1.5]
    l_wave = np.zeros(n_samp)
    r_wave = np.zeros(n_samp)
    for idx, d in enumerate(detunes):
        f = freq * (1.0 + d)
        phase = tt * f
        saw = 2.0 * (phase - np.floor(0.5 + phase))
        pan = (idx / (len(detunes) - 1))
        l_wave += saw * (1 - pan * 0.6)
        r_wave += saw * (0.4 + pan * 0.6)
    
    env = np.ones(n_samp)
    attack = int(SAMPLE_RATE * 0.008)
    release = int(SAMPLE_RATE * 0.02)
    if attack < n_samp:
        env[:attack] = np.linspace(0, 1, attack)
    if release < n_samp:
        env[-release:] = np.linspace(1, 0, release)
    
    return l_wave * env * 0.2, r_wave * env * 0.2

# Generate stabs & bassline
for bar_idx, ch_info in enumerate(chord_prog):
    bar_time = bar_idx * 4 * BEAT_DUR
    root_freq = note_to_freq(ch_info['root'])

    # Add Sub-bass / Reese bass with sidechain pumping
    bar_samples = int(4 * BEAT_DUR * SAMPLE_RATE)
    bar_start_idx = int(bar_time * SAMPLE_RATE)
    t_bar = np.linspace(0, 4 * BEAT_DUR, bar_samples, endpoint=False)
    sub_wave = (np.sin(2 * np.pi * root_freq * t_bar) * 0.6 + 
                np.sin(2 * np.pi * (root_freq * 2) * t_bar) * 0.3)
    beat_phase = (t_bar % BEAT_DUR) / BEAT_DUR
    sidechain = np.clip(beat_phase * 2.8, 0.15, 1.0)
    sub_wave *= sidechain * 0.45

    if bar_start_idx + bar_samples <= NUM_SAMPLES:
        left[bar_start_idx:bar_start_idx + bar_samples] += sub_wave
        right[bar_start_idx:bar_start_idx + bar_samples] += sub_wave

    # Add Stabs
    for step_idx, is_hit in enumerate(stab_pattern):
        if is_hit:
            step_time = bar_time + step_idx * STEP_DUR
            step_samp_idx = int(step_time * SAMPLE_RATE)
            stab_dur = STEP_DUR * 0.88

            # Chords
            for note_name in ch_info['chord']:
                f = note_to_freq(note_name)
                sw_l, sw_r = synth_supersaw(f, stab_dur, detune=0.012)
                l_len = len(sw_l)
                if step_samp_idx + l_len <= NUM_SAMPLES:
                    left[step_samp_idx:step_samp_idx + l_len] += sw_l
                    right[step_samp_idx:step_samp_idx + l_len] += sw_r

            # Lead melody note on top
            lead_f = note_to_freq(ch_info['lead'])
            ld_l, ld_r = synth_supersaw(lead_f, stab_dur, detune=0.02)
            ld_len = len(ld_l)
            if step_samp_idx + ld_len <= NUM_SAMPLES:
                left[step_samp_idx:step_samp_idx + ld_len] += ld_l * 1.3
                right[step_samp_idx:step_samp_idx + ld_len] += ld_r * 1.3

# Master Limiter / Compression
max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1.0)
left = np.tanh(left / max_val * 1.4) * 0.95
right = np.tanh(right / max_val * 1.4) * 0.95

# Convert to 16-bit PCM WAV
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
with wave.open(str(OUTPUT_WAV), 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    interleaved = np.empty((NUM_SAMPLES * 2,), dtype=np.int16)
    interleaved[0::2] = (left * 32767).astype(np.int16)
    interleaved[1::2] = (right * 32767).astype(np.int16)
    wf.writeframes(interleaved.tobytes())

print(f"✅ WAV generated: {OUTPUT_WAV} ({OUTPUT_WAV.stat().st_size} bytes)")

# Convert to MP3 via ffmpeg
subprocess.run([
    "ffmpeg", "-y", "-i", str(OUTPUT_WAV),
    "-codec:a", "libmp3lame", "-b:a", "192k",
    str(OUTPUT_MP3)
], check=True)

# Clean up temporary WAV
OUTPUT_WAV.unlink(missing_ok=True)
print(f"👑 GigaChad Theme MP3 ready: {OUTPUT_MP3} ({OUTPUT_MP3.stat().st_size} bytes)")
