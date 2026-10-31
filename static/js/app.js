const { createApp } = Vue;

createApp({
  data() {
    return {
      profiles: [],
      storageEngine: "Detecting...",
      loading: false,
      resetting: false,
      injecting: false,
      summary: null,
      selectedProfile: null,
      audioEnabled: true,
      audioPlaying: false,
      audioPlayer: null,
      errorMessage: null,
      newProfile: {
        name: "",
        email: "",
        age: 28,
        employment_years: 6,
        account_balance: 55000,
        credit_score: 720
      }
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

    openInjectModal() {
      if (!this.newProfile.name) {
        this.loadPreset("child_prodigy");
      }
      const modalEl = document.getElementById("injectModal");
      if (modalEl && window.bootstrap) {
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
      }
    },

    loadPreset(type) {
      if (type === "child_prodigy") {
        this.newProfile = {
          name: "Julian Vance-Ross",
          email: "julian.ross@ventureseed.io",
          age: 18,
          employment_years: 15,
          account_balance: 185000,
          credit_score: 790
        };
      } else if (type === "senior_doc") {
        this.newProfile = {
          name: "Dr. Alistair Finch",
          email: "afinch@stmarys-medical.org",
          age: 54,
          employment_years: 28,
          account_balance: 310000,
          credit_score: 810
        };
      } else if (type === "delinquent_prime") {
        this.newProfile = {
          name: "Chloe Bennett-Stark",
          email: "c.bennett@starkholdings.net",
          age: 41,
          employment_years: 19,
          account_balance: -24500,
          credit_score: 795
        };
      }
    },

    async injectProfile() {
      this.injecting = true;
      this.errorMessage = null;

      try {
        const res = await fetch("/api/profiles", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.newProfile)
        });
        const data = await res.json();

        if (data.status === "success") {
          this.profiles = data.profiles;

          // Close modal
          const modalEl = document.getElementById("injectModal");
          if (modalEl && window.bootstrap) {
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
          }

          // Trigger audio if injected profile is a ghost
          if (data.profile.verdict === "Ghost" && this.audioEnabled) {
            this.playAudioAlert(1);
          }
        } else {
          this.errorMessage = "Failed to inject identity.";
        }
      } catch (err) {
        console.error("Inject error:", err);
        this.errorMessage = "Failed to communicate with API.";
      } finally {
        this.injecting = false;
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
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
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
