#!/bin/bash
if [[ "${1:-}" == "-a" || "${1:-}" == "--author" ]]; then
  echo "Author: FoxSecIntel"
  echo "Repository: https://github.com/FoxSecIntel/dmarc.exe
  echo "Tool: update.sh"
  exit 0
fi

set -euo pipefail

__r17q_blob="wqhWaWN0b3J5IGlzIG5vdCB3aW5uaW5nIGZvciBvdXJzZWx2ZXMsIGJ1dCBmb3Igb3RoZXJzLiAtIFRoZSBNYW5kYWxvcmlhbsKoCg=="
if [[ "${1:-}" == "m" || "${1:-}" == "-m" ]]; then
  echo "$__r17q_blob" | base64 --decode
  exit 0
fi


# Safe update helper:
# - requires explicit files (or -A for all tracked+untracked)
# - requires explicit commit message
# - pushes current branch to origin
#
# Usage:
#   ./update.sh -m "Your commit message" file1 file2
#   ./update.sh -m "Your commit message" -A

usage() {
  echo "Usage: $0 -m \"commit message\" [--all|-A | <file1> <file2> ...]"
  exit 1
}

message=""
add_all=false
files=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -m|--message)
      shift
      [[ $# -gt 0 ]] || usage
      message="$1"
      ;;
    -A|--all)
      add_all=true
      ;;
    -h|--help)
      usage
      ;;
    *)
      files+=("$1")
      ;;
  esac
  shift
done

[[ -n "$message" ]] || { echo "Error: commit message is required."; usage; }

if [[ "$add_all" == true ]]; then
  echo "[+] Staging all changes (-A)"
  git add -A
else
  [[ ${#files[@]} -gt 0 ]] || { echo "Error: provide files to stage, or use -A."; usage; }
  echo "[+] Staging explicit files: ${files[*]}"
  git add -- "${files[@]}"
fi

# Abort if nothing staged
if git diff --cached --quiet; then
  echo "No staged changes to commit."
  exit 1
fi

current_branch="$(git branch --show-current)"
[[ -n "$current_branch" ]] || { echo "Error: could not determine current branch."; exit 1; }

echo "[+] Committing on branch '$current_branch'"
git commit -m "$message"

echo "[+] Pushing to origin/$current_branch"
git push origin "$current_branch"

echo "Done."

