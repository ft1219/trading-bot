#!/usr/bin/env bash
# One practice-mode run inside GitHub Actions: fetch the data branch, record
# a snapshot, push the data back. Needs GH_TOKEN with contents: write.
set -euo pipefail

BRANCH="${PM_DATA_BRANCH:-polymarket-shadow-data}"
URL="https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
HERE="$(cd "$(dirname "$0")" && pwd)"
DATA="${RUNNER_TEMP:-/tmp}/shadow-data"

rm -rf "$DATA"
# ls-remote exits 2 when the branch does not exist; anything else non-zero
# means the repository could not be reached, which must not start a new branch.
found=0
git ls-remote --exit-code --heads "$URL" "$BRANCH" >/dev/null || found=$?
if [ "$found" -eq 0 ]; then
  git clone --quiet --depth 1 --branch "$BRANCH" "$URL" "$DATA"
elif [ "$found" -eq 2 ]; then
  echo "No $BRANCH branch yet; starting a new one."
  mkdir -p "$DATA"
  git -C "$DATA" init --quiet -b "$BRANCH"
  git -C "$DATA" remote add origin "$URL"
else
  echo "Could not reach the repository to read the $BRANCH branch." >&2
  exit 1
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
