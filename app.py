import os
import time
import requests
from flask import Flask, jsonify, render_template, request, Response
from dotenv import load_dotenv

from seed_data import (
    seed_database,
    fetch_profiles,
    update_profile_scan,
    is_mongo_available
)
from detectors.tabpfn_engine import calculate_tabular_anomalies
from detectors.gemma_engine import run_gemma_reasoning

load_dotenv()

# Sentry Agent Tracing Integration ($100 Prize Track)
SENTRY_DSN = os.getenv("SENTRY_DSN", "").strip()
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        environment=os.getenv("SENTRY_ENVIRONMENT", "production")
    )
    print("[PhantomID] Sentry Agent Tracing initialized.")
else:
    print("[PhantomID] Sentry DSN not set (running in local telemetry mode).")

app = Flask(__name__)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM").strip()


@app.before_request
def ensure_seeded_db():
    """Seeds the database on first boot if needed."""
    if not hasattr(app, "_db_initialized"):
        seed_database()
        app._db_initialized = True


@app.route("/")
def index():
    """Serves the reactive cyber-fintech dashboard."""
    return render_template("index.html")


@app.route("/api/profiles", methods=["GET"])
def get_profiles():
    """Returns the current catalog of profiles from MongoDB Atlas or SQLite."""
    profiles, storage_engine = fetch_profiles()
    return jsonify({
        "status": "success",
        "storage_engine": storage_engine,
        "count": len(profiles),
        "profiles": profiles
    })


@app.route("/api/scan", methods=["POST"])
def scan_identities():
    """
    Executes 'Ghost Protocol':
    1. Fetches profiles from MongoDB Atlas / SQLite
    2. Runs TabPFN tabular anomaly detection
    3. Prompts Google Gemma 2 for logical cognitive fraud deduction
    4. Persists the verdicts and scores back to database
    5. Returns unified forensic telemetry
    """
    total_start = time.time()
    profiles, storage_engine = fetch_profiles()

    # Step 1: Run TabPFN Anomaly Engine ($200 Prize)
    tabpfn_output = calculate_tabular_anomalies(profiles)
    tabpfn_scores = tabpfn_output["scores"]

    # Step 2: Run Google Gemma 2 Cognitive Reasoning Engine ($200 Prize)
    gemma_output = run_gemma_reasoning(profiles, tabpfn_scores)
    gemma_verdicts = gemma_output["verdicts"]

    # Step 3: Persist results
    ghost_count = 0
    real_count = 0
    updated_profiles = []

    for p in profiles:
        pid = p["id"]
        v_info = gemma_verdicts.get(pid, {"verdict": "Real", "reason": "No anomalies found."})
        verdict = v_info.get("verdict", "Real")
        reason = v_info.get("reason", "Verified identity.")
        score = tabpfn_scores.get(pid, 0.05)

        if verdict == "Ghost":
            ghost_count += 1
        else:
            real_count += 1

        update_profile_scan(pid, verdict, reason, score)

        p_copy = dict(p)
        p_copy["status"] = "Scanned"
        p_copy["verdict"] = verdict
        p_copy["reason"] = reason
        p_copy["anomaly_score"] = score
        updated_profiles.append(p_copy)

    total_duration_ms = round((time.time() - total_start) * 1000, 2)

    return jsonify({
        "status": "success",
        "summary": {
            "total_analyzed": len(updated_profiles),
            "ghosts_detected": ghost_count,
            "real_verified": real_count,
            "threat_level": "ELEVATED" if ghost_count > 0 else "NOMINAL",
            "storage_engine": storage_engine,
            "tabpfn_engine": tabpfn_output["engine"],
            "tabpfn_latency_ms": tabpfn_output["latency_ms"],
            "gemma_engine": gemma_output["engine"],
            "gemma_mode": gemma_output["mode"],
            "gemma_latency_ms": gemma_output["latency_ms"],
            "total_duration_ms": total_duration_ms
        },
        "profiles": updated_profiles
    })


@app.route("/api/reset", methods=["POST"])
def reset_db():
    """Resets the mock dataset to unscanned state."""
    msg = seed_database()
    profiles, storage_engine = fetch_profiles()
    return jsonify({
        "status": "success",
        "message": msg,
        "storage_engine": storage_engine,
        "profiles": profiles
    })


@app.route("/api/voice-alert", methods=["POST"])
def voice_alert():
    """
    ElevenLabs Voice API ($100 Prize Track)
    Streams eerie audio alert or provides browser speech fallback payload.
    """
    data = request.get_json(silent=True) or {}
    ghost_count = data.get("ghost_count", 3)
    alert_text = (
        f"Warning: Ghost Protocol has detected {ghost_count} synthetic identities in the banking ledger. "
        "Logical contradictions isolated. Threat profiles quarantined."
    )

    if ELEVENLABS_API_KEY:
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
            headers = {
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            }
            body = {
                "text": alert_text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8
                }
            }
            resp = requests.post(url, json=body, headers=headers, timeout=10)
            if resp.status_code == 200:
                return Response(resp.content, mimetype="audio/mpeg")
        except Exception as e:
            print(f"[ElevenLabs Voice Notice] {e}")

    # Fallback to Web Speech JSON response
    return jsonify({
        "mode": "web_speech",
        "text": alert_text
    })


@app.route("/health")
def health():
    """Healthcheck endpoint for Render cloud hosting."""
    return jsonify({
        "status": "healthy",
        "service": "PhantomID - The Synthetic Identity Hunter",
        "version": "1.0.0"
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    print(f"\n=======================================================")
    print(f"👻 PhantomID: The Synthetic Identity Hunter Online!")
    print(f"📡 Dashboard running at: http://127.0.0.1:{port}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=debug)

