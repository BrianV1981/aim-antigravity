# A.I.M. Issue Ledger

*Last Synchronized: 2026-04-02 12:01 AM*
*This file serves as the local, zero-latency index of all active project tasks.*

## 🟢 OPEN ISSUES — `BrianV1981/aim-antigravity`

* **#52** - P2: Audit and Sunset Legacy Terminal TUI Interfaces (aim_init.py & aim_config.py) [enhancement] *(Created: 2026-04-02)*
* **#51** - P1: Remove dead bubblewrap code from plugins/run_skill/run.py [bug] *(Created: 2026-04-02)*
* **#50** - P1: Three scripts hardcode Linux venv/bin/python3 path [bug] *(Created: 2026-04-02)*
* **#49** - P0: Daemon start/stop/status uses Linux-only nohup/kill/tail [bug] *(Created: 2026-04-02)*
* **#48** - P0: Fix Linux-only root traversal (while current != '/') in 25 files [bug] *(Created: 2026-04-02)*
* **#47** - Achieve zero test failures: fix test_aim_doctor collection error and Python 3.14 requests compat [bug] *(Created: 2026-04-02)*
* **#46** - Triage dead quarantine tests and remove tests/quarantine/ directory [enhancement] *(Created: 2026-04-02)*
* **#45** - Port 5 evolved test suites from aim-claude: handoff, memory_pipeline, skills, mcp_server, config/init [enhancement] *(Created: 2026-04-02)*
* **#44** - Resurrect 4 quarantined tests with sys.path fixes: sovereign_sync, waterfall_pipeline, daemon, context_injector [bug] *(Created: 2026-04-02)*
* **#43** - Port DataJack pipeline integration tests from aim-claude (test_datajack_pipeline.py) [enhancement] *(Created: 2026-04-02)*
* **#42** - Port aim_exchange.py DataJack module from original aim repo to aim-antigravity [enhancement] *(Created: 2026-04-02)*
* **#41** - Validate DataJack and Engram DB against SQLite file-locking crashes on Windows concurrent access [enhancement] *(Created: 2026-04-02)*
* **#40** - Bug: Python 3.14 compatibility â€” requests.exceptions.ConnectionError not found in mocked test [bug] *(Created: 2026-04-02)*
* **#39** - Bug: test_aim_doctor.py fails collection with ModuleNotFoundError for aim_doctor [bug] *(Created: 2026-04-02)*
* **#38** - Automate session transcript export: replace manual UI Export button with programmatic trigger [enhancement] *(Created: 2026-04-02)*
* **#37** - Resurrect 8 quarantined legacy tests: rewrite to mock .md export parsing instead of dead daemon/JSONL modules [enhancement] *(Created: 2026-04-02)*
* **#36** - Overhaul testing suite: Emulate aim-claude unit/integration/e2e architecture and harden for Windows paths/execution [bug] *(Created: 2026-04-01)*
* **#35** - Restore TUI aim_config.py (test_provider, setup_cognitive_tier, all 14 menu handlers); re-enable tier1/default_reasoning in CONFIG.json; fix Windows path compatibility in reasoning_utils.py; remove DEPRECATED wiki banners [bug] *(Created: 2026-04-01)*
* **#31** - Harden agent boot sequence: add PRE-FLIGHT LOCKOUT to prevent agents responding before reading HANDOFF, GAMEPLAN, ISSUE_TRACKER, and CURRENT_PULSE [bug] *(Created: 2026-04-01)*
* **#28** - Local Ollama embeddings and summarizer pipeline hangs indefinitely if provider is offline [bug] *(Created: 2026-04-01)*
* **#26** - Refactor history_scribe.py: Event-Driven Chunker triggered by /reincarnate instead of live daemon polling [enhancement] *(Created: 2026-04-01)*
* **#22** - Restore history_scribe.py and the mechanical Flight Recorder pipeline [enhancement] *(Created: 2026-03-31)*
* **#21** - Enhancement Strategy: Cross-Platform Vector Acceleration [enhancement] *(Created: 2026-03-31)*
* **#20** - Vector Search Scaling Strategy (NumPy vs. sqlite-vec) [enhancement] *(Created: 2026-03-31)*
* **#14** - Implement TDD Coverage for Antigravity Decoupled Backends [enhancement] *(Created: 2026-03-31)*

