# Vibe Coding Pipelines

**Date Established:** March 28, 2026
**Target Model:** Gemini 3.1 Pro (Preview) & Above
**Category:** Automated Software Assembly

---

## What is a Vibe Coding Pipeline?

"Vibe Coding" traditionally refers to a human developer sitting in an AI-powered IDE (like Cursor or Windsurf) and typing natural language prompts to generate code. 

A **Vibe Coding Pipeline** takes this a step further. It is an **Automated Agentic Macro**. Instead of a human manually typing prompts, we encode a Senior Architect's step-by-step blueprint into a Python array. A background harness script (`tmux send-keys`) sequentially injects these prompts into an A.I.M. Sovereign Agent. 

You run the script, go to sleep, and wake up to a fully built, Git-versioned, and unit-tested codebase. The AI handles the TDD, the branching, and the execution. You just provide the blueprint.

---

## Pipeline 1: SovereignX (Local Dark-Pool Crypto Exchange)

**Goal:** Build a highly performant, asynchronous, local algorithmic trading dashboard with live WebSockets.
**Estimated Time to Auto-Build:** ~25 Minutes
**Complexity:** High (Asyncio, WebSockets, DOM Manipulation)

### The Blueprint (21-Turn Sequence)
You can drop this array into `run_vibe_killer.py` to automate the build.

**Phase 1: The Foundation (Data & Schema)**
1. "Initialize a FastAPI app in `main.py`."
2. "We are building a trading exchange. Set up an asynchronous SQLite database (`aiosqlite`) using SQLAlchemy in `database.py`."
3. "Create a database model called `Ledger_Entries` with columns for ID, symbol, side (BUY/SELL), price, quantity, and status. Use Python's `Decimal` type strictly for price and quantity."
4. "Create a database model called `Trades` to record matched orders, including a flat $2.00 fee column."
5. "Write exhaustive `pytest` scripts to verify the database migrations and schema."

**Phase 2: The Core Logic (The Matching Engine)**
6. "Create `engine.py`. Write a purely mathematical matching function that takes a new `Ledger_Entry` and pairs it against existing open entries of the opposite side."
7. "Implement partial-fill logic in the engine. If a BUY is larger than a SELL, generate a new `Trade` record and correctly reduce the open quantity of the BUY order."
8. "Write complex unit tests in `test_engine.py` simulating edge cases (exact matches, partial fills, no matches) to mathematically prove the engine works."

**Phase 3: The API & WebSockets (The Bridge)**
9. "In `main.py`, build the `POST /orders` endpoint. It must save the order to the database, run the matching engine, and commit the results asynchronously."
10. "Build the `GET /orderbook` and `GET /pnl` (Profit and Loss) endpoints."
11. "Implement a FastAPI WebSocket manager class to handle multiple connected clients."
12. "Update the `POST /orders` endpoint to broadcast a `TRADE_EXECUTED` JSON payload via the WebSocket manager whenever the matching engine generates a trade."

**Phase 4: The Interface (The Frontend)**
13. "Create a `static/` folder. Configure FastAPI to serve static files from it."
14. "Create `static/index.html`. Scaffold a trading dashboard using a 'Cyberpunk Neon' CSS theme (dark backgrounds, bright pink/blue accents). No Tailwind, pure CSS."
15. "Create `static/app.js`. Establish a WebSocket connection to the backend."
16. "Write JS functions to render the initial order book on page load using the `GET /orderbook` endpoint."
17. "Update `app.js` to listen for WebSocket `TRADE_EXECUTED` events and dynamically append them to a 'Recent Trades' HTML table without reloading the page."
18. "Build an HTML form on the dashboard to submit new BUY/SELL orders directly to the API."

**Phase 5: The Market Simulation (Testing)**
19. "Write a standalone script called `bot.py`."
20. "Program `bot.py` to use `asyncio` and `httpx` to fire 5 random BUY or SELL orders per second at the FastAPI backend to simulate live market volume."
21. "Run the bot and the FastAPI server simultaneously to prove the architecture handles asynchronous database locks cleanly and updates the UI in real-time."
