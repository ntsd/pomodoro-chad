#!/usr/bin/env python3
"""
Sync Voice Vault Manifest
Scans public/vault/scripts and public/vault/audio to compile public/vault/manifest.json.
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

def sync_manifest():
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    manifest_data = {
        "version": "1.0.0",
        "description": "Chadodoro Git Voice Vault - Pre-rendered GigaChad audio coaching clips",
        "total_clips": 0,
        "categories": {cat: [] for cat in CATEGORY_KEYS}
    }

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

            clip_entry = {
                "id": clip_id,
                "category": category,
                "text": meta.get("text", ""),
                "audio_url": f"/vault/audio/{audio_filename}" if has_audio else None,
                "has_audio": has_audio,
                "voice_id": meta.get("voice_id", ""),
                "model": meta.get("model", "")
            }
            manifest_data["categories"][category].append(clip_entry)
            manifest_data["total_clips"] += 1
        except Exception as e:
            print(f"Warning: Failed to parse {script_path}: {e}")

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Manifest synced successfully: {manifest_data['total_clips']} clips indexed in {MANIFEST_FILE}")
    return manifest_data

if __name__ == "__main__":
    sync_manifest()
