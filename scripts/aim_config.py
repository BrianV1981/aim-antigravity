#!/usr/bin/env python3
import os
import json
import sys
import subprocess
import time
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

# --- DYNAMIC ROOT DISCOVERY ---
def find_aim_root():
    current = os.path.abspath(os.getcwd())
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, "core", "CONFIG.json")):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AIM_ROOT = find_aim_root()
CONFIG_PATH = os.path.join(AIM_ROOT, "core/CONFIG.json")
sys.path.insert(0, os.path.join(AIM_ROOT, "src"))
sys.path.insert(0, os.path.join(AIM_ROOT, "scripts"))

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

CONFIG = load_config()
console = Console()

tui_style = questionary.Style([
    ('qmark', 'fg:#FF9D00 bold'),
    ('question', 'bold'),
    ('answer', 'fg:#5F819D bold'),
    ('pointer', 'fg:#FF9D00 bold'),
    ('highlighted', 'fg:#FF9D00 bold'),
    ('selected', 'fg:#5F819D'),
    ('separator', 'fg:#6C6C6C'),
    ('instruction', ''),
    ('text', ''),
    ('disabled', 'fg:#858585 italic')
])

TIER_LABELS = {
    "default_reasoning": "Primary (Cortex)",
    "tier1": "Tier 1: Harvester",
    "tier2": "Tier 2: Proposer",
    "tier3": "Tier 3: Refiner",
    "tier4": "Tier 4: Consolidator",
    "tier5": "Tier 5: Archivist"
}

PROVIDERS = ["google", "anthropic", "openrouter", "openai-compat", "local", "codex-cli", "disabled"]
AUTH_TYPES = ["OAuth (System Default / CLI)", "API Key"]

def test_provider(provider, model, endpoint, tier_name, auth_type):
    """
    Actually tests a provider by firing a live generate_reasoning() call.
    Returns (success: bool, message: str).
    """
    if provider == "disabled":
        return False, "Provider is disabled"
    try:
        from reasoning_utils import generate_reasoning
        result = generate_reasoning(
            "Respond with only the word: OK",
            brain_type=tier_name,
            config=CONFIG,
            timeout=30
        )
        if not result:
            return False, "Empty response"
        # Fail on known error prefixes
        for bad in ["Error:", "Exception", "[ERROR", "[FATAL", "Gemini CLI Error", "Ollama Error"]:
            if result.startswith(bad) or bad in result[:80]:
                return False, result[:80]
        return True, result[:60].strip()
    except ImportError:
        return False, "reasoning_utils not available"
    except Exception as e:
        return False, str(e)[:80]

def setup_cognitive_tier(tier_name):
    """Interactive prompt to configure a cognitive tier and save to CONFIG.json."""
    tier_display = TIER_LABELS.get(tier_name, tier_name)
    rprint(f"\n[cyan]--- Configure {tier_display} ---[/cyan]")

    current = CONFIG.get('models', {}).get('tiers', {}).get(tier_name, {})

    provider = questionary.select(
        "Provider:",
        choices=PROVIDERS,
        default=current.get('provider', 'google'),
        style=tui_style
    ).ask()
    if not provider:
        return

    model = questionary.text(
        "Model (e.g. gemini-2.5-flash):",
        default=current.get('model', '')
    ).ask()
    if model is None:
        return

    endpoint = current.get('endpoint', '')
    if provider in ["openai-compat", "local"]:
        endpoint = questionary.text(
            "Endpoint URL:",
            default=endpoint or "http://localhost:11434/api/generate"
        ).ask() or endpoint
    elif provider == "google":
        endpoint = "https://generativelanguage.googleapis.com"
    elif provider == "anthropic":
        endpoint = "https://api.anthropic.com"
    elif provider == "openrouter":
        endpoint = "https://openrouter.ai/api/v1/chat/completions"

    auth_type = questionary.select(
        "Auth Type:",
        choices=AUTH_TYPES,
        default=current.get('auth_type', 'OAuth (System Default / CLI)'),
        style=tui_style
    ).ask()
    if not auth_type:
        return

    CONFIG.setdefault('models', {}).setdefault('tiers', {})[tier_name] = {
        "provider": provider,
        "model": model,
        "endpoint": endpoint,
        "auth_type": auth_type
    }
    save_config(CONFIG)
    rprint(f"[green]{tier_display} saved.[/green]")
    time.sleep(1)

