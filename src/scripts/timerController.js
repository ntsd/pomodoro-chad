// src/scripts/timerController.js
/**
 * Chadodoro Client Controller
 * Manages Pomodoro countdown, Git Voice Vault playback, Avatar reactive states,
 * Grass-touched tracker, and Web Speech API baritone fallback.
 */

class ChadodoroController {
  constructor() {
    this.manifest = null;
    this.audioPlayer = new Audio();
    this.bgmPlayer = new Audio('/vault/themes/theme_focus_01/theme_focus_01.mp3');
    this.bgmPlayer.loop = false;
    this.currentClip = null;
    
    // Default Settings
    this.settings = {
      focusMinutes: 25,
      breakMinutes: 5,
      longBreakMinutes: 15,
      longBreakInterval: 4,
      voiceEnabled: true,
      volume: 90,
      bgmEnabled: true,
      bgmVolume: 35,
      repeatTheme: false,
      autoStartBreak: false,
      autoStartFocus: false,
      speechFallback: true
    };

    // State
    this.mode = 'focus'; // 'focus' | 'break' | 'long_break'
    this.isRunning = false;
    this.timeRemaining = this.settings.focusMinutes * 60;
    this.totalDuration = this.timeRemaining;
    this.timerInterval = null;
    this.cyclesCompleted = 0;
    this.grassCount = 0;

    this.init();
  }

  async init() {
    this.loadStorage();
    await this.fetchManifest();
    this.cacheDom();
    this.bindEvents();
    this.applySettingsToUI();
    this.updateDisplay();
    this.updateAvatarState();
    this.updateGrassDisplay();
    this.updateVoiceUI();
    this.updateBgmVolume();
    this.updateBgmUI();
    this.bgmPlayer.loop = !!this.settings.repeatTheme;

    // Set initial audio volume
    this.audioPlayer.volume = this.settings.volume / 100;
  }

  loadStorage() {
    try {
      const savedSettings = localStorage.getItem('chad_settings');
      if (savedSettings) {
        this.settings = { ...this.settings, ...JSON.parse(savedSettings) };
      }
      const savedGrass = localStorage.getItem('chad_grass_touched');
      if (savedGrass) {
        this.grassCount = parseInt(savedGrass, 10) || 0;
      }
      const savedCycles = localStorage.getItem('chad_cycles');
      if (savedCycles) {
        this.cyclesCompleted = parseInt(savedCycles, 10) || 0;
      }
    } catch (e) {
      console.warn("Storage load error:", e);
    }
  }

  saveStorage() {
    try {
      localStorage.setItem('chad_settings', JSON.stringify(this.settings));
      localStorage.setItem('chad_grass_touched', this.grassCount.toString());
      localStorage.setItem('chad_cycles', this.cyclesCompleted.toString());
    } catch (e) {
      console.warn("Storage save error:", e);
    }
  }

  async fetchManifest() {
    try {
      const res = await fetch('/vault/manifest.json');
      if (res.ok) {
        this.manifest = await res.json();
        console.log(`[Chad Voice Vault] Loaded ${this.manifest.total_clips} clips from static manifest.`);
      } else {
        throw new Error(`HTTP ${res.status}`);
      }
    } catch (e) {
      console.warn("[Chad Voice Vault] Manifest unavailable, will use synthetic fallback:", e);
    }
  }

