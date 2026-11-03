# Intelligent Library Resource Allocation Agent (Capstone, Assignment 5.2)

One autonomous agent that combines all five units: core loop (1), TCP workers (2), cooperation (3), BDI and knowledge (4), signature security (5).

## Run it in VS Code

```
pip install cryptography
python main.py
```

The dashboard opens at http://127.0.0.1:8765. Other options:

- `python main.py --cli` runs the whole lifecycle plus the attack suite in the terminal.
- `python main.py --port 8766` if 8765 is busy. `--speed 0.4` makes the agent step faster.
- On macOS, hostile request A7 needs a loopback alias, otherwise it shows as "skipped": `sudo ifconfig lo0 alias 127.0.0.2`

Only third-party dependency: `cryptography`. Python 3.9+.

## How the simple screen works

1. Pick a book. The signed request goes to the agent over TCP.
2. The agent checks the shelf and the North branch, then shows the options that work right now (shelf copy, transfer, e-book, wait-list) with a "Best match" tag.
3. You choose, or click "Let the agent choose for me" for the automatic behaviour.
4. If the situation changes mid-plan, the agent comes back with fresh options.

The "Behind the scenes" tab holds the technical panels, the automatic demo and the security tests.

## Layout

| File | Unit | Role |
|---|---|---|
| `agent/core.py` | 1, 3, 4 | core loop, cooperation, beliefs/desires/intentions, plan library |
| `agent/workers.py`, `agent/net.py` | 2 | worker hosts and TCP socket layer |
| `agent/security.py` | 5 | Ed25519 envelopes, 7 checkpoints, policy manifest, audit chain |
| `agent/attacks.py` | 5 | hostile requests A1-A9 and policy-tamper breach H1 |
| `agent/dashboard.py`, `web/index.html` | UI | live dashboard |
| `docs/architecture.svg / .png` | | system architecture schematic |

## 3-minute video script (screen-record the dashboard)

1. **0:00-0:20** Show the architecture diagram, then the dashboard. Say: one agent, two worker hosts, every message signed.
2. **0:20-0:50** Type a request and click *Reserve book*. Point at the log: signed request verified, subtask to Beta, signature verified, 3 copies becomes 2.
3. **0:50-1:50** Click *Run the full lifecycle demo*. Narrate the two surprises: last shelf copy borrowed (P1 aborted, P2 adopted), courier delayed (P2 aborted, P3 completes), restock desire fires. Show the beliefs table and plan trail.
4. **1:50-2:30** Click *Run 9 hostile requests*. Show the results table and that inventory is unchanged.
5. **2:30-3:00** Click *Tamper with the policy file*. Agent goes QUARANTINED even for a valid command. Click *Restore policy*. Finish on the audit chain showing intact.
