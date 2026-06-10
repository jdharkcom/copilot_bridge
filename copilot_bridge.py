#!/usr/bin/env python3
import sys
import json
import subprocess
import threading

# Path to your actual copilot binary
COPILOT_PATH = "/opt/homebrew/bin/copilot"


def stream_copilot_to_xcode(process):
    """Reads stdout from Copilot and writes it directly back to Xcode."""
    try:
        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
    except Exception:
        pass


def main():
    # Launch the real copilot process in ACP/stdio mode
    try:
        copilot = subprocess.Popen(
            [COPILOT_PATH, "--acp", "--stdio"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1  # Line buffered
        )
    except Exception as e:
        sys.stderr.write(f"Failed to start copilot binary: {e}\n")
        sys.exit(1)

    # Start a background thread to forward Copilot's responses back to Xcode immediately
    stdout_thread = threading.Thread(target=stream_copilot_to_xcode, args=(copilot,), daemon=True)
    stdout_thread.start()

    # Read from Xcode's stdin, intercept/patch the handshake, and forward to Copilot
    try:
        for line in sys.stdin:
            if not line.strip():
                continue

            try:
                payload = json.loads(line)

                # Check if this is the handshake method causing the schema rejection
                if payload.get("method") == "initialize":
                    params = payload.get("params")
                    if isinstance(params, dict):
                        if "protocolVersion" not in params:
                            params["protocolVersion"] = 1

                # Re-serialize the corrected payload and send it down the pipe
                copilot.stdin.write(json.dumps(payload) + "\n")
                copilot.stdin.flush()

            except json.JSONDecodeError:
                # If Xcode passes raw chunks or unexpected framing, forward it untouched
                copilot.stdin.write(line)
                copilot.stdin.flush()

    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        copilot.terminate()


if __name__ == "__main__":
    main()