def main_menu():
    health_cache = {}
    while True:
        # Reload config on each loop iteration so TUI reflects latest saves
        global CONFIG
        CONFIG = load_config()

        console.clear()
        rprint(Panel(
            "[bold green]A.I.M. COCKPIT (Configuration TUI)[/bold green]\n"
            "[dim]Manage your sovereign cognitive exoskeleton[/dim]\n"
            f"[dim]Root: {AIM_ROOT}[/dim]"
        ))

        table = Table(title="Cognitive Tier Status", show_header=True, header_style="bold magenta")
        table.add_column("Tier", style="dim")
        table.add_column("Provider")
        table.add_column("Model")
        table.add_column("Status", justify="center")
        table.add_column("Diagnostics")

        tiers_config = CONFIG.get('models', {}).get('tiers', {})
        tiers = list(TIER_LABELS.keys())
        for t in tiers:
            details = tiers_config.get(t, {"provider": "NOT SET", "model": "N/A"})
            status_indicator, diag_msg = health_cache.get(t, ("[white]○[/white]", ""))
            table.add_row(
                TIER_LABELS.get(t, t),
                details.get('provider', 'NOT SET'),
                details.get('model', 'N/A'),
                status_indicator,
                diag_msg
            )
        rprint(table)

        choice = questionary.select(
            "Main Settings:",
            choices=[
                "1. Run Cognitive Health Check (Test All Tiers)",
                "2. Manage Secret Vault (API Keys)",
                "3. Configure Default Brain (Primary)",
                "4. Configure Cognitive Pipeline (T1-T5)",
                "5. Manage MCP Server (IDE Integration)",
                "6. Update Operator Profile & Behavior",
                "7. Update Obsidian Vault Path",
                "8. Archive Retention (Current: " + str(CONFIG.get('settings', {}).get('archive_retention_days', 30)) + "d)",
                "9. Auto-Memory Distillation (Current: " + CONFIG.get('settings', {}).get('auto_distill_tier', 'Off') + ")",
                "10. Set Agent Persona (Specialty Mandate)",
                "11. Configure Cognitive Mantra (Anti-Drift)",
                "12. Configure Handoff Context Tail",
                "13. Configure Waterfall Pipeline (Intervals & Cleanup)",
                "14. Reincarnation Protocol (Auto-Rebirth: " + ("ON" if CONFIG.get('settings', {}).get('auto_rebirth', False) else "OFF") + ")",
                "15. Exit"
            ],
            style=tui_style
        ).ask()

        if not choice or choice == "15. Exit":
            break

        # --- OPTION 1: Health Check ---
        if choice.startswith("1."):
            rprint("\n[cyan]Running Cognitive Health Check...[/cyan]")
            for t in tiers:
                details = tiers_config.get(t)
                if not details or details.get('provider') == "NOT SET":
                    health_cache[t] = ("[red]●[/red]", "NOT SET")
                    continue
                rprint(f"  Testing [bold]{TIER_LABELS.get(t, t)}[/bold]...")
                success, msg = test_provider(
                    details.get('provider', ''),
                    details.get('model', ''),
                    details.get('endpoint', ''),
                    t,
                    details.get('auth_type', 'API Key')
                )
                if success:
                    health_cache[t] = ("[bold green]●[/bold green]", "OK")
                else:
                    health_cache[t] = ("[bold red]●[/bold red]", str(msg)[:60])
            rprint("[green]Health check complete.[/green]")
            time.sleep(1)

        # --- OPTION 2: Secret Vault ---
        elif choice.startswith("2."):
            vault_choice = questionary.select(
                "Vault Actions:",
                choices=["List Keys", "Set Key", "Back"],
                style=tui_style
            ).ask()
            try:
                from aim_vault import list_keys, set_key
                if vault_choice == "List Keys":
                    list_keys()
                    input("\nPress Enter to continue...")
                elif vault_choice == "Set Key":
                    service = "aim-system"
                    key_name = questionary.select(
                        "Select Key:",
                        choices=[
                            "google-api-key",
                            "openrouter-api-key",
                            "openai-api-key",
                            "anthropic-api-key",
                            "reasoning-api-key"
                        ],
                        style=tui_style
                    ).ask()
                    if key_name:
                        set_key(service, key_name)
                    time.sleep(1)
            except ImportError:
                rprint("[red]aim_vault.py not available. Install keyring: pip install keyring[/red]")
                time.sleep(2)

        # --- OPTION 3: Configure Default Brain ---
        elif choice.startswith("3."):
            setup_cognitive_tier("default_reasoning")

        # --- OPTION 4: Configure Pipeline T1-T5 ---
        elif choice.startswith("4."):
            tier = questionary.select(
                "Select Tier to Configure:",
                choices=list(TIER_LABELS.keys()) + ["Back"],
                style=tui_style
            ).ask()
            if tier and tier != "Back":
                setup_cognitive_tier(tier)

        # --- OPTION 5: MCP Server ---
        elif choice.startswith("5."):
            mcp_path = os.path.join(AIM_ROOT, "src", "mcp_server.py")
            if os.path.exists(mcp_path):
                rprint("[cyan]Launching MCP Server (Ctrl+C to stop)...[/cyan]")
                try:
                    subprocess.run([sys.executable, mcp_path])
                except KeyboardInterrupt:
                    rprint("[yellow]MCP Server stopped.[/yellow]")
            else:
                rprint("[red]mcp_server.py not found at expected path.[/red]")
            time.sleep(1)

        # --- OPTION 6: Operator Profile ---
        elif choice.startswith("6."):
            rprint("\n[cyan]--- Update Operator Profile ---[/cyan]")
            full_name = questionary.text("Full Name:", default="Brian Vasquez").ask()
            github = questionary.text("GitHub Handle:", default="BrianV1981").ask()
            social = questionary.text("Social Alias:", default="@brianv1981").ask()

            if full_name:
                gemini_path = os.path.join(AIM_ROOT, "GEMINI.md")
                if os.path.exists(gemini_path):
                    import re
                    with open(gemini_path, 'r') as f:
                        content = f.read()
                    content = re.sub(
                        r'(- \*\*Operator:\*\* ).*',
                        f'- **Operator:** {full_name} (GitHub: {github} | Socials: {social})',
                        content
                    )
                    with open(gemini_path, 'w') as f:
                        f.write(content)
                    rprint(f"[green]GEMINI.md updated.[/green]")
                    rprint("[dim]Run /sync to update your KI artifacts with the new operator profile.[/dim]")
                else:
                    rprint("[red]GEMINI.md not found.[/red]")
            time.sleep(2)

        # --- OPTION 7: Obsidian Vault Path ---
        elif choice.startswith("7."):
            current_path = CONFIG.get('settings', {}).get('obsidian_vault_path', '')
            new_path = questionary.text("Obsidian Vault Path:", default=current_path).ask()
            if new_path is not None:
                CONFIG.setdefault('settings', {})['obsidian_vault_path'] = new_path
                save_config(CONFIG)
                rprint("[green]Obsidian path saved.[/green]")
            time.sleep(1)

        # --- OPTION 8: Archive Retention ---
        elif choice.startswith("8."):
            current = str(CONFIG.get('settings', {}).get('archive_retention_days', 30))
            val = questionary.text("Archive Retention (Days):", default=current).ask()
            if val and val.isdigit():
                CONFIG.setdefault('settings', {})['archive_retention_days'] = int(val)
                save_config(CONFIG)
                rprint(f"[green]Archive retention set to {val} days.[/green]")
            time.sleep(1)

        # --- OPTION 9: Auto-Memory Distillation ---
        elif choice.startswith("9."):
            current = CONFIG.get('settings', {}).get('auto_distill_tier', 'Off')
            val = questionary.select(
                "Auto-Memory Distillation Tier:",
                choices=["Off", "tier1", "tier2", "tier3", "tier4", "tier5"],
                default=current,
                style=tui_style
            ).ask()
            if val:
                CONFIG.setdefault('settings', {})['auto_distill_tier'] = val
                save_config(CONFIG)
                rprint(f"[green]Auto-distill set to: {val}[/green]")
            time.sleep(1)

        # --- OPTION 10: Agent Persona ---
        elif choice.startswith("10."):
            rprint("\n[cyan]--- Set Agent Persona (Specialty Mandate) ---[/cyan]")
            current = CONFIG.get('settings', {}).get('agent_persona', '')
            persona = questionary.text(
                "Specialty Mandate (e.g. 'Senior Backend Architect', leave blank to clear):",
                default=current
            ).ask()
            if persona is not None:
                CONFIG.setdefault('settings', {})['agent_persona'] = persona
                save_config(CONFIG)
                rprint(f"[green]Persona saved: {persona or '(cleared)'}[/green]")
            time.sleep(1)

        # --- OPTION 11: Cognitive Mantra ---
        elif choice.startswith("11."):
            rprint("\n[cyan]--- Configure Cognitive Mantra (Anti-Drift) ---[/cyan]")
            current = CONFIG.get('settings', {}).get('cognitive_mantra', '')
            mantra = questionary.text(
                "Anti-Drift Mantra (injected as a constant reminder):",
                default=current
            ).ask()
            if mantra is not None:
                CONFIG.setdefault('settings', {})['cognitive_mantra'] = mantra
                save_config(CONFIG)
                rprint("[green]Mantra saved.[/green]")
            time.sleep(1)

        # --- OPTION 12: Handoff Context Tail ---
        elif choice.startswith("12."):
            current_tail = str(CONFIG.get('settings', {}).get('handoff_context_lines', 0))
            tail_input = questionary.text(
                "Context Tail (Max Lines, 0 for Full Session):",
                default=current_tail
            ).ask()
            if tail_input and tail_input.isdigit():
                CONFIG.setdefault('settings', {})['handoff_context_lines'] = int(tail_input)
                save_config(CONFIG)
                rprint(f"[green]Handoff context set to {tail_input} lines.[/green]")
            time.sleep(1)

        # --- OPTION 13: Waterfall Pipeline ---
        elif choice.startswith("13."):
            rprint("\n[cyan]--- Configure Waterfall Refinement Pipeline ---[/cyan]")
            pipeline_config = CONFIG.get('memory_pipeline', {
                'intervals': {'tier1': 1, 'tier2': 12, 'tier3': 24, 'tier4': 72, 'tier5': 144},
                'cleanup_mode': 'archive'
            })

            sub_choice = questionary.select(
                "Memory Pipeline Settings:",
                choices=[
                    "Set Tier Intervals (Hours)",
                    f"Toggle Cleanup Mode (Current: {pipeline_config.get('cleanup_mode', 'archive').upper()})",
                    "Back"
                ],
                style=tui_style
            ).ask()

            if sub_choice == "Set Tier Intervals (Hours)":
                intervals = pipeline_config.get('intervals', {})
                new_intervals = {}
                for t in ['tier1', 'tier2', 'tier3', 'tier4', 'tier5']:
                    val = questionary.text(
                        f"Interval for {t.upper()} (Hours):",
                        default=str(intervals.get(t, 0))
                    ).ask()
                    new_intervals[t] = int(val) if val and val.isdigit() else intervals.get(t, 0)
                CONFIG.setdefault('memory_pipeline', {})['intervals'] = new_intervals
                save_config(CONFIG)
                rprint("[green]Intervals updated.[/green]")
                time.sleep(1)

            elif sub_choice and sub_choice.startswith("Toggle"):
                current = pipeline_config.get('cleanup_mode', 'archive')
                new_mode = "delete" if current == "archive" else "archive"
                CONFIG.setdefault('memory_pipeline', {})['cleanup_mode'] = new_mode
                save_config(CONFIG)
                rprint(f"[green]Cleanup mode → {new_mode.upper()}[/green]")
                time.sleep(1)

        # --- OPTION 14: Reincarnation Protocol ---
        elif choice.startswith("14."):
            current_rebirth = CONFIG.get('settings', {}).get('auto_rebirth', False)
            toggle = questionary.confirm("Enable Auto-Rebirth?", default=current_rebirth).ask()
            if toggle is not None:
                CONFIG.setdefault('settings', {})['auto_rebirth'] = toggle
                save_config(CONFIG)
                rprint(f"[green]Auto-Rebirth → {'ON' if toggle else 'OFF'}[/green]")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        sys.exit(0)
