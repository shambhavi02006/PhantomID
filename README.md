# 👻 PhantomID: The Synthetic Identity Hunter
> **Theme Context:** *"Ghost in the Machine"* — Hacktoberfest 2026 (Fintech Fraud Detection)  
> **Target Prize Potential:** Up to **$1,000 USD** across 7 Prize Tracks  
> **Status:** Production-Ready & Deployed

---

## 📌 Executive Summary

**PhantomID** is an AI-powered financial fraud detection terminal designed to hunt down **synthetic identities**—the literal *"ghosts in the banking machine."*

Synthetic Identity Fraud (SIF) is the fastest-growing form of financial identity crime. Instead of stealing a single victim's identity in whole, scammers stitch together real credentials (often SSNs from children or the deceased) with fabricated names, addresses, and contradictory work histories to produce "Frankenstein profiles". 

To traditional rule engines and regex validators, these synthetic identities appear completely valid. However, they harbor subtle, chronological, and statistical impossibilities.

PhantomID deploys a **Dual-Engine AI architecture** combining **quantitative tabular foundation models** with **cognitive open-weight LLMs** to quarantine synthetic ghosts with forensic explanations.

---

## 🏆 Hacktoberfest Prize Track Matrix ($1,000 Potential)

| Prize Category | Bounty | How PhantomID Integrates It |
| :--- | :--- | :--- |
| **Best Use of Gemma** | **$200** | **Google Gemma 2 (`google/gemma-2-9b-it`)**: Acts as the cognitive reasoning engine, performing common-sense deduction to explain the logical contradictions in flagged profiles. |
| **Best Use of TabPFN** | **$200** | **Prior Labs TabPFN-3.5**: Tabular foundation model computing in-context statistical anomaly probability scores across demographic and financial vectors. |
| **Best Use of Render** | **$200** | Infrastructure-as-code deployment via `render.yaml` for live, zero-downtime cloud hosting. |
| **Best Use of MongoDB Atlas** | **$100** | Cloud identity ledger & audit trail store using MongoDB Atlas (with automatic local SQLite fallback). |
| **Best Use of Sentry Agent Tracing** | **$100** | Full observability and latency flame-graph instrumentation across all AI pipeline spans (`sentry-sdk`). |
| **Best Use of ElevenLabs** | **$100** | Eerie synthetic voice security broadcast when "Ghost Protocol" catches synthetic identities. |
| **Best Use of a .tech Domain** | **$100** | Custom hackathon domain linked to the live Render deployment. |

---

## 🧠 System Architecture: The Dual-Engine Hunter

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

## 👥 The 10 Identities: 7 Real Humans vs 3 Synthetic Ghosts

| ID | Name | Age | Employment | Balance | Credit | Status | The Forensic Flaw / Reality |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **01** | Marcus Vance | 42 | 18 yrs | $84,250 | 760 | 🟢 **Real** | Consistent mid-career executive. |
| **02** | Elena Rostova | 29 | 6 yrs | $32,100 | 710 | 🟢 **Real** | Plausible young professional. |
| **03** | Arthur Pendelton | 68 | 44 yrs | $210,000 | 815 | 🟢 **Real** | Well-established retiree profile. |
| **04** | Tyler Durden-Smith | 19 | 16 yrs | $145,000 | 790 | 🔴 **GHOST** | **Contradiction:** 19 years old with 16 years of work history (career started at age 3). |
| **05** | Priya Sharma | 35 | 11 yrs | $67,400 | 740 | 🟢 **Real** | Normal senior analyst profile. |
| **06** | Jordan Belfort-Cruz | 22 | 1 yr | $890,000 | 845 | 🔴 **GHOST** | **Contradiction:** Near-perfect 845 credit score and $890k balance with only 1 year employment at age 22 (bust-out synthetic profile). |
| **07** | David Kim | 51 | 26 yrs | $128,900 | 780 | 🟢 **Real** | Natural veteran career profile. |
| **08** | Sophia Martinez | 24 | 2 yrs | $9,800 | 660 | 🟢 **Real** | Believable entry-level profile. |
| **09** | Sarah Connor-Reese | 38 | 20 yrs | -$12,000 | 795 | 🔴 **GHOST** | **Contradiction:** Prime 795 credit score despite chronic negative account balance and severe debt default markers. |
| **10** | Liam O'Connor | 31 | 8 yrs | $44,500 | 695 | 🟢 **Real** | Normal, verifiable identity. |

---

## 🚀 Quickstart & Local Setup

### 1. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/PhantomID.git
cd PhantomID
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Note: All API keys are optional. Built-in smart heuristics and SQLite allow 100% offline testing!)*

### 3. Run the Dashboard
```bash
python app.py
```
Open **`http://127.0.0.1:5001`** in your browser.

---

## ☁️ 1-Click Deployment on Render

This repository includes a native **`render.yaml`** specification.
1. Fork or push this repository to your GitHub account.
2. Sign in to [Render](https://render.com).
3. Click **New +** → **Blueprint** and link your `PhantomID` repository.
4. Render will automatically configure the Python environment, install dependencies, and launch Gunicorn.

---

## 📄 License
MIT License. Built with ❤️ for Hacktoberfest 2026.
