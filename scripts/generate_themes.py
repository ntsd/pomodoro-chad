#!/usr/bin/env python3
"""
Generate Pure Instrumental GigaChad Themes & Anthems
Synthesizes high-energy, royalty-free instrumental loops inspired by viral meme anthems:
- Focus 01: g3ox_em - GigaChad Theme (Phonk House Version / Can You Feel My Heart)
- Focus 02: DVRST - Close Eyes (Sigma Drift Phonk Tribute)
- Focus 03: Kordhell - Murder In My Mind (Aggressive Workout Phonk)
- Break 01: Home - Resonance (Sunlit Meadow Sunset Chillwave)
- Break 02: Kevin MacLeod - Carefree / Elevator Meme (Outdoor Oxygen Lo-Fi)
- Break 03: Chillstep Grass Serenade (Peaceful Ambient Lo-Fi)
- Long Break 01: Titan Outdoor Walk & Hydration (Ambient Earth Drone)
- Long Break 02: Forest Canopy Reverie (Lush Nature Lo-Fi)
- Motivation 01: g3ox_em & Hensonn - Warrior Ascendance Phonk
- Motivation 02: Ghostface Playa - Iron Discipline Apex Phonk

Outputs:
- MP3 audio files to public/vault/audio/
- Reference JSON metadata files to public/vault/themes/
- Registry compiled into public/vault/manifest.json
"""

import os
import json
import wave
import subprocess
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_AUDIO_DIR = BASE_DIR / "public" / "vault" / "audio"
OUTPUT_THEMES_DIR = BASE_DIR / "public" / "vault" / "themes"
MANIFEST_FILE = BASE_DIR / "public" / "vault" / "manifest.json"
SCRATCH_DIR = BASE_DIR / ".cache_audio"

SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_THEMES_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 44100

