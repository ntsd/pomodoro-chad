#!/usr/bin/env python3
"""
Sync Voice Vault Manifest
Scans public/vault/scripts and public/vault/audio to compile public/vault/manifest.json,
indexing all clips along with their specific GigaChad voice IDs and metadata.
"""

import os
import json
import glob
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
VAULT_DIR = BASE_DIR / "public" / "vault"
SCRIPTS_DIR = VAULT_DIR / "scripts"
AUDIO_DIR = VAULT_DIR / "audio"
MANIFEST_FILE = VAULT_DIR / "manifest.json"

CATEGORY_KEYS = ["START_FOCUS", "SHORT_BREAK", "LONG_BREAK", "CHAD_MOTIVATION"]

KNOWN_VOICE_NAMES = {
    "pNInz6obpgDQGcFmaJgB": "Adam (Dominant Chad)",
    "SOYHLrjzK2X1ezoPC6cr": "Harry (Fierce Warrior Chad)",
    "nPczCjzI2devNBz1zQrb": "Brian (Deep Resonant Chad)",
    "IKne3meq5aSn9XLyUdCD": "Charlie (Energetic Chad)",
    "N2lVS1w4EtoT3dr4eOWO": "Callum (Husky Chad)",
    "JBFqnCBsd6RMkjVDRZzb": "George (Storyteller Chad)"
}

def sync_manifest():
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
    else:
        manifest_data = {
            "version": "1.2.0",
            "description": "Chadodoro Git Voice Vault - Pre-rendered GigaChad audio coaching clips and instrumental themes",
            "total_clips": 0,
            "voice_ids": [],
            "voice_names": {},
            "categories": {cat: [] for cat in CATEGORY_KEYS},
            "themes": {cat: [] for cat in CATEGORY_KEYS}
        }

    # Ensure standardized categories exist
    if "categories" not in manifest_data:
        manifest_data["categories"] = {}
    for cat in CATEGORY_KEYS:
        if cat not in manifest_data["categories"]:
            manifest_data["categories"][cat] = []

    # Ensure standardized themes exist
    if "themes" not in manifest_data:
        manifest_data["themes"] = {}
    for cat in CATEGORY_KEYS:
        if cat not in manifest_data["themes"]:
            manifest_data["themes"][cat] = []

    # Verify and update audio status for all clips
    total_clips = 0
    voice_id_set = set()
    for cat, clips in manifest_data["categories"].items():
        for clip in clips:
            total_clips += 1
            cid = clip.get("id")
            vid = clip.get("voice_id", "pNInz6obpgDQGcFmaJgB")
            voice_id_set.add(vid)
            if vid in KNOWN_VOICE_NAMES and not clip.get("voice_name"):
                clip["voice_name"] = KNOWN_VOICE_NAMES[vid]

            # Check audio file
            audio_path = SCRIPTS_DIR / cid / f"{cid}.mp3"
            has_audio = audio_path.exists()
            clip["has_audio"] = has_audio
            if has_audio:
                clip["audio_url"] = f"/vault/scripts/{cid}/{cid}.mp3"

    manifest_data["total_clips"] = total_clips
    manifest_data["voice_ids"] = sorted(list(voice_id_set))
    manifest_data["voice_names"] = {vid: KNOWN_VOICE_NAMES.get(vid, f"Voice {vid[:8]}") for vid in manifest_data["voice_ids"]}

    # Verify themes
    themes_dir = VAULT_DIR / "themes"
    for t_cat, t_list in manifest_data["themes"].items():
        for theme in t_list:
            tid = theme.get("id")
            t_audio = themes_dir / tid / f"{tid}.mp3"
            if t_audio.exists():
                theme["audio_url"] = f"/vault/themes/{tid}/{tid}.mp3"

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    total_themes = sum(len(v) for v in manifest_data["themes"].values())
    print(f"✅ Manifest verified: {manifest_data['total_clips']} clips across {len(manifest_data['categories'])} categories and {total_themes} themes across {len(manifest_data['themes'])} theme categories.")
    return manifest_data

if __name__ == "__main__":
    sync_manifest()
