# 👑 Chadodoro (`pomodoro-chad`)
> **The Uncompromising GigaChad Pomodoro + Zero-Latency Git Voice Vault**  
> *Hacktoberfest 2026 Open-Source AI Challenge — Week 1: "Touch Grass"*

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ntsd/pomodoro-chad)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-chadodoro.ntsd.dev-10b981?style=flat-square&logo=render&logoColor=white)](https://chadodoro.ntsd.dev/)
[![DEV Submission](https://img.shields.io/badge/DEV%20Challenge-Touch%20Grass%20Week%201-0a0a0a?style=flat-square&logo=devdotto&logoColor=white)](BLOG_POST.md)

🌐 **Live Production App:** [https://chadodoro.ntsd.dev/](https://chadodoro.ntsd.dev/)  
📝 **DEV Challenge Write-Up:** [BLOG_POST.md](BLOG_POST.md) (Submission for [Hacktoberfest Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05))

---

## 🌿 1. Overview & "Touch Grass" Theme

Modern developers suffer from infinite screen-lock, chronic desk posture, and doom-scrolling. **Chadodoro** cures this with an unapologetic, stoic GigaChad productivity coach.

- **Lock In for Deep Work:** Focus sessions demand unbroken discipline. No tabs, no distractions, only execution.
- **Grass Counter Tracker:** Log each real-world outdoor session with the tactile **"I Touched Grass"** button with haptic chime and floating grass confetti.

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
                            ┌──────────────────────────────────────────────┐
                            │           PUBLIC GIT VOICE VAULT             │
                            │  public/vault/manifest.json                  │
                            │  public/vault/scripts/<id>/<id>.{json,mp3}   │
                            │  public/vault/themes/<id>/<id>.{json,mp3}    │
                            └──────────────────────────────────────────────┘
                                              │
                     ═════════════════════════╪═══════════════════════════
                                              │ (Committed to Git)
                  ┌───────────────────────────┴────────────────────────────┐
                  │                     RUNTIME (RENDER)                   │
                  │   - 100% Static HTML / CSS / JS (Astro)                │
                  │   - 0ms API Latency                                    │
                  │   - Zero Runtime Secrets / Zero API Costs              │
                  │   - Edge Cached Audio Assets (/vault/*)                │
                  │   - Native Web Speech API Fallback                     │
                  └────────────────────────────────────────────────────────┘
```

1. **Open-Weight AI Brain:** Script generation is driven by `google/gemma-4-26B-A4B-it` hosted on an open-weights inference node (`https://spark.ntsd.dev:8001/v1`).
2. **ElevenLabs Baritone Voice Synthesis:** Transcripts are pre-synthesized by **ElevenLabs** using multiple deep baritone voices (Adam, Harry, Brian).
3. **Committed Directly to Git:** Generated `.json` metadata and `.mp3` audio files are committed directly into Git under `public/vault/`.
4. **Zero Runtime API Dependency:** The Astro static site serves vault assets locally from `dist/vault/` with instant zero-latency playback and zero runtime API bills.

---

## 🎨 3. Key Features

- **Circular Countdown Progress Ring:** Athletic SVG ring displaying `MM:SS` with animated stroke dashoffset.
- **Three Distinct Reactive Avatar States:**
  - *Focus Mode (Lock In):* Cyberpunk deep-work GigaChad with neon emerald laser eyes, reticle lines, and focused aura.
  - *Short Break (Hydrate & Rest):* Indoor warm acoustic lounge GigaChad taking a mindful breath, holding a steaming Chad crown ceramic coffee mug with golden ambient lighting.
  - *Long Break (Touch Grass):* Outdoor sunny meadow GigaChad wearing aviator sunglasses, gently caressing lush green grass stalks.
- **Voice Coach Pre-Synthesized by ElevenLabs:**
  - 16 high-impact coaching lines across `START_FOCUS`, `SHORT_BREAK`, `LONG_BREAK`, and `CHAD_MOTIVATION`.
  - Replayable on-demand via the **CHADODORO COACH** card.
- **Hybrid Anthem BGM Engine (YouTube + Git Vault):**
  - Curated library of 27 viral phonk and motivation tracks on YouTube (including *REVENGE*, *MONTAGEM PEGADORA*, *GigaChad Theme Phonk House*, *MOTIVATION FUNK*, *METAMORPHOSIS*, *DIA DELÍCIA*, *PARA COMEÇAR O FINAL DE SEMANA*, *AURA*, etc.) with precise start timestamps.
  - **Live Song Attribution & Direct Link:** Both the *Now Playing* banner and the *CHADODORO COACH* card display the active song title with direct links to the YouTube video.
  - **30s Burst or Continuous Play:** By default, anthems play for 30s as a high-intensity phase transition, with a **"Keep Song Running"** toggle in Settings for continuous background music.
  - **Anthem Audio Source Selector (Dropdown):** Choose between **Vault Audio Only** (100% ad-free static Git Vault `.mp3` tracks), **Youtube Only** (curated viral phonk & meme tracks), or **Hybrid** (prioritizes YouTube tracks with Git Vault themes as backup).
  - Independent Anthem toggle, volume control, and shuffle per timer phase.
- **Audio Waveform Visualizer:** Animated speech bars synchronize with coach audio and anthem playback.
- **"I Touched Grass" Soundboard:** Tactile button increments user grass counter, triggers floating grass/clover confetti, and plays audio feedback.
- **Instant Motivation Button:** Soundboard trigger for stoic motivation one-liners anytime.
- **Web Speech API Fallback:** If audio files fail to load or offline, browser synthetic baritone voice takes over.
- **Customizable Settings Modal:** Configurable focus (default 25m), short break (5m), long break (15m), volume slider, auto-start breaks, keep song running, anthem audio source selector (Vault Only / YouTube Only / Hybrid), and stats reset.
- **Keyboard Shortcuts:**
  - <kbd>Space</kbd>: Start / Pause
  - <kbd>R</kbd>: Reset timer
  - <kbd>S</kbd>: Skip phase
  - <kbd>V</kbd>: Toggle GigaChad Voice Coach
  - <kbd>B</kbd>: Toggle GigaChad Anthem BGM
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
│   │   ├── Avatar.astro      # Three distinct reactive SVG avatars (Focus, Lounge, Touch Grass)
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
│       ├── scripts/          # Grouped voice coaching folders (<id>/<id>.json & <id>.mp3)
│       │   ├── focus_001/
│       │   ├── break_touch_grass_001/
│       │   ├── long_break_001/
│       │   └── motivation_001/
│       └── themes/           # Grouped instrumental meme themes (<id>/<id>.json & <id>.mp3)
│           ├── theme_focus_01/
│           ├── theme_break_01/
│           ├── theme_long_break_01/
│           └── theme_motivation_01/
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

# Generate specifically for SHORT_BREAK category
python3 scripts/generate_vault.py --category SHORT_BREAK --count 2

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
      - path: /vault/*
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
4. Vault assets under `/vault/*` are cached immutably at the edge with HTTP Cache-Control headers for instant streaming.

---

## 🏆 8. Hacktoberfest 2026 Week 1 Challenge Summary

| Criterion / Track | Implementation & Technology |
|---|---|
| **Theme: "Touch Grass"** | Forces outdoor long breaks, 3 reactive avatars (Focus, Lounge Hydrate, Meadow Grass), tactile "I Touched Grass" soundboard counter & clover confetti |
| **Open-Source AI Core** | Transcripts created with open-weight `google/gemma-4-26B-A4B-it` via self-hosted OpenAI-compatible inference endpoint |
| **Partner Track: Best Use of ElevenLabs** | 16 high-impact baritone coach clips synthesized via **ElevenLabs** (Adam, Harry, Brian) and baked into zero-latency Git Voice Vault |
| **Partner Track: Best Use of Render** | Automated 1-click deployment via [`render.yaml`](render.yaml) with custom immutable edge cache headers (`max-age=31536000, immutable`) |
| **Partner Track: Best Use of Gemma** | Automated voice script generation pipeline utilizing `google/gemma-4-26B-A4B-it` for stoic motivation prompts |
| **Architecture** | 100% Client-Side Static Astro app with 0ms runtime API latency, 0 runtime keys, 0 API costs |
| **Submission Write-Up** | Full DEV post available at [`BLOG_POST.md`](BLOG_POST.md) |

---

*“Discipline equals freedom, King. Step outside and touch physical grass.”* 👑🌱