THEME_SPECS = [
    # --- FOCUS THEMES ---
    {
        "id": "theme_focus_01",
        "category": "focus",
        "title": "GigaChad Anthem - Can You Feel My Heart (Phonk House)",
        "meme_reference": "g3ox_em - GigaChad Theme (Phonk House Version)",
        "original_artist_reference": "g3ox_em / Bring Me The Horizon",
        "bpm": 128,
        "duration": 15.0,
        "key": "E minor",
        "genre": "Phonk House / Drift House",
        "instruments": [
            "4-on-the-floor House Kick",
            "Bring Me The Horizon 808 Cowbell Melody",
            "Supersaw Chord Stabs (Em - C - G - D)",
            "Sidechained Saturated Sub-Bass",
            "16th Rolling Hi-Hats & Claps"
        ],
        "style": "g3ox_em_gigachad",
        "license": "Royalty-Free Procedural Parody / Public Domain Tribute",
        "description": "Authentic Phonk House recreation of the viral g3ox_em GigaChad Theme with driving 128 BPM 4-on-the-floor house kick, Bring Me The Horizon cowbell melody, and pumping sidechain bass."
    },
    {
        "id": "theme_focus_02",
        "category": "focus",
        "title": "Sigma Drift Phonk - Close Eyes",
        "meme_reference": "DVRST - Close Eyes (Sigma Chad / Megamind Phonk)",
        "original_artist_reference": "DVRST",
        "bpm": 132,
        "duration": 14.5,
        "key": "C minor",
        "genre": "Drift Phonk / Sigma Phonk",
        "instruments": [
            "Punchy Drift Kick",
            "Syncopated Memphis Cowbell Arpeggio",
            "Gliding 808 Sub-Bass",
            "Snappy Memphis Snare",
            "High-Octave Cowbell Fills"
        ],
        "style": "dvrst_close_eyes",
        "license": "Royalty-Free Procedural Parody / Public Domain Tribute",
        "description": "High-octane Sigma Drift Phonk recreation inspired by DVRST's Close Eyes with syncopated cowbell stabs and deep distorted 808 slides."
    },
    {
        "id": "theme_focus_03",
        "category": "focus",
        "title": "Titan Hyper-Focus Phonk",
        "meme_reference": "Kordhell - Murder In My Mind / Live Another Day",
        "original_artist_reference": "Kordhell",
        "bpm": 136,
        "duration": 14.1,
        "key": "F# minor",
        "genre": "Aggressive Gym Phonk",
        "instruments": [
            "Hardstyle Punch Kick",
            "Resonant 808 Cowbell Hooks",
            "Relentless Trap Rolling Hats",
            "Dark Heavy Distorted Bassline"
        ],
        "style": "kordhell_aggressive",
        "license": "Royalty-Free Procedural Parody / Public Domain Tribute",
        "description": "Relentless 136 BPM aggressive gym phonk beat engineered for deep focus tunnel vision and PR crushing sessions."
    },

    # --- BREAK THEMES (TOUCH GRASS) ---
    {
        "id": "theme_break_01",
        "category": "break",
        "title": "Sunlit Meadow - Resonance Chillwave",
        "meme_reference": "Home - Resonance (Sunset Walk Meme)",
        "original_artist_reference": "Home",
        "bpm": 96,
        "duration": 15.0,
        "key": "C major / G major",
        "genre": "Synthwave / Chillwave",
        "instruments": [
            "Warm Analog Synth Swells (Cmaj9 - D9 - Gmaj7 - Em7)",
            "Vintage Lo-Fi Acoustic Drums",
            "Sparkling Chime Arpeggios",
            "Lush Outdoor Atmospheric Reverb"
        ],
        "style": "home_resonance",
        "license": "Royalty-Free Procedural Parody / Public Domain Tribute",
        "description": "Nostalgic, warm chillwave pads inspired by Home's Resonance, providing a calming sonic backdrop to step outside and touch physical grass."
    },
    {
        "id": "theme_break_02",
        "category": "break",
        "title": "Outdoor Oxygen Lo-Fi Groove",
        "meme_reference": "Kevin MacLeod - Carefree / Elevator Meme",
        "original_artist_reference": "Kevin MacLeod (Incompetech)",
        "bpm": 104,
        "duration": 13.8,
        "key": "F major",
        "genre": "Meme Lo-Fi / Chillhop",
        "instruments": [
            "Bouncy Acoustic Kick & Snare",
            "Rhodes Electric Piano",
            "Playful Whistling Chimes",
            "Warm Vinyl Texture"
        ],
        "style": "carefree_lofi",
        "license": "Creative Commons / Royalty-Free Tribute",
        "description": "Playful, lighthearted lo-fi bounce that playfully commands you to detach from monitors and breathe fresh air."
    },
    {
        "id": "theme_break_03",
        "category": "break",
        "title": "Breeze of the Meadow (Chillstep Pulse)",
        "meme_reference": "Meadow Breeze Ambient Lo-Fi",
        "original_artist_reference": "Chadodoro Originals",
        "bpm": 100,
        "duration": 14.4,
        "key": "D major",
        "genre": "Chillstep / Ambient",
        "instruments": [
            "Reverb Electric Piano",
            "Mellow Syncopated Sub Pulse",
            "Ambient Nature Drone",
            "Gentle High Chimes"
        ],
        "style": "chillstep",
        "license": "CC0 Public Domain",
        "description": "Tranquil ambient chillstep rhythm with soft piano harmonics and soothing outdoor resonance."
    },

    # --- LONG BREAK THEMES ---
    {
        "id": "theme_long_break_01",
        "category": "long_break",
        "title": "Titan Outdoor Walk & Hydration",
        "meme_reference": "Open Sky March & Nature Reverie",
        "original_artist_reference": "Chadodoro Originals",
        "bpm": 92,
        "duration": 15.6,
        "key": "A minor",
        "genre": "Ambient March / Downtempo",
        "instruments": [
            "Steadfast Marching Percussion",
            "Hydration Water-Drop Chimes",
            "Deep Earth Sub Drone",
            "Open Sky Acoustic Harmonics"
        ],
        "style": "ambient_walk",
        "license": "CC0 Public Domain",
        "description": "Paced 92 BPM cadence designed for a long physical walk under the sun with cold water hydration."
    },
    {
        "id": "theme_long_break_02",
        "category": "long_break",
        "title": "Forest Canopy Reverie (Lush Lo-Fi)",
        "meme_reference": "Forest Lo-Fi Girl / Sunlight Walk",
        "original_artist_reference": "Chadodoro Originals",
        "bpm": 86,
        "duration": 16.7,
        "key": "G major",
        "genre": "Lush Lo-Fi / Nature Beats",
        "instruments": [
            "Slow Organic Heartbeat Kick",
            "Gentle Electric Piano Swells",
            "Warm Analog Tape Saturation",
            "Forest Breeze Texture"
        ],
        "style": "forest_ambient",
        "license": "CC0 Public Domain",
        "description": "Ultra-relaxed 86 BPM lo-fi beats with organic heartbeat rhythm for deep recovery before your next work block."
    },

    # --- MOTIVATION THEMES ---
    {
        "id": "theme_motivation_01",
        "category": "motivation",
        "title": "Warrior Ascendance - Pure GigaChad Phonk",
        "meme_reference": "g3ox_em & Hensonn - Sahara / Warrior Gym Edit",
        "original_artist_reference": "g3ox_em / Hensonn",
        "bpm": 130,
        "duration": 14.8,
        "key": "E minor",
        "genre": "Warrior Workout Phonk",
        "instruments": [
            "Triumphant Brass-Style Synth Lead",
            "Distorted 808 Memphis Cowbells",
            "Thunderous Sub-Bass Drops",
            "Double-Time Trap Hi-Hat Rolls"
        ],
        "style": "warrior_phonk",
        "license": "Royalty-Free Procedural Parody / Public Domain Tribute",
        "description": "Apex warrior motivation phonk drop featuring heroic brass stabs, screaming cowbells, and thunderous 808s."
    },
    {
        "id": "theme_motivation_02",
        "category": "motivation",
        "title": "Iron Discipline Apex (Titan War Stabs)",
        "meme_reference": "Ghostface Playa - Why Not / Chad Drift Meme",
        "original_artist_reference": "Ghostface Playa",
        "bpm": 134,
        "duration": 14.3,
        "key": "D minor",
        "genre": "Hard Drift Phonk",
        "instruments": [
            "Heavy Distorted War Kick",
            "Menacing Cowbell Hooks",
            "Unstoppable Driving Bass",
            "Hard Memphis Claps"
        ],
        "style": "iron_discipline",
        "license": "Royalty-Free Procedural Parody / Public Domain Tribute",
        "description": "Dark, heavy bounce drift phonk for instant adrenaline surges and breaking through procrastination barriers."
    }
]