  cacheDom() {
    // Timer DOM
    this.domTime = document.getElementById('timer-time-display');
    this.domProgress = document.getElementById('timer-progress-circle');
    this.domModeTag = document.getElementById('timer-mode-tag');
    this.domCycleText = document.getElementById('cycle-text-display');
    this.domBtnToggle = document.getElementById('btn-timer-toggle');
    this.domToggleLabel = document.getElementById('btn-toggle-label');
    this.domIconPlay = document.getElementById('icon-play');
    this.domIconPause = document.getElementById('icon-pause');
    this.domBtnReset = document.getElementById('btn-timer-reset');
    this.domBtnSkip = document.getElementById('btn-timer-skip');

    // Tabs
    this.domTabFocus = document.getElementById('tab-focus');
    this.domTabBreak = document.getElementById('tab-break');
    this.domTabLongBreak = document.getElementById('tab-long-break');

    // Cycle Dots
    this.domDots = [
      document.getElementById('dot-0'),
      document.getElementById('dot-1'),
      document.getElementById('dot-2'),
      document.getElementById('dot-3')
    ];

    // Avatar DOM
    this.domAvatarFocus = document.getElementById('avatar-focus');
    this.domAvatarBreak = document.getElementById('avatar-break');
    this.domAvatarLongBreak = document.getElementById('avatar-long-break');
    this.domAvatarGlow = document.getElementById('avatar-ring-glow');
    this.domAvatarSpeech = document.getElementById('avatar-speech-status');
    this.domSpeechLabel = document.getElementById('speech-label');

    // Quote DOM
    this.domQuoteText = document.getElementById('quote-text-content');
    this.domQuoteBadge = document.getElementById('quote-category-badge');
    this.domQuoteClipId = document.getElementById('quote-clip-id');
    this.domQuoteVoiceTag = document.getElementById('quote-voice-tag');
    this.domBtnReplay = document.getElementById('btn-quote-replay');

    // Grass & Motivation
    this.domBtnGrass = document.getElementById('btn-touch-grass');
    this.domGrassDisplay = document.getElementById('grass-count-display');
    this.domSettingsGrassCount = document.getElementById('settings-grass-count');
    this.domHeaderGrassCount = document.getElementById('header-grass-count');
    this.domBtnMotivation = document.getElementById('btn-instant-motivation');

    // Settings Modal DOM
    this.domSettingsModal = document.getElementById('settings-modal');
    this.domBtnOpenSettings = document.getElementById('btn-open-settings');
    this.domBtnCloseSettings = document.getElementById('btn-close-settings');
    this.domBtnCancelSettings = document.getElementById('btn-cancel-settings');
    this.domSettingsForm = document.getElementById('settings-form');
    this.domInputVolume = document.getElementById('setting-volume');
    this.domVolumeValDisplay = document.getElementById('volume-val-display');
    this.domBtnResetGrass = document.getElementById('btn-reset-grass');

    // BGM & Voice Controls DOM
    this.domBtnToggleVoice = document.getElementById('btn-toggle-voice');
    this.domHeaderVoiceStatus = document.getElementById('header-voice-status');
    this.domInputVoiceEnabled = document.getElementById('setting-voice-enabled');
    this.domBtnToggleBgm = document.getElementById('btn-toggle-bgm');
    this.domHeaderBgmStatus = document.getElementById('header-bgm-status');
    this.domInputBgmEnabled = document.getElementById('setting-bgm-enabled');
    this.domInputBgmVolume = document.getElementById('setting-bgm-volume');
    this.domBgmVolumeDisplay = document.getElementById('bgm-volume-val-display');
  }

