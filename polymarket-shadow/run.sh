#!/usr/bin/env bash
# One practice-mode run inside GitHub Actions: fetch the data branch, record
# a snapshot, push the data back. Needs GH_TOKEN with contents: write.
set -euo pipefail

BRANCH="${PM_DATA_BRANCH:-polymarket-shadow-data}"
URL="https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
HERE="$(cd "$(dirname "$0")" && pwd)"
DATA="${RUNNER_TEMP:-/tmp}/shadow-data"

rm -rf "$DATA"
if ! git clone --quiet --depth 1 --branch "$BRANCH" "$URL" "$DATA" 2>/dev/null; then
  echo "No $BRANCH branch yet; starting a new one."
  mkdir -p "$DATA"
  git -C "$DATA" init --quiet -b "$BRANCH"
  git -C "$DATA" remote add origin "$URL"
fi

python3 "$HERE/snapshot.py" --data "$DATA"

cd "$DATA"
git add -A
if git diff --cached --quiet; then
  echo "Nothing new to save."
  exit 0
fi
git -c user.name="polymarket-practice" -c user.email="actions@users.noreply.github.com" \
  commit --quiet -m "Practice snapshot $(date -u +%Y-%m-%dT%H:%MZ)"
git push --quiet origin "HEAD:$BRANCH"
echo "Saved to the $BRANCH branch."
