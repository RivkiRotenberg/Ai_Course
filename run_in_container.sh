#!/usr/bin/env bash
# Wrapper to run a single command in PowerShell inside the container and exit
set -euo pipefail

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <command>"
  exit 1
fi

cmd="$*"

# Run PowerShell with -NoProfile -Command and then exit
pwsh -NoProfile -NonInteractive -Command "$cmd"
