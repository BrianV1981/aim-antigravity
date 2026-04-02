# Getting Started with A.I.M. (Antigravity Native)

Welcome to **Actual Intelligent Memory**, the sovereign context and working memory layer explicitly designed for the Antigravity IDE environment on Windows.

## 🚀 The Sovereign Deployment Manual

### 1. The Environment

The `aim-antigravity` exoskeleton operates as a File-Based State Engineering bridge for the IDE agent, completely replacing the old A.I.M. Linux CLI wrapper and daemon polling.

Prerequisites:
*   **Windows 11** (WSL not strictly required, as the ecosystem is natively porting to Windows arrays).
*   **Python 3.10+** (For autonomic hooks, memory processors, and database generation).
*   **Git** (For the rigid GitOps bridge).

### 2. Sovereign Infrastructure (Ollama)

A.I.M.'s deep memory (`engram.db`) uses the Nomic text embedding model for local, sovereign retrieval, ensuring you never send your codebase memory to a corporate vector database API.

```powershell
# Install Ollama for Windows (Download from ollama.com first)
ollama pull nomic-embed-text
```

### 3. A.I.M. Installation

Clone the repository to securely establish the agent's brain framework.

```powershell
git clone https://github.com/BrianV1981/aim-antigravity.git
cd aim-antigravity
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Agent Initialization (The /init Workflow)

> ⚠️ The legacy terminal CLI commands (`aim init` and `aim tui`) have been permanently orphaned. Do not run them.

Instead, initialize the agent natively inside Antigravity by issuing the Slash Workflow to the agent:

**`/init`**

This instructs the agent to:
1. Verify the Engram DB connection and GitHub Auth.
2. Establish your `aim_operator_profile` (Tier 3 Immediate Memory).
3. Establish your `aim_project_architecture` Knowledge Item.

### 5. Continuous Re-calibration (The /sync Workflow)

As your repository evolves or new architectural constraints are discovered over the lifecycle of the project, do NOT run `/init` again. Simply trigger the calibration command:

**`/sync`**

---

## 🏗️ The Boot Verification Gate

If the agent has successfully booted inside Antigravity, it will not answer your first question directly. To ensure **Epistemic Certainty**, the system forces the agent through a Pre-Flight Lockout (`HANDOFF.md`). 

The agent's first output must *always* be a structured **Boot Acknowledgment**, proving it has read your Commander's Intent, the active Edge, and the Issue Tracker before generating tokens.

---

"I believe I've made my point." — **A.I.M.**