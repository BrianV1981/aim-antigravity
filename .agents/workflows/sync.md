---
description: Re-calibration command. Updates KI artifacts when stable knowledge changes (operator info, architectural decisions). Safe to run anytime — fully idempotent.
---
# /sync — Synchronization

This command re-calibrates the agent's persistent KI memory. Run it whenever stable knowledge changes — for example, after updating your operator name, after a major architectural decision, or after any significant project pivot.

This is **not** a per-session command. For session continuity, use `/reincarnate`.

When the user types `/sync` or `/synchronization`, execute the following steps in exact order:

## Step 1 — Read Current State
Gather the current values from the live sources before writing anything.

1. Use `view_file` to read `GEMINI.md` — extract the current `Operator` field (name + aliases).
2. Run `python scripts/aim_cli.py search "OPERATOR_PROFILE.md"` — check if any additional operator preferences are stored in the Engram DB.
3. Run `python scripts/aim_cli.py mail check` — check swarm inbox.

## Step 2 — Compare Against Existing KIs
Read the current KI artifacts to detect what has changed.

1. Read `C:\Users\<user>\.gemini\antigravity\knowledge\aim_operator_profile\artifacts\content.md`
2. Read `C:\Users\<user>\.gemini\antigravity\knowledge\aim_project_architecture\artifacts\content.md`

If either file does not exist, treat it as a first-time write (same as `/init` Step 2 and 3).

## Step 3 — Update Operator Profile KI
Overwrite `aim_operator_profile\artifacts\content.md` with the current values read in Step 1.
Update `metadata.json` with a new `updated_at` timestamp.

Report: "Updated" if values changed, "No changes detected" if values were identical.

## Step 4 — Update Project Architecture KI
If the user has stated any new architectural decisions in this session or in the current prompt, incorporate them into `aim_project_architecture\artifacts\content.md`.
Update `metadata.json` with a new `updated_at` timestamp.

If no changes were stated, report "No changes detected — architecture KI is current."

## Step 5 — Report
Provide a clean markdown summary:
- Mail check result
- Operator Profile KI: what changed (or "no changes")
- Project Architecture KI: what changed (or "no changes")
- Timestamp of sync
