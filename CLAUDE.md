# CLAUDE.md — Project Context & Roadmap

> Drop this file in the root of `my-finance-app/`. It gives Claude Code full context instantly, saving tokens on every session.

---

## 🎯 Goal

Turn this **Supabase-backed** AI finance tracker into a polished **portfolio piece** for AI engineering / FinTech job applications. Deployed publicly ✅. Then do the same for the EdTech tool.

---

## 📁 Project: my-finance-app

### What it does (working end-to-end today)
- **AI entry flow** (`finance_app.py`): Natural language input → Gemini 2.5 Flash parses → structured JSON → AI confirmation card (review/edit before saving) → saves to Supabase. Demo mode shows fake confirmation without writing real data.
- **Manual entry form** (sidebar): Date picker, category dropdown, description, amount → save to Supabase.
- **Dashboard tab** (`tab1`): Date range filter, 3 metric cards (income, expenses, net balance), AI insights panel (Gemini commentary on demand), savings rate slider with save/spend split, charts, monthly breakdown with MoM deltas.
- **Manage Data tab** (`tab2`): Full data table, delete a transaction by row number, Export to CSV download button.
- **User filter** (sidebar): Filter dashboard by Me / Partner / Joint.

### Architecture
**Supabase (Postgres)** as backend + Gemini 2.5 Flash AI + Streamlit frontend. Migrated from Google Sheets in April 2026 for better scalability, real SQL queries, and EdTech consistency.

---

## 🐛 Bugs — All resolved

| # | Bug | Status |
|---|-----|--------|
| 1 | Charts hidden when balance is **positive** | ✅ Fixed |
| 2 | `NameError` crash on empty DB — `total_income`/`total_expense` uninitialised | ✅ Fixed |
| 3 | `NameError` on Spending Trend / Recent Transactions — `filtered_df` uninitialised | ✅ Fixed |
| 4 | **Category mismatch** between AI prompt and manual form | ✅ Fixed — unified category list |
| 5 | **Double success toast** on manual form save | ✅ Fixed |
| 6 | `st.experimental_rerun()` crash in `app_local.py` | ✅ Fixed |
| 7 | **CRITICAL SECURITY: credentials committed to git** | ✅ Fixed — rotated, `.gitignore`d |
| 8 | **Column name casing bugs** after Supabase migration | ✅ Fixed |

---

## 🚀 Improvements Roadmap (ranked by impact vs effort)

| Rank | Improvement | Impact | Effort | Status |
|------|-------------|--------|--------|--------|
| 1 | Fix bugs 1–3 (charts, NameError crashes, categories) | Eliminates demo-killing failures | 30 min | ✅ Done |
| 2 | **Secure credentials** + `.gitignore` | Prevents security incident | 15 min | ✅ Done |
| 3 | **AI confirmation step** — review/edit before saving | Makes AI feel agentic & trustworthy | 1–2 hrs | ✅ Done |
| 4 | **Supabase migration** — replace Google Sheets with Postgres | Better scalability, real SQL, EdTech consistency | 2–3 hrs | ✅ Done |
| 5 | **Professional visual redesign** — dark navy/gold theme, custom CSS cards, animated deltas | Biggest perception upgrade: "student project" → "portfolio showpiece" | 2–4 hrs | ✅ Done |
| 6 | **AI spending insights panel** — Gemini commentary after data load ("You spent 40% more on food this month") | Demonstrates agentic AI reasoning | 2–3 hrs | ✅ Done |
| 7 | **Monthly breakdown view** — group by month, show MoM delta metrics | Adds real analytical depth | 2–3 hrs | ✅ Done |
| 8 | **Budget alerts** — per-category limits, progress bar + warning | Practical feature, shows product thinking | 2–3 hrs | Skipped |
| 9 | **Export to CSV** — download button in Manage Data tab | Common user request, trivial | 20 min | ✅ Done |
| 10 | **Receipt / photo upload** — Gemini Vision reads receipt, auto-fills confirmation card | Impressive demo feature | 2–3 hrs | — |

---

## 🚢 Deployment Readiness

**Status: DEPLOYED ✅**

### Resolved blockers
- ✅ Credentials rotated, `.streamlit/secrets.toml` in `.gitignore`, Supabase URL/key set in Streamlit Cloud Secrets UI
- ✅ Entry point: `app.py` imports and calls `main()` from `finance_app.py` — all UI rendering inside `main()` so it re-runs on every Streamlit interaction
- ✅ `requirements.txt` pinned to exact versions; Google Sheets deps removed; `supabase>=2.0` and `google-genai>=1.0.0` added
- ✅ `finance.db` and `app_local.py` added to `.gitignore`
- ✅ All Phase 2 features complete and syntax-verified
- ✅ Migrated from deprecated `google-generativeai` to `google-genai` SDK
- ✅ `.python-version` fixed from invalid `3.14` to `3.11`
- ✅ `streamlit` pinned to `==1.41.1` to prevent silent breaking upgrades on Cloud