  bindEvents() {
    // Controls
    if (this.domBtnToggle) this.domBtnToggle.addEventListener('click', () => this.toggleTimer());
    if (this.domBtnReset) this.domBtnReset.addEventListener('click', () => this.resetTimer());
    if (this.domBtnSkip) this.domBtnSkip.addEventListener('click', () => this.skipPhase());

    // Tabs
    if (this.domTabFocus) this.domTabFocus.addEventListener('click', () => this.setMode('focus'));
    if (this.domTabBreak) this.domTabBreak.addEventListener('click', () => this.setMode('break'));
    if (this.domTabLongBreak) this.domTabLongBreak.addEventListener('click', () => this.setMode('long_break'));

    // Replay Voice
    if (this.domBtnReplay) this.domBtnReplay.addEventListener('click', () => this.replayCurrentClip());

    // Grass & Motivation
    if (this.domBtnGrass) this.domBtnGrass.addEventListener('click', (e) => this.handleTouchGrass(e));
    if (this.domBtnMotivation) this.domBtnMotivation.addEventListener('click', () => this.handleInstantMotivation());

    // Audio Toggles
    if (this.domBtnToggleVoice) this.domBtnToggleVoice.addEventListener('click', () => this.toggleVoice());
    if (this.domBtnToggleBgm) this.domBtnToggleBgm.addEventListener('click', () => this.toggleBgm());

    // Settings Modal
    if (this.domBtnOpenSettings) this.domBtnOpenSettings.addEventListener('click', () => this.openSettings());
    if (this.domBtnCloseSettings) this.domBtnCloseSettings.addEventListener('click', () => this.closeSettings());
    if (this.domBtnCancelSettings) this.domBtnCancelSettings.addEventListener('click', () => this.closeSettings());
    if (this.domSettingsModal) {
      this.domSettingsModal.addEventListener('click', (e) => {
        if (e.target === this.domSettingsModal) this.closeSettings();
      });
    }

    if (this.domSettingsForm) {
      this.domSettingsForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.saveSettingsFromForm();
        this.closeSettings();
      });
    }

    if (this.domInputVolume) {
      this.domInputVolume.addEventListener('input', (e) => {
        const val = e.target.value;
        if (this.domVolumeValDisplay) this.domVolumeValDisplay.textContent = `${val}%`;
        this.settings.volume = parseInt(val, 10);
        this.audioPlayer.volume = this.settings.volume / 100;
      });
    }

    if (this.domBtnToggleBgm) {
      this.domBtnToggleBgm.addEventListener('click', () => this.toggleBgm());
    }

    if (this.domInputBgmVolume) {
      this.domInputBgmVolume.addEventListener('input', (e) => {
        const val = e.target.value;
        if (this.domBgmVolumeDisplay) this.domBgmVolumeDisplay.textContent = `${val}%`;
        this.settings.bgmVolume = parseInt(val, 10);
        this.updateBgmVolume();
      });
    }

    if (this.domBtnResetGrass) {
      this.domBtnResetGrass.addEventListener('click', () => {
        this.grassCount = 0;
        this.saveStorage();
        this.updateGrassDisplay();
        if (this.domSettingsGrassCount) this.domSettingsGrassCount.textContent = '0';
      });
    }

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
      // Ignore if user is inside an input
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

      if (e.code === 'Space') {
        e.preventDefault();
        this.toggleTimer();
      } else if (e.code === 'KeyR') {
        this.resetTimer();
      } else if (e.code === 'KeyS') {
        this.skipPhase();
      } else if (e.code === 'KeyM') {
        this.handleInstantMotivation();
      } else if (e.code === 'KeyG') {
        this.handleTouchGrass();
      } else if (e.code === 'KeyV') {
        this.toggleVoice();
      } else if (e.code === 'KeyB') {
        this.toggleBgm();
      } else if (e.code === 'Escape') {
        this.closeSettings();
      }
    });

    // Audio Visualizer synchronization
    this.audioPlayer.addEventListener('play', () => this.setSpeakingState(true));
    this.audioPlayer.addEventListener('ended', () => this.setSpeakingState(false));
    this.audioPlayer.addEventListener('pause', () => this.setSpeakingState(false));
    this.audioPlayer.addEventListener('error', (e) => {
      console.warn("Audio element error, falling back to Web Speech:", e);
      this.setSpeakingState(false);
      if (this.currentClip && this.settings.speechFallback) {
        this.speakFallback(this.currentClip.text);
      }
    });
  }

  toggleTimer() {
    if (this.isRunning) {
      this.pauseTimer();
    } else {
      this.startTimer();
    }
  }

  startTimer() {
    this.isRunning = true;
    this.updateToggleBtnUI();
    this.updateBgmPlayback();

    // If starting a fresh phase, play coach directive
    if (this.timeRemaining === this.totalDuration) {
      if (this.mode === 'focus') {
        this.playCategoryClip('START_FOCUS');
      } else if (this.mode === 'long_break') {
        this.playCategoryClip('TOUCH_GRASS');
      } else if (this.mode === 'break') {
        this.playCategoryClip('LONG_BREAK');
      }
    }

    this.timerInterval = setInterval(() => {
      if (this.timeRemaining > 0) {
        this.timeRemaining--;
        this.updateDisplay();
      } else {
        this.handlePhaseComplete();
      }
    }, 1000);
  }

  pauseTimer() {
    this.isRunning = false;
    clearInterval(this.timerInterval);
    this.updateToggleBtnUI();
    this.updateDocumentTitle();
    this.updateBgmPlayback();
  }

  resetTimer() {
    this.pauseTimer();
    const durationMins = this.getDurationForMode(this.mode);
    this.timeRemaining = durationMins * 60;
    this.totalDuration = this.timeRemaining;
    this.updateDisplay();
  }

  skipPhase() {
    this.pauseTimer();
    this.handlePhaseComplete(true);
  }

  handlePhaseComplete(isSkipped = false) {
    clearInterval(this.timerInterval);
    this.isRunning = false;

    if (this.mode === 'focus') {
      this.cyclesCompleted++;
      this.saveStorage();

      // Check if long break interval reached
      if (this.cyclesCompleted % this.settings.longBreakInterval === 0) {
        this.setMode('long_break');
        if (!isSkipped) this.playCategoryClip('TOUCH_GRASS');
      } else {
        this.setMode('break');
        if (!isSkipped) this.playCategoryClip('LONG_BREAK');
      }

      if (this.settings.autoStartBreak) {
        setTimeout(() => this.startTimer(), 1500);
      }
    } else {
      // End of break -> back to focus
      this.setMode('focus');
      if (!isSkipped) this.playCategoryClip('START_FOCUS');

      if (this.settings.autoStartFocus) {
        setTimeout(() => this.startTimer(), 1500);
      }
    }

    this.updateToggleBtnUI();
  }

  setMode(newMode) {
    this.mode = newMode;
    const durationMins = this.getDurationForMode(newMode);
    this.timeRemaining = durationMins * 60;
    this.totalDuration = this.timeRemaining;
    
    // Update active tab styles
    if (this.domTabFocus) this.domTabFocus.classList.toggle('active', newMode === 'focus');
    if (this.domTabBreak) this.domTabBreak.classList.toggle('active', newMode === 'break');
    if (this.domTabLongBreak) this.domTabLongBreak.classList.toggle('active', newMode === 'long_break');

    this.updateAvatarState();
    this.updateDisplay();
    this.updateToggleBtnUI();
    this.updateBgmPlayback();
  }

  getDurationForMode(mode) {
    switch (mode) {
      case 'focus': return this.settings.focusMinutes;
      case 'break': return this.settings.breakMinutes;
      case 'long_break': return this.settings.longBreakMinutes;
      default: return 25;
    }
  }

  updateDisplay() {
    const minutes = Math.floor(this.timeRemaining / 60);
    const seconds = this.timeRemaining % 60;
    const timeStr = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    
    if (this.domTime) this.domTime.textContent = timeStr;

    // Progress Ring Dashoffset
    if (this.domProgress && this.totalDuration > 0) {
      const circumference = 2 * Math.PI * 120; // ~753.98
      const progressFraction = (this.totalDuration - this.timeRemaining) / this.totalDuration;
      const offset = circumference * (1 - progressFraction);
      this.domProgress.style.strokeDashoffset = offset;

      // Ring stroke color
      if (this.mode === 'focus' || this.mode === 'long_break') {
        this.domProgress.setAttribute('stroke', 'url(#ringEmeraldGradient)');
      } else {
        this.domProgress.setAttribute('stroke', 'url(#ringBreakGradient)');
      }
    }

    // Mode Tag
    if (this.domModeTag) {
      if (this.mode === 'focus') {
        this.domModeTag.textContent = 'LOCK-IN FOCUS // DEEP WORK';
        this.domModeTag.style.color = 'var(--emerald-bright)';
      } else if (this.mode === 'break') {
        this.domModeTag.textContent = 'SHORT BREAK // QUICK RESET';
        this.domModeTag.style.color = '#fde047';
      } else {
        this.domModeTag.textContent = 'TOUCH GRASS // RADICAL RECOVERY';
        this.domModeTag.style.color = 'var(--emerald-bright)';
      }
    }

    // Cycle Dots & Round Text
    const currentRound = (this.cyclesCompleted % this.settings.longBreakInterval) + 1;
    if (this.domCycleText) {
      this.domCycleText.textContent = `ROUND ${currentRound} OF ${this.settings.longBreakInterval}`;
    }

    if (this.domDots) {
      const activeDots = this.cyclesCompleted % this.settings.longBreakInterval;
      this.domDots.forEach((dot, idx) => {
        if (dot) dot.classList.toggle('filled', idx < activeDots);
      });
    }

    this.updateDocumentTitle();
  }

  updateDocumentTitle() {
    const minutes = Math.floor(this.timeRemaining / 60);
    const seconds = this.timeRemaining % 60;
    const timeStr = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    let modeLabel = 'Lock In ⚡';
    if (this.mode === 'break') {
      modeLabel = 'Short Break ☕';
    } else if (this.mode === 'long_break') {
      modeLabel = 'Touch Grass 🌿';
    }
    const stateIcon = this.isRunning ? '▶' : '⏸';
    document.title = `${stateIcon} (${timeStr}) Chadodoro - ${modeLabel}`;
  }

  updateToggleBtnUI() {
    if (this.domIconPlay && this.domIconPause) {
      this.domIconPlay.classList.toggle('hidden', this.isRunning);
      this.domIconPause.classList.toggle('hidden', !this.isRunning);
    }
    if (this.domToggleLabel) {
      if (this.isRunning) {
        this.domToggleLabel.textContent = 'PAUSE';
      } else {
        if (this.mode === 'focus') {
          this.domToggleLabel.textContent = 'LOCK IN NOW';
        } else if (this.mode === 'long_break') {
          this.domToggleLabel.textContent = 'TOUCH GRASS NOW';
        } else {
          this.domToggleLabel.textContent = 'START BREAK';
        }
      }
    }
  }

  updateAvatarState() {
    if (this.domAvatarFocus) this.domAvatarFocus.classList.toggle('active', this.mode === 'focus');
    if (this.domAvatarBreak) this.domAvatarBreak.classList.toggle('active', this.mode === 'break');
    if (this.domAvatarLongBreak) this.domAvatarLongBreak.classList.toggle('active', this.mode === 'long_break');

    if (this.domAvatarGlow) {
      if (this.mode === 'focus') {
        this.domAvatarGlow.style.background = 'radial-gradient(circle, var(--emerald-glow-strong) 0%, rgba(16, 185, 129, 0) 70%)';
      } else if (this.mode === 'break') {
        this.domAvatarGlow.style.background = 'radial-gradient(circle, rgba(245, 158, 11, 0.45) 0%, rgba(245, 158, 11, 0) 70%)';
      } else {
        this.domAvatarGlow.style.background = 'radial-gradient(circle, rgba(52, 211, 153, 0.55) 0%, rgba(16, 185, 129, 0) 70%)';
      }
    }
  }

  playCategoryClip(category) {
    if (!this.manifest || !this.manifest.categories || !this.manifest.categories[category]) {
      console.warn(`[Vault] Category ${category} not found, using fallback.`);
      this.triggerSyntheticFallback(category);
      return;
    }

    const clips = this.manifest.categories[category];
    if (!clips || clips.length === 0) {
      this.triggerSyntheticFallback(category);
      return;
    }

    // Pick random clip
    const randomClip = clips[Math.floor(Math.random() * clips.length)];
    this.currentClip = randomClip;

    this.updateQuoteUI(randomClip.text, category, randomClip.audio_url || "vault-audio", randomClip.voice_name);

    if (this.settings.voiceEnabled) {
      if (randomClip.has_audio && randomClip.audio_url) {
        this.audioPlayer.src = randomClip.audio_url;
        this.audioPlayer.play().catch(e => {
          console.warn("Autoplay audio blocked or failed:", e);
          if (this.settings.speechFallback) {
            this.speakFallback(randomClip.text);
          }
        });
      } else if (this.settings.speechFallback) {
        this.speakFallback(randomClip.text);
      }
    }
  }

  handleInstantMotivation() {
    this.playCategoryClip('CHAD_MOTIVATION');
    if (this.settings.bgmEnabled) {
      const motThemes = (this.manifest && this.manifest.themes && this.manifest.themes.motivation) || [];
      if (motThemes.length > 0) {
        this.currentTheme = motThemes[Math.floor(Math.random() * motThemes.length)];
        this.currentThemeCategory = 'motivation';
        this.bgmPlayer.src = this.currentTheme.audio_url;
        this.bgmPlayer.play().catch(() => {});
        this.updateBgmUI();
      }
    }
  }

  toggleVoice() {
    this.settings.voiceEnabled = !this.settings.voiceEnabled;
    this.saveStorage();
    this.updateVoiceUI();
    if (!this.settings.voiceEnabled) {
      this.audioPlayer.pause();
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
      this.setSpeakingState(false);
    }
  }

  updateVoiceUI() {
    if (this.domBtnToggleVoice) {
      this.domBtnToggleVoice.classList.toggle('active', this.settings.voiceEnabled);
      this.domBtnToggleVoice.title = `Toggle GigaChad Voice Coach (Shortkey: V) - Currently ${this.settings.voiceEnabled ? 'ON' : 'OFF'}`;
    }
    if (this.domHeaderVoiceStatus) {
      this.domHeaderVoiceStatus.textContent = this.settings.voiceEnabled ? 'VOICE ON' : 'VOICE OFF';
    }
    if (this.domInputVoiceEnabled) {
      this.domInputVoiceEnabled.checked = this.settings.voiceEnabled;
    }
  }

  replayCurrentClip() {
    if (this.currentClip && this.currentClip.audio_url) {
      this.audioPlayer.currentTime = 0;
      this.audioPlayer.play().catch(() => {
        if (this.settings.speechFallback) {
          this.speakFallback(this.currentClip.text);
        }
      });
    } else if (this.currentClip && this.settings.speechFallback) {
      this.speakFallback(this.currentClip.text);
    }
  }

  triggerSyntheticFallback(category) {
    const defaultLines = {
      START_FOCUS: "Lock in, King. The world belongs to those who conquer distraction.",
      TOUCH_GRASS: "Screen time is over, King. Step outside and touch physical grass right now.",
      LONG_BREAK: "Take a long walk under the open sky, Brother. Drink cold water and recharge.",
      CHAD_MOTIVATION: "Discipline equals freedom, Champion. Embrace the grind."
    };
    const text = defaultLines[category] || "Lock in, King.";
    this.currentClip = { text, category, audio_url: "/vault/scripts/focus_001/focus_001.mp3" };
    this.updateQuoteUI(text, category, "synthetic-fallback");
    if (this.settings.voiceEnabled && this.settings.speechFallback) {
      this.speakFallback(text);
    }
  }

  updateQuoteUI(text, category, audioSrc, voiceName) {
    if (this.domQuoteText) this.domQuoteText.textContent = text;
    if (this.domQuoteBadge) this.domQuoteBadge.textContent = category;
    if (this.domQuoteClipId) this.domQuoteClipId.textContent = audioSrc.replace('/vault/', 'vault/');
    if (this.domQuoteVoiceTag) {
      this.domQuoteVoiceTag.textContent = voiceName ? `🎙️ ${voiceName}` : '🎙️ elevenlabs';
    }
  }

  setSpeakingState(isSpeaking) {
    if (this.domAvatarSpeech) {
      this.domAvatarSpeech.classList.toggle('is-active', isSpeaking);
      const wave = this.domAvatarSpeech.querySelector('.audio-wave');
      if (wave) wave.classList.toggle('is-speaking', isSpeaking);
    }

    // Duck BGM during speech so the commanding voice is crystal clear
    if (this.bgmPlayer && this.settings.bgmEnabled) {
      if (isSpeaking) {
        this.bgmPlayer.volume = Math.max(0, (this.settings.bgmVolume * 0.2) / 100);
      } else {
        this.updateBgmVolume();
      }
    }
  }

  toggleBgm() {
    this.settings.bgmEnabled = !this.settings.bgmEnabled;
    this.saveStorage();
    this.updateBgmUI();
    this.updateBgmPlayback(true);
  }

  updateBgmVolume() {
    if (this.bgmPlayer) {
      this.bgmPlayer.volume = Math.max(0, Math.min(1, this.settings.bgmVolume / 100));
    }
  }

  getRandomThemeForMode(mode) {
    if (!this.manifest || !this.manifest.themes) {
      return { audio_url: '/vault/themes/theme_focus_01/theme_focus_01.mp3', title: 'GigaChad Anthem' };
    }
    const cat = mode === 'focus' ? 'focus' : (mode === 'break' ? 'break' : (mode === 'long_break' ? 'long_break' : 'motivation'));
    const pool = this.manifest.themes[cat] || this.manifest.themes['focus'] || [];
    if (pool.length === 0) {
      return { audio_url: '/vault/themes/theme_focus_01/theme_focus_01.mp3', title: 'GigaChad Anthem' };
    }
    // Avoid repeating the same theme consecutively if multiple options exist
    const candidates = (pool.length > 1 && this.currentTheme)
      ? pool.filter(t => t.id !== this.currentTheme.id)
      : pool;
    return candidates[Math.floor(Math.random() * candidates.length)];
  }

  updateBgmUI() {
    if (this.domBtnToggleBgm) {
      this.domBtnToggleBgm.classList.toggle('active', this.settings.bgmEnabled);
      if (this.currentTheme) {
        const ref = this.currentTheme.meme_reference ? ` [${this.currentTheme.meme_reference}]` : '';
        this.domBtnToggleBgm.title = `Theme: ${this.currentTheme.title}${ref} (Shortkey: B) - Currently ${this.settings.bgmEnabled ? 'ON' : 'OFF'}`;
      }
    }
    if (this.domHeaderBgmStatus) {
      this.domHeaderBgmStatus.textContent = this.settings.bgmEnabled ? 'ANTHEM ON' : 'ANTHEM OFF';
    }
    if (this.domInputBgmEnabled) {
      this.domInputBgmEnabled.checked = this.settings.bgmEnabled;
    }
  }

  updateBgmPlayback(forceNew = false) {
    if (!this.bgmPlayer) return;
    if (this.isRunning && this.settings.bgmEnabled) {
      if (forceNew || !this.currentTheme || this.currentThemeCategory !== this.mode) {
        this.currentTheme = this.getRandomThemeForMode(this.mode);
        this.currentThemeCategory = this.mode;
        this.bgmPlayer.src = this.currentTheme.audio_url;
        this.updateBgmUI();
      }
      this.bgmPlayer.play().catch(e => {
        // Autoplay may be restricted until initial user click
      });
    } else {
      this.bgmPlayer.pause();
    }
  }

  speakFallback(text) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.pitch = 0.65; // Deep baritone pitch
    utterance.rate = 0.92;  // Deliberate, commanding tempo

    // Try to find deep masculine voice
    const voices = window.speechSynthesis.getVoices();
    const deepMaleVoice = voices.find(v => 
      v.lang.startsWith('en') && (v.name.includes('Male') || v.name.includes('David') || v.name.includes('Daniel') || v.name.includes('George') || v.name.includes('Guy'))
    );
    if (deepMaleVoice) {
      utterance.voice = deepMaleVoice;
    }

    utterance.onstart = () => this.setSpeakingState(true);
    utterance.onend = () => this.setSpeakingState(false);
    utterance.onerror = () => this.setSpeakingState(false);

    window.speechSynthesis.speak(utterance);
  }

  handleTouchGrass(event) {
    this.grassCount++;
    this.saveStorage();
    this.updateGrassDisplay();

    // Spawn floating grass confetti / particles
    this.spawnGrassParticles(event);

    // Audio cue / haptic feedback
    this.playGrassChime();
  }

  spawnGrassParticles(event) {
    const originX = event ? event.clientX : window.innerWidth / 2;
    const originY = event ? event.clientY : window.innerHeight / 2;
    const particles = ['🌱', '🌿', '🍀', '✨', '☀️'];

    for (let i = 0; i < 8; i++) {
      const el = document.createElement('span');
      el.className = 'floating-grass-particle';
      el.textContent = particles[Math.floor(Math.random() * particles.length)];
      el.style.left = `${originX + (Math.random() * 80 - 40)}px`;
      el.style.top = `${originY + (Math.random() * 40 - 20)}px`;
      el.style.fontSize = `${1.2 + Math.random() * 0.8}rem`;
      document.body.appendChild(el);

      setTimeout(() => el.remove(), 1800);
    }
  }

  playGrassChime() {
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
      osc.frequency.exponentialRampToValueAtTime(659.25, ctx.currentTime + 0.15); // E5
      gain.gain.setValueAtTime(0.15, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.35);
    } catch (e) {
      // AudioContext not allowed or not supported
    }
  }

  updateGrassDisplay() {
    if (this.domGrassDisplay) this.domGrassDisplay.textContent = this.grassCount;
    if (this.domHeaderGrassCount) this.domHeaderGrassCount.textContent = this.grassCount;
    if (this.domSettingsGrassCount) this.domSettingsGrassCount.textContent = this.grassCount;
  }

  openSettings() {
    if (!this.domSettingsModal) return;
    this.domSettingsModal.classList.add('active');
    this.domSettingsModal.setAttribute('aria-hidden', 'false');
  }

  closeSettings() {
    if (!this.domSettingsModal) return;
    this.domSettingsModal.classList.remove('active');
    this.domSettingsModal.setAttribute('aria-hidden', 'true');
  }

  applySettingsToUI() {
    const elFocus = document.getElementById('setting-focus');
    const elBreak = document.getElementById('setting-break');
    const elLong = document.getElementById('setting-long-break');
    const elInterval = document.getElementById('setting-interval');
    const elVol = document.getElementById('setting-volume');
    const elAutoBreak = document.getElementById('setting-autostart-break');
    const elAutoFocus = document.getElementById('setting-autostart-focus');
    const elSpeech = document.getElementById('setting-speech-fallback');
    const elRepeatTheme = document.getElementById('setting-repeat-theme');

    if (elFocus) elFocus.value = this.settings.focusMinutes;
    if (elBreak) elBreak.value = this.settings.breakMinutes;
    if (elLong) elLong.value = this.settings.longBreakMinutes;
    if (elInterval) elInterval.value = this.settings.longBreakInterval;
    if (elVol) elVol.value = this.settings.volume;
    if (this.domVolumeValDisplay) this.domVolumeValDisplay.textContent = `${this.settings.volume}%`;
    if (this.domInputVoiceEnabled) this.domInputVoiceEnabled.checked = this.settings.voiceEnabled;
    if (this.domInputBgmEnabled) this.domInputBgmEnabled.checked = this.settings.bgmEnabled;
    if (elRepeatTheme) elRepeatTheme.checked = !!this.settings.repeatTheme;
    if (this.domInputBgmVolume) this.domInputBgmVolume.value = this.settings.bgmVolume;
    if (this.domBgmVolumeDisplay) this.domBgmVolumeDisplay.textContent = `${this.settings.bgmVolume}%`;
    if (elAutoBreak) elAutoBreak.checked = this.settings.autoStartBreak;
    if (elAutoFocus) elAutoFocus.checked = this.settings.autoStartFocus;
    if (elSpeech) elSpeech.checked = this.settings.speechFallback;
  }

  saveSettingsFromForm() {
    const formData = new FormData(this.domSettingsForm);
    this.settings.focusMinutes = parseInt(formData.get('focusMinutes'), 10) || 25;
    this.settings.breakMinutes = parseInt(formData.get('breakMinutes'), 10) || 5;
    this.settings.longBreakMinutes = parseInt(formData.get('longBreakMinutes'), 10) || 15;
    this.settings.longBreakInterval = parseInt(formData.get('longBreakInterval'), 10) || 4;
    this.settings.voiceEnabled = formData.get('voiceEnabled') === 'on';
    this.settings.volume = parseInt(formData.get('volume'), 10) || 90;
    this.settings.bgmEnabled = formData.get('bgmEnabled') === 'on';
    this.settings.repeatTheme = formData.get('repeatTheme') === 'on';
    this.bgmPlayer.loop = this.settings.repeatTheme;
    this.settings.bgmVolume = parseInt(formData.get('bgmVolume'), 10) || 35;
    this.settings.autoStartBreak = formData.get('autoStartBreak') === 'on';
    this.settings.autoStartFocus = formData.get('autoStartFocus') === 'on';
    this.settings.speechFallback = formData.get('speechFallback') === 'on';

    this.saveStorage();
    this.updateVoiceUI();
    if (!this.settings.voiceEnabled) {
      this.audioPlayer.pause();
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
      this.setSpeakingState(false);
    }
    this.updateBgmVolume();
    this.updateBgmUI();
    this.updateBgmPlayback();

    // If timer is not running, adjust current remaining
    if (!this.isRunning) {
      this.resetTimer();
    }
  }
}

// Instantiate on DOM load
if (typeof window !== 'undefined') {
  window.addEventListener('DOMContentLoaded', () => {
    window.chadodoro = new ChadodoroController();
  });
}
