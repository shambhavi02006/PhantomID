# 👻 PhantomID: The Synthetic Identity Hunter
> **Theme Context:** *"Ghost in the Machine"* — Hacktoberfest Week 4 (Fintech Fraud Detection)  
> **Target Prize Potential:** Up to **$1,000 USD** across 7 Prize Tracks  
> **License:** Open Source  

---

## 1. Project Overview

### What is PhantomID?
**PhantomID** is an AI-powered financial fraud intelligence dashboard designed to hunt down **synthetic identities**—the literal *"ghosts in the banking machine."*

Synthetic Identity Fraud (SIF) is one of the fastest-growing financial crimes. Instead of stealing a single person's complete identity, sophisticated scammers fabricate "Frankenstein profiles" by combining real Social Security Numbers (often belonging to children or the deceased) with fabricated names, addresses, and contradictory work histories. 

To standard database checks and regex validators, these synthetic identities appear completely valid. However, they harbor subtle, chronological, and statistical impossibilities.

### What Does PhantomID Do?
PhantomID provides bank risk officers with a real-time fraud investigation terminal that:
1. **Ingests financial profiles** stored in a cloud database.
2. **Runs a dual-engine AI audit**:
   - **Quantitative Anomaly Scoring** using a tabular foundation model to spot mathematical and statistical outliers.
   - **Cognitive Logical Deduction** using an open-weight LLM to uncover common-sense contradictions (e.g., an 18-year-old claiming 15 years of employment or holding senior executive tenure).
3. **Quarantines "Ghosts" in real-time** on a reactive dashboard, highlighting fraudulent profiles in crimson warning states with verifiable evidence logs.
4. **Broadcasts an automated audio security alert** upon breach isolation.
5. **Traces the entire inspection pipeline** with production telemetry, logging latency, token consumption, and execution spans.

---

## 2. End-to-End Workflow & Architecture

```
                                  [ Cloud / Local Storage ]
                                      MongoDB Atlas M0
                                    (SQLite Smart Fallback)
                                              │
                                              ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               FLASK BACKEND ORCHESTRATOR                               │
│                                                                                        │
│  [Sentry Agent Tracing Span]                                                           │
│  ├── 1. Fetch Profile Batch                                                            │
│  ├── 2. Dispatch Tabular Data ────────► Prior Labs TabPFN-3.5                          │
│  │                                      (Statistical Outlier & Distribution Scoring)   │
│  ├── 3. Dispatch Demographics + Score ─► Google Gemma 2 (9B-Instruct)                 │
│  │                                      (Logical Contradiction & Common-Sense Audit)   │
│  └── 4. Synthesize Alert Event ───────► ElevenLabs Text-to-Speech API                  │
└─────────────────────────────────────────────┬──────────────────────────────────────────┘
                                              │
                                              ▼
                                 [ Cyber-Fintech UI (Vue 3) ]
                             Hosted on Render + Custom .tech Domain
```

---

## 3. Tech Stack: Why Each Tool Was Chosen & How It Enhances PhantomID

Every single tool in our stack was chosen to maximize **real-world fraud detection capabilities**, create a **stunning hackathon demo**, and qualify for **specific cash prize categories**.

---