### Non-blockers worth noting
- `_lessons/` directory is committed — fine for portfolio repo, adds context

---

## 📋 Session Workflow (for Claude Code)

When starting a new session, read this file first, then tackle the next unchecked item below:

### Phase 1 — Security & Stability ✅ COMPLETE
- [x] **Rotate credentials** — Gemini key + GCP service account revoked
- [x] Add `.streamlit/secrets.toml` to `.gitignore`
- [x] Fix Bug 1: Charts hidden when balance positive
- [x] Fix Bug 2: NameError on empty DB — initialise totals to 0
- [x] Fix Bug 3: NameError on Spending Trend / Recent Transactions — initialise `filtered_df`
- [x] Fix Bug 4: Unify category lists between AI prompt and manual form
- [x] Fix Bug 5: Remove duplicate success toast
- [x] Fix Bug 6: Replace `st.experimental_rerun()` with `st.rerun()`
- [x] Pin `requirements.txt` versions; remove `gspread`/`oauth2client`; add `supabase>=2.0`
- [x] Set entry point in Streamlit Cloud settings (`finance_app.py`)
- [x] Add `finance.db`, `app_local.py` to `.gitignore`
- [x] **Supabase migration** — replaced Google Sheets entirely; fixed column casing bugs; tested end-to-end locally

### Phase 2 — Portfolio Polish ✅ COMPLETE
- [x] AI confirmation step — `st.session_state["pending_tx"]` stores parse result; gold-bordered review card with editable fields; Confirm & Save / Cancel buttons; `st.toast` persists through rerun
- [x] **Professional visual redesign** — dark navy/gold theme (`#0a0e1a`/`#f59e0b`), `inject_custom_css()`, `render_metric_card()`, `style_figure()`, sidebar logo/tagline/section labels, Inter font via Google Fonts
- [x] **AI spending insights panel** — `generate_insights()` calls Gemini 2.5 Flash; button-triggered, cached in `st.session_state["ai_insights"]`; dark card with gold header; hidden when `filtered_df` is empty
- [x] **Monthly breakdown view** — groups by `dt.to_period("M")`; grouped bar chart (Income #3b82f6 / Expenses #ef4444) via `px.bar`; summary table with pandas Styler highlighting net-negative months in red; MoM £ and % deltas; hidden if fewer than 2 months of data
- [x] **Export to CSV** — `st.download_button` in Manage Data tab, only shown when data exists
- [ ] Budget alerts — explicitly skipped
- [ ] **Receipt / photo upload** — deferred

### Phase 3 — Deploy ✅ COMPLETE
- [x] Set Streamlit Cloud secrets (Supabase URL + key, Gemini API key)
- [x] Push latest code — blank screen resolved
- [x] Smoke-test with empty DB, then with real data
- [x] Make repo public (after confirming no secrets remain)

### Phase 4 — EdTech Tool
- [x] Finance app now uses Supabase — consistent with EdTech backend
- [x] App working locally ✅
- [x] Deployed on Streamlit Cloud ✅
- [x] README done ✅
- [ ] Repo public — pending

---

## 🗂 Key File Map

| File | Purpose |
|------|---------|
| `finance_app.py` | Main Streamlit app — all UI inside `main()`, Supabase backend, Gemini AI, full feature set |
| `app.py` | Entry point — imports and calls `main()` from `finance_app` on every Streamlit rerun |
| `supabase/migrations/` | DB migration files for Supabase schema |
| `.streamlit/secrets.toml` | 🔴 Local secrets only — `.gitignore`d, NEVER push |
| `requirements.txt` | Pinned dependencies (`streamlit==1.41.1`, `supabase`, `google-genai`, etc.) |
| `_lessons/` | Learning exercises — kept for portfolio context |
| `app_local.py` | Old SQLite local version — `.gitignore`d, not for deployment |
| `finance_app_v1.py` | Old Google Sheets version — ignore |

---

## 💼 Job Application Context

- Target roles: AI engineering, FinTech
- This is a **first project** — the concept and AI integration are legitimately impressive
- Bugs 1–3 would cause visible failures within 60 seconds of a live demo → fix these first
- The four changes that transform this: fix bugs → secure credentials → visual redesign → AI insights panel
- Once deployed: add live URL to CV/LinkedIn/portfolio

---

## 🔑 Key Lessons Learned

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Blank screen on any interaction | `from finance_app import *` causes Python module caching — UI code only runs on first load | Move all UI into `main()`, import and call `main()` from `app.py` |
| Deployed app crashing silently | `google.generativeai` SDK fully deprecated on Streamlit Cloud | Migrate to `google-genai` SDK |
| App restarting mid-session | Streamlit Cloud redeploys on every git push | Stop pushing during live testing |
| Streamlit version mismatch | Loose version pin allowed Cloud to upgrade to breaking version | Pin `streamlit==1.41.1` in `requirements.txt` |

---

*Last updated: 2026-04-30 — Phase 3 complete, app deployed and live*
