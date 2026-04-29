# CLAUDE.md — Project Context & Roadmap

> Drop this file in the root of `my-finance-app/`. It gives Claude Code full context instantly, saving tokens on every session.

---

## 🎯 Goal

Turn this **Supabase-backed** AI finance tracker into a polished **portfolio piece** for AI engineering / FinTech job applications. Then deploy publicly. Then do the same for the EdTech tool.

---

## 📁 Project: my-finance-app

### What it does (working end-to-end today)
- **AI entry flow** (`finance_app.py`): Natural language input → Gemini 2.5 Flash parses → structured JSON → AI confirmation card (review/edit before saving) → saves to Supabase. Demo mode shows fake confirmation without writing real data.
- **Manual entry form** (sidebar): Date picker, category dropdown, description, amount → save to Supabase.
- **Dashboard tab** (`tab1`): Date range filter, 3 metric cards (income, expenses, net balance), savings rate slider with save/spend split.
- **Manage Data tab** (`tab2`): Full data table, delete a transaction by row number.
- **User filter** (sidebar): Filter dashboard by Me / Partner / Joint.

### Architecture
**Supabase (Postgres)** as backend + Gemini 2.5 Flash AI + Streamlit frontend. Migrated from Google Sheets in April 2026 for better scalability, real SQL queries, and EdTech consistency.

---

## 🐛 Bugs — All Phase 1 bugs resolved

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
| 5 | **Professional visual redesign** — dark navy/gold theme, custom CSS cards, animated deltas | Biggest perception upgrade: "student project" → "portfolio showpiece" | 2–4 hrs | ⬅️ **NEXT** |
| 6 | **AI spending insights panel** — Gemini commentary after data load ("You spent 40% more on food this month") | Demonstrates agentic AI reasoning | 2–3 hrs | — |
| 7 | **Monthly breakdown view** — group by month, show MoM delta metrics | Adds real analytical depth | 2–3 hrs | — |
| 8 | **Budget alerts** — per-category limits, progress bar + warning | Practical feature, shows product thinking | 2–3 hrs | — |
| 9 | **Export to CSV** — download button in Manage Data tab | Common user request, trivial | 20 min | — |
| 10 | **Receipt / photo upload** — Gemini Vision reads receipt, auto-fills confirmation card | Impressive demo feature | 2–3 hrs | — |

---

## 🚢 Deployment Readiness

**Status: NEARLY READY — 1 pending action**

### Resolved blockers
- ✅ Credentials rotated, `.streamlit/secrets.toml` in `.gitignore`, Supabase URL/key set in Streamlit Cloud Secrets UI
- ✅ Entry point: `finance_app.py` set as main file in Streamlit Cloud deploy settings
- ✅ `requirements.txt` pinned with minimum versions; Google Sheets deps (`gspread`, `oauth2client`) removed; `supabase>=2.0` added
- ✅ `finance.db` and `app_local.py` added to `.gitignore`

### Pending — Streamlit Cloud blank page
The deployed page is currently blank. Root cause: Supabase migration code not yet pushed to `origin/main`. Will resolve after the next `git push`.

**After push, verify:**
1. App loads with demo data (no Supabase credentials needed for demo mode)
2. Login with real Supabase credentials loads actual transactions
3. AI entry flow → confirmation card → save → transaction appears in table

### Non-blockers worth noting
- `.python-version` specifies 3.9; Streamlit Cloud supports it but 3.11+ is recommended for performance
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

### Phase 2 — Portfolio Polish
- [x] AI confirmation step — `st.session_state["pending_tx"]` stores parse result; green-bordered review card with editable fields; Confirm & Save / Cancel buttons; `st.toast` persists through rerun
- [ ] **Professional visual redesign** — dark navy/gold theme, custom CSS cards ⬅️ **START HERE**
- [ ] AI spending insights panel
- [ ] Monthly breakdown view
- [ ] Budget alerts
- [ ] Export to CSV button
- [ ] **Receipt / photo upload** — file uploader accepts image; Gemini Vision reads receipt and auto-fills the confirmation card (same `pending_tx` flow)

### Phase 3 — Deploy
- [x] Set Streamlit Cloud secrets (Supabase URL + key, Gemini API key)
- [ ] Push latest code → confirm blank page resolves
- [ ] Smoke-test with empty DB, then with real data
- [ ] Make repo public (after confirming no secrets remain)

### Phase 4 — EdTech Tool
- [x] Finance app now uses Supabase — consistent with EdTech backend
- [ ] (Add EdTech project details here when ready)

---

## 🗂 Key File Map

| File | Purpose |
|------|---------|
| `finance_app.py` | Main Streamlit app — Supabase backend, Gemini AI, full feature set |
| `app.py` | Entry point shim that imports `finance_app` (Streamlit Cloud compatibility) |
| `supabase/migrations/` | DB migration files for Supabase schema |
| `.streamlit/secrets.toml` | 🔴 Local secrets only — `.gitignore`d, NEVER push |
| `requirements.txt` | Pinned dependencies (`streamlit`, `supabase`, `google-generativeai`, etc.) |
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

*Last updated: 2026-04-29 — Supabase migration complete, Phase 2 visual redesign next*
