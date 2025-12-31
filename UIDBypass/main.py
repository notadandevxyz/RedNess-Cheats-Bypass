"""
═══════════════════════════════════════════════════════════════════
    UID-BYPASS (United Corporation)
    Created by: Dev luffy.cpp
═══════════════════════════════════════════════════════════════════
"""
import subprocess
import sys
import os
import signal
import time

def terminate_process(p):
    try:
        if p and p.poll() is None:
            p.terminate()
            try:
                p.wait(timeout=3)
            except subprocess.TimeoutExpired:
                p.kill()
    except Exception:
        pass
"""
═══════════════════════════════════════════════════════════════════
    UID-BYPASS (United Corporation)
    Created by: Dev luffy.cpp
═══════════════════════════════════════════════════════════════════
"""
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    addon_script = os.path.join(script_dir, "mitmproxyutils.py")
    confdir = os.path.join(script_dir, "certs")
    bot_script = os.path.join(script_dir, "bot.py")

    if not os.path.exists(addon_script):
        print(f"Error: Addon script not found at {addon_script}")
        sys.exit(1)
    if not os.path.isdir(confdir):
        print(f"Error: certs directory not found at {confdir}")
        sys.exit(1)
    if not os.path.exists(bot_script):
        print(f"Error: Bot script not found at {bot_script}")
        sys.exit(1)

    mitm_cmd = [
        "./.local/bin/mitmdump",
        "-s", addon_script,
        "-p", "30253",
        "--listen-host", "0.0.0.0",
        "--set", "block_global=false",
        "--set", f"confdir={confdir}"
    ]

    bot_cmd = [sys.executable, bot_script]

    mitm_proc = None
    bot_proc = None

    try:
        bot_proc = subprocess.Popen(bot_cmd)
        mitm_proc = subprocess.Popen(mitm_cmd)
        print(f"Started bot (pid={bot_proc.pid}) and mitmdump (pid={mitm_proc.pid})")
        while True:
            if mitm_proc.poll() is not None:
                break
            if bot_proc.poll() is not None:
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nReceived KeyboardInterrupt, shutting down...")
    except FileNotFoundError as e:
        print(f"Error: executable not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        terminate_process(mitm_proc)
        terminate_process(bot_proc)
        print("Shutdown complete")
"""
═══════════════════════════════════════════════════════════════════
    UID-BYPASS (United Corporation)
    Created by: Dev luffy.cpp
═══════════════════════════════════════════════════════════════════
"""
if __name__ == "__main__":
    main()
