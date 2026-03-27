#!/usr/bin/env python3
"""Deploy NailyDews to VPS via SSH."""

import subprocess
import sys

VPS_HOST = "root@72.61.94.178"
VPS_PATH = "/opt/nailydews"
REPO_URL = "https://github.com/Pil0tKart0n/NailyDews.git"


def run(cmd: str, description: str = ""):
    """Run a command and print output."""
    if description:
        print(f"\n--- {description} ---")
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(f"ERROR: Command failed with exit code {result.returncode}")
        sys.exit(1)
    return result


def main():
    print("=== NailyDews Deploy ===\n")

    # Step 1: Push local changes
    run("git add -A && git commit -m 'deploy' --allow-empty && git push", "Pushing to GitHub")

    # Step 2: SSH commands on VPS
    ssh_commands = f"""
    # Clone or pull
    if [ ! -d {VPS_PATH} ]; then
        git clone {REPO_URL} {VPS_PATH}
    fi
    cd {VPS_PATH}
    git pull

    # Copy .env if not exists
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "WARNING: .env copied from example - edit it with real values!"
    fi

    # Build and start
    docker compose build --no-cache
    docker compose up -d

    # Show status
    docker compose ps
    """

    run(f'ssh {VPS_HOST} "{ssh_commands}"', "Deploying on VPS")

    print("\n=== Deploy Complete ===")


if __name__ == "__main__":
    main()
