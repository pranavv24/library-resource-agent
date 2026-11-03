"""Intelligent Library Resource Allocation Agent - capstone entry point.

    pip install cryptography
    python main.py            # starts everything and opens the dashboard in your browser
    python main.py --cli      # terminal-only run of the full lifecycle (no browser)
"""
import argparse, os, sys, threading, time, webbrowser
from agent.bus import Bus
from agent.core import LibraryAgent
from agent.dashboard import make_server
from agent.workers import TITLES

BASE = os.path.dirname(os.path.abspath(__file__))
BANNER = "=" * 100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765, help="dashboard port")
    ap.add_argument("--cli", action="store_true", help="run the scripted lifecycle in the terminal and exit")
    ap.add_argument("--speed", type=float, default=0.8, help="seconds between agent cycles")
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    bus = Bus()
    print(BANNER)
    print("CAPSTONE - UNIFIED AUTONOMOUS LIBRARY AGENT | Core Loop | Workers | Cooperation | BDI | Signature Security")
    print(BANNER)
    agent = LibraryAgent(bus, BASE, step_delay=a.speed)
    if a.cli:
        agent.next_schedule = {2: "borrow_last", 4: "courier_delay"}
        agent.submit_request("S102", TITLES[0], auto=True)
        time.sleep(0.5)
        while agent.state != "COMPLETE":
            time.sleep(0.2)
        from agent.attacks import run_attacks
        run_attacks(agent)
        print(BANNER)
        return
    try:
        server = make_server(agent, bus, a.port)
    except OSError:
        sys.exit(f"Port {a.port} is busy. Try: python main.py --port 8766")
    url = f"http://127.0.0.1:{a.port}"
    bus.emit("SYSTEM", f"Dashboard running at {url}  (Ctrl+C to stop)")
    if not a.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
