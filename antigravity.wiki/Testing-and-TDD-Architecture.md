# Testing & TDD Architecture (Antigravity Native)

The A.I.M.-Antigravity integration brought a massive paradigm shift to testing infrastructure. Legacy iterations of the exoskeleton (`aim`, `aim-codex`, and `aim-claude`) assumed a Linux shell environment where tools inherently ran in sandboxed sub-processes and where session polling loops extracted raw JSONL files (`*.jsonl`). 

In contrast, **A.I.M.-Antigravity completely drops live CLI daemon polling in favor of parsing the explicitly exported session markdown (`.md`) from your local `Downloads/` folder.** Therefore, the fundamental testing architecture engineered for past A.I.M. daemon wrappers was completely overhauled.

## The GitOps Migration Constraint

In earlier versions of A.I.M., tests (`test_full_session.py`, `test_hooks_session_summarizer.py`) validated complex daemon interactions. Because Antigravity leverages isolated execution (file-listening rather than daemon polling), those tests represented **Architectural Debt** and were deeply incompatible with the underlying ideology. 

In this overhaul, all legacy CLI test suites relying on silent `jsonl` daemon polling over active shells have been permanently **quarantined or purged**. Tests now focus entirely on native hook registry mechanics and explicit file parsing.

---

## 🚀 The Bubblewrap Eradication

The greatest blocker inherited from the `aim-claude` and `aim-codex` repositories was the **Model Context Protocol (MCP)** execution module (`src/mcp_server.py`). The legacy script hard-coded Linux [Bubblewrap (`bwrap`)](https://github.com/containers/bubblewrap) kernel isolation for executing dynamic scripts, injecting intense `--ro-bind` kernel commands that universally crash on Windows 11.

### The Antigravity Solution
Because Antigravity operates natively inside your IDE context rather than via an externally hosted sub-container, isolated security virtualization was removed in favor of GitOps-driven ACLs:
- `mcp_server.py` now leverages native Python `subprocess.run()`.
- The corresponding testing suite (`test_mcp_integration.py`) has been rewritten to validate tool routing seamlessly across standard sys environments without kernel flags.
- **Result:** You can run pure, un-mocked skill verifications on any OS environment instantly.

---

## 🔬 Running the Pytest Suite

Tests are isolated by target layer. Due to the shift away from Daemon polling, running `--e2e` tests is no longer supported on the codebase. Validation focuses on tight `unit` checks and structural `integration` routes.

> [!WARNING]
> Do **NOT** run pytest recursively over the entire `tests/` folder (e.g., `python -m pytest tests/`). Legacy integration tests that still expect daemon namespaces exist within `tests/quarantine/` and will cause a chain of module-resolution `ImportError` crashes.

### Valid Execution Command
To ensure proper `PYTHONPATH` loading and to test the healthy suites:
```powershell
$env:PYTHONPATH="src;scripts"
python -m pytest tests/unit/ tests/integration/ -v
```

### Path & Cross-Platform Conventions
The testing codebase previously suffered from hardcoded UNIX path fragments (`/tmp/`). The updated testing suite now universally implements `tempfile.gettempdir()` alongside standard Python `os.path.join()` or `pathlib.Path` constructions, validating cross-environment operability exactly as intended by the Antigravity system.