### A. Google Gemma 2 (`google/gemma-2-9b-it`)
* **Role:** Cognitive Fraud Reasoning Engine
* **Prize Track:** 🏆 **Best Use of Gemma ($200 USD)**
* **Why We Chose It:**
  Rule-based systems cannot reason through nuanced linguistic or chronological discrepancies. Gemma 2 (Google's state-of-the-art open-weight model) excels at strict logic and common-sense deduction.
* **How It Enhances the Project:**
  Instead of just outputting an opaque `"Fraud / Not Fraud"` flag, Gemma provides **clear, human-readable forensic explanations** for compliance officers (e.g., *"Identity flagged as Ghost: User is 19 years old but claims 16 years of continuous employment, which is chronologically impossible."*).

---

### B. Prior Labs TabPFN-3.5
* **Role:** Tabular Anomaly Foundation Model
* **Prize Track:** 🏆 **Best Use of TabPFN ($200 USD)**
* **Why We Chose It:**
  TabPFN is Prior Labs' breakthrough foundation model pre-trained on millions of tabular datasets. It performs in-context anomaly detection and classification on structured data without requiring extensive custom training pipelines.
* **How It Enhances the Project:**
  TabPFN acts as **Engine 1** of our dual-engine architecture. It analyzes multi-dimensional tabular distributions (`age`, `credit_score`, `account_balance`, `employment_years`, `open_credit_lines`) and generates an objective **Anomaly Probability Score** ($0.00$ to $1.00$). This quantitative score is fed directly into Gemma, giving the LLM empirical statistical backing.

---

### C. MongoDB Atlas (Cloud NoSQL)
* **Role:** Cloud Financial Ledger & Identity Store
* **Prize Track:** 🏆 **Best Use of MongoDB Atlas ($100 USD)**
* **Why We Chose It:**
  Financial profiles are multi-faceted and change schema over time (credit history, biometric flags, external bureau metadata). MongoDB Atlas provides a flexible, distributed cloud document database.
* **How It Enhances the Project:**
  Stores the 10 mock identities and persists an immutable audit log of every "Ghost Protocol" scan. Judges can see profiles pulled in real-time from a production cloud database cluster instead of a static local file.

---

### D. Sentry Agent Tracing (`sentry-sdk`)
* **Role:** AI Agent Observability & Performance Telemetry
* **Prize Track:** 🏆 **Best Use of Sentry Agent Tracing ($100 USD)**
* **Why We Chose It:**
  Multi-engine AI workflows can suffer from latency bottlenecks or unexpected API failures. Sentry provides enterprise-grade performance monitoring and AI pipeline tracing.
* **How It Enhances the Project:**
  Instruments every step of the scan pipeline (`mongo_fetch_profiles`, `tabpfn_anomaly_scoring`, `gemma_reasoning_inference`). It generates visual flame graphs, latency metrics, and token cost traces that can be screenshotted directly into the hackathon submission write-up.

---

### E. ElevenLabs Voice AI API
* **Role:** Eerie Cyber Security Incident Announcer
* **Prize Track:** 🏆 **Best Use of ElevenLabs ($100 USD)**
* **Why We Chose It:**
  To bring the *"Ghost in the Machine"* theme to life. A visual dashboard alone is passive; an automated spoken telemetry alert creates an unforgettable presentation.
* **How It Enhances the Project:**
  The second the scan identifies synthetic identities, ElevenLabs generates a low-latency, futuristic security broadcast:  
  > *"Attention Security Operations: Ghost Protocol has detected 3 synthetic identities in the banking ledger. Threat profiles isolated."*

---

### F. Render Cloud Platform + Custom `.tech` Domain
* **Role:** Production Cloud Hosting & Live URL
* **Prize Tracks:** 🏆 **Best Use of Render ($200 USD)** + 🏆 **Best Use of a .tech Domain ($100 USD)**
* **Why We Chose It:**
  Projects running only on `localhost` have a much lower chance of winning hackathons. Render provides zero-downtime, automated Git deployments for Python Web Services.
* **How It Enhances the Project:**
  Provides judges and community reviewers with a live, fast-loading, public URL (e.g. `https://phantomid.tech`), with automatic SSL and zero local setup required.

---

### G. Vue.js 3 + Cyber-Fintech Glassmorphism UI
* **Role:** Real-Time Reactive Dashboard
* **Why We Chose It:**
  Vue 3 (via CDN) delivers reactive data binding without the overhead of heavy Node.js build configurations.
* **How It Enhances the Project:**
  Delivers a dark cyber-fintech command center aesthetic (deep slate canvas, radar scan pulses, neon status badges, glassmorphic profile cards). It elevates the project from a simple hackathon script into an enterprise-grade security terminal.

---

## 4. The 10 Mock Profiles: 7 Real Humans vs 3 Synthetic "Ghosts"

| ID | Name | Age | Employment | Balance | Credit Score | Profile Status | The Hidden Flaw / Reality |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **01** | Marcus Vance | 42 | 18 yrs | $84,250 | 760 | 🟢 **Real** | Consistent mid-career executive. |
| **02** | Elena Rostova | 29 | 6 yrs | $32,100 | 710 | 🟢 **Real** | Plausible young professional. |
| **03** | Arthur Pendelton | 68 | 44 yrs | $210,000 | 815 | 🟢 **Real** | Well-established retiree profile. |
| **04** | Tyler Durden-Smith | 19 | 16 yrs | $145,000 | 790 | 🔴 **GHOST** | **Contradiction:** 19 years old with 16 years of work history (started at age 3). |
| **05** | Priya Sharma | 35 | 11 yrs | $67,400 | 740 | 🟢 **Real** | Normal senior analyst profile. |
| **06** | Jordan Belfort-Cruz | 22 | 1 yr | $890,000 | 845 | 🔴 **GHOST** | **Contradiction:** Near-perfect 845 credit score and $890k balance with only 1 year employment at age 22 (bust-out synthetic profile). |
| **07** | David Kim | 51 | 26 yrs | $128,900 | 780 | 🟢 **Real** | Natural veteran career profile. |
| **08** | Sophia Martinez | 24 | 2 yrs | $9,800 | 660 | 🟢 **Real** | Believable entry-level profile. |
| **09** | Sarah Connor-Reese | 38 | 20 yrs | -$12,000 | 795 | 🔴 **GHOST** | **Contradiction:** Prime 795 credit score despite chronic negative account balance and severe debt default markers. |
| **10** | Liam O'Connor | 31 | 8 yrs | $44,500 | 695 | 🟢 **Real** | Normal, verifiable identity. |

---

## 5. Built-in "Zero-Friction Fallback" Architecture

To ensure you can run, test, and demo PhantomID without being blocked by missing credentials:
* **Database:** Connects to MongoDB Atlas if `MONGO_URI` is present; automatically falls back to an embedded SQLite database if unset.
* **AI Engine:** Calls Hugging Face Gemma 2 API if `HF_TOKEN` is present; falls back to an intelligent local heuristic reasoning engine if offline.
* **Audio:** Streams ElevenLabs synthesized audio if `ELEVENLABS_API_KEY` is present; falls back to browser-native Web Speech synthesis.
* **Sentry:** Records full traces if `SENTRY_DSN` is present; cleanly bypasses if unconfigured.

**Result:** The application runs 100% out of the box right now, and lights up every external integration as you plug in your free keys!

---

## 6. Step-by-Step Implementation Plan & Delivery Roadmap

Here is the exact step-by-step execution plan we will follow to build, test, and deploy PhantomID:

```
[ Phase 1: Data Layer ]  ──►  [ Phase 2: Dual AI Engines ]  ──►  [ Phase 3: Flask & Sentry API ]
                                                                             │
[ Phase 6: Render Deploy ] ◄──  [ Phase 5: Free API Keys ]   ◄──  [ Phase 4: Cyber-Fintech UI ]
```

### Phase 1: Project Setup & Dual-Database Seeding
* **Objective:** Establish the project structure and seed the 10 financial profiles.
* **Deliverables:**
  * `seed_data.py`: Multi-storage seed script that writes to MongoDB Atlas (if configured) or local `phantom.db` (SQLite).
  * `models.py`: Data schemas for profiles, anomaly scores, and audit verdicts.

### Phase 2: Dual AI Intelligence Engines
* **Objective:** Build the two fraud detection engines with smart local fallbacks.
* **Deliverables:**
  * `detectors/tabpfn_engine.py`: Runs Prior Labs TabPFN-3.5 on tabular features (`age`, `employment_years`, `balance`, `credit_score`) to produce anomaly probability scores.
  * `detectors/gemma_engine.py`: Prompts Google Gemma 2 (`google/gemma-2-9b-it`) to evaluate the common-sense logic of each profile and output structured JSON reasons.

### Phase 3: Flask Backend & Sentry Agent Tracing
* **Objective:** Build the REST API orchestrating data retrieval, AI analysis, audio alerts, and performance monitoring.
* **Deliverables:**
  * `app.py`: Flask application.
  * `GET /api/profiles`: Returns the raw profile catalog for initial rendering.
  * `POST /api/scan`: Executes the dual-engine scan inside a Sentry transaction span (`run_ghost_protocol`), returning enriched profiles with TabPFN scores and Gemma verdicts.
  * `POST /api/voice-alert`: Generates the ElevenLabs audio security alert (or browser TTS fallback).

### Phase 4: Cyber-Fintech Reactive Dashboard
* **Objective:** Create a visual "Ghost in the Machine" terminal interface.
* **Deliverables:**
  * `templates/index.html`: Vue.js 3 single-page dashboard with Bootstrap 5.
  * `static/css/cyber.css`: Custom glassmorphism, radar-scan animation, crimson fraud badges, and glowing telemetry panels.
  * `static/js/app.js`: Vue application handling scan states, audio triggers, and modal forensic breakdowns.

### Phase 5: Free API Keys Configuration (Guided Walkthrough)
* **Objective:** Transition smoothly from local fallbacks to production services.
* **Deliverables:**
  * `.env.example` & `.env` configuration file.
  * Step-by-step guided instructions to collect free keys for MongoDB Atlas, Hugging Face, Sentry, and ElevenLabs.

### Phase 6: Production Deployment & Hacktoberfest Submission
* **Objective:** Take the project live and prepare write-up assets.
* **Deliverables:**
  * `render.yaml` & `requirements.txt`: 1-click cloud deployment blueprint for Render.
  * DNS guide to connect the free `.tech` domain.
  * Sentry trace export guide (screenshots of flame graphs and latency for your DEV.to article).

