# Runbook: How to Forge a Knowledge Item (KI)

*Antigravity natively manages state via Knowledge Items (KIs). This runbook walks you through the exact process of creating curated, immutable technical memory for A.I.M. to replace the legacy `.engram` system.*

---

## Step 1: Gather Your Raw Materials
Before you can forge a KI, you need to curate the technical data. 

1. Identify the core patterns, architecture rules, or bugs you want to permanently remember.
2. Draft a clear, concise Markdown document summarizing the context.

## Step 2: Formulate the Knowledge Item
You do not need to run heavy Python SQLite embedding scripts to ingest knowledge. Antigravity handles indexing natively.

1. Open the **Knowledge** panel in your Antigravity IDE.
2. Click **New Knowledge Item**.
3. Paste your curated markdown.
4. Name it descriptively (e.g., `django_v5_auth_patterns`).

### What Happens in the Background:
1. **Instant Ingestion:** Antigravity reads the KI and injects it into the agent's active neural workspace.
2. **Persistence:** The KI is saved natively as a JSON artifact within `<appDataDir>\knowledge`.
3. **Universality:** This KI will now automatically load anytime you open this repository in the future.

## Step 3: Test Your Knowledge Item
Your new Knowledge Item is now sitting in the core memory of A.I.M.

Before relying on it, test it locally to ensure it works. 

1. Open a new chat in Antigravity.
2. Run a test prompt:
   ```text
   Review the django auth patterns in my knowledge base. How should I build this login function?
   ```
3. Verify that the agent perfectly cites your new KI.

## Step 4: Share It with the World (The GitOps Way)
Because Antigravity KIs are lightweight, human-readable text documents (rather than brittle SQLite `.engram` binaries), they are perfectly designed for version control.

To share them:
1. Copy the KI text into a standard Markdown file (e.g., `docs/django-auth-patterns.md`).
2. Commit it to your repository via a standard PR.
3. Your team can now natively read it, and any other Antigravity agent opening the repository can ingest the `.md` file to instantly build their own KIs.

---
> [!NOTE]
> *(This completely replaces the legacy A.I.M. v1.0 `aim bake` and `.engram` Torrent network, eliminating the need for complex database sharing mechanisms.)*