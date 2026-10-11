# 👑 Chadodoro (`pomodoro-chad`)
> **The Uncompromising GigaChad Pomodoro + Zero-Latency Git Voice Vault**  
> *Hacktoberfest 2026 Open-Source AI Challenge — Week 1: "Touch Grass"*

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ntsd/pomodoro-chad)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-chadodoro.ntsd.dev-10b981?style=flat-square&logo=render&logoColor=white)](https://chadodoro.ntsd.dev/)

🌐 **Live Production App:** [https://chadodoro.ntsd.dev/](https://chadodoro.ntsd.dev/)

---

## 🌿 1. Overview & "Touch Grass" Theme

Modern developers suffer from infinite screen-lock, chronic desk posture, and doom-scrolling. **Chadodoro** cures this with an unapologetic, stoic GigaChad productivity coach.

- **Lock In for Deep Work:** Focus sessions demand unbroken discipline. No tabs, no distractions, only execution.
- **Radical Screen Breaks:** When the timer strikes zero, Chadodoro aggressively orders you away from screens. Close the laptop, step outside, breathe oxygen, hydrate with cold water, and **violently touch physical grass**.
- **Progressive Chad Ranks:** Log each real-world outdoor session with the **"I Touched Grass"** button to ascend from *Screen Goblin* to *Ascended Earth Titan*.

---

## ⚡ 2. Architecture: Zero-Latency Static Git Voice Vault

Traditional AI applications make expensive, high-latency API calls whenever an event triggers. **Chadodoro completely decouples AI generation from user runtime:**

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 BUILD / PIPELINE TIME                  │
                  └────────────────────────────────────────────────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
         [Open-Source AI Brain]                              [Voice Synthesis]
      google/gemma-4-26B-A4B-it                             ElevenLabs API
    (spark.ntsd.dev:8001/v1)                               (Adam - Deep Baritone)
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              │
                                              ▼
                                 [scripts/generate_vault.py]
                                              │
                                              ▼
                            ┌───────────────────────────────────┐
                            │      PUBLIC GIT VOICE VAULT       │
                            │  public/vault/manifest.json       │
                            │  public/vault/scripts/*.json      │
                            │  public/vault/audio/*.mp3         │
                            └───────────────────────────────────┘
                                              │
                     ═════════════════════════╪═══════════════════════════
                                              │ (Committed to Git)
                  ┌───────────────────────────┴────────────────────────────┐
                  │                     RUNTIME (RENDER)                   │
                  │   - 100% Static HTML / CSS / JS (Astro)                │
                  │   - 0ms API Latency                                    │
                  │   - Zero Runtime Secrets / Zero API Costs              │
                  │   - Edge Cached Audio Assets (/vault/audio/*)          │
                  │   - Native Web Speech API Fallback                     │
                  └────────────────────────────────────────────────────────┘
```

1. **Open-Weight AI Brain:** Script generation is driven by `google/gemma-4-26B-A4B-it` hosted on an open-weights inference node (`https://spark.ntsd.dev:8001/v1`).
2. **Deep Baritone Voice Synthesis:** Transcripts are synthesized via ElevenLabs using Adam's commanding baritone voice (`pNInz6obpgDQGcFmaJgB`).
3. **Committed to Git:** Generated `.json` metadata and `.mp3` audio files are committed directly into Git under `public/vault/`.
4. **Zero Runtime API Dependency:** The Astro static site serves vault assets locally from `dist/vault/` with instant zero-latency playback.

---

## 🎨 3. Key Features

- **Circular Countdown Progress Ring:** Athletic SVG ring displaying `MM:SS` with animated stroke dashoffset.
- **Dual Reactive Avatar States:**
  - *Focus Mode:* Stoic GigaChad silhouette with laser-focused emerald aura and jawline contours.
  - *Break Mode ("Touch Grass"):* GigaChad standing outdoors in a sunlit meadow touching physical emerald grass blades.
- **Audio Waveform Visualizer:** Animated speech bars synchronize with coach audio playback.
- **"I Touched Grass" Soundboard:** Tactile button increments user grass counter, triggers floating grass/clover confetti, and calculates Chad ranks:
  - `0 - 4`: Screen Goblin 💻
  - `5 - 14`: Sprout Wanderer 🌱
  - `15 - 29`: Sunlight Walker ☀️
  - `30 - 49`: Meadow Chad 🌿
  - `50+`: Ascended Earth Titan 👑
- **Instant Motivation Button:** Soundboard trigger for stoic motivation one-liners anytime.
- **Web Speech API Fallback:** If audio files fail to load or offline, browser synthetic baritone voice takes over.
- **Customizable Settings Modal:** Configurable focus (default 25m), short break (5m), long break (15m), volume slider, auto-start breaks, and stats reset.
- **Keyboard Shortcuts:**
  - <kbd>Space</kbd>: Start / Pause
  - <kbd>R</kbd>: Reset timer
  - <kbd>S</kbd>: Skip phase
  - <kbd>M</kbd>: Instant Motivation
  - <kbd>G</kbd>: I Touched Grass
  - <kbd>Esc</kbd>: Close settings

---

## 📂 4. Repository & Directory Layout

```
pomodoro-chad/
├── .env.example              # Environment variables template
├── astro.config.mjs          # Astro static site configuration
├── package.json              # NPM dependencies & scripts
├── render.yaml               # Render static site blueprint with cache headers
├── src/
│   ├── layouts/
│   │   └── Layout.astro      # Master layout with header stats & footer
│   ├── components/
│   │   ├── Timer.astro       # Circular countdown ring & main controls
│   │   ├── Avatar.astro      # Dual reactive SVG states (Focus vs Grass)
│   │   ├── QuoteDisplay.astro# Coach transcript & audio replay card
│   │   └── SettingsModal.astro # Durations, volume, and preferences modal
│   ├── styles/
│   │   └── global.css        # Athletic dark theme design tokens & animations
│   ├── pages/
│   │   └── index.astro       # Main dashboard layout
│   └── scripts/
│       └── timerController.js# Pomodoro engine, audio controller, local storage
├── scripts/
│   ├── requirements.txt      # Python dependencies (openai, requests, dotenv, numpy)
│   ├── generate_vault.py     # LLM + ElevenLabs multi-voice generation pipeline
│   ├── generate_themes.py    # Pure instrumental GigaChad anthems generator
│   └── sync_manifest.py      # Manifest compiler
├── public/
│   ├── favicon.svg           # Crown & emerald blade SVG favicon
│   └── vault/
│       ├── manifest.json     # Compiled audio clip & theme registry
│       ├── scripts/          # Clip metadata JSON files
│       └── audio/            # Voice clips and pure instrumental theme MP3s
│           ├── focus_001.mp3 ... focus_004.mp3
│           ├── break_touch_grass_001.mp3 ...
│           ├── theme_focus_01.mp3 ... theme_focus_03.mp3
│           ├── theme_break_01.mp3 ... theme_break_03.mp3
│           ├── theme_long_break_01.mp3 ... theme_long_break_02.mp3
│           └── theme_motivation_01.mp3 ... theme_motivation_02.mp3
└── README.md
```

---

## 🛠️ 5. Local Development

### Prerequisites
- Node.js `v18+` (or `v20+`)
- Python `3.10+` (optional, for vault generation pipeline)

### 1. Clone & Install Frontend
```bash
git clone https://github.com/ntsd/pomodoro-chad.git
cd pomodoro-chad
npm install
```

### 2. Run Astro Local Dev Server
```bash
npm run dev
```
Open [http://localhost:4321](http://localhost:4321) in your browser.

### 3. Build Static Bundle
```bash
npm run build
```
Generates production-ready static assets into `dist/`.

---

## 🎙️ 6. Git Voice Vault Generation Pipeline

To generate additional coaching clips or regenerate the static voice vault:

### 1. Setup Python Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

### 2. Configure `.env`
Create a `.env` in the repository root:
```env
ELEVENLABS_API_KEY="your-elevenlabs-api-key"
ELEVENLABS_VOICE_ID="pNInz6obpgDQGcFmaJgB"
OPENAI_BASE_URL="https://spark.ntsd.dev:8001/v1"
OPENAI_API_KEY=""
OPENAI_MODEL="google/gemma-4-26B-A4B-it"
```

### 3. Run Generator
```bash
# Generate 1 clip for each category
python3 scripts/generate_vault.py --count 1

# Generate specifically for TOUCH_GRASS category
python3 scripts/generate_vault.py --category TOUCH_GRASS --count 2

# Preview generation without writing files
python3 scripts/generate_vault.py --dry-run

# Generate and automatically stage & commit to Git
python3 scripts/generate_vault.py --count 1 --commit
```

### 4. Sync Manifest
```bash
python3 scripts/sync_manifest.py
```

### 5. Generate Pure Instrumental Anthems (BGM)
```bash
python3 scripts/generate_themes.py
```
Synthesizes 10 pure instrumental multi-track themes (Phonk, Synthwave, Meadow Lo-Fi, Chillstep) across `focus`, `break`, `long_break`, and `motivation`. Pure instrumentals are completely decoupled from voice coach lines, allowing separate enabling, disabling, and volume adjustment.

---

## 🚀 7. Deployment to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ntsd/pomodoro-chad)

🌐 **Live Application:** [https://chadodoro.ntsd.dev/](https://chadodoro.ntsd.dev/)

This repository includes a native [`render.yaml`](render.yaml) blueprint:

```yaml
services:
  - type: web
    name: pomodoro-chad
    env: static
    buildCommand: npm install && npm run build
    staticPublishPath: ./dist
    headers:
      - path: /vault/audio/*
        name: Cache-Control
        value: public, max-age=31536000, immutable
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
```

### 1-Click Deploy:
1. Click the **Deploy to Render** button above or connect your GitHub repository in Render.
2. Render detects the [`render.yaml`](render.yaml) blueprint automatically.
3. Render automatically builds with `npm install && npm run build` and serves static assets from `dist/`.
4. Audio clips under `/vault/audio/*` are cached immutably at the edge with HTTP Cache-Control headers for instant streaming.

---

## 🏆 8. Hacktoberfest 2026 Week 1 Challenge Summary

| Criterion | Implementation |
|---|---|
| **Theme: "Touch Grass"** | Core timer forces outdoor breaks, displays lush meadow Chad avatar, tracks real-world grass touched counter |
| **Open-Source AI Core** | Transcripts created with open-weight `google/gemma-4-26B-A4B-it` via OpenAI-compatible endpoint |
| **Zero-Latency Static Vault** | ElevenLabs clips committed directly to Git under `public/vault/`, 0 runtime API calls |
| **Static Framework** | Astro Static Output (`dist`), zero servers required |
| **Deployment Target** | Render Static Site with immutable edge cache headers |

---

*“Discipline equals freedom, King. Step outside and touch physical grass.”* 👑🌱