def make_phonk_cowbell(freq: float, duration: float) -> np.ndarray:
    """Synthesizes crunchy, authentic Roland TR-808 Phonk Cowbell."""
    num_s = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_s, endpoint=False)
    # Dual frequencies: fundamental and characteristic 1.48 metallic overtone
    w1 = np.sin(2 * np.pi * freq * t)
    w2 = np.sin(2 * np.pi * freq * 1.482 * t)
    # Add subtle square wave grit
    sq = np.sign(np.sin(2 * np.pi * freq * 2.0 * t)) * 0.15
    raw = (w1 * 0.65 + w2 * 0.35 + sq)
    # Memphis saturation & sharp decay envelope
    env = np.exp(-t * 16.0)
    cowbell = np.tanh(raw * 2.6) * env
    return cowbell

def synthesize_instrumental_theme(spec: dict, out_wav: Path):
    """Synthesizes high-fidelity pure instrumental theme based on style spec."""
    bpm = spec["bpm"]
    duration = spec["duration"]
    style = spec["style"]
    num_samples = int(SAMPLE_RATE * duration)
    beat_dur = 60.0 / bpm
    step_dur = beat_dur / 4

    left = np.zeros(num_samples)
    right = np.zeros(num_samples)

    # 1. Kick synthesis
    kick_dur = 0.22
    kick_samples = int(SAMPLE_RATE * kick_dur)
    tk = np.linspace(0, kick_dur, kick_samples, endpoint=False)
    kick_pitch = 160.0 * np.exp(-tk * 28.0) + 45.0
    kick_w = np.sin(2 * np.pi * np.cumsum(kick_pitch) / SAMPLE_RATE) * np.exp(-tk * 13.0)
    # Kick punch click
    click_len = int(SAMPLE_RATE * 0.008)
    kick_w[:click_len] += np.random.uniform(-0.3, 0.3, click_len)

    # 2. Snare / Clap synthesis
    snare_dur = 0.22
    snare_samples = int(SAMPLE_RATE * snare_dur)
    tsn = np.linspace(0, snare_dur, snare_samples, endpoint=False)
    snare_w = (np.random.uniform(-1, 1, snare_samples) * np.exp(-tsn * 16.0) * 0.75 +
               np.sin(2 * np.pi * 195 * tsn) * np.exp(-tsn * 24.0) * 0.35) * 0.70

    # 3. Hi-hat synthesis
    hat_dur = 0.045
    hat_samples = int(SAMPLE_RATE * hat_dur)
    that = np.linspace(0, hat_dur, hat_samples, endpoint=False)
    hat_w = np.random.uniform(-1, 1, hat_samples) * np.exp(-that * 65.0) * 0.28

    total_beats = int(duration / beat_dur)
    total_steps = int(duration / step_dur)

    is_phonk_or_dance = "phonk" in style or "gigachad" in style or "close_eyes" in style or "aggressive" in style or "iron" in style

    # Percussion placement
    for b in range(total_beats):
        bs = int(b * beat_dur * SAMPLE_RATE)
        if is_phonk_or_dance:
            # 4-on-the-floor kick
            if bs + kick_samples <= num_samples:
                left[bs:bs + kick_samples] += kick_w * 0.85
                right[bs:bs + kick_samples] += kick_w * 0.85
            # Snare/Clap on 2 and 4
            if b % 2 == 1 and bs + snare_samples <= num_samples:
                left[bs:bs + snare_samples] += snare_w * 0.85
                right[bs:bs + snare_samples] += snare_w * 0.85
        else:
            # Chill / Lo-Fi half-time
            if b % 2 == 0 and bs + kick_samples <= num_samples:
                left[bs:bs + kick_samples] += kick_w * 0.65
                right[bs:bs + kick_samples] += kick_w * 0.65
            if b % 2 == 1 and bs + snare_samples <= num_samples:
                left[bs:bs + snare_samples] += snare_w * 0.55
                right[bs:bs + snare_samples] += snare_w * 0.55

    # Hi-hat patterns
    for s in range(total_steps):
        ss = int(s * step_dur * SAMPLE_RATE)
        if is_phonk_or_dance:
            hat_gain = 0.35 if (s % 2 == 1) else 0.22
            if ss + hat_samples <= num_samples:
                left[ss:ss + hat_samples] += hat_w * hat_gain
                right[ss:ss + hat_samples] += hat_w * hat_gain
        else:
            if s % 2 == 1 and ss + hat_samples <= num_samples:
                left[ss:ss + hat_samples] += hat_w * 0.20
                right[ss:ss + hat_samples] += hat_w * 0.20

    # 4. Melodic / Harmonic Stems
    if style == "g3ox_em_gigachad":
        # Iconic g3ox_em "Can You Feel My Heart" GigaChad Anthem:
        # Chords: Em - C - G - D
        chord_roots = [41.2, 32.7, 49.0, 36.7]
        chord_stabs = [
            [164.8, 196.0, 246.9, 329.6],  # Em
            [130.8, 164.8, 196.0, 261.6],  # C
            [196.0, 246.9, 293.7, 392.0],  # G
            [146.8, 185.0, 220.0, 293.7]   # D
        ]
        bar_dur = 4 * beat_dur
        total_bars = int(duration / bar_dur)
        stab_rhythm = [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0]

        # The legendary g3ox_em Bring Me The Horizon Cowbell Melody:
        # Measure 1: B4, B4, B4, G4, A4, B4, D5, C5
        # Measure 2: B4, A4, G4, E4, D4, E4, G4, E4
        melody_motif_bar1 = [(0, 493.88), (2, 493.88), (4, 493.88), (6, 392.00), (8, 440.00), (10, 493.88), (12, 587.33), (14, 523.25)]
        melody_motif_bar2 = [(0, 493.88), (2, 440.00), (4, 392.00), (6, 329.63), (8, 293.66), (10, 329.63), (12, 392.00), (14, 329.63)]

        for bar_idx in range(total_bars):
            bar_start = bar_idx * bar_dur
            ch_idx = bar_idx % 4
            root = chord_roots[ch_idx]
            ch_freqs = chord_stabs[ch_idx]

            # 808 Sub-bass with kick ducking
            b_samps = int(bar_dur * SAMPLE_RATE)
            b_idx = int(bar_start * SAMPLE_RATE)
            tb = np.linspace(0, bar_dur, b_samps, endpoint=False)
            sub = (np.sin(2 * np.pi * root * tb) * 0.72 + np.sin(2 * np.pi * root * 2 * tb) * 0.28)
            duck = np.clip(((tb % beat_dur) / beat_dur) * 3.0, 0.2, 1.0)
            if b_idx + b_samps <= num_samples:
                left[b_idx:b_idx + b_samps] += sub * duck * 0.50
                right[b_idx:b_idx + b_samps] += sub * duck * 0.50

            # Supersaw stabs
            for s_idx, hit in enumerate(stab_rhythm):
                if hit:
                    st_time = bar_start + s_idx * step_dur
                    st_idx = int(st_time * SAMPLE_RATE)
                    dur_st = step_dur * 0.88
                    nst = int(dur_st * SAMPLE_RATE)
                    tst = np.linspace(0, dur_st, nst, endpoint=False)
                    env_st = np.exp(-tst * 7.5)
                    for f in ch_freqs:
                        saw1 = 2 * (tst * f - np.floor(0.5 + tst * f))
                        saw2 = 2 * (tst * (f * 1.004) - np.floor(0.5 + tst * (f * 1.004)))
                        saw = (saw1 + saw2) * 0.5
                        if st_idx + nst <= num_samples:
                            left[st_idx:st_idx + nst] += saw * env_st * 0.13
                            right[st_idx:st_idx + nst] += saw * env_st * 0.13

            # Distorted Phonk Cowbell Lead
            current_motif = melody_motif_bar1 if (bar_idx % 2 == 0) else melody_motif_bar2
            for s_step, note_freq in current_motif:
                c_time = bar_start + s_step * step_dur
                c_idx = int(c_time * SAMPLE_RATE)
                cb_dur = step_dur * 1.8
                cb_wave = make_phonk_cowbell(note_freq, cb_dur)
                ncb = len(cb_wave)
                if c_idx + ncb <= num_samples:
                    left[c_idx:c_idx + ncb] += cb_wave * 0.28
                    right[c_idx:c_idx + ncb] += cb_wave * 0.28

    elif style == "dvrst_close_eyes":
        # DVRST "Close Eyes" Sigma Drift Phonk
        # Chords: Cm -> G# -> D# -> A#
        chord_roots = [32.7, 51.9, 38.9, 46.2]
        bar_dur = 4 * beat_dur
        total_bars = int(duration / bar_dur)
        # Iconic syncopated DVRST cowbell riff
        dvrst_notes = [
            (0, 523.25),   # C5
            (3, 622.25),   # D#5
            (6, 698.46),   # F5
            (8, 783.99),   # G5
            (10, 698.46),  # F5
            (12, 622.25),  # D#5
            (14, 523.25)   # C5
        ]

        for bar_idx in range(total_bars):
            bar_start = bar_idx * bar_dur
            root = chord_roots[bar_idx % len(chord_roots)]

            # Saturated 808 glides
            b_samps = int(bar_dur * SAMPLE_RATE)
            b_idx = int(bar_start * SAMPLE_RATE)
            tb = np.linspace(0, bar_dur, b_samps, endpoint=False)
            sub = np.tanh(np.sin(2 * np.pi * root * tb) * 1.8) * 0.45
            duck = np.clip(((tb % beat_dur) / beat_dur) * 3.2, 0.2, 1.0)
            if b_idx + b_samps <= num_samples:
                left[b_idx:b_idx + b_samps] += sub * duck
                right[b_idx:b_idx + b_samps] += sub * duck

            # Cowbell riff
            for s_step, note_freq in dvrst_notes:
                c_time = bar_start + s_step * step_dur
                c_idx = int(c_time * SAMPLE_RATE)
                cb_dur = step_dur * 1.6
                cb_wave = make_phonk_cowbell(note_freq, cb_dur)
                ncb = len(cb_wave)
                if c_idx + ncb <= num_samples:
                    left[c_idx:c_idx + ncb] += cb_wave * 0.30
                    right[c_idx:c_idx + ncb] += cb_wave * 0.30

    elif style in ["kordhell_aggressive", "warrior_phonk", "iron_discipline"]:
        # Aggressive Gym / Warrior Phonk
        roots = [46.2, 41.2, 38.9, 43.6]
        bar_dur = 4 * beat_dur
        total_bars = int(duration / bar_dur)
        lead_riff = [
            (0, 659.25), (2, 587.33), (4, 493.88), (6, 440.00),
            (8, 392.00), (10, 440.00), (12, 493.88), (14, 659.25)
        ]

        for bar_idx in range(total_bars):
            bar_start = bar_idx * bar_dur
            root = roots[bar_idx % len(roots)]

            # Heavy hardstyle 808
            b_samps = int(bar_dur * SAMPLE_RATE)
            b_idx = int(bar_start * SAMPLE_RATE)
            tb = np.linspace(0, bar_dur, b_samps, endpoint=False)
            dist_808 = np.tanh((np.sin(2 * np.pi * root * tb) + np.sin(2 * np.pi * root * 2 * tb) * 0.4) * 2.2) * 0.48
            duck = np.clip(((tb % beat_dur) / beat_dur) * 3.4, 0.2, 1.0)
            if b_idx + b_samps <= num_samples:
                left[b_idx:b_idx + b_samps] += dist_808 * duck
                right[b_idx:b_idx + b_samps] += dist_808 * duck

            # High-octave lead stabs
            for s_step, note_freq in lead_riff:
                c_time = bar_start + s_step * step_dur
                c_idx = int(c_time * SAMPLE_RATE)
                cb_dur = step_dur * 1.5
                cb_wave = make_phonk_cowbell(note_freq, cb_dur)
                ncb = len(cb_wave)
                if c_idx + ncb <= num_samples:
                    left[c_idx:c_idx + ncb] += cb_wave * 0.26
                    right[c_idx:c_idx + ncb] += cb_wave * 0.26

    elif style == "home_resonance":
        # Home - Resonance Warm Synthwave Swells
        chords_resonance = [
            [261.6, 329.6, 392.0, 493.9, 587.3],  # Cmaj9
            [293.7, 369.9, 440.0, 587.3, 659.3],  # D9
            [196.0, 246.9, 293.7, 392.0, 493.9],  # Gmaj7
            [164.8, 196.0, 246.9, 329.6, 392.0]   # Em7
        ]
        bar_dur = 4 * beat_dur
        total_bars = int(duration / bar_dur)
        for b_idx in range(total_bars):
            ch_freqs = chords_resonance[b_idx % 4]
            b_start = int(b_idx * bar_dur * SAMPLE_RATE)
            b_samps = int(bar_dur * SAMPLE_RATE)
            tb = np.linspace(0, bar_dur, b_samps, endpoint=False)
            pad_env = (np.sin(np.pi * tb / bar_dur) ** 1.4)  # Lush analog swell
            for f in ch_freqs:
                # Analog detuned sine/saw blend
                s1 = np.sin(2 * np.pi * f * tb)
                s2 = np.sin(2 * np.pi * (f * 1.003) * tb)
                pad = (s1 * 0.6 + s2 * 0.4) * pad_env * 0.12
                if b_start + b_samps <= num_samples:
                    left[b_start:b_start + b_samps] += pad
                    right[b_start:b_start + b_samps] += pad

            # Sparkling chime arpeggio
            for p_step in range(8):
                pf = ch_freqs[p_step % len(ch_freqs)] * 2.0
                pt_time = b_idx * bar_dur + p_step * (step_dur * 2)
                pts_idx = int(pt_time * SAMPLE_RATE)
                np_s = int(step_dur * 1.8 * SAMPLE_RATE)
                if pts_idx + np_s <= num_samples:
                    tp = np.linspace(0, step_dur * 1.8, np_s, endpoint=False)
                    chime = np.sin(2 * np.pi * pf * tp) * np.exp(-tp * 6.5) * 0.08
                    left[pts_idx:pts_idx + np_s] += chime
                    right[pts_idx:pts_idx + np_s] += chime

    else:
        # Carefree / Ambient Lo-Fi Outdoor Pads
        chords_lofi = [
            [261.6, 329.6, 392.0, 493.9],  # Cmaj7
            [293.7, 349.2, 440.0, 523.3],  # Dm7
            [196.0, 246.9, 293.7, 349.2],  # G7
            [164.8, 196.0, 246.9, 329.6]   # Em7
        ]
        bar_dur = 4 * beat_dur
        total_bars = int(duration / bar_dur)
        for b_idx in range(total_bars):
            ch_freqs = chords_lofi[b_idx % 4]
            b_start = int(b_idx * bar_dur * SAMPLE_RATE)
            b_samps = int(bar_dur * SAMPLE_RATE)
            tb = np.linspace(0, bar_dur, b_samps, endpoint=False)
            pad_env = np.sin(np.pi * tb / bar_dur)
            for f in ch_freqs:
                pad = np.sin(2 * np.pi * f * tb) * pad_env * 0.10
                if b_start + b_samps <= num_samples:
                    left[b_start:b_start + b_samps] += pad
                    right[b_start:b_start + b_samps] += pad

            # Electric piano Rhodes motif
            for step in range(4):
                rf = ch_freqs[step] * 1.5
                rt_time = b_idx * bar_dur + step * beat_dur
                r_idx = int(rt_time * SAMPLE_RATE)
                rdur = int(beat_dur * 0.9 * SAMPLE_RATE)
                if r_idx + rdur <= num_samples:
                    tr = np.linspace(0, beat_dur * 0.9, rdur, endpoint=False)
                    rhodes = (np.sin(2 * np.pi * rf * tr) + np.sin(2 * np.pi * rf * 2 * tr) * 0.3) * np.exp(-tr * 8.0) * 0.12
                    left[r_idx:rdur + r_idx] += rhodes
                    right[r_idx:rdur + r_idx] += rhodes

    # Compression & Master Limiter
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1.0)
    left = np.tanh(left / max_val * 1.38) * 0.92
    right = np.tanh(right / max_val * 1.38) * 0.92

    # Write 16-bit stereo WAV
    with wave.open(str(out_wav), 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        interleaved = np.empty((num_samples * 2,), dtype=np.int16)
        interleaved[0::2] = (left * 32767).astype(np.int16)
        interleaved[1::2] = (right * 32767).astype(np.int16)
        wf.writeframes(interleaved.tobytes())

def convert_wav_to_mp3(wav_path: Path, mp3_path: Path):
    """Encode synthesized WAV to high quality 192k MP3."""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(wav_path),
        "-codec:a", "libmp3lame",
        "-b:a", "192k",
        str(mp3_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_all_themes():
    print("👑 GigaChad Theme Generator Starting (with Meme References & JSON Vault)...")
    themes_manifest = {
        "focus": [],
        "break": [],
        "long_break": [],
        "motivation": []
    }

    for spec in THEME_SPECS:
        theme_id = spec["id"]
        cat = spec["category"]
        print(f"\n⚡ Generating Theme: [{cat.upper()}] {spec['title']}")
        print(f"   Meme Reference: {spec['meme_reference']}")

        raw_wav = SCRATCH_DIR / f"{theme_id}.wav"
        out_mp3 = OUTPUT_AUDIO_DIR / f"{theme_id}.mp3"
        out_json = OUTPUT_THEMES_DIR / f"{theme_id}.json"

        # 1. Synthesize instrumental track
        print(f"  [Synthesizer] Rendering {spec['style']} ({spec['bpm']} BPM, {spec['duration']}s)...")
        synthesize_instrumental_theme(spec, raw_wav)

        # 2. Encode to MP3
        print(f"  [Encoder] Writing MP3 to {out_mp3.name}...")
        convert_wav_to_mp3(raw_wav, out_mp3)

        raw_wav.unlink(missing_ok=True)

        # 3. Create individual metadata JSON for this theme
        theme_meta = {
            "id": theme_id,
            "category": cat,
            "title": spec["title"],
            "meme_reference": spec["meme_reference"],
            "original_artist_reference": spec["original_artist_reference"],
            "bpm": spec["bpm"],
            "duration": spec["duration"],
            "key": spec["key"],
            "genre": spec["genre"],
            "instruments": spec["instruments"],
            "audio_url": f"/vault/audio/{theme_id}.mp3",
            "is_instrumental": True,
            "license": spec["license"],
            "description": spec["description"]
        }

        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(theme_meta, f, indent=2, ensure_ascii=False)
        print(f"  📄 Saved Theme JSON Reference: {out_json.name}")

        themes_manifest[cat].append(theme_meta)
        print(f"  ✅ Finished: {out_mp3.name} ({out_mp3.stat().st_size} bytes)")

    # 4. Update manifest.json with full themes registry
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        manifest_data["themes"] = themes_manifest
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2, ensure_ascii=False)
        print(f"\n🏆 Updated manifest.json with {sum(len(v) for v in themes_manifest.values())} GigaChad themes!")

if __name__ == "__main__":
    generate_all_themes()
