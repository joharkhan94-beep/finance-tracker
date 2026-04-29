-- 001_create_transactions.sql
-- Finance Tracker — initial schema
--
-- Run once in Supabase dashboard → SQL Editor → New query → paste → Run.
-- Safe to re-run: all statements use IF NOT EXISTS / IF EXISTS guards.

-- ── Table ────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS transactions (
    id          bigint         GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date        date           NOT NULL,
    type        text           NOT NULL CHECK (type IN ('Income', 'Expense')),
    category    text           NOT NULL,
    item        text           NOT NULL,
    cost        numeric(10, 2) NOT NULL,
    "user"      text           NOT NULL CHECK ("user" IN ('Me', 'Partner', 'Joint')),
    created_at  timestamptz    NOT NULL DEFAULT now()
);

-- ── Index ─────────────────────────────────────────────────────────────────────
-- Dashboard filters by date range on every render — index makes it fast.

CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions (date);

-- ── Row Level Security ────────────────────────────────────────────────────────
-- Single-user personal app using the service role key; RLS not needed.

ALTER TABLE transactions DISABLE ROW LEVEL SECURITY;
