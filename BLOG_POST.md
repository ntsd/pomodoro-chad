---
title: "Chadodoro: The Stoic GigaChad Pomodoro Coach That Forces You to Touch Physical Grass"
published: false
tags: devchallenge, hf26challenge, elevenlabs, opensource
canonical_url: https://chadodoro.ntsd.dev/
cover_image: https://chadodoro.ntsd.dev/favicon.svg
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

---

## What I Built

Modern developers face an epidemic of infinite screen-lock: sitting motionless in dark rooms, doom-scrolling Reddit and Twitter during "breaks," and accumulating chronic desk fatigue. We tell ourselves we are resting, but our eyes remain glued to 120Hz glass panels.

**Chadodoro** (`pomodoro-chad`) was built to break this cycle. It is an unapologetic, athletic productivity coach inspired by the stoic GigaChad ethos, engineered around a single physical mandate: **when your work interval ends, you step away from the monitors and touch physical grass.**

### Key Features

1. **Circular Countdown Progress Ring:** Athletic SVG countdown ring displaying `MM:SS` with animated stroke dashoffset, instant phase indicators, and reactive glow.
2. **Three Reactive Reactive Avatars:**
   - **Focus Mode (Lock In):** Cyberpunk deep-work GigaChad with neon emerald laser eyes, HUD reticle targeting lines, and unbroken focus aura.
   - **Short Break (Hydrate & Rest):** Warm acoustic lounge GigaChad taking a mindful breath, holding a steaming ceramic Chad crown mug in golden ambient light.
   - **Long Break (Touch Grass):** Outdoor sunny meadow GigaChad wearing aviator sunglasses, gently caressing lush green grass stalks under natural sunlight.
3. **Voice Coach Pre-Synthesized by ElevenLabs:** 16 high-impact coaching lines across `START_FOCUS`, `SHORT_BREAK`, `LONG_BREAK`, and `CHAD_MOTIVATION`, delivered in a commanding baritone voice and replayable on-demand via the soundboard.
4. **"I Touched Grass" Physical Tracker:** Tactile soundboard button that increments your real-world grass counter, triggers floating clover and grass confetti, and plays audio feedback.
5. **Hybrid Anthem BGM Engine (YouTube + Git Vault):** Curated library of 27 viral phonk and motivation tracks (including *REVENGE*, *MONTAGEM PEGADORA*, *GigaChad Theme Phonk House*, *MOTIVATION FUNK*, *METAMORPHOSIS*, *DIA DELÍCIA*, *AURA*) with precise start timestamps. Choose between 30s phase-change bursts or continuous play, and switch between Vault Audio Only, YouTube Only, or Hybrid mode.
6. **Live Song Attribution & Direct Links:** Real-time track display with direct links to original artists on YouTube.
7. **The Chadodoro Code:** Three non-negotiable principles displayed on the dashboard:
   - *01 Unbroken Focus:* Single-task deep work with zero tab switching.
   - *02 Radical Screen Break:* Hands off the keyboard and eyes away from screens.
   - *03 Touch Physical Grass:* Reconnecting with sunlight, earth, and fresh air.

---

## Demo

