#!/usr/bin/env python3
"""
Chadodoro Git Voice Vault Generator Pipeline
Generates coaching transcripts via google/gemma-4-26B-A4B-it and synthesizes
ultra-commanding GigaChad audio via ElevenLabs with multi-voice ID support.
Outputs committed static assets to public/vault/scripts and public/vault/audio.
"""

import os
import sys
import json
import random
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

# Ensure environment variables are loaded from root .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Configuration
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://spark.ntsd.dev:8001/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "dummy"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "google/gemma-4-26B-A4B-it")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# Multi-Voice ID parsing
raw_voice_ids = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")
VOICE_IDS = [v.strip() for v in raw_voice_ids.split(",") if v.strip()]
if not VOICE_IDS:
    VOICE_IDS = ["pNInz6obpgDQGcFmaJgB"]

KNOWN_VOICE_NAMES = {
    "pNInz6obpgDQGcFmaJgB": "Adam (Dominant Chad)",
    "SOYHLrjzK2X1ezoPC6cr": "Harry (Fierce Warrior Chad)",
    "nPczCjzI2devNBz1zQrb": "Brian (Deep Resonant Chad)",
    "IKne3meq5aSn9XLyUdCD": "Charlie (Energetic Chad)",
    "N2lVS1w4EtoT3dr4eOWO": "Callum (Husky Chad)",
    "JBFqnCBsd6RMkjVDRZzb": "George (Storyteller Chad)"
}

VAULT_DIR = BASE_DIR / "public" / "vault"
SCRIPTS_DIR = VAULT_DIR / "scripts"
AUDIO_DIR = VAULT_DIR / "audio"

SYSTEM_PROMPT = (
    "You are Chadodoro, an uncompromising, stoic GigaChad productivity and fitness coach. "
    "Deliver 1 to 2 punchy, commanding sentences. Address the user as 'King', 'Champion', or 'Brother'. "
    "Focus on discipline, stoicism, and radical outdoor screen breaks ('touch grass'). "
    "Keep it purely in-character without mentioning AI models or hardware."
)

CATEGORY_CONFIG = {
    "START_FOCUS": {
        "prefix": "focus",
        "description": "Lock-in commands for deep work",
        "user_prompt": "Deliver a fierce, commanding order to lock in for deep work right now. Zero distractions.",
        "fallback_pool": [
            "Lock in, King. The world belongs to those who conquer distraction.",
            "Eliminate all distractions, Champion. Your empire is built in this exact block of deep work.",
            "Focus, Brother. Weakness seeks excuses, but a Chad executes without hesitation.",
            "Silence the noise, King. Put your head down and let results speak for you.",
            "Time to grind, Champion. The clock is ticking, and greatness waits for no man."
        ]
    },
    "TOUCH_GRASS": {
        "prefix": "break_touch_grass",
        "description": "Urgent commands to step away from monitors and touch physical grass",
        "user_prompt": "Time is up! Order the user urgently to stand up, close their laptop, and go outside to touch physical grass.",
        "fallback_pool": [
            "Screen time is over, King. Drop everything, step into the sunlight, and touch physical grass right now.",
            "Stand up, Champion! Disconnect from the machine and reconnect with the earth. Touch grass immediately.",
            "Time is up, Brother. Your eyes need the horizon and your soul needs raw soil. Step outside and touch grass.",
            "Halt the work, King. A true Chad knows when to step into nature. Go outside and feel the grass beneath your shoes.",
            "Step away from that monitor, Champion! Hydrate, breathe real oxygen, and plant your feet in physical grass."
        ]
    },
    "LONG_BREAK": {
        "prefix": "long_break",
        "description": "Outdoor walk directives and physical recovery",
        "user_prompt": "Direct the user to take a 15-minute outdoor walk, hydrate with cold water, and recharge under the sky.",
        "fallback_pool": [
            "Long break granted, Brother. Go for a brisk walk under the open sky and drink cold water like a champion.",
            "Take the field, King. March outside, let the sun hit your skin, and recharge your vitality for the next war.",
            "Step away for an extended recovery, Champion. Walk outside, clear your mind, and let nature restore your focus.",
            "Time to roam, Brother. Leave the digital cave behind, walk outside, and breathe deeply under the open sky."
        ]
    },
    "CHAD_MOTIVATION": {
        "prefix": "motivation",
        "description": "Stoic one-liners for instant motivation",
        "user_prompt": "Deliver a stoic, raw motivational one-liner reminding the user why they embrace the grind.",
        "fallback_pool": [
            "Comfort is the enemy of glory, King. Embrace the resistance.",
            "Discipline equals freedom, Champion. Do the hard work, especially when you don't feel like it.",
            "You were not born to scroll endlessly, Brother. You were forged to dominate your craft.",
            "Pain is temporary, King. Regret is permanent. Stay stoic and keep moving forward.",
            "Every second you stay disciplined, you separate yourself from the average man, Champion."
        ]
    }
}

def get_voice_name(voice_id: str) -> str:
    """Get clean human-readable name for a voice ID."""
    return KNOWN_VOICE_NAMES.get(voice_id, f"Voice {voice_id[:8]}")

def generate_script_text(category: str) -> str:
    """Generate script text using OpenAI API with fallback pool."""
    config = CATEGORY_CONFIG[category]
    user_prompt = config["user_prompt"]
    
    try:
        from openai import OpenAI
        client = OpenAI(
            base_url=OPENAI_BASE_URL,
            api_key=OPENAI_API_KEY,
            timeout=8.0
        )
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=80
        )
        text = response.choices[0].message.content.strip().strip('"').strip("'")
        if text and len(text) > 10:
            print(f"  [LLM Gemma] Generated: {text}")
            return text
    except Exception as e:
        print(f"  [LLM Notice] ({type(e).__name__}): Using curated neural fallback pool.")

    return random.choice(config["fallback_pool"])

