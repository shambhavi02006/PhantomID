const { createApp } = Vue;

createApp({
  data() {
    return {
      profiles: [],
      storageEngine: "Detecting...",
      loading: false,
      resetting: false,
      summary: null,
      selectedProfile: null,
      audioEnabled: true,
      audioPlaying: false,
      audioPlayer: null,
      errorMessage: null
    };
  },
  computed: {
    ghostCount() {
      return this.profiles.filter(p => p.verdict === "Ghost").length;
    },
    realCount() {
      return this.profiles.filter(p => p.verdict === "Real").length;
    },
    unscannedCount() {
      return this.profiles.filter(p => !p.verdict).length;
    }
  },
  methods: {
    async fetchProfiles() {
      try {
        const res = await fetch("/api/profiles");
        const data = await res.json();
        if (data.status === "success") {
          this.profiles = data.profiles;
          this.storageEngine = data.storage_engine;
        }
      } catch (err) {
        console.error("Failed to fetch profiles:", err);
        this.errorMessage = "Unable to connect to backend service.";
      }
    },

    async runGhostProtocol() {
      this.loading = true;
      this.errorMessage = null;

      try {
        const res = await fetch("/api/scan", {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
        const data = await res.json();

        if (data.status === "success") {
          this.profiles = data.profiles;
          this.summary = data.summary;
          this.storageEngine = data.summary.storage_engine;

          // Trigger Audio Telemetry
          if (this.audioEnabled && data.summary.ghosts_detected > 0) {
            this.playAudioAlert(data.summary.ghosts_detected);
          }
        } else {
          this.errorMessage = "Ghost Protocol scan interrupted.";
        }
      } catch (err) {
        console.error("Scan error:", err);
        this.errorMessage = "Failed to run AI scan. Check server console.";
      } finally {
        this.loading = false;
      }
    },

    async resetLedger() {
      this.resetting = true;
      this.summary = null;
      try {
        const res = await fetch("/api/reset", { method: "POST" });
        const data = await res.json();
        if (data.status === "success") {
          this.profiles = data.profiles;
          this.storageEngine = data.storage_engine;
        }
      } catch (err) {
        console.error("Reset error:", err);
      } finally {
        this.resetting = false;
      }
    },

    async playAudioAlert(ghostCount) {
      this.audioPlaying = true;
      try {
        const res = await fetch("/api/voice-alert", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ghost_count: ghostCount })
        });

        const contentType = res.headers.get("content-type") || "";
        if (contentType.includes("audio/mpeg")) {
          // ElevenLabs MP3 Stream
          const blob = await res.blob();
          const audioUrl = URL.createObjectURL(blob);
          this.audioPlayer = new Audio(audioUrl);
          this.audioPlayer.play();
          this.audioPlayer.onended = () => { this.audioPlaying = false; };
        } else {
          // Web Speech Synthesis Fallback
          const data = await res.json();
          if (data.text && "speechSynthesis" in window) {
            const utterance = new SpeechSynthesisUtterance(data.text);
            utterance.rate = 0.95;
            utterance.pitch = 0.85; // slightly lower cyber tone
            utterance.onend = () => { this.audioPlaying = false; };
            window.speechSynthesis.speak(utterance);
          } else {
            this.audioPlaying = false;
          }
        }
      } catch (err) {
        console.warn("Audio alert failed, fallback disabled:", err);
        this.audioPlaying = false;
      }
    },

    openInspectModal(profile) {
      this.selectedProfile = profile;
      const modalEl = document.getElementById("inspectModal");
      if (modalEl && window.bootstrap) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
      }
    },

    formatCurrency(val) {
      if (val === undefined || val === null) return "$0.00";
      return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(val);
    },

    getAnomalyColor(score) {
      if (!score) return "text-secondary";
      if (score >= 0.8) return "text-danger fw-bold";
      if (score >= 0.4) return "text-warning";
      return "text-success";
    }
  },
  mounted() {
    this.fetchProfiles();
  }
}).mount("#app");