- 🌐 **Live Interactive Web App:** [https://chadodoro.ntsd.dev/](https://chadodoro.ntsd.dev/)
- ⚡ **Zero Setup / Zero Latency:** Instant load directly in any modern browser, fully functional on mobile and desktop.

```
┌────────────────────────────────────────────────────────┐
│  👑 CHADODORO — LOCK IN & TOUCH GRASS                  │
│                                                        │
│  [ AVATAR: GigaChad Laser Eyes / Meadow Aviators ]     │
│                                                        │
│                     ( 25:00 )                          │
│            [ START ]  [ RESET ]  [ SKIP ]              │
│                                                        │
│  CHADODORO COACH: "Lock in, King. Disconnect the noise"│
│  NOW PLAYING: 🎵 GigaChad Theme (Phonk House Version)  │
│                                                        │
│  🌱 Real Grass Touched: [ 42 ] [ + TOUCH GRASS ]       │
└────────────────────────────────────────────────────────┘
```

---

## Code

The entire codebase is open-source under the permissive MIT License:

- 🐙 **GitHub Repository:** [https://github.com/ntsd/pomodoro-chad](https://github.com/ntsd/pomodoro-chad)
- 🚀 **1-Click Deploy Blueprint:** Includes native `render.yaml` for instant deployment on Render.

---

## How I Built It

### Architecture: Zero-Latency Static Git Voice Vault

Traditional AI web applications make expensive, high-latency API calls to LLMs and speech synthesis services on every user interaction. This introduces loading spinners, billing unpredictable costs, and network vulnerabilities.

Chadodoro completely decouples AI synthesis from user runtime:

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

1. **Open-Source AI Core:** Coaching lines are generated at pipeline time by `google/gemma-4-26B-A4B-it` hosted on an open-weight inference node (`https://spark.ntsd.dev:8001/v1`).
2. **ElevenLabs Audio Synthesis:** The generated transcripts are synthesized into punchy, resonant baritone speech using ElevenLabs API (voices Adam, Harry, Brian).
3. **Committed into Git:** Both the transcript metadata (`.json`) and compressed audio (`.mp3`) are committed directly to `public/vault/` alongside `manifest.json`.
4. **Static Astro Delivery:** Built with Astro and pure vanilla CSS/JS. Assets are pre-rendered into `dist/` and served with zero server-side compute.
5. **Edge Caching on Render:** Deployed as a static site on Render with custom immutable cache headers (`Cache-Control: public, max-age=31536000, immutable`) for instant audio streaming.

---

## Why Does Open Innovation Matter?

1. **Zero Runtime API Dependency & Cost Freedom:** By combining an open-weight model (`google/gemma-4-26B-A4B-it`) with a Git-based artifact vault, the application runs forever with **0 API bills** and **0 runtime keys exposed**. Anyone can fork the repository and host it without an API key or credit card.
2. **Local Privacy & Self-Sovereignty:** All timer data, grass counter metrics, and audio preferences live in browser `localStorage`. No user tracking, no backend database, and no telemetry.
3. **Reproducibility & Customization:** Developers can run `scripts/generate_vault.py` with their own local or self-hosted LLM endpoints (Ollama, vLLM, sparkrun) to generate new personas, voice scripts, and motivational quotes.

---

## My Agent Session

All coach transcripts and stoic motivational lines were generated by running **Gemma** (`google/gemma-4-26B-A4B-it`) through an automated pipeline workflow:
- **Stoic Persona Prompting:** Gemma was prompted with strict character constraints: uncompromising discipline, high-impact brevity, tough-love accountability, and mandatory real-world outdoors/grass reminders.
- **Structured Content Generation:** Gemma parsed phase contexts (`START_FOCUS`, `SHORT_BREAK`, `LONG_BREAK`, `CHAD_MOTIVATION`) to produce structured transcript metadata and text.
- **Automated Pipeline Integration:** The Gemma outputs were automatically fed into `scripts/generate_vault.py` to synthesize audio clips, validate duration thresholds, and compile `manifest.json`.

---

## Prize Categories

### 🎙️ Best Use of ElevenLabs
Chadodoro utilizes ElevenLabs' speech synthesis to give the GigaChad coach an authoritative, ultra-realistic baritone voice. 16 distinct audio assets across 4 timer phases were synthesized using ElevenLabs voices (Adam, Harry, Brian) and baked into the Git Voice Vault. The app triggers these clips on phase transitions and features an instant replay soundboard.

### 🚀 Best Use of Render
The application is deployed on Render via a declarative [`render.yaml`](file:///home/ntsd/git/ntsd/pomodoro-chad/render.yaml) blueprint. Render builds the Astro static bundle and serves both the single-page application and static audio assets with custom HTTP Cache-Control headers (`public, max-age=31536000, immutable`), ensuring sub-millisecond edge response times worldwide.

### 🧠 Best Use of Gemma
Motivational scripts and Stoic Touch Grass reminders were generated using the open-weight `google/gemma-4-26B-A4B-it` model running on an OpenAI-compatible self-hosted inference cluster, demonstrating how open-weight LLMs can drive automated creative production pipelines.

---

*“Discipline equals freedom, King. Step outside and touch physical grass.”* 👑🌱