def synthesize_audio_elevenlabs(text: str, output_path: Path, voice_id: str) -> bool:
    """Synthesize voice using ElevenLabs API with ultra-GigaChad settings."""
    if not ELEVENLABS_API_KEY:
        print("  [ElevenLabs] Error: ELEVENLABS_API_KEY is not set.")
        return False

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Ultra-GigaChad voice settings: dynamic delivery, resonant deep fidelity, exaggerated style
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.90,
            "style": 0.65,
            "use_speaker_boost": True
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response.content)
            voice_label = get_voice_name(voice_id)
            print(f"  [ElevenLabs: {voice_label}] Synthesized: {output_path.name} ({len(response.content)} bytes)")
            return True
        else:
            print(f"  [ElevenLabs Error] HTTP {response.status_code}: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"  [ElevenLabs Exception] {e}")
        return False

def get_next_id(prefix: str) -> str:
    """Find the next available 3-digit index for a prefix."""
    existing = list(SCRIPTS_DIR.glob(f"{prefix}_*.json"))
    max_idx = 0
    for p in existing:
        parts = p.stem.split("_")
        try:
            idx = int(parts[-1])
            if idx > max_idx:
                max_idx = idx
        except ValueError:
            continue
    next_idx = max_idx + 1
    return f"{prefix}_{next_idx:03d}"

def generate_clip(category: str, voice_id: str = None, custom_text: str = None, dry_run: bool = False) -> str:
    """Generate a single clip metadata and audio with chosen GigaChad voice ID."""
    config = CATEGORY_CONFIG[category]
    prefix = config["prefix"]
    clip_id = get_next_id(prefix)
    
    # Pick voice ID if not specified
    selected_voice_id = voice_id or random.choice(VOICE_IDS)
    voice_name = get_voice_name(selected_voice_id)

    text = custom_text or generate_script_text(category)
    clip_dir = SCRIPTS_DIR / clip_id
    clip_dir.mkdir(parents=True, exist_ok=True)
    script_file = clip_dir / f"{clip_id}.json"
    audio_file = clip_dir / f"{clip_id}.mp3"
    
    meta = {
        "id": clip_id,
        "category": category,
        "prefix": prefix,
        "text": text,
        "audio_file": f"vault/scripts/{clip_id}/{clip_id}.mp3",
        "audio_url": f"/vault/scripts/{clip_id}/{clip_id}.mp3",
        "voice_id": selected_voice_id,
        "voice_name": voice_name,
        "model": OPENAI_MODEL,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    if dry_run:
        print(f"  [Dry Run] Would create {script_file.name} in {clip_dir.name}/ using {voice_name} ({selected_voice_id})")
        print(f"            Text: {text}")
        return clip_id

    # Write script JSON
    with open(script_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    print(f"  [Script Saved] {clip_dir.name}/{script_file.name} (Voice: {voice_name})")

    # Synthesize Audio
    synthesize_audio_elevenlabs(text, audio_file, selected_voice_id)

    return clip_id

def commit_vault(message: str = "feat(vault): update Chadodoro voice clips"):
    """Stage and commit vault assets to Git."""
    try:
        subprocess.run(["git", "add", "public/vault"], cwd=BASE_DIR, check=True)
        status = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=BASE_DIR)
        if status.returncode != 0:
            subprocess.run(["git", "commit", "-m", message], cwd=BASE_DIR, check=True)
            print(f"✅ Vault committed to Git: '{message}'")
        else:
            print("ℹ️ No new changes to commit in public/vault.")
    except Exception as e:
        print(f"❌ Git commit failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Chadodoro Voice Vault Generator")
    parser.add_argument("--category", choices=["all", "START_FOCUS", "TOUCH_GRASS", "LONG_BREAK", "CHAD_MOTIVATION"], default="all", help="Category to generate")
    parser.add_argument("--count", type=int, default=1, help="Number of clips per category")
    parser.add_argument("--voice-id", type=str, default=None, help="Explicit ElevenLabs Voice ID override")
    parser.add_argument("--commit", action="store_true", help="Stage and commit generated clips to Git")
    parser.add_argument("--dry-run", action="store_true", help="Preview generation without writing files")
    args = parser.parse_args()

    categories = [args.category] if args.category != "all" else list(CATEGORY_CONFIG.keys())
    generated_ids = []

    print(f"👑 Chadodoro Voice Vault Generator Starting...")
    print(f"   Model: {OPENAI_MODEL} @ {OPENAI_BASE_URL}")
    print(f"   GigaChad Voices Configured: {len(VOICE_IDS)}")
    for vid in VOICE_IDS:
        print(f"     - {vid} ({get_voice_name(vid)})")
    print(f"   Categories: {', '.join(categories)} (Count: {args.count})")

    # Generate across categories and cycle voices
    voice_idx = 0
    for cat in categories:
        print(f"\n⚡ Generating category: {cat}")
        for i in range(args.count):
            chosen_voice = args.voice_id or VOICE_IDS[voice_idx % len(VOICE_IDS)]
            clip_id = generate_clip(cat, voice_id=chosen_voice, dry_run=args.dry_run)
            generated_ids.append(clip_id)
            voice_idx += 1

    # Sync manifest
    if not args.dry_run:
        from sync_manifest import sync_manifest
        sync_manifest()

    if args.commit and not args.dry_run:
        commit_vault(f"feat(vault): add {len(generated_ids)} clips across {len(VOICE_IDS)} GigaChad voices")

    print("\n🏆 Vault Generation Complete!")

if __name__ == "__main__":
    main()
