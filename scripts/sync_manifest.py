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

CATEGORY_KEYS = ["START_FOCUS", "TOUCH_GRASS", "LONG_BREAK", "CHAD_MOTIVATION"]

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
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    manifest_data = {
        "version": "1.1.0",
        "description": "Chadodoro Git Voice Vault - Pre-rendered GigaChad audio coaching clips",
        "total_clips": 0,
        "voice_ids": [],
        "voice_names": {},
        "categories": {cat: [] for cat in CATEGORY_KEYS}
    }

    voice_id_set = set()
    script_files = sorted(glob.glob(str(SCRIPTS_DIR / "*.json")))

    for script_path in script_files:
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            
            clip_id = meta.get("id") or Path(script_path).stem
            category = meta.get("category", "START_FOCUS")
            if category not in manifest_data["categories"]:
                manifest_data["categories"][category] = []
            
            audio_filename = f"{clip_id}.mp3"
            audio_path = AUDIO_DIR / audio_filename
            has_audio = audio_path.exists()

            voice_id = meta.get("voice_id", "pNInz6obpgDQGcFmaJgB")
            voice_name = meta.get("voice_name") or KNOWN_VOICE_NAMES.get(voice_id, f"Voice {voice_id[:8]}")
            
            voice_id_set.add(voice_id)
            manifest_data["voice_names"][voice_id] = voice_name

            clip_entry = {
                "id": clip_id,
                "category": category,
                "text": meta.get("text", ""),
                "audio_url": f"/vault/audio/{audio_filename}" if has_audio else None,
                "has_audio": has_audio,
                "voice_id": voice_id,
                "voice_name": voice_name,
                "model": meta.get("model", "google/gemma-4-26B-A4B-it")
            }
            manifest_data["categories"][category].append(clip_entry)
            manifest_data["total_clips"] += 1
        except Exception as e:
            print(f"Warning: Failed to parse {script_path}: {e}")

    manifest_data["voice_ids"] = sorted(list(voice_id_set))

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Manifest synced: {manifest_data['total_clips']} clips indexed across voices: {manifest_data['voice_ids']}")
    return manifest_data

if __name__ == "__main__":
    sync_manifest()
