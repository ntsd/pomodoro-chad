#!/usr/bin/env python3
"""
Generate Pure Instrumental GigaChad Themes & Anthems
Synthesizes high-energy, seamless instrumental loops for Chadodoro:
- Focus: "Can You Feel My Heart" Phonk Drop, Dark Synthwave Cyber-Pulse, Hyper-Focus Titan Phonk
- Break: Sunlit Meadow Serenade, Outdoor Oxygen Lo-Fi Groove, Meadow Breeze Chillstep
- Long Break: Titan Outdoor Walk & Hydration, Forest Canopy Reverie
- Motivation: Warrior Ascendance Phonk, Iron Discipline Apex Phonk

All tracks are pure instrumental music, completely separate from the GigaChad voice quotes,
allowing users to enable, disable, or adjust volume for voice and theme music independently!
"""

import os
import json
import wave
import subprocess
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "public" / "vault" / "audio"
MANIFEST_FILE = BASE_DIR / "public" / "vault" / "manifest.json"
SCRATCH_DIR = BASE_DIR / ".cache_audio"

SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 44100

THEME_SPECS = [
    # --- FOCUS THEMES ---
    {
        "id": "theme_focus_01",
        "category": "focus",
        "title": "GigaChad Anthem - Can You Feel My Heart (Phonk Drop)",
        "bpm": 128,
        "duration": 15.0,
        "style": "phonk_classic"
    },
    {
        "id": "theme_focus_02",
        "category": "focus",
        "title": "Deep Work Lock-In (Dark Synthwave Pulse)",
        "bpm": 132,
        "duration": 14.5,
        "style": "synthwave"
    },
    {
        "id": "theme_focus_03",
        "category": "focus",
        "title": "Hyper-Focus Titan Rhythm (Aggressive Phonk)",
        "bpm": 136,
        "duration": 14.1,
        "style": "phonk_aggressive"
    },

    # --- BREAK THEMES (TOUCH GRASS) ---
    {
        "id": "theme_break_01",
        "category": "break",
        "title": "Sunlit Meadow - Touch Grass Serenade",
        "bpm": 96,
        "duration": 15.0,
        "style": "meadow_acoustic"
    },
    {
        "id": "theme_break_02",
        "category": "break",
        "title": "Outdoor Oxygen Lo-Fi Groove",
        "bpm": 104,
        "duration": 13.8,
        "style": "lofi_groove"
    },
    {
        "id": "theme_break_03",
        "category": "break",
        "title": "Breeze of the Meadow (Chillstep Pulse)",
        "bpm": 100,
        "duration": 14.4,
        "style": "chillstep"
    },

    # --- LONG BREAK THEMES ---
    {
        "id": "theme_long_break_01",
        "category": "long_break",
        "title": "Titan Outdoor Walk & Hydration",
        "bpm": 92,
        "duration": 15.6,
        "style": "ambient_walk"
    },
    {
        "id": "theme_long_break_02",
        "category": "long_break",
        "title": "Forest Canopy Reverie (Lush Lo-Fi)",
        "bpm": 86,
        "duration": 16.7,
        "style": "forest_ambient"
    },

    # --- MOTIVATION THEMES ---
    {
        "id": "theme_motivation_01",
        "category": "motivation",
        "title": "Warrior Ascendance - Pure GigaChad Phonk",
        "bpm": 130,
        "duration": 14.8,
        "style": "phonk_warrior"
    },
    {
        "id": "theme_motivation_02",
        "category": "motivation",
        "title": "Iron Discipline Apex (Titan War Stabs)",
        "bpm": 134,
        "duration": 14.3,
        "style": "iron_discipline"
    }
]

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
    kick_samples = int(SAMPLE_RATE * 0.22)
    tk = np.linspace(0, 0.22, kick_samples, endpoint=False)
    kick_pitch = 160.0 * np.exp(-tk * 28.0) + 42.0
    kick_w = np.sin(2 * np.pi * np.cumsum(kick_pitch) / SAMPLE_RATE) * np.exp(-tk * 14.0)

    # 2. Snare / Clap synthesis
    snare_samples = int(SAMPLE_RATE * 0.22)
    tsn = np.linspace(0, 0.22, snare_samples, endpoint=False)
    snare_w = (np.random.uniform(-1, 1, snare_samples) * np.exp(-tsn * 16.0) * 0.75 +
               np.sin(2 * np.pi * 190 * tsn) * np.exp(-tsn * 24.0) * 0.35) * 0.65

    # 3. Hi-hat synthesis
    hat_samples = int(SAMPLE_RATE * 0.05)
    that = np.linspace(0, 0.05, hat_samples, endpoint=False)
    hat_w = np.random.uniform(-1, 1, hat_samples) * np.exp(-that * 65.0) * 0.25

    # Place percussion rhythm
    total_beats = int(duration / beat_dur)
    total_steps = int(duration / step_dur)

    is_phonk_or_dance = "phonk" in style or "synthwave" in style or "iron" in style

    # Percussion placement
    for b in range(total_beats):
        bs = int(b * beat_dur * SAMPLE_RATE)
        if is_phonk_or_dance:
            # 4-on-the-floor kick
            if bs + kick_samples <= num_samples:
                left[bs:bs + kick_samples] += kick_w * 0.82
                right[bs:bs + kick_samples] += kick_w * 0.82
            # Snare on 2 and 4
            if b % 2 == 1 and bs + snare_samples <= num_samples:
                left[bs:bs + snare_samples] += snare_w * 0.85
                right[bs:bs + snare_samples] += snare_w * 0.85
        else:
            # Relaxed lo-fi / chillstep rhythm (kick on 1 and 3, or half-time)
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
            # 16th or 8th note rolling hats
            hat_gain = 0.35 if (s % 2 == 1) else 0.20
            if ss + hat_samples <= num_samples:
                left[ss:ss + hat_samples] += hat_w * hat_gain
                right[ss:ss + hat_samples] += hat_w * hat_gain
        else:
            # Chill swing hats on offbeats
            if s % 2 == 1 and ss + hat_samples <= num_samples:
                left[ss:ss + hat_samples] += hat_w * 0.22
                right[ss:ss + hat_samples] += hat_w * 0.22

    # 4. Melodic / Harmonic Stems
    if style in ["phonk_classic", "phonk_aggressive", "phonk_warrior", "iron_discipline"]:
        # Iconic GigaChad progression: Em - C - G - D
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

        for bar_idx in range(total_bars):
            bar_start = bar_idx * bar_dur
            ch_idx = bar_idx % 4
            root = chord_roots[ch_idx]
            ch_freqs = chord_stabs[ch_idx]

            # 808 Sub-bass with kick ducking
            b_samps = int(bar_dur * SAMPLE_RATE)
            b_idx = int(bar_start * SAMPLE_RATE)
            tb = np.linspace(0, bar_dur, b_samps, endpoint=False)
            sub = (np.sin(2 * np.pi * root * tb) * 0.70 + np.sin(2 * np.pi * root * 2 * tb) * 0.28)
            duck = np.clip(((tb % beat_dur) / beat_dur) * 3.0, 0.2, 1.0)
            if b_idx + b_samps <= num_samples:
                left[b_idx:b_idx + b_samps] += sub * duck * 0.48
                right[b_idx:b_idx + b_samps] += sub * duck * 0.48

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
                        # Rich detuned saw
                        saw1 = 2 * (tst * f - np.floor(0.5 + tst * f))
                        saw2 = 2 * (tst * (f * 1.004) - np.floor(0.5 + tst * (f * 1.004)))
                        saw = (saw1 + saw2) * 0.5
                        if st_idx + nst <= num_samples:
                            left[st_idx:st_idx + nst] += saw * env_st * 0.14
                            right[st_idx:st_idx + nst] += saw * env_st * 0.14

            # Phonk lead melody on warrior/aggressive styles
            if style in ["phonk_warrior", "phonk_aggressive"]:
                lead_notes = [659.3, 587.3, 493.9, 440.0, 392.0, 440.0, 493.9, 659.3]
                for l_idx, lf in enumerate(lead_notes):
                    l_time = bar_start + l_idx * (step_dur * 2)
                    ls_idx = int(l_time * SAMPLE_RATE)
                    dur_l = step_dur * 1.8
                    nl = int(dur_l * SAMPLE_RATE)
                    tl = np.linspace(0, dur_l, nl, endpoint=False)
                    cowbell = (np.sin(2 * np.pi * lf * tl) * 0.6 + np.sin(2 * np.pi * lf * 1.5 * tl) * 0.4) * np.exp(-tl * 10.0)
                    if ls_idx + nl <= num_samples:
                        left[ls_idx:ls_idx + nl] += cowbell * 0.18
                        right[ls_idx:ls_idx + nl] += cowbell * 0.18

    elif style == "synthwave":
        # Dark Cyber Synthwave arpeggiator (E minor pentatonic)
        notes_arp = [164.8, 196.0, 246.9, 329.6, 392.0, 329.6, 246.9, 196.0]
        total_arps = int(duration / (len(notes_arp) * step_dur) + 1)
        full_arp = notes_arp * total_arps
        for idx, f in enumerate(full_arp):
            st_time = idx * step_dur
            st_idx = int(st_time * SAMPLE_RATE)
            nst = int(step_dur * 0.95 * SAMPLE_RATE)
            if st_idx + nst <= num_samples:
                tst = np.linspace(0, step_dur * 0.95, nst, endpoint=False)
                wave_p = (np.sin(2 * np.pi * f * tst) * 0.7 + np.sin(2 * np.pi * f * 2 * tst) * 0.3) * np.exp(-tst * 9.0)
                left[st_idx:st_idx + nst] += wave_p * 0.28
                right[st_idx:st_idx + nst] += wave_p * 0.28

        # Driving 80s bassline
        bass_notes = [82.4, 82.4, 65.4, 65.4, 98.0, 98.0, 73.4, 73.4]
        for b_i, bf in enumerate(bass_notes * total_arps):
            bt_time = b_i * (step_dur * 2)
            bts_idx = int(bt_time * SAMPLE_RATE)
            nb = int(step_dur * 1.9 * SAMPLE_RATE)
            if bts_idx + nb <= num_samples:
                tb = np.linspace(0, step_dur * 1.9, nb, endpoint=False)
                bass_w = (np.sin(2 * np.pi * bf * tb) * 0.7 + np.sin(2 * np.pi * bf * 2 * tb) * 0.3) * np.exp(-tb * 5.0)
                left[bts_idx:bts_idx + nb] += bass_w * 0.38
                right[bts_idx:bts_idx + nb] += bass_w * 0.38

    else:
        # Chill Meadow / Outdoor Lo-Fi & Ambient Pads (Major 7th / 9th warmth)
        chords_meadow = [
            [261.6, 329.6, 392.0, 493.9, 587.3],  # Cmaj9
            [293.7, 369.9, 440.0, 587.3, 659.3],  # D9
            [196.0, 246.9, 293.7, 392.0, 493.9],  # Gmaj7
            [164.8, 196.0, 246.9, 329.6, 392.0]   # Em7
        ]
        bar_dur = 4 * beat_dur
        total_bars = int(duration / bar_dur)
        for b_idx in range(total_bars):
            ch_freqs = chords_meadow[b_idx % 4]
            b_start = int(b_idx * bar_dur * SAMPLE_RATE)
            b_samps = int(bar_dur * SAMPLE_RATE)
            tb = np.linspace(0, bar_dur, b_samps, endpoint=False)
            pad_env = np.sin(np.pi * tb / bar_dur) ** 1.3  # gentle organic swell
            for f in ch_freqs:
                # Soft organ/sine pad
                pad = (np.sin(2 * np.pi * f * tb) * 0.8 + np.sin(2 * np.pi * f * 2 * tb) * 0.2) * pad_env * 0.10
                if b_start + b_samps <= num_samples:
                    left[b_start:b_start + b_samps] += pad
                    right[b_start:b_start + b_samps] += pad

            # Electric piano / chime arpeggios
            for p_step in range(8):
                pf = ch_freqs[p_step % len(ch_freqs)] * 2.0
                pt_time = b_idx * bar_dur + p_step * (step_dur * 2)
                pts_idx = int(pt_time * SAMPLE_RATE)
                np_s = int(step_dur * 1.8 * SAMPLE_RATE)
                if pts_idx + np_s <= num_samples:
                    tp = np.linspace(0, step_dur * 1.8, np_s, endpoint=False)
                    chime = np.sin(2 * np.pi * pf * tp) * np.exp(-tp * 7.0) * 0.08
                    left[pts_idx:pts_idx + np_s] += chime
                    right[pts_idx:pts_idx + np_s] += chime

    # Compression & Master Limiter
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1.0)
    left = np.tanh(left / max_val * 1.35) * 0.92
    right = np.tanh(right / max_val * 1.35) * 0.92

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
    print("👑 GigaChad Pure Instrumental Theme Generator Starting...")
    themes_manifest = {
        "focus": [],
        "break": [],
        "long_break": [],
        "motivation": []
    }

    for spec in THEME_SPECS:
        theme_id = spec["id"]
        cat = spec["category"]
        print(f"\n⚡ Generating Pure Instrumental Theme: [{cat.upper()}] {spec['title']}")

        raw_wav = SCRATCH_DIR / f"{theme_id}.wav"
        out_mp3 = OUTPUT_DIR / f"{theme_id}.mp3"

        # 1. Synthesize instrumental track
        print(f"  [Synthesizer] Rendering {spec['style']} ({spec['bpm']} BPM, {spec['duration']}s)...")
        synthesize_instrumental_theme(spec, raw_wav)

        # 2. Encode to MP3
        print(f"  [Encoder] Writing high-bitrate MP3 to {out_mp3.name}...")
        convert_wav_to_mp3(raw_wav, out_mp3)

        raw_wav.unlink(missing_ok=True)

        entry = {
            "id": theme_id,
            "category": cat,
            "title": spec["title"],
            "audio_url": f"/vault/audio/{theme_id}.mp3",
            "bpm": spec["bpm"],
            "duration": spec["duration"],
            "is_instrumental": True
        }
        themes_manifest[cat].append(entry)
        print(f"  ✅ Finished: {out_mp3.name} ({out_mp3.stat().st_size} bytes)")

    # Update manifest.json with clean themes registry
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, "r") as f:
            manifest_data = json.load(f)
        manifest_data["themes"] = themes_manifest
        with open(MANIFEST_FILE, "w") as f:
            json.dump(manifest_data, f, indent=2, ensure_ascii=False)
        print(f"\n🏆 Updated manifest.json with {sum(len(v) for v in themes_manifest.values())} pure instrumental GigaChad themes!")

if __name__ == "__main__":
    generate_all_themes()
